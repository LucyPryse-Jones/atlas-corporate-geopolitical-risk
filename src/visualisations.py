from pathlib import Path
import pandas as pd
import plotly.express as px


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "processed" / "risk_register_scored.csv"
OUTPUT_FILE = ROOT / "outputs" / "charts" / "risk_priority_chart.html"


def main() -> None:
    risks = pd.read_csv(INPUT_FILE)

    risks["label"] = risks["country"] + " — " + risks["risk_category"].str.replace("_", " ")

    figure = px.bar(
        risks.sort_values("risk_score_100", ascending=True),
        x="risk_score_100",
        y="label",
        orientation="h",
        color="risk_band",
        color_discrete_map={
            "Low": "#2E8B57",
            "Moderate": "#F4A261",
            "High": "#E76F51",
            "Critical": "#9B2226",
        },
        text="risk_score_100",
        title="Atlas: Geopolitical Exposure Risk Priorities",
        labels={
            "risk_score_100": "Exposure-Weighted Risk Score (0–100)",
            "label": "",
            "risk_band": "Risk Band",
        },
    )

    figure.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    figure.update_layout(
        template="plotly_white",
        height=450,
        legend_title_text="Risk Band",
        margin=dict(l=30, r=30, t=80, b=40),
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    figure.write_html(OUTPUT_FILE)

    print(f"Chart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    