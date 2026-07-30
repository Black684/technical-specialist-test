import csv
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


CSV_PATH = "data/review.csv"

def clean_rating(value):
    if not value:
        return None

    value = value.strip()

    if value.lower() in ["n/a", "na", "none", "null"]:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def clean_reviews_count(value):
    if not value:
        return 0

    value = value.strip()

    if value.lower() in ["n/a", "na", "none", "null"]:
        return 0

    try:
        return int(float(value))
    except ValueError:
        return 0

INSERT_SQL = """
INSERT INTO companies (
    id,
    name,
    category,
    city,
    address,
    rating,
    reviews_count,
    site,
    phone
)
VALUES (
    %(id)s,
    %(name)s,
    %(category)s,
    %(city)s,
    %(address)s,
    %(rating)s,
    %(reviews_count)s,
    %(site)s,
    %(phone)s
)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    city = EXCLUDED.city,
    address = EXCLUDED.address,
    rating = EXCLUDED.rating,
    reviews_count = EXCLUDED.reviews_count,
    site = EXCLUDED.site,
    phone = EXCLUDED.phone;
"""


def main():

    with open(CSV_PATH, encoding="utf-8") as file:
        reader = csv.DictReader(file)

        rows = list(reader)

    print(f"Найдено записей: {len(rows)}")


    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


    inserted = 0

    try:
        with conn.cursor() as cur:

            for row in rows:

                cur.execute(
                    INSERT_SQL,
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "category": row["category"],
                        "city": row["city"],
                        "address": row["address"],
                        "rating": clean_rating(row["rating"]),
                        "reviews_count": clean_reviews_count(row["reviews_count"]),
                        "site": row["site"] or None,
                        "phone": row["phone"] or None,
                    }
                )

                inserted += 1

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


    print(f"Загружено записей: {inserted}")


if __name__ == "__main__":
    main()