# Company Import
## Запуск
```bash
pip install -r requirements.txt
copy .env.example .env
psql -U your_username -d your_database -f sql/schema.sql
python scripts/load_json.py
```

Перед запуском заполните `.env` параметрами подключения к PostgreSQL.
