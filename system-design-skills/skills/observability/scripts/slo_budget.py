#!/usr/bin/env python3
"""Error budget and burn-rate calculator (standard library only).

Definitions
  budget_ratio   = 1 - SLO                       (allowed bad fraction)
  budget_minutes = window_minutes * budget_ratio (allowed bad minutes at 100% traffic)
  burn_rate      = observed_error_ratio / budget_ratio
                   (1.0 means the budget lasts exactly one SLO window)
  time_to_exhaust = window / burn_rate           (from a full budget)
  budget_consumed = burn_rate * alert_window / slo_window

Examples
  python3 slo_budget.py --slo 99.9
  python3 slo_budget.py --slo 99.9 --window-days 30 --error-ratio 0.0144
  python3 slo_budget.py --slo 99.9 --burn-rate 14.4 --alert-window-hours 1
  python3 slo_budget.py --selftest

Notes
  Request-based SLOs: the "minutes" figure is a time-equivalent of the budget,
  not a literal downtime allowance. Error ratio must be measured over the same
  population of events the SLO is defined on.
"""
import argparse
import sys


def budget_ratio(slo_percent):
    if not (0.0 < slo_percent < 100.0):
        raise ValueError("SLO must be strictly between 0 and 100 (percent), got %r" % slo_percent)
    return 1.0 - slo_percent / 100.0


def budget_minutes(slo_percent, window_days):
    if window_days <= 0:
        raise ValueError("window must be positive")
    return window_days * 24 * 60 * budget_ratio(slo_percent)


def burn_rate(slo_percent, error_ratio):
    if error_ratio < 0 or error_ratio > 1:
        raise ValueError("error ratio must be within [0, 1], got %r" % error_ratio)
    return error_ratio / budget_ratio(slo_percent)


def hours_to_exhaust(window_days, rate):
    if rate <= 0:
        return float("inf")
    return window_days * 24 / rate


def budget_consumed(rate, alert_window_hours, window_days):
    return rate * alert_window_hours / (window_days * 24)


def selftest():
    def close(a, b, tol=1e-9):
        return abs(a - b) <= tol * max(1.0, abs(b))

    # 30 days = 43200 minutes. Hand computed: 43200 * 0.001 = 43.2, *0.0005 = 21.6, *0.0001 = 4.32
    assert close(budget_minutes(99.9, 30), 43.2), budget_minutes(99.9, 30)
    assert close(budget_minutes(99.95, 30), 21.6), budget_minutes(99.95, 30)
    assert close(budget_minutes(99.99, 30), 4.32), budget_minutes(99.99, 30)
    # 99% over 30 days: 432 minutes
    assert close(budget_minutes(99.0, 30), 432.0)
    # Burn rate: error ratio 0.0144 against 0.001 budget = 14.4
    assert close(burn_rate(99.9, 0.0144), 14.4)
    # Error ratio equal to budget ratio -> burn rate 1
    assert close(burn_rate(99.9, 0.001), 1.0)
    # 14.4x on 30 days exhausts in 720h / 14.4 = 50h
    assert close(hours_to_exhaust(30, 14.4), 50.0)
    # Consumed fractions for the SRE Workbook example rows (hand computed over 720h):
    # 14.4 * 1/720 = 0.02 ; 6 * 6/720 = 0.05 ; 1 * 72/720 = 0.10
    assert close(budget_consumed(14.4, 1, 30), 0.02)
    assert close(budget_consumed(6, 6, 30), 0.05)
    assert close(budget_consumed(1, 72, 30), 0.10)
    # Zero errors -> infinite time to exhaust
    assert hours_to_exhaust(30, 0.0) == float("inf")
    # Invalid input is rejected
    for bad in (0.0, 100.0, -1.0):
        try:
            budget_ratio(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for SLO %r" % bad)
    print("selftest OK (9 groups of hand-computed asserts passed)")


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Compute error budget minutes, burn rate and time to exhaustion for an SLO.",
        epilog="See the module docstring (python3 -c 'import slo_budget; help(slo_budget)') for formulas.",
    )
    p.add_argument("--slo", type=float, help="SLO target in percent, e.g. 99.9")
    p.add_argument("--window-days", type=float, default=30.0, help="SLO window in days (default 30)")
    p.add_argument("--error-ratio", type=float,
                   help="observed bad/total ratio in [0,1], e.g. 0.0144 for 1.44%%")
    p.add_argument("--burn-rate", type=float, help="burn rate to evaluate (alternative to --error-ratio)")
    p.add_argument("--alert-window-hours", type=float,
                   help="with a burn rate: fraction of budget consumed if that rate lasts this long")
    p.add_argument("--selftest", action="store_true", help="run built-in asserts and exit")
    args = p.parse_args(argv)

    if args.selftest:
        selftest()
        return 0
    if args.slo is None:
        p.error("--slo is required (or use --selftest)")
    try:
        print("SLO %.4f%% over %g days" % (args.slo, args.window_days))
        print("  allowed bad ratio : %.6f" % budget_ratio(args.slo))
        print("  budget (minutes)  : %.4f" % budget_minutes(args.slo, args.window_days))
        rate = None
        if args.error_ratio is not None:
            rate = burn_rate(args.slo, args.error_ratio)
        elif args.burn_rate is not None:
            if args.burn_rate < 0:
                raise ValueError("burn rate must be >= 0")
            rate = args.burn_rate
        if rate is not None:
            print("  burn rate         : %.4f" % rate)
            h = hours_to_exhaust(args.window_days, rate)
            print("  hours to exhaust  : %s" % ("never at this rate" if h == float("inf") else "%.2f" % h))
            if args.alert_window_hours is not None:
                c = budget_consumed(rate, args.alert_window_hours, args.window_days)
                print("  budget consumed in %g h at this rate: %.2f%%" % (args.alert_window_hours, c * 100))
    except ValueError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
