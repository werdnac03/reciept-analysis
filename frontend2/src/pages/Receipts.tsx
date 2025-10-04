import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import type { Receipt } from "../models/receipt";
import { listReceipts } from "../lib/api";

export default function Receipts() {
  const [data, setData] = useState<Receipt[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const rows = await listReceipts();
        setData(rows);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, []);

  if (error) return <p className="text-red-600">{error}</p>;
  if (!data) return <p>Loading receipts…</p>;

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">All Receipts</h1>
      <ul className="divide-y border rounded">
        {data.map((r) => (
          <li key={r.id} className="p-3 flex items-center justify-between">
            <div>
              <p className="font-medium">{r.storeName}</p>
              <p className="text-sm opacity-80">
                ${r.totalAmount.toFixed(2)} • {new Date(r.createdAt).toLocaleString()}
              </p>
            </div>
            <Link to={`/receipts/${r.id}`} className="underline">
              View
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
