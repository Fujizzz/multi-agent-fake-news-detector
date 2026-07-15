from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class NewsItem:
    content: str
    title: str = ""
    subject: str = ""
    date: str = ""
    identifier: str = ""

    def render(self) -> str:
        parts = []
        if self.title:
            parts.append(f"Title: {self.title}")
        if self.subject:
            parts.append(f"Subject: {self.subject}")
        if self.date:
            parts.append(f"Date: {self.date}")
        parts.append(f"Content: {self.content}")
        return "\n".join(parts)


@dataclass(frozen=True)
class VerificationResult:
    fake_probability: float
    rationale: str


@dataclass(frozen=True)
class DetectionResult:
    label: str
    fake_probability: float
    stage: str
    aspect_scores: dict[str, float]
    explanation: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
