# Multi-Agent Fake-News Detector

This repository contains a reproducible two-stage fake-news detection pipeline. Four
specialist agents independently inspect a news item for:

- emotional incitement;
- exaggeration and clickbait;
- one-sided or partisan bias; and
- conflict with commonsense or basic plausibility.

Their weighted scores form a first-stage screening decision. Uncertain cases—and
moderately confident fake predictions—are routed to a second verification layer. This
keeps the original multi-agent research design while exposing a clean provider boundary.

Two providers are included:

- `heuristic`: deterministic, offline, dependency-free, and suitable for smoke tests;
- `deepseek`: an OpenAI-compatible HTTP client using `DEEPSEEK_API_KEY`.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e .
```

The runtime has no third-party dependencies. For development:

```bash
python -m pip install -e ".[dev]"
```

## Offline quick start

Analyze one item:

```bash
mafnd --provider heuristic \
  --title "SHOCKING SECRET" \
  --text "An unbelievable miracle has been exposed!"
```

Analyze a CSV file:

```bash
mafnd --provider heuristic \
  --input examples/news.csv \
  --output outputs/predictions.csv
```

The CSV reader accepts `content` or `text`, plus optional `id`, `title`, `subject`,
`date`, and `label` columns. If labels are present, the command reports accuracy.

## DeepSeek mode

Never store an API key in source code or configuration committed to Git. Export it in
your shell and select the provider:

```bash
export DEEPSEEK_API_KEY="..."
mafnd --provider deepseek --input examples/news.csv
```

PowerShell:

```powershell
$env:DEEPSEEK_API_KEY = "..."
mafnd --provider deepseek --input examples/news.csv
```

`DEEPSEEK_BASE_URL` defaults to `https://api.deepseek.com`; `--base-url` and `--model`
can target another OpenAI-compatible chat-completions endpoint.

## Decision flow

Each specialist returns a suspicion score in `[0, 1]`. The screening probability is a
normalized weighted average. Scores at or below `0.30` are initially real, scores at or
above `0.70` are initially fake, and the region in between is uncertain. The second
stage reviews uncertain cases and fake predictions below `0.90`.

The defaults mirror the original prototype and can be changed through the Python API:

```python
from mafnd import HeuristicProvider, MultiAgentDetector, NewsItem

detector = MultiAgentDetector(
    HeuristicProvider(),
    real_threshold=0.30,
    fake_threshold=0.70,
    second_layer_fake_cap=0.90,
    self_consistency=1,
)
result = detector.detect(NewsItem(title="Example", content="Article text"))
print(result.to_dict())
```

## Testing

```bash
pytest
```

Tests cover provider-free end-to-end detection, screening/verification behavior, weight
validation, and CSV output. DeepSeek requests are intentionally excluded from automated
tests to avoid network calls and credential use.

## Responsible use

This is a research prototype, not an automated fact-checker. Style, emotion, bias, and
plausibility cues are not proof that a claim is false. Human review and evidence from
reliable external sources are required before moderation, publication, or enforcement
decisions. Only synthetic examples are included; verify dataset licenses and privacy
requirements before redistributing real data.

No open-source license has been selected for this code yet. The repository owner should
choose one before encouraging third-party reuse. See `RESEARCH_NOTES.md` for curation
details and the mapping to the original prototype.
