import glob
import json
import os
import sys

import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

INSERT_SQL = """
    INSERT INTO companies (
        id, name, category, city, address,
        rating, reviews_count, site, phone
    ) VALUES (
        %(id)s, %(name)s, %(category)s, %(city)s, %(address)s,
        %(rating)s, %(reviews_count)s, %(site)s, %(phone)s
    )
    ON CONFLICT (id) DO NOTHING
"""

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_dir = BASE_DIR / "data"
    files = sorted(data_dir.glob("page_*.json"))

    if not files:
        print("Файлы page_*.json не найдены в папке data/")
        return

    conn = None

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
    except psycopg2.OperationalError:
        print("Не удалось подключиться к PostgreSQL.")
        print("Проверьте, что PostgreSQL запущен, и параметры в файле .env.")
        sys.exit(1)

    total_items = 0
    total_inserted = 0

    try:
        with conn.cursor() as cur:
            for path in files:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)

                items = data.get("items", [])
                if not items:
                    print(f"{os.path.basename(path)}: пустой items, пропуск")
                    continue

                cur.executemany(INSERT_SQL, items)
                inserted = cur.rowcount
                total_items += len(items)
                total_inserted += inserted

                print(f"{os.path.basename(path)}: {inserted}/{len(items)} вставлено")

        conn.commit()
        print(f"\nГотово: {total_inserted} из {total_items} записей вставлено")

    except Exception:
        conn.rollback()
        raise
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()