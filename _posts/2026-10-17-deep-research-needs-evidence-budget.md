---
layout: post
title: "Deep Research Needs an Evidence Budget"
date: 2026-10-17 12:58:00 +0300
post_type: applied research note
description: "Deep-research agents need explicit budgets for discovery, inspection, verification, and stopping before their reports can support business decisions."
context_reviewed: 2026-10-17
series: applied-paper-notes
tags: [agents, retrieval, evaluation, decision-support, business]
---

A deep-research agent is a system that turns an open question into a report by planning searches, reading sources, retaining intermediate evidence, and deciding when to stop. That makes it relevant to vendor due diligence, market mapping, regulatory scans, incident reviews, and other business tasks where the answer cannot be copied from one document.

The operational goal is not a longer response. It is a defensible evidence path from the question to the decision. A useful system must find enough of the relevant record, inspect the sources it finds, resolve conflicts and duplicates, and expose the remaining uncertainty. A fluent report can fail at any one of those steps.

Recent work on search agents approaches this problem through different training methods and benchmarks. Across those differences, a common design constraint emerges: token and tool-call limits are not enough. The system also needs an evidence budget that says how much discovery, inspection, verification, and synthesis a task deserves.

## Search is only the discovery layer

[Search-R1](https://arxiv.org/abs/2503.09516) and [ReSearch](https://arxiv.org/abs/2503.19470) train language models to interleave reasoning with multiple search calls. The point is not simply to attach a search API. The policy learns when a knowledge gap justifies a query and how retrieved material should change the next reasoning step.

That is a necessary capability, but a search result is not evidence yet. A result page contains rankings, titles, URLs, and snippets selected by another system. It may omit the qualifying sentence, point to an inaccessible page, or combine text that was not adjacent in the source. Treating the snippet as the source makes the research process fast and fragile.

[OpenResearcher](https://arxiv.org/abs/2603.20278) makes this distinction explicit. Its offline environment exposes three browser operations: `search`, `open`, and `find`. The authors report more than 97,000 synthesized trajectories over a fixed 15-million-document corpus, including trajectories with more than 100 tool calls. In their ablations, retrieving a relevant document did not guarantee a correct answer. Opening and inspecting it materially improved performance.

The same distinction appears in different forms elsewhere. [SFR-DeepResearch](https://arxiv.org/abs/2509.06283) gives a single agent web search, page browsing, and Python. [DeepResearcher](https://arxiv.org/abs/2504.03160) trains against live web interactions rather than assuming a clean closed corpus. [Tongyi DeepResearch](https://arxiv.org/abs/2510.24701) maintains an evolving report as compressed memory instead of carrying the entire history unchanged. These are different implementations of one operational fact: finding, reading, computing, and remembering are separate actions with separate failure modes.

## Four budgets make the process inspectable

An evidence budget can be recorded as four related limits.

| Budget | What it controls | Example completion test |
| --- | --- | --- |
| Discovery | Queries, result pages, repositories, and databases searched | Every required market, jurisdiction, and synonym has a documented search path. |
| Inspection | Full sources opened and relevant passages checked | Every material claim cites an inspected source rather than a search snippet. |
| Verification | Cross-checks, contradiction searches, calculations, and entity resolution | High-impact claims have independent support or an explicit conflict note. |
| Synthesis | Space for comparing evidence, recording uncertainty, and writing the result | The report distinguishes findings, assumptions, unresolved questions, and recommendations. |

The budgets do not have to be fixed counts. A low-risk product comparison may permit one strong primary source per specification. A regulatory interpretation may require the rule text, the effective date, the responsible authority, later amendments, and jurisdiction-specific guidance. The important property is that the allocation follows the consequence of being wrong.

This framing also makes cost discussion more useful. A team can ask whether another ten searches add coverage, whether another source inspection resolves a material uncertainty, or whether the synthesis stage is consuming tokens without adding evidence. Counting all tool calls together hides those differences.

## Stopping is a claim about coverage

[DeepSearchQA](https://arxiv.org/abs/2601.20975) contains 900 multi-step information-seeking tasks across 17 fields. It evaluates complete answer sets, not only a single fact. The reported failure modes include premature stopping, which sacrifices recall, and hedging, which adds low-confidence items to widen coverage at the expense of precision.

That trade-off is familiar in business research. A market map can miss a small supplier that satisfies a critical constraint. It can also become unusable if every remotely related company is included. The right stopping rule therefore depends on the set definition. Before the search begins, the owner should specify:

- inclusion and exclusion criteria;
- the dimensions along which completeness matters;
- acceptable evidence for each item;
- how duplicates and subsidiaries are resolved;
- the residual uncertainty that may remain at the deadline.

The agent can then stop because the declared coverage test is satisfied, not because it has produced a plausible number of paragraphs. If the budget expires first, the output should state which branch remains incomplete.

## The evaluation must follow the decision

[DRACO](https://arxiv.org/abs/2602.11685) builds 100 complex tasks across 10 domains and sources from 40 countries. Its task-specific rubrics cover factual accuracy, breadth and depth, presentation quality, and citation quality. This is stronger than one overall judge score because a system can write clearly while missing evidence, or cite extensively while misunderstanding the sources.

[DR Tulu](https://arxiv.org/abs/2511.19399) goes further during training. Its rubrics evolve with retrieved evidence and contrasting model responses, so the feedback can continue to distinguish outputs as the policy changes. [Rethinking the Design of Reinforcement Learning-Based Deep Research Agents](https://arxiv.org/abs/2510.15862), the paper behind PokeeResearch, separately tests reward design, RL algorithm, data curation, and error-tolerant execution. The authors report gains from LLM feedback, on-policy RLOO, filtering weak training questions, and allowing malformed actions to be repaired at test time.

None of those benchmark results transfers automatically to procurement or compliance. The lesson is structural. A business acceptance test should preserve separate axes for source validity, factual support, required coverage, contradiction handling, citation placement, and presentation. If the organization collapses them into one score, a gain on formatting can conceal a loss on evidence.

## A due-diligence run as a controlled artifact

Consider a team comparing three software vendors for a regulated workflow. A useful research request is more specific than "compare the vendors." It defines the decision, the evidence hierarchy, and the stopping conditions.

The discovery budget might require official product documentation, security and privacy materials, contractual terms, public incident records, and the relevant regulator's guidance. The inspection budget requires the actual documents to be opened, dated, and quoted at the point supporting each claim. The verification budget assigns a second source or reviewer to claims about certifications, data location, breach history, and contractual liability. The synthesis budget produces both a comparison and an exception register.

The resulting artifact should contain at least:

1. the exact question and decision date;
2. the search plan and sources consulted;
3. an evidence ledger linking claims to inspected passages;
4. a contradiction and missing-information queue;
5. the inclusion, exclusion, and stopping rules;
6. the recommendation, with assumptions kept separate from findings.

That record makes human review faster. A reviewer can concentrate on weak evidence and judgment calls instead of reconstructing the entire browsing session. It also makes refreshes cheaper because the next run can identify which sources or facts changed.

## Build the smallest loop that exposes failure

[OpenSeeker](https://arxiv.org/abs/2603.15594) generates difficult questions by traversing a web graph and obscuring entities that would permit keyword shortcuts. It also uses retrospective summarization to compress older observations while keeping recent evidence in detail. Both ideas are useful beyond model training: test cases should require real evidence traversal, and memory compression should preserve provenance rather than only conclusions.

A first implementation does not need a frontier model or a complicated multi-agent hierarchy. It needs a traceable loop:

```text
plan -> search -> open -> extract -> record -> check coverage
                         ^                    |
                         +---- revise --------+
```

Each extracted claim receives a source URL, retrieval time, quoted or structured evidence, and a confidence or conflict state. Search results that were never opened stay marked as leads. The coverage check chooses the next unresolved branch or stops with a reason. A separate synthesis step writes only from the evidence ledger.

This design can use one model, several models, or deterministic tools. [SFR-DeepResearch](https://arxiv.org/abs/2509.06283) is a useful reminder that the control surface can remain small. Adding roles does not repair an undefined evidence standard.

The evidence budget will not make web research certain. Sources can be wrong, inaccessible, coordinated, or outdated. It does make uncertainty visible at the level where a decision owner can act on it. The report is no longer judged by how much research it resembles. It is judged by what was searched, what was inspected, what was verified, and why the process stopped.
