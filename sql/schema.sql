DROP TABLE IF EXISTS companies;

CREATE TABLE companies (
    id TEXT PRIMARY KEY,

    name TEXT NOT NULL,
    category TEXT NOT NULL,
    city TEXT NOT NULL,
    address TEXT NOT NULL,

    rating NUMERIC(2,1),
    reviews_count INTEGER NOT NULL DEFAULT 0,

    site TEXT,
    phone TEXT
);

CREATE INDEX idx_companies_name
ON companies (name);

CREATE INDEX idx_companies_city
ON companies (city);

CREATE INDEX idx_companies_category
ON companies (category);