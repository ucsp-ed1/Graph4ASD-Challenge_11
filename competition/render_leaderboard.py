import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "leaderboard" / "leaderboard.csv"
MD_PATH = ROOT / "leaderboard" / "leaderboard.md"

def read_rows():
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if (r.get("team") or "").strip()]
    return rows

def main():
    rows = read_rows()
    
    # -------------------------
    # Sort by score desc (float), then timestamp desc
    # -------------------------
    def score_key(r):
        try:
            return float(r.get("macro_f1","-inf"))
        except:
            return float("-inf")
    def ts_key(r):
        try:
            return datetime.fromisoformat(r.get("timestamp_utc","").replace("Z","+00:00"))
        except:
            return datetime.fromtimestamp(0)

    # Sort rows: higher score first, then more recent timestamp
    rows.sort(key=lambda r: (score_key(r), ts_key(r)), reverse=True)

    # -------------------------
    # Assign dense ranks
    # -------------------------
    ranks = []
    last_score = None
    last_rank = 0
    for i, r in enumerate(rows, start=1):
        current_score = score_key(r)
        if current_score == last_score:
            rank = last_rank
        else:
            rank = i
            last_score = current_score
            last_rank = rank
        ranks.append(rank)

    # -------------------------
    # Build markdown
    # -------------------------
    lines = []
    lines.append("# Leaderboard\n")

    lines.append("| Rank | Team | Model | Type | Macro-F1 | Date (UTC) |\n")
    lines.append("|------|------|-------|------|----------|------------|\n")

    for r, rank in zip(rows, ranks):
        team = (r.get("team") or "").strip()
        model = (r.get("model") or "").strip()
        score = (r.get("macro_f1") or "").strip()
        type_ = (r.get("type") or "").strip()
        ts = (r.get("timestamp_utc") or "").strip()
        model_disp = f"`{model}`" if model else ""
        lines.append(f"| {rank} | {team} | {model_disp} | {type_} | {score} | {ts} |\n")

    MD_PATH.write_text("".join(lines), encoding="utf-8")

if __name__ == "__main__":
    main()
