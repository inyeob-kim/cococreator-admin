from dataclasses import dataclass


@dataclass
class MetricPoint:
    bucket: str
    value: float
