#!/usr/bin/env python3
"""Back-of-the-envelope capacity calculator (standard library only).

Model (all rates are per second, sizes in bytes, decimal units: 1 GB = 1e9 B)
  requests_per_day = DAU * requests_per_user_per_day
  avg_qps          = requests_per_day / 86400
  peak_qps         = avg_qps * peak_factor
  write_qps        = peak_qps * write_fraction ; read_qps = peak_qps - write_qps
  egress_bps       = peak_qps * response_bytes * 8
  new_bytes_per_day= requests_per_day * write_fraction * bytes_per_write
  raw_storage      = new_bytes_per_day * retention_days
  provisioned      = raw_storage * replication * headroom

Assumptions baked in: uniform write size, constant growth (no user growth term),
requests are independent. Use --growth to multiply DAU for a future horizon.

Examples
  python3 capacity.py --dau 2000000 --req-per-user 40 --peak-factor 4 \\
      --write-fraction 0.05 --write-bytes 2000 --response-bytes 8000 \\
      --retention-days 365 --replication 3 --headroom 1.5 --sensitivity
  python3 capacity.py --selftest
"""
import argparse
import json
import sys

DAY_SECONDS = 86400.0
INPUT_KEYS = ["dau", "req_per_user", "peak_factor", "write_fraction", "write_bytes",
              "response_bytes", "retention_days", "replication", "headroom"]


def compute(p):
    """Return derived quantities for parameter dict p."""
    for k in INPUT_KEYS:
        if p[k] is None or p[k] < 0:
            raise ValueError("parameter %s must be provided and >= 0" % k)
    if not 0 <= p["write_fraction"] <= 1:
        raise ValueError("write_fraction must be within [0, 1]")
    req_day = p["dau"] * p["req_per_user"]
    avg_qps = req_day / DAY_SECONDS
    peak_qps = avg_qps * p["peak_factor"]
    write_qps = peak_qps * p["write_fraction"]
    new_bytes_day = req_day * p["write_fraction"] * p["write_bytes"]
    raw = new_bytes_day * p["retention_days"]
    return {
        "requests_per_day": req_day,
        "avg_qps": avg_qps,
        "peak_qps": peak_qps,
        "peak_write_qps": write_qps,
        "peak_read_qps": peak_qps - write_qps,
        "peak_egress_mbit_s": peak_qps * p["response_bytes"] * 8 / 1e6,
        "new_gb_per_day": new_bytes_day / 1e9,
        "raw_storage_tb": raw / 1e12,
        "provisioned_tb": raw * p["replication"] * p["headroom"] / 1e12,
    }


def sensitivity(p, factors=(2.0, 10.0)):
    """Scale one input at a time; report multiplier on peak QPS and provisioned storage."""
    base = compute(p)
    rows = []
    for key in INPUT_KEYS:
        if key in ("write_fraction",):
            # bounded in [0,1]: use x2 capped at 1 and x10 capped at 1
            pass
        for f in factors:
            q = dict(p)
            q[key] = p[key] * f
            if key == "write_fraction":
                q[key] = min(1.0, q[key])
            r = compute(q)
            rows.append((key, f,
                         r["peak_qps"] / base["peak_qps"] if base["peak_qps"] else 0.0,
                         r["peak_write_qps"] / base["peak_write_qps"] if base["peak_write_qps"] else 0.0,
                         r["provisioned_tb"] / base["provisioned_tb"] if base["provisioned_tb"] else 0.0))
    return rows


def selftest():
    def close(a, b, tol=1e-6):
        return abs(a - b) <= tol * max(1.0, abs(b))

    p = dict(dau=2_000_000, req_per_user=40, peak_factor=4, write_fraction=0.05,
             write_bytes=2000, response_bytes=8000, retention_days=365,
             replication=3, headroom=1.5)
    r = compute(p)
    # Hand computed: 2e6*40 = 8e7 requests/day ; /86400 = 925.9259... ; *4 = 3703.7037...
    assert close(r["requests_per_day"], 8e7)
    assert close(r["avg_qps"], 8e7 / 86400)
    assert close(r["peak_qps"], 3703.7037037)
    assert close(r["peak_write_qps"], 185.185185)
    assert close(r["peak_read_qps"], 3518.518518)
    # 3703.7037 req/s * 8000 B * 8 bit = 237,037,037 bit/s = 237.037 Mbit/s
    assert close(r["peak_egress_mbit_s"], 237.037037)
    # 8e7 * 0.05 * 2000 B = 8e9 B = 8 GB/day ; *365 = 2.92 TB ; *3*1.5 = 13.14 TB
    assert close(r["new_gb_per_day"], 8.0)
    assert close(r["raw_storage_tb"], 2.92)
    assert close(r["provisioned_tb"], 13.14)
    # Sensitivity: doubling peak_factor doubles peak QPS and leaves storage unchanged
    rows = {(k, f): (a, b, c) for k, f, a, b, c in sensitivity(p)}
    assert close(rows[("peak_factor", 2.0)][0], 2.0) and close(rows[("peak_factor", 2.0)][2], 1.0)
    assert close(rows[("retention_days", 10.0)][2], 10.0) and close(rows[("retention_days", 10.0)][0], 1.0)
    # Invalid input rejected
    bad = dict(p, write_fraction=1.5)
    try:
        compute(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for write_fraction > 1")
    print("selftest OK")


def build_parser():
    ap = argparse.ArgumentParser(
        description="Back-of-the-envelope capacity calculator. Prints QPS, bandwidth, storage "
                    "and an optional one-at-a-time sensitivity table.")
    ap.add_argument("--dau", type=float, help="daily active users")
    ap.add_argument("--req-per-user", type=float, help="requests per user per day")
    ap.add_argument("--peak-factor", type=float, help="peak QPS / average QPS (ratio)")
    ap.add_argument("--write-fraction", type=float, help="fraction of requests that write, 0..1")
    ap.add_argument("--write-bytes", type=float, help="bytes stored per write")
    ap.add_argument("--response-bytes", type=float, help="average response size in bytes")
    ap.add_argument("--retention-days", type=float, help="days data is kept")
    ap.add_argument("--replication", type=float, default=1.0, help="copies stored (default 1)")
    ap.add_argument("--headroom", type=float, default=1.0, help="capacity headroom factor (default 1.0)")
    ap.add_argument("--growth", type=float, default=1.0, help="multiply DAU for a future horizon (default 1)")
    ap.add_argument("--sensitivity", action="store_true", help="print x2 and x10 sensitivity table")
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    ap.add_argument("--selftest", action="store_true", help="run built-in asserts and exit")
    return ap


def main(argv=None):
    ap = build_parser()
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    p = dict(dau=None if a.dau is None else a.dau * a.growth, req_per_user=a.req_per_user,
             peak_factor=a.peak_factor, write_fraction=a.write_fraction, write_bytes=a.write_bytes,
             response_bytes=a.response_bytes, retention_days=a.retention_days,
             replication=a.replication, headroom=a.headroom)
    missing = [k for k in INPUT_KEYS if p[k] is None]
    if missing:
        ap.error("missing required inputs: " + ", ".join("--" + m.replace("_", "-") for m in missing))
    try:
        res = compute(p)
        rows = sensitivity(p) if a.sensitivity else []
    except ValueError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"inputs": p, "results": res,
                          "sensitivity": [dict(input=k, factor=f, peak_qps_x=x, write_qps_x=w, storage_x=s)
                                          for k, f, x, w, s in rows]}, indent=2))
        return 0
    print("Derived load")
    print("  requests/day        : %.0f" % res["requests_per_day"])
    print("  average QPS         : %.1f req/s" % res["avg_qps"])
    print("  peak QPS            : %.1f req/s" % res["peak_qps"])
    print("  peak write QPS      : %.1f /s" % res["peak_write_qps"])
    print("  peak read QPS       : %.1f /s" % res["peak_read_qps"])
    print("  peak egress         : %.1f Mbit/s" % res["peak_egress_mbit_s"])
    print("  new data            : %.2f GB/day" % res["new_gb_per_day"])
    print("  raw storage         : %.2f TB over retention" % res["raw_storage_tb"])
    print("  provisioned storage : %.2f TB (x replication x headroom)" % res["provisioned_tb"])
    if rows:
        print("\nSensitivity (multiplier vs baseline when one input is scaled)")
        print("  %-16s %-7s %-10s %-10s %-10s" % ("input", "scale", "peak QPS", "write QPS", "storage"))
        for k, f, x, w, s in rows:
            print("  %-16s x%-6g %-10.2f %-10.2f %-10.2f" % (k, f, x, w, s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
