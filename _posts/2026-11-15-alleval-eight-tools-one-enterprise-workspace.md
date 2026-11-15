---
layout: post
title: "alleval: Eight Evaluation Tools, One Enterprise-Ready Workspace"
date: 2026-11-15 10:30:00 +0800
author: Danny Zeng
categories: [alleval, LLM Evaluation]
tags: [alleval, llm-eval, observability, enterprise, open-source]
---

[alleval](https://github.com/dz3ai/alleval) just went through a full de-staleness pass: every submodule was pinned fresh, three major tools joined the workspace, and a live enterprise-readiness survey now documents what's actually safe to build on. Here's what changed and what we learned.

## What alleval is

alleval is a parent repository that curates the open-source LLM evaluation and observability landscape as pinned git submodules — one clone, eight tools, with honest guidance about which ones are license-safe and actively maintained for enterprise on-prem use.

## The November update

**Three submodules refreshed to main tips:**

| Tool | New pin | Note |
|---|---|---|
| promptfoo | `45f68f0d` | evals + red teaming |
| deepeval | `34db63dd` | pytest-style evals |
| phoenix | `a9ce4b0f` | LLM observability |

**Three new tools joined:**

| Tool | Pin | Why it's here |
|---|---|---|
| [langfuse](https://github.com/langfuse/langfuse) | `48a31810` | Full observability + evals + prompt management (MIT, self-hostable via Docker/K8s) |
| [trulens](https://github.com/truera/trulens) | `32f57106` | Agentic evals, RAG metrics, OTel-native tracing (MIT) |
| [inspect-ai](https://github.com/UKGovernmentBEIS/inspect_ai) | `f72aaad9` | Sandboxed agent evals, 200+ benchmarks (MIT) |

**ragas got repointed and re-pinned.** The project's org moved from `explodinggradients/ragas` to `vibrantlabsai/ragas`, so `.gitmodules` now points at the new home. This surfaced a subtle submodule gotcha: the old pin (`298b6827`) was only reachable from the *old* remote, so fresh clones would have failed `git submodule update --init`. Re-pinning to the new org's main tip (`8c63f10d`, v0.4.4) fixed it. If you maintain a parent repo with submodules, check that every pin resolves from its *declared* URL — not just from wherever you fetched it.

## What the survey found

The full write-up lives in [`docs/ENTERPRISE-READINESS-2026-11-14.md`](https://github.com/dz3ai/alleval/blob/main/docs/ENTERPRISE-READINESS-2026-11-14.md), but the short version:

**The defensible enterprise core is permissively licensed and actively maintained:**

- **promptfoo** (MIT) — evals, red teaming, CI-friendly
- **deepeval** (Apache-2.0) — pytest-style evals, broad metric coverage
- **langfuse** (MIT) — end-to-end observability stack; needs Postgres + ClickHouse + Redis
- **trulens** (MIT) — 7 dedicated agent evaluators, lightweight, OTel-native
- **inspect-ai** (MIT) — library-only sandboxed evals and benchmark reproduction

**The caveats:**

- **phoenix** is Elastic License 2.0 — fine for internal use, but not OSI-approved and it has a third-party-service clause. If that's a problem, [opik](https://github.com/comet-ml/opik) is the Apache-2.0 alternative.
- **ragas** is dormant since February 2026 (and its org moved).
- **helm** is research-grade and slowing.
- The hosted OpenAI Evals service shut down November 30, 2026 — self-hosted tooling is the only durable path.

## Recommended starting stack

For a private enterprise deployment:

1. **promptfoo** — evals, red teaming, CI regression
2. **deepeval** — pytest-style evals with broad metric coverage
3. **langfuse** — full observability, LLM-as-judge, prompt management
4. **trulens** — agentic evals, RAG metrics, OTel tracing
5. **inspect-ai** — sandboxed agent evals and benchmark reproduction
6. **phoenix** — if ELv2 internal-use terms are acceptable

Clone the workspace and get everything in one shot:

```bash
git clone --recurse-submodules git@github.com:dz3ai/alleval.git
```
