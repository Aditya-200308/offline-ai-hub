"""
Model Comparison & Performance Benchmarking Harness
Executes standardized prompts across local models, measuring latency, TTFT, speed, and memory.
"""

import time
import time
import pandas as pd
from typing import List, Dict
from src.local_llm import LocalLLMEngine
from src.hardware_monitor import HardwareMonitor


BENCHMARK_PROMPTS = [
    {
        "id": "BENCH-01",
        "category": "Code Synthesis",
        "prompt": "Write a Python function to compute the longest common subsequence between two strings using dynamic programming with O(m*n) space.",
        "eval_criteria": "Requires correct syntax, DP table memoization, and docstrings."
    },
    {
        "id": "BENCH-02",
        "category": "Multi-Step Logic",
        "prompt": "A clinic has 3 doctors: Dr. A works Mon-Wed, Dr. B works Wed-Fri, Dr. C works Fri-Sun. An emergency surgery requires 2 doctors on a single day. Which days can the surgery happen, and who would be on duty?",
        "eval_criteria": "Requires step-by-step constraint elimination yielding Wednesday and Friday."
    },
    {
        "id": "BENCH-03",
        "category": "Information Extraction",
        "prompt": "Extract JSON from: 'Invoice #INV-8821 dated 2026-03-12 for Client Acme Corp totaling $14,250.00 with 15% VAT included. Net amount is $12,391.30.' Output keys: invoice_id, client, net, vat, total.",
        "eval_criteria": "Requires valid strict JSON output matching extracted entity fields."
    },
    {
        "id": "BENCH-04",
        "category": "Private Document Summarization",
        "prompt": "Summarize this clinical trial protocol: 'Phase II double-blind placebo study of Compound X-79 in 240 randomized patients with Stage 2 hypertension. Primary endpoint is systolic reduction at 12 weeks. Secondary endpoints include adverse cardiac events and renal filtration rate.' In 3 bullet points.",
        "eval_criteria": "Requires concise 3-bullet factual summary without speculative additions."
    }
]


class BenchmarkRunner:
    """Runs automated performance evaluation across local and fallback models."""

    def __init__(self, engine: LocalLLMEngine = None):
        self.engine = engine or LocalLLMEngine()

    def run_benchmark(self, models: List[str], max_tests: int = 4, progress_callback=None) -> pd.DataFrame:
        """
        Executes benchmark suite across listed models.
        Returns detailed telemetry dataframe.
        """
        records = []
        tests_to_run = BENCHMARK_PROMPTS[:max_tests]
        total_steps = len(models) * len(tests_to_run)
        current_step = 0

        for model in models:
            for test in tests_to_run:
                current_step += 1
                if progress_callback:
                    progress_callback(current_step, total_steps, f"Testing {model} on {test['category']}...")

                # Track hardware & inference
                def _infer():
                    return self.engine.generate(
                        prompt=test["prompt"],
                        model=model,
                        temperature=0.3
                    )

                result, telemetry = HardwareMonitor.track_inference(_infer)

                # Quality heuristic: length check + keyword presence
                resp_text = result.get("response", "")
                quality_score = self._score_response(test["category"], resp_text)

                records.append({
                    "Model": model,
                    "Benchmark ID": test["id"],
                    "Category": test["category"],
                    "Tokens/Sec": result.get("tokens_per_sec", 0.0),
                    "TTFT (ms)": result.get("ttft_ms", 0.0),
                    "Latency (s)": result.get("total_latency_s", 0.0),
                    "Tokens Generated": result.get("tokens_generated", 0),
                    "RAM Delta (MB)": telemetry.get("memory_delta_mb", 0.0),
                    "Quality Score (0-100)": quality_score,
                    "Engine": result.get("engine", "Local")
                })

        return pd.DataFrame(records)

    def _score_response(self, category: str, text: str) -> int:
        """Heuristic response scoring for rapid automated evaluation."""
        if not text or len(text.strip()) < 20:
            return 20
        
        score = 75
        if category == "Code Synthesis" and ("def " in text or "```python" in text):
            score += 20
        elif category == "Multi-Step Logic" and ("Wednesday" in text or "Friday" in text or "wednesday" in text.lower()):
            score += 25
        elif category == "Information Extraction" and ("{" in text and "}" in text):
            score += 20
        elif category in ["Private Document Summarization", "Air-Gap Summarization"] and (text.count("•") >= 2 or text.count("-") >= 2 or text.count("1.") >= 1):
            score += 20

        return min(score, 100)

    @staticmethod
    def create_speed_comparison_chart(df: pd.DataFrame):
        """Generates an interactive Plotly bar chart comparing generation speed."""
        import plotly.express as px
        avg_df = df.groupby("Model").agg({
            "Tokens/Sec": "mean",
            "TTFT (ms)": "mean",
            "Latency (s)": "mean",
            "Quality Score (0-100)": "mean"
        }).reset_index()

        fig = px.bar(
            avg_df,
            x="Model",
            y="Tokens/Sec",
            color="Model",
            text="Tokens/Sec",
            title="🦙 Average Token Generation Speed (Tokens / Second)",
            template="plotly_dark",
            color_discrete_sequence=["#f59e0b", "#38bdf8", "#10b981", "#ec4899", "#8b5cf6"]
        )
        fig.update_traces(texttemplate='%{text:.1f} t/s', textposition='outside')
        fig.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.4)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            font=dict(family="JetBrains Mono, monospace", color="#e2e8f0"),
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig

    @staticmethod
    def create_latency_ttft_chart(df: pd.DataFrame):
        """Generates an interactive scatter chart of TTFT vs Generation Latency."""
        import plotly.express as px
        fig = px.scatter(
            df,
            x="TTFT (ms)",
            y="Latency (s)",
            color="Model",
            size="Tokens Generated",
            hover_data=["Category", "Tokens/Sec"],
            title="⏱️ Time-To-First-Token (TTFT) vs Total Latency",
            template="plotly_dark",
            color_discrete_sequence=["#f59e0b", "#38bdf8", "#10b981", "#ec4899"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.4)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            font=dict(family="JetBrains Mono, monospace", color="#e2e8f0"),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig

