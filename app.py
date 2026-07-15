"""
app.py

Entry point for the Token Cost Agent.
"""

from __future__ import annotations

import traceback

from graph import graph
from state import AgentState


def print_banner() -> None:
    """Display application banner."""

    print("=" * 60)
    print("        TOKEN COST AGENT")
    print("=" * 60)
    print()


def print_metrics(state: AgentState) -> None:
    """Print token usage metrics."""

    print("\n" + "=" * 60)
    print("TOKEN USAGE")
    print("=" * 60)

    if not state.token_usage:
        print("No metrics available.")
        return

    for node, metrics in state.token_usage.items():

        print(f"\n[{node.upper()}]")

        for key, value in metrics.items():
            print(f"{key:<20}: {value}")


def main():

    print_banner()

    while True:

        try:

            question = input("\nQuestion > ").strip()

            if not question:
                continue

            if question.lower() in {

                "exit",
                "quit",
                "q",

            }:
                print("\nGoodbye 👋")
                break

            state = AgentState(

                question=question

            )

            result = graph.invoke(state)

            print("\n" + "=" * 60)
            print("ANSWER")
            print("=" * 60)

            print(result.response)

            print_metrics(result)

        except KeyboardInterrupt:

            print("\nInterrupted.")

            break

        except Exception as exc:

            print("\nERROR")

            print("-" * 60)

            print(exc)

            traceback.print_exc()


if __name__ == "__main__":

    main()