# Company Import

## Запуск
1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. Создать файл `.env`:
```bash
copy .env.example .env
```

Заполнить параметры подключения к PostgreSQL.

3. Создать таблицу:
```bash
psql -U your_username -d your_database -f sql/schema.sql
```

4. Загрузить исходные данные:
```bash
python scripts/load_json.py
```

5. Выполнить аналитические запросы (по желанию):
```bash
psql -U your_username -d your_database -f sql/queries.sql
```

6. Запустить Next.js-приложение:
```bash
cd company-app
npm install
npm run dev
```

После запуска страница доступна по адресу:
```
http://localhost:3000/companies
```

7. Загрузить дополнительную выгрузку:
```bash
python scripts/load_reviews.py
```

8. Проанализировать данные `review.csv`:
```bash
python scripts/analyze_reviews.py
```

## Используемые технологии
* Python
* PostgreSQL
* SQL
* Next.js (App Router)
* TypeScript
* React
