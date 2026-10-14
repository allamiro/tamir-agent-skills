# `reliability-resilience`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> A slow payment provider keeps taking checkout down through retry storms. Add timeouts, backoff, circuit breakers and a degradation plan for a 99.95% availability target.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 16,386 | 4,596 |
| Input tokens read across all turns (including cached context) | 297,637 | 73,572 |
| Extra input tokens when the skill is installed | | -224,066 |
| Cost, US dollars at list price | 0.569 | 0.227 |
| Skills invoked in the sample run | none | `reliability-resilience` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 220 tokens for its name and description, which are in every session where the skill is installed, and about 3,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
There's no code in this directory (only `.claude/`), so I couldn't add these to a service directly. Below is the design. Every threshold is a starting value that you need to tune against your provider's real latency numbers and your traffic.

## 1. Target and what counts as "available"

- **99.95% leaves about 21.6 minutes of downtime per 30 days.** For comparison, 99.9% leaves 43.2 minutes.
- **Count a checkout as successful** when it returns a definite result within 10 s: authorized, declined, or "order accepted, payment pending". A card decline is a success. So are "payment unavailable, cart saved" pages served while degraded, as long as they stay within your degradation budget (section 6). A 5xx, a hang, or a timeout with no answer is a failure.
- **Why degradation is required:** checkout = your stack × provider. If your stack is 99.99% and the provider is 99.9%, you get 0.9999 × 0.999 ≈ **99.89%**. That is below target even before retry storms. When a dependency is less available than your target, the target is only reachable if checkout can keep working when that dependency fails, or if you add a second provider.

## 2. Why the retry storms happen

The provider slows down. Each retry layer (client app, gateway, checkout service, payment SDK) multiplies the load: 3 retries at each of 3 layers is up to 27× the calls. Threads and connections fill up waiting on the provider. Then health checks fail, instances are removed, and the remaining instances take more load. Checkout goes down even for traffic that never needed the provider.

## 3. Timeouts and deadlines

| Call | Timeout | Basis |
|---|---|---|
| Whole checkout request (edge) | 10 s absolute deadline, passed down in a header | UX limit |
| Provider TCP/TLS connect | 500 ms | Connects should be fast; slow means unhealthy |
| Provider authorize (each attempt) | `min(provider p99.9 + 30%, remaining deadline − 1 s)`, e.g. 3 s | Measured latency, not SDK defaults |
| Provider status lookup | 2 s | |
| Internal calls (cart, inventory, fraud) | Each callee's p99.9 + margin, all within the deadline | |

- Before each attempt, check the remaining deadline. If it's below the attempt timeout, skip the call and go straight to the fallback.
- **A timed-out authorization has an unknown outcome, not a failed one.** The provider may have charged the card. Never resend it as a new charge (section 4).

## 4. Retries: one layer only, idempotent, with a budget

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
I've written a standalone resilience layer for the payment call, a four-level fallback plan for checkout, and a design doc. The tests are written but haven't been run: the test command needed an approval I didn't have.

**The directory was empty**, so none of this is connected to your real checkout or payment provider yet. It's TypeScript with no dependencies and runs on Node 22.6+ (Node strips the types itself).

To run the tests:
```
node --test test/resilience.test.ts
```

**What stops the retry storm** (`src/resilience.ts`, `src/paymentClient.ts`). Each call passes through a concurrency cap, then the circuit breaker, then a timeout, before reaching the provider:
- **Timeouts:** 2s per attempt and 3.5s in total, so the payment step fits inside a 4s p99 target for checkout. The timeout also cancels the in-flight request.
- **Retries:** at most one, with randomised exponential backoff (100–400ms) that respects the provider's `Retry-After`. Total retries are capped at 10% of traffic, so load on the provider can never more than roughly 1.1×. A call is only retried after a timeout, a 429, or an error the provider marks as retryable, and every call needs an idempotency key.
- **Circuit breaker:** opens when at least half of calls fail, or 60% take longer than 1.5s, over a 10s window with at least 20 calls. The slow-call check catches a slow-but-working provider before timeouts pile up. It stays open for 15s, then lets 3 test calls through. 4xx errors don't count as failures.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
