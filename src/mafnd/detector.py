"""Two-stage orchestration for specialist fake-news detection agents."""

from __future__ import annotations

import statistics
from typing import Mapping

from .models import DetectionResult, NewsItem
from .providers import ASPECTS, AgentProvider


DEFAULT_WEIGHTS = {
    "emotion": 0.30,
    "exaggeration": 0.25,
    "bias": 0.30,
    "commonsense": 0.15,
}


class MultiAgentDetector:
    """Four specialist agents followed by a conditional verification layer."""

    def __init__(
        self,
        provider: AgentProvider,
        *,
        weights: Mapping[str, float] | None = None,
        real_threshold: float = 0.30,
        fake_threshold: float = 0.70,
        second_layer_fake_cap: float = 0.90,
        self_consistency: int = 1,
    ) -> None:
        if not 0.0 <= real_threshold < fake_threshold <= 1.0:
            raise ValueError("Thresholds must satisfy 0 <= real < fake <= 1")
        if self_consistency < 1:
            raise ValueError("self_consistency must be at least 1")
        selected = dict(weights or DEFAULT_WEIGHTS)
        if set(selected) != set(ASPECTS):
            raise ValueError(f"weights must contain exactly: {', '.join(ASPECTS)}")
        total = sum(float(value) for value in selected.values())
        if total <= 0:
            raise ValueError("weights must have a positive sum")
        self.provider = provider
        self.weights = {name: float(selected[name]) / total for name in ASPECTS}
        self.real_threshold = real_threshold
        self.fake_threshold = fake_threshold
        self.second_layer_fake_cap = second_layer_fake_cap
        self.self_consistency = self_consistency

    def detect(self, item: NewsItem) -> DetectionResult:
        scores = {
            aspect: statistics.median(
                float(self.provider.score(aspect, item)) for _ in range(self.self_consistency)
            )
            for aspect in ASPECTS
        }
        stage_one_probability = sum(scores[name] * self.weights[name] for name in ASPECTS)
        if stage_one_probability >= self.fake_threshold:
            initial_label = "fake"
        elif stage_one_probability <= self.real_threshold:
            initial_label = "real"
        else:
            initial_label = "uncertain"

        needs_verification = initial_label == "uncertain" or (
            initial_label == "fake" and stage_one_probability < self.second_layer_fake_cap
        )
        if needs_verification:
            verification = self.provider.verify(item, scores)
            probability = max(0.0, min(1.0, verification.fake_probability))
            return DetectionResult(
                label="fake" if probability >= 0.5 else "real",
                fake_probability=probability,
                stage="verification",
                aspect_scores=scores,
                explanation=verification.rationale,
            )

        explanation = (
            "The first-stage specialist consensus was outside the uncertainty region; "
            "the verification layer was not invoked."
        )
        return DetectionResult(
            label=initial_label,
            fake_probability=stage_one_probability,
            stage="screening",
            aspect_scores=scores,
            explanation=explanation,
        )
