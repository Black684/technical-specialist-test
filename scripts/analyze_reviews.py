import json
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "review.csv"


COLUMNS = [
    "id",
    "name",
    "category",
    "city",
    "address",
    "rating",
    "reviews_count",
    "site",
    "phone",
]


def load_review_csv() -> tuple[pd.DataFrame, set[str]]:
    df = pd.read_csv(DATA_PATH)

    source_ids = set()

    for json_path in sorted((BASE_DIR / "data").glob("page_*.json")):
        with open(json_path, encoding="utf-8") as file:
            data = json.load(file)

            for item in data.get("items", []):
                if item.get("id"):
                    source_ids.add(item["id"])

    return df, source_ids


def analyze_review_data(
    df: pd.DataFrame,
    source_ids: set[str]
) -> dict[str, Any]:

    review_ids = set(
        str(value).strip()
        for value in df["id"].dropna()
    )

    review_only_ids = sorted(review_ids - source_ids)
    source_only_ids = sorted(source_ids - review_ids)

    duplicate_rows = int(df.duplicated().sum())

    duplicate_ids = (
        df["id"]
        .value_counts()
        [lambda x: x > 1]
        .index
        .tolist()
    )

    missing_id = int(df["id"].isna().sum())

    missing_required = int(
        df[
            ["name", "category", "city", "address"]
        ]
        .isna()
        .any(axis=1)
        .sum()
    )

    invalid_rating = 0

    for value in df["rating"]:
        if pd.isna(value) or str(value).strip() in ["", "None", "null", "N/A"]:
            continue

        try:
            rating = float(value)

            if rating < 0 or rating > 5:
                invalid_rating += 1

        except ValueError:
            invalid_rating += 1


    suspicious_city = df[
        df["city"]
        .astype(str)
        .str.contains(
            "санкат",
            case=False,
            na=False
        )
    ]


    return {
        "rows": len(df),
        "unique_ids": len(review_ids),
        "duplicate_rows": duplicate_rows,
        "duplicate_ids": duplicate_ids,
        "missing_id": missing_id,
        "missing_required": missing_required,
        "invalid_rating": invalid_rating,
        "suspicious_city": suspicious_city["city"].tolist(),
        "review_only_ids": review_only_ids,
        "source_only_ids": source_only_ids,
    }


def main() -> None:
    df, source_ids = load_review_csv()

    analysis = analyze_review_data(df, source_ids)

    print("=" * 60)
    print("ОТЧЁТ ПО review.csv")
    print("=" * 60)

    print(f"Строк: {analysis['rows']}")
    print(f"Уникальных ID: {analysis['unique_ids']}")
    print(f"ID только в CSV: {len(analysis['review_only_ids'])}")
    print(f"ID только в исходных JSON: {len(analysis['source_only_ids'])}")
    print(f"Полных дублей строк: {analysis['duplicate_rows']}")

    print("\nАНОМАЛИИ:")
    print(f"- Записей без ID: {analysis['missing_id']}")
    print(f"- Записей с пустыми обязательными полями: {analysis['missing_required']}")
    print(f"- Некорректный рейтинг: {analysis['invalid_rating']}")

    if analysis["duplicate_ids"]:
        print(
            "- Повторяющиеся ID:",
            ", ".join(analysis["duplicate_ids"])
        )

    if analysis["suspicious_city"]:
        print(
            "- Возможная опечатка города:",
            ", ".join(analysis["suspicious_city"])
        )

    if analysis["review_only_ids"]:
        print(
            f"- Новых ID в CSV: {len(analysis['review_only_ids'])}"
        )

    if analysis["source_only_ids"]:
        print(
            f"- Отсутствующих ID из JSON: {len(analysis['source_only_ids'])}"
        )


if __name__ == "__main__":
    main()