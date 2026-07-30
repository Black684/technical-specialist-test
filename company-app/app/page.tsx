import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  return (
    <main style={{ padding: "24px" }}>
      <h1>Company App</h1>
      <p>
        <a href="/companies">Перейти к списку компаний</a>
      </p>
    </main>
  );
}
