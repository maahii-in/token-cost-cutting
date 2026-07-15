"""
Pipeline Metrics
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class PipelineMetrics:
    """
    Stores token statistics for every node.
    """

    node_metrics: Dict[str, dict] = field(
        default_factory=dict
    )

    def add(
        self,
        node: str,
        input_tokens: int,
        output_tokens: int,
    ):

        self.node_metrics[node] = {

            "input": input_tokens,

            "output": output_tokens,

            "saved": input_tokens - output_tokens,

        }

    @property
    def total_input(self):

        return sum(
            m["input"]
            for m in self.node_metrics.values()
        )

    @property
    def total_output(self):

        return sum(
            m["output"]
            for m in self.node_metrics.values()
        )

    @property
    def total_saved(self):

        return self.total_input - self.total_output

    def summary(self):

        print("\n" + "=" * 60)

        print("TOKEN COST REPORT".center(60))

        print("=" * 60)

        print(
            f"{'Node':20}"
            f"{'Input':>10}"
            f"{'Output':>10}"
            f"{'Saved':>10}"
        )

        print("-" * 60)

        for node, metric in self.node_metrics.items():

            print(
                f"{node:20}"
                f"{metric['input']:>10}"
                f"{metric['output']:>10}"
                f"{metric['saved']:>10}"
            )

        print("-" * 60)

        print(
            f"{'Total Input':20}"
            f"{self.total_input:>10}"
        )

        print(
            f"{'Total Output':20}"
            f"{self.total_output:>10}"
        )

        print(
            f"{'Total Saved':20}"
            f"{self.total_saved:>10}"
        )

        print("=" * 60)