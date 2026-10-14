# `observability`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Define SLOs and alerts for checkout so we stop getting paged on CPU. Include burn-rate alerts and a check for metric cardinality.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 15,370 | 11,691 |
| Input tokens read across all turns (including cached context) | 349,186 | 367,026 |
| Extra input tokens when the skill is installed | | +17,840 |
| Cost, US dollars at list price | 0.555 | 0.520 |
| Skills invoked in the sample run | none | `observability` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 200 tokens for its name and description, which are in every session where the skill is installed, and about 3,400 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I've written two checkout SLOs, the burn-rate alerts, and a cardinality check, and removed CPU from paging. The cardinality checker passed its test and the YAML files parse. The alert rules themselves haven't been run against Prometheus yet: `promtool` isn't installed here, and I didn't have your real metric names, so I assumed `http_requests_total` and `http_request_duration_seconds` with labels `service`, `route` and `code`. Rename them to match your instrumentation.

**SLOs (30-day window)**

| SLO | Good event | Target | Error budget |
|---|---|---|---|
| Availability | non-5xx responses on `/checkout*` (4xx left out as client errors) | 99.9% | 43.2 min-equivalent |
| Latency | successful requests that finish in ≤ 1 s | 99% | 432 min-equivalent |

The latency SLI needs a histogram bucket at exactly `le="1"` (1 second). If you don't have one, change the threshold to a bucket you do have.

**Alerts**

Each burn-rate alert fires only when both of its windows are over the threshold. Burn rate is how fast the error budget is being used: 1× uses it up exactly at the end of the 30 days.

| Alert | Fires when | Budget used | Action |
|---|---|---|---|
| Fast burn | over 14.4× for both 1 h and 5 min | 2% in 1 h | page |
| Medium burn | over 6× for both 6 h and 30 min | 5% in 6 h | page |
| Slow burn | over 1× for both 3 days and 6 h | 10% in 3 days | ticket |
| `CheckoutSLIMissing` | no checkout request metrics for 10 min | — | page |
| CPU throttling | throttled more than 25% of the time for 2 h | — | ticket |

I checked the budget figures with the observability skill's `slo_budget.py` script. The last two alerts are there because missing data would otherwise look healthy, and so CPU still gets looked at without waking anyone.

**Why CPU no longer pages:** high CPU is a cause, not something customers see. If it does hurt them, the latency or availability alerts fire within minutes; if it doesn't, it shows on the dashboard and sustained throttling opens a ticket.

**Cardinality check** (cardinality means the number of distinct label combinations, i.e. separate time series)
- **In Prometheus:** a ticket opens if checkout goes over 20,000 series in total, any one metric goes over 5,000, or the count doubles within 24 hours. That last one is usually a deploy that added a bad label.
- **In CI, before a bad label ships:** `check_cardinality.py` fails the build if a metric uses a banned label (such as `user_id`, `order_id` or `request_id`), has more than 200 values for one label, or has ID-like values such as raw URLs. Against a test file with a `user_id` label and 300 raw URLs, it caught both problems and failed with exit code 1; a clean file passed.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
I've added SLOs, burn-rate alerts and a cardinality check for checkout in `monitoring/checkout/`. With these rules, only user impact pages anyone; CPU alerts now open tickets. The workspace was empty, so I assumed a Prometheus and Alertmanager setup and guessed the metric names. Those names need checking against what checkout actually exports before you deploy.

The YAML files parse and I ran the cardinality script on a small sample file, where it caught an `order_id` label as expected. I haven't run `promtool` (it isn't installed here) or loaded the rules into a real Prometheus.

**SLOs (30-day window)**
- **Availability:** 99.9% of requests don't return a 5xx error.
- **Latency:** 99% of successful requests finish within 500ms.

**What pages**
- **Fast burn rate:** errors are eating the monthly budget 14.4× faster than allowed over 1 hour, or 6× faster over 6 hours. Each check also needs a short window (5 or 30 minutes) to agree, which cuts false alarms and lets the alert clear soon after the problem stops.
- **Missing metrics:** checkout has reported no request metrics for 10 minutes. Without this, the burn-rate alerts would go quiet during exactly that kind of outage.

**What opens a ticket instead**
- **Slow burn rate:** the budget is being used 3× too fast over a day, or 1× over 3 days.
- **CPU:**
  - Pods being CPU-throttled more than 25% of the time for 30 minutes. Throttling predicts slow responses much better than raw CPU usage.
  - Fleet CPU above 90% of its requested amount for 2 hours, as a capacity warning.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
