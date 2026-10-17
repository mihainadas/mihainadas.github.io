---
layout: page
title: Applied Papers
permalink: /papers/
description: "A business-facing map of research papers on agents, evaluation, efficient models, data, and retrieval."
---

This section starts from research papers and asks a different question from a conventional literature review: what decision, control, or operating practice could the result change? The current map covers 88 entries from Ritvik Rastogi's [Papers Explained archive](https://ritvik19.github.io/papers-explained/), corresponding to the reviewed set numbered 551 through 640. Entries 580 and 586 were not present in that set.

The summaries below are editorial classifications, not substitutes for the papers. Each link points to the public explanation that identified the work. Articles in this section go back to the original paper, separate reported evidence from interpretation, and make the business application explicit.

## Published notes

{% assign applied_posts = site.posts | where: "series", "applied-paper-notes" %}
{% for post in applied_posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.description }}
{% endfor %}

## Evidence systems and research agents

These papers treat research as a sequence of search, reading, state management, verification, and stopping decisions. The business question is not whether an agent can produce a long report. It is whether the organization can inspect how the report acquired and tested its evidence.

| Issue | Research contribution | Business test |
| --- | --- | --- |
| [640: OpenResearcher](https://ritvik19.medium.com/8995d77a1b9a) | Makes long research trajectories reproducible with a fixed corpus and explicit search, open, and find operations. | Can a due-diligence run be replayed after a decision is challenged? |
| [639: OpenSeeker](https://ritvik19.medium.com/ce56311ee04f) | Builds difficult multi-hop questions from web structure and compresses noisy search history. | Can training cases require real evidence traversal instead of keyword matching? |
| [638: DRACO](https://ritvik19.medium.com/ca9e3ffabbb8) | Evaluates research reports across factual accuracy, coverage, presentation, and citation quality. | Does the acceptance test score the dimensions the decision owner actually needs? |
| [637: DeepSearchQA](https://ritvik19.medium.com/f8e42f211c50) | Tests exhaustive, multi-step search where entity resolution and stopping are part of the task. | Does the system stop because the answer set is complete or because its budget expired? |
| [636: DR Tulu](https://ritvik19.medium.com/17f13ca39293) | Trains long-form research with rubrics that evolve as the policy discovers new evidence and failure modes. | Can evaluation keep discriminating after the system learns yesterday's checklist? |
| [635: Tongyi DeepResearch](https://ritvik19.medium.com/8366b11678a8) | Combines agentic mid-training, post-training, automatic data synthesis, and a compressed working memory. | Which research state must remain verbatim, and which can be summarized safely? |
| [634: PokeeResearch](https://ritvik19.medium.com/b6976532d436) | Isolates reward, RL algorithm, data curation, and error recovery as separate design choices. | Is a weak result caused by the model, the training signal, the task mix, or brittle execution? |
| [633: SFR-DeepResearch](https://ritvik19.medium.com/186281b33e3b) | Shows a single agent can combine web search, page reading, and Python under a compact tool interface. | Is a multi-agent organization necessary, or is it hiding a simpler control problem? |
| [632: DeepResearcher](https://ritvik19.medium.com/dbd4d21c23c4) | Trains research behavior against the noisy live web rather than only a closed retrieval corpus. | Has the evaluation included blocked pages, stale snippets, and inconsistent sources? |
| [631: ReSearch](https://ritvik19.medium.com/1f3ba010f95f) | Learns when to interleave reasoning and search without supervised reasoning traces. | Does the agent search to resolve uncertainty, or merely because a workflow tells it to? |
| [630: Search-R1](https://ritvik19.medium.com/614b480de319) | Uses outcome-based RL to teach multiple real-time searches inside a reasoning trajectory. | Are search calls improving the answer enough to justify their latency and cost? |
| [567: Advancing Search Augmented Language Models](https://ritvik19.medium.com/bceb21866e26) | Separates supervised deployment behavior from RL for accuracy and efficient tool use. | Which requirements are hard guardrails, and which should be optimized from outcomes? |
| [562: Is Grep All You Need](https://ritvik19.medium.com/5b10a6e92f77) | Finds that retrieval quality depends on the tool harness and presentation, not only the retrieval algorithm. | Has the team compared the simplest exact-search baseline inside the actual user workflow? |

## Evaluation, governance, and safety

This cluster is about proxies. Benchmarks, rubrics, verifiers, safety classifiers, and privacy filters can make quality measurable, but every proxy creates a new surface for overfitting or omission.

| Issue | Research contribution | Business test |
| --- | --- | --- |
| [629: FRAMES](https://ritvik19.medium.com/f14764317676) | Combines retrieval, multi-hop reasoning, and factual response quality in end-to-end RAG questions. | Does a RAG test isolate retrieval failure from reasoning failure? |
| [628: CRAG](https://ritvik19.medium.com/cff01593ce2d) | Adds diverse question types and simulated web and knowledge-graph APIs to factual QA. | Does the test set include changing facts, unavailable facts, and false premises? |
| [627: FanOutQA](https://ritvik19.medium.com/07b02a669eef) | Measures broad answer-set construction with human decompositions across many documents. | Can the system enumerate a market completely without duplicating the same entity? |
| [626: MultiHop-RAG](https://ritvik19.medium.com/f857b7472974) | Tests inference, comparison, temporal, and null questions that require several documents. | Can the system say that no supported answer exists after a multi-source search? |
| [621: Artificial Hivemind](https://ritvik19.medium.com/1615e8079c92) | Measures how model answers collapse diverse human preferences into similar responses. | Is an ideation tool widening the option set or standardizing everyone on one safe answer? |
| [617: Unsupervised Process Reward Models](https://ritvik19.medium.com/7ee981eb13c4) | Locates likely first errors in reasoning without step labels or final-answer verification. | Can process monitoring find where a workflow first went wrong before damage propagates? |
| [600: Rubric Dropout](https://ritvik19.medium.com/97c3ca77cae7) | Randomly hides rubric criteria during training so a policy cannot optimize one fixed checklist. | Does performance survive when auditors vary the inspection criteria? |
| [596: Shieldstral](https://ritvik19.medium.com/535b8ff3209b) | Frames multimodal moderation under configurable policies as binary question answering. | Can policy changes be versioned independently from the content classifier? |
| [588: LLM-as-a-Verifier](https://ritvik19.medium.com/58c8ab45fb3f) | Uses the verifier's score distribution instead of a single discrete judgment. | Are borderline cases routed by calibrated uncertainty rather than a brittle pass or fail? |
| [581: Rubric Guided Self Distillation](https://ritvik19.medium.com/bd61a188450f) | Distills rubric-conditioned behavior into a model that no longer needs a verifier on every call. | Which quality controls can be internalized, and which still require independent review? |
| [579: POW3R](https://ritvik19.medium.com/6fa98f57e4f9) | Reweights rubric criteria according to which ones still distinguish current outputs. | Is optimization effort spent on unresolved quality gaps rather than already-saturated metrics? |
| [578: Reward Hacking in Rubric-Based RL](https://ritvik19.medium.com/cfefd83ed729) | Shows that better rubric scores can coexist with worse broader quality. | What holdout review would reveal checklist compliance without actual improvement? |
| [572: IFBench](https://ritvik19.medium.com/959c7204cf10) | Tests instruction following on new, programmatically verifiable constraints. | Does a workflow obey unfamiliar contractual formats or only templates seen in tuning? |
| [566: OpenAI Privacy Filter](https://ritvik19.medium.com/04d7eae93107) | Uses an efficient long-context token classifier to find and redact personal information. | Is privacy filtering measured for recall, over-redaction, context length, and local policy? |
| [564: How2Everything](https://ritvik19.medium.com/baef4f7ae61f) | Builds data, a benchmark, and a judge for detecting critical errors in generated procedures. | Can an operations assistant be tested for unsafe omissions rather than fluent wording? |
| [563: Likelihood-Based Reward Designs](https://ritvik19.medium.com/e889106eff08) | Compares probability and log-probability rewards across verifiable and open-ended reasoning. | Does the reward preserve meaningful differences, or collapse outcomes into a coarse binary signal? |
| [555: IH Challenge](https://ritvik19.medium.com/cf2433051b7e) | Trains and evaluates obedience to instruction priority across system, developer, user, and tool roles. | Can lower-trust content override policy or authorization in the deployed prompt stack? |
| [553: Rubrics as Rewards](https://ritvik19.medium.com/229ff69f7355) | Turns instance-specific, interpretable criteria into reinforcement-learning rewards. | Can domain experts inspect and amend the definition of a good result? |

## Training, curricula, and specialist agents

The common theme is allocation: which examples, traces, rewards, teachers, and specialist tasks deserve training compute. For a business, the practical unit is not the parameter count alone but the cost of acquiring a dependable capability.

| Issue | Research contribution | Business test |
| --- | --- | --- |
| [625: Nemotron Labs IMO 2026](https://ritvik19.medium.com/73ce03261940) | Uses repeated natural-language proof generation, verification, and refinement without a formal prover. | When does an expensive generate-check-refine loop beat one fast answer? |
| [624: GenCluster](https://ritvik19.medium.com/8ad12cc83bac) | Clusters diverse candidate programs before ranking and submission. | Can validation spend cover different solution families instead of near-duplicates? |
| [623: Nemotron 3 CC](https://ritvik19.medium.com/6d6d3b72b060) | Joins problem curation, synthetic traces, SFT, RL, and test-time correction for competitive programming. | Which stage contributes measurable reliability in an agentic software pipeline? |
| [622: Complete Reasoning Traces](https://ritvik19.medium.com/9eb91bf0b897) | Finds that partial or endpoint traces can retain much of the post-training value of full traces. | Are costly full process logs necessary, or would verified milestones carry the signal? |
| [618: SFT Conflicts, RL Coexists](https://ritvik19.medium.com/1ecd4a2d9bd8) | Reports stronger cross-task interference in sequential SFT than in sparse RL updates. | Does adding one capability erase another in the release regression suite? |
| [616: Is One Layer Enough](https://ritvik19.medium.com/36b5241b379b) | Concentrates much of the measured RL gain in a small number of middle layers. | Can adaptation scope be narrowed without losing the target behavior? |
| [610: TailSFT](https://ritvik19.medium.com/4875d05e400f) | Focuses SFT on sequences the model has not yet covered rather than repeatedly fitting easy cases. | Is the training queue reducing failure coverage or only average loss? |
| [609: TinyGSM](https://ritvik19.medium.com/da8672bca027) | Uses large synthetic math data plus a verifier to train small generation systems. | Can synthetic cases and automated checks substitute for scarce expert-written examples? |
| [608: TinyStories](https://ritvik19.medium.com/0218b6d43763) | Constrains vocabulary and story structure so very small models expose learning behavior clearly. | Can a reduced-domain prototype test the learning pipeline before full-scale spend? |
| [607: CLRS-Text](https://ritvik19.medium.com/60a80a8e43ef#ee39) | Expresses algorithmic execution traces as text across classical tasks. | Can process reasoning be evaluated against exact state transitions rather than prose quality? |
| [606: On-policy Distillation with Verifiable Reward](https://ritvik19.medium.com/3f231794b5b4) | Combines token-level teacher guidance with trajectory-level correctness. | Can dense coaching remain subordinate to the outcome that matters? |
| [605: Passive Skill Distillation](https://ritvik19.medium.com/481e342aa9d1) | Extracts reusable procedural skills from agent trajectories and injects them as compact instructions. | Which repeated workflow knowledge belongs in a playbook instead of the model weights? |
| [602: SOAR](https://ritvik19.medium.com/7b56235c07c2) | Rewards a problem-generating teacher according to the student's improvement on hard cases. | Can test generation be optimized for learning value rather than novelty alone? |
| [601: SCRL](https://ritvik19.medium.com/c1d94c6f3b00) | Converts hard problems into verified subproblems ordered as a curriculum. | Can a complex business process be taught through auditable intermediate competencies? |
| [598: Compress Distil](https://ritvik19.medium.com/c5f78c8c8a18) | Rewrites long correct reasoning traces into shorter supervision before training a student. | How much explanation cost can be removed without removing the decision signal? |
| [597: Leanstral](https://ritvik19.medium.com/06f0927fe5b0) | Specializes general code agents for Lean proof work without a bespoke operating shell. | When should a shared agent interface host a high-assurance specialist? |
| [595: Unsupervised On-Policy Self Distillation](https://ritvik19.medium.com/13e21a1df42d) | Uses agreement among a model's own rollouts to create a corrective teaching signal. | Can internal consensus improve a system without hiding correlated mistakes? |
| [594: TREK](https://ritvik19.medium.com/da20a690b2ad) | Uses a short teacher-guided phase to expand the student's exploration before returning to RL. | Is a weak learner missing knowledge, or merely failing to visit useful solution modes? |
| [593: Self-Distillation Fine-Tuning](https://ritvik19.medium.com/651ba44d1163) | Teaches from demonstrations through a privileged self-teacher while the student trains on its own rollouts. | Can new procedures be learned without a separate reward service or broad capability loss? |
| [592: Self-Distilled Reasoner](https://ritvik19.medium.com/72bb42dd93ed) | Gives one model privileged answer information in the teacher role and removes it in the student role. | What information may guide training but will not exist at production time? |
| [591: Generalized Knowledge Distillation](https://ritvik19.medium.com/52bebe2e0252) | Applies teacher feedback to sequences sampled from the student rather than only fixed teacher outputs. | Is the teacher correcting mistakes the deployed student actually makes? |
| [589: Weak-to-Strong On-Policy Distillation](https://ritvik19.medium.com/6dd143fcdd0b) | Constructs a capability direction from contrasting weak models and transfers it to a stronger student. | Can cheap specialist signals improve a stronger general system without copying a weak model wholesale? |
| [587: OpenThoughts Agent](https://ritvik19.medium.com/567cddd67283) | Uses controlled ablations to identify which instructions, teachers, filters, and task sources matter for agent data. | Has the data pipeline measured contribution by source rather than assuming more traces are better? |
| [585: VibeThinker-3B](https://ritvik19.medium.com/a82a4fe1299f) | Combines curriculum SFT, multi-domain RL, and self-distillation in a compact reasoning model. | What capability floor is achievable under a strict deployment-size budget? |
| [584: VibeThinker-1.5B](https://ritvik19.medium.com/ef56288a0329) | Separates diverse solution discovery in SFT from reinforcement of correct paths in RL. | Should exploration and reliability be optimized in different training stages? |
| [577: MAI-Thinking-1](https://ritvik19.medium.com/e5afeca9bbfc) | Builds a large reasoning model with human-generated data and iterative empirical optimization. | Is model provenance compatible with the organization's licensing and audit requirements? |
| [576: Aryabhata 2](https://ritvik19.medium.com/9d3d23738731) | Applies phased RL to a cleaned curriculum for competitive-exam reasoning. | Does a narrow expert model benefit from domain sequencing more than a mixed training pool? |
| [560: Apriel-1.5-OpenReasoner](https://ritvik19.medium.com/5826103aac57) | Balances five reasoning domains with adaptive sampling and difficulty-aware length penalties. | Can the training scheduler prevent one high-volume domain from consuming the model? |
| [559: Composer 2](https://ritvik19.medium.com/9bc921210902) | Trains a coding agent in realistic software environments for long planning and multi-step execution. | Does coding evaluation include repository navigation, recovery, and end-to-end task completion? |
| [557: Beyond Web](https://ritvik19.medium.com/eb0483a21dff) | Rephrases targeted documents to make synthetic pretraining data denser and more diverse. | Is synthetic data adding useful coverage or merely restating the same source distribution? |
| [556: The Art of Asking](https://ritvik19.medium.com/604ba808ff26) | Optimizes translated prompts for naturalness, cultural fit, and difficulty across languages. | Has a multilingual product localized the task itself, not only translated its words? |
| [552: Nemotron Cascade 2](https://ritvik19.medium.com/1ac869c28c8c) | Combines multi-stage RL and on-policy distillation in an efficient mixture-of-experts model. | Which staged training costs buy reusable capability across math, code, and agents? |
| [551: QED Nano](https://ritvik19.medium.com/dd7f19dec9d7) | Trains a compact proof model with SFT, rubric rewards, and an iterative reasoning cache. | Can formal-quality output be decomposed into drafting, checking, and memory controls? |

## Architecture, context, and deployment efficiency

These papers change where computation and parameters live. Their business relevance is a cost ledger: training cost, serving cost, task-specific storage, latency, and operational flexibility are different quantities.

| Issue | Research contribution | Business test |
| --- | --- | --- |
| [620: NoRA](https://ritvik19.medium.com/18c1ed7abf2a) | Normalizes LoRA's down-projection to improve optimization while retaining exact mergeability. | Does a cheaper adaptation method remain stable across tasks and release merges? |
| [619: Low-Rank Training](https://ritvik19.medium.com/cc3f8c294de5) | Applies low-rank parameterization to feed-forward layers during pretraining, not only adaptation. | Is the organization reducing training compute or only task-specific parameter count? |
| [615: YaRN](https://ritvik19.medium.com/3eb0225c90db) | Extends RoPE context lengths with limited additional training. | Does the long-context claim survive the document lengths and positions in production? |
| [614: NoPE](https://ritvik19.medium.com/9a670429a736) | Challenges explicit positional encodings on length generalization tasks. | Is the architecture feature improving the target workload or persisting by convention? |
| [613: ALiBi](https://ritvik19.medium.com/66ff030750bf) | Adds distance-dependent attention bias instead of positional embeddings. | Can longer inputs be supported without retraining the entire representation scheme? |
| [612: RoPE](https://ritvik19.medium.com/5797f508073f) | Represents absolute position through rotation while exposing relative distance in attention. | Which context-extension methods remain compatible with the deployed backbone? |
| [611: Position Encodings](https://ritvik19.medium.com/3dafda9e6f47) | Compares the mechanisms that give a parallel Transformer token order. | Is sequence order encoded in a way that matches extrapolation and latency requirements? |
| [604: Kimi K3](https://ritvik19.medium.com/97c6b5e539bb) | Combines sparse activation, native multimodality, and very long context at large scale. | Which claimed capability requires the full model, and which can be served by a smaller route? |
| [603: Kimi K2.5](https://ritvik19.medium.com/2598a949ad61) | Jointly trains text and vision for an open multimodal agentic model. | Does multimodality improve the actual workflow or add an expensive unused interface? |
| [599: Sparse Upcycling](https://ritvik19.medium.com/804de5de9c18) | Converts a trained dense checkpoint into a sparse mixture-of-experts model. | Can sunk pretraining cost be reused without multiplying serving complexity? |
| [590: Nemotron 3 Nano Omni](https://ritvik19.medium.com/7761aa5c9e09) | Adds native audio, image, and video support to an efficient sparse backbone. | Which modalities need one shared model, and which require separate quality controls? |
| [583: Mellum 2](https://ritvik19.medium.com/7c59fdbfb6e6) | Uses sparse experts for code editing, debugging, tool use, and conversational programming. | Does one coding model meet both interactive latency and agentic execution needs? |
| [582: Mellum](https://ritvik19.medium.com/765aef2f7e6c) | Targets low-latency, multi-line IDE completion with a compact open model. | Is the product optimizing for completion speed rather than benchmark breadth? |
| [573: EMO](https://ritvik19.medium.com/9ab88479e1f2) | Encourages domain-specialized experts that can be composed or deployed selectively. | Can unused capabilities be removed from a deployment without retraining the whole model? |
| [571: Olmo 3](https://ritvik19.medium.com/1ee7134a4e67) | Releases models, data, training details, and checkpoints across general and reasoning variants. | Does openness reduce vendor risk enough to offset self-hosting responsibility? |
| [568: Arcee Trinity](https://ritvik19.medium.com/03b148275c8a) | Mixes local and global attention with sparse experts and explicit load balancing. | Are throughput gains preserved under the organization's real request distribution? |
| [565: Sarvam 30B and 105B](https://ritvik19.medium.com/fea8e76080fa) | Builds Indic-focused reasoning models with locally optimized tokenization. | Does regional language coverage require a different tokenizer and data supply chain? |
| [558: Nemotron 3 Super](https://ritvik19.medium.com/a85eaac06bc3) | Combines hybrid sequence layers, sparse experts, low precision, and multi-token prediction. | Which optimization lowers total serving cost after hardware and software constraints are included? |

## Data and representation

This group concerns what the system stores, compares, and retrieves. The practical concern is whether the representation preserves the distinctions needed by a search, classification, or multimodal workflow.

| Issue | Research contribution | Business test |
| --- | --- | --- |
| [575: Gemini Embedding 2](https://ritvik19.medium.com/a9e9ed849227) | Maps text, image, video, audio, and PDFs into one multilingual space with variable dimensions. | Does one index improve cross-modal discovery without erasing modality-specific evidence? |
| [574: Jina Embeddings v5 Omni](https://ritvik19.medium.com/1a08a156e52e) | Adds frozen modality encoders around a text embedding space and trains small connectors. | Can new document types be added without rebuilding the entire retrieval stack? |
| [570: gzip and Scaling Laws](https://ritvik19.medium.com/44c1d94b1213) | Uses compression as a proxy for data complexity when predicting scaling behavior. | Can a cheap complexity measure improve data and compute planning before a training run? |
| [569: Text Classification with Gzip](https://ritvik19.medium.com/ffda2859c6f4) | Combines normalized compression distance with nearest-neighbor classification. | Has the team tested a transparent non-neural baseline before adopting a larger classifier? |
| [561: FinePhrase](https://ritvik19.medium.com/bf43cd53d6b9) | Treats synthetic pretraining data as a recipe optimized through many controlled experiments. | Are synthetic-data costs tied to ablations that show which transformations help? |
| [554: Jina Embeddings v5 Text](https://ritvik19.medium.com/09ac59ff93b7) | Combines distillation and contrastive objectives for compact, multilingual, quantization-tolerant embeddings. | Do retrieval tests include truncation, language mix, and the quantized production index? |

## Editorial rule for this section

An applied note must identify the system and question before presenting a result. It must link the original paper, state what the experiment actually measured, name at least one plausible business use, and include a reason the result may fail to transfer. A benchmark table is evidence about a benchmark. It is not a procurement decision, a compliance approval, or a production reliability claim by itself.
