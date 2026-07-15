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
