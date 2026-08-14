from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "raw" / "exposure_register.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "risk_register_scored.csv"


def risk_band(score: float) -> str:
    if score < 15:
        return "Low"
    if score < 30:
        return "Moderate"
    if score < 50:
        return "High"
    return "Critical"


def score_exposures(exposures: pd.DataFrame) -> pd.DataFrame:
    scored = exposures.copy()

    scored["base_risk_score"] = (
        scored["exposure_weight"]
        * (scored["likelihood"] / 5)
        * (scored["impact"] / 5)
        * scored["confidence"]
    )

    scored["risk_score_100"] = (scored["base_risk_score"] * 100).round(1)
    scored["risk_band"] = scored["risk_score_100"].apply(risk_band)

    return scored.sort_values("risk_score_100", ascending=False)


def main() -> None:
    exposures = pd.read_csv(INPUT_FILE)
    scored_exposures = score_exposures(exposures)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    scored_exposures.to_csv(OUTPUT_FILE, index=False)

    print("\nAtlas risk scoring complete.\n")
    print(
        scored_exposures[
            ["exposure_id", "country", "risk_category", "risk_score_100", "risk_band"]
        ].to_string(index=False)
    )
    print(f"\nSaved scored register to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    