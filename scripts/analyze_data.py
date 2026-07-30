from pathlib import Path
import json
from collections import Counter

DATA_DIR = Path("data")

companies = []

# -----------------------
# Загрузка данных
# -----------------------

for file in sorted(DATA_DIR.glob("page_*.json")):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        companies.extend(data["items"])

print("=" * 60)
print("СТАТИСТИКА")
print("=" * 60)

print(f"Всего компаний: {len(companies)}")

# -----------------------
# ID
# -----------------------

ids = [c["id"] for c in companies]
duplicate_ids = [k for k, v in Counter(ids).items() if v > 1]

print(f"Уникальных ID: {len(set(ids))}")
print(f"Повторяющихся ID: {len(duplicate_ids)}")

# -----------------------
# Названия
# -----------------------

names = [c["name"] for c in companies]
duplicate_names = [k for k, v in Counter(names).items() if v > 1]

print(f"Повторяющихся названий: {len(duplicate_names)}")

# -----------------------
# Название + адрес
# -----------------------

pairs = [(c["name"], c["address"]) for c in companies]

duplicate_pairs = [
    k for k, v in Counter(pairs).items()
    if v > 1
]

print("\nПовторяющиеся name + address")

for pair in duplicate_pairs:
    print(pair)

print("\nПолные записи с повторяющимися ID:\n")

for dup in duplicate_ids:
    for company in companies:
        if company["id"] == dup:
            print(company)

# -----------------------
# Города
# -----------------------

cities = Counter(c["city"] for c in companies)

print(f"Количество городов: {len(cities)}")

# -----------------------
# Категории
# -----------------------

categories = Counter(c["category"] for c in companies)

print(f"Количество категорий: {len(categories)}")

# -----------------------
# Сайт
# -----------------------

without_site = sum(
    1 for c in companies
    if not c["site"]
)

print(f"Без сайта: {without_site}")

# -----------------------
# Телефон

without_phone = sum(
    1 for c in companies
    if not c["phone"]
)

print(f"Без телефона: {without_phone}")

# -----------------------
# Рейтинг
# -----------------------

bad_rating = [
    c for c in companies
    if c["rating"] is not None and (c["rating"] < 0 or c["rating"] > 5)
]

print(f"Некорректный рейтинг: {len(bad_rating)}")

missing_rating = sum(
    1 for c in companies
    if c["rating"] is None
)

print(f"Без рейтинга: {missing_rating}")

# -----------------------
# Отзывы
# -----------------------

bad_reviews = [
    c for c in companies
    if c["reviews_count"] < 0
]

print(f"Отрицательное количество отзывов: {len(bad_reviews)}")

print("=" * 60)

print("\nТОП-10 категорий")

for category, count in categories.most_common(10):
    print(f"{category:<30} {count}")

print("\nТОП-10 городов")

for city, count in cities.most_common(10):
    print(f"{city:<20} {count}")
