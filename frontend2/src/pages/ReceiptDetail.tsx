import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import type { Receipt } from "../models/receipt";
import { getReceipt, updateReceipt } from "../lib/api";

export default function ReceiptDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [receipt, setReceipt] = useState<Receipt | null>(null);
  const [storeName, setStoreName] = useState("");
  const [totalAmount, setTotalAmount] = useState(0);
  const [ocrText, setOcrText] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      if (!id) return;
      try {
        const r = await getReceipt(id);
        setReceipt(r);
        setStoreName(r.storeName);
        setTotalAmount(r.totalAmount);
        setOcrText(r.ocrText ?? "");
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [id]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!id) return;
    setSaving(true);
    try {
      const updated = await updateReceipt(id, { storeName, totalAmount, ocrText });
      setReceipt(updated);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSaving(false);
    }
  }

  if (error) return <p className="text-red-600">{error}</p>;
  if (!receipt) return <p>Loading…</p>;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <button className="underline" onClick={() => navigate(-1)}>
          ← Back
        </button>
        <h1 className="text-2xl font-semibold">Receipt #{receipt.id}</h1>
      </div>

      <form onSubmit={onSubmit} className="grid gap-3 max-w-2xl">
        <label>
          <span className="block text-sm">Store name</span>
          <input
            className="border rounded px-3 py-2 w-full"
            value={storeName}
            onChange={(e) => setStoreName(e.target.value)}
          />
        </label>

        <label>
          <span className="block text-sm">Total amount</span>
          <input
            type="number"
            step="0.01"
            className="border rounded px-3 py-2 w-full"
            value={totalAmount}
            onChange={(e) => setTotalAmount(Number(e.target.value))}
          />
        </label>

        <label>
          <span className="block text-sm">OCR text</span>
          <textarea
            rows={8}
            className="border rounded px-3 py-2 w-full font-mono"
            value={ocrText}
            onChange={(e) => setOcrText(e.target.value)}
          />
        </label>

        <button type="submit" className="border rounded px-4 py-2" disabled={saving}>
          {saving ? "Saving…" : "Save changes"}
        </button>
      </form>
    </div>
  );
}
