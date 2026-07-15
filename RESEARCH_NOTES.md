# Research provenance and curation notes

This release was reconstructed from the two-layer prototype under
`DAAL/MetaAgent/Agent`. The research design is preserved as four specialist agents
(emotion, exaggeration, bias, and commonsense) followed by conditional verification.

The release fixes or changes the following engineering issues:

- removed the API key that was stored in the original YAML configuration;
- removed local Windows/Linux paths and made all inputs command-line arguments;
- normalized aspect identifiers so configured weights cannot silently miss agents;
- isolated the model provider from orchestration and added strict output parsing;
- added a deterministic offline provider for tests and end-to-end demonstrations;
- used environment variables for credentials and excluded `.env` from Git;
- added CSV and single-item interfaces, structured results, examples, and tests;
- excluded datasets, generated articles, caches, model weights, and experiment logs.

The offline provider is an integration baseline, not a replacement for an LLM or an
external fact-checking service. The DeepSeek provider uses the same two-stage control
flow through an OpenAI-compatible `/chat/completions` endpoint.

## Aegis research materials

The repository README also documents the broader neural architecture developed under
`DAAL/MetaAgent/Aegis`. This architecture uses four LoRA-adapted encoders, a gated
communication module, aspect heads, mutual-prediction heads, and a fused classifier.
It is presented as a research blueprint and is explicitly separated from the validated
lightweight package under `src/mafnd`.

The following project-owned assets were added on 2026-07-15:

- `docs/assets/aegis-architecture.jpg`, copied from `DAAL/MetaAgent/架构图.jpg`;
- `docs/assets/pheme-eventwise-metrics.png`, extracted from slide 20 of
  `DAAL/MetaAgent/国创立项PPT(演讲版).pptx`;
- `docs/assets/baseline-comparison.png`, extracted from the same slide.

The presentation identifies Luo Ziyu as the project member and Gao Min as the advisor.
The extracted experimental tables are labeled preliminary because the current GitHub CI
does not include the full dataset split, checkpoints, or neural training environment
needed to reproduce them.
