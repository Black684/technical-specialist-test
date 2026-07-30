import { getPool } from "@/lib/db";

type Company = {
  id: string;
  name: string;
  category: string;
  city: string;
  address: string;
  rating: string | null;
  reviews_count: number;
  site: string | null;
  phone: string | null;
};

type PageProps = {
  searchParams: Promise<{
    name?: string;
    city?: string;
  }>;
};

async function getCities(): Promise<string[]> {
  const pool = getPool();
  const result = await pool.query<{ city: string }>(
    "SELECT DISTINCT city FROM companies ORDER BY city"
  );
  return result.rows.map((row) => row.city);
}

async function getCompanies(name?: string, city?: string): Promise<Company[]> {
  const pool = getPool();
  const conditions: string[] = [];
  const values: string[] = [];

  if (name?.trim()) {
    values.push(`%${name.trim()}%`);
    conditions.push(`name ILIKE $${values.length}`);
  }

  if (city?.trim()) {
    values.push(city.trim());
    conditions.push(`city = $${values.length}`);
  }

  const where = conditions.length ? `WHERE ${conditions.join(" AND ")}` : "";

  const result = await pool.query<Company>(
    `SELECT id, name, category, city, address, rating, reviews_count, site, phone
     FROM companies
     ${where}
     ORDER BY name`,
    values
  );

  return result.rows;
}

export default async function CompaniesPage({ searchParams }: PageProps) {
  const { name = "", city = "" } = await searchParams;

  const [companies, cities] = await Promise.all([
    getCompanies(name, city),
    getCities(),
  ]);

  return (
    <main style={{ padding: "24px", maxWidth: "1200px", margin: "0 auto" }}>
      <h1>Компании</h1>

      <form method="GET" style={{ margin: "16px 0", display: "flex", gap: "12px", flexWrap: "wrap" }}>
        <label>
          Название:{" "}
          <input type="text" name="name" defaultValue={name} placeholder="Поиск..." />
        </label>

        <label>
          Город:{" "}
          <select name="city" defaultValue={city}>
            <option value="">Все города</option>
            {cities.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>

        <button type="submit">Применить</button>
        {(name || city) && (
          <a href="/companies" style={{ alignSelf: "center" }}>
            Сбросить
          </a>
        )}
      </form>

      <p>Найдено: {companies.length}</p>

      <table border={1} cellPadding={8} cellSpacing={0} style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Название</th>
            <th>Категория</th>
            <th>Город</th>
            <th>Адрес</th>
            <th>Рейтинг</th>
            <th>Отзывы</th>
            <th>Сайт</th>
            <th>Телефон</th>
          </tr>
        </thead>
        <tbody>
          {companies.length === 0 ? (
            <tr>
              <td colSpan={8}>Ничего не найдено</td>
            </tr>
          ) : (
            companies.map((company) => (
              <tr key={company.id}>
                <td>{company.name}</td>
                <td>{company.category}</td>
                <td>{company.city}</td>
                <td>{company.address}</td>
                <td>{company.rating ?? "—"}</td>
                <td>{company.reviews_count}</td>
                <td>
                  {company.site ? (
                    <a href={company.site} target="_blank" rel="noreferrer">
                      {company.site}
                    </a>
                  ) : (
                    "—"
                  )}
                </td>
                <td>{company.phone ?? "—"}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </main>
  );
}