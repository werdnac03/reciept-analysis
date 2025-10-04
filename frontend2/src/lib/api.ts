import type { Receipt } from "../models/receipt";

const baseURL = import.meta.env.VITE_API_URL ?? "http://localhost:5000";

export async function loginApi(
  email: string,
  password: string
): Promise<{ token: string }> {
  //const res = await fetch(`${baseURL}/auth/login`, {
  const res = await fetch(`/api/accounts/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Login failed");
  return res.json();
}

export async function listReceipts(): Promise<Receipt[]> {
  // Mocked data for now
  return [
    {
      id: "r_1",
      storeName: "Target",
      totalAmount: 42.17,
      createdAt: new Date().toISOString(),
    },
    {
      id: "r_2",
      storeName: "Whole Foods",
      totalAmount: 19.5,
      createdAt: new Date().toISOString(),
    },
  ];
}

export async function getReceipt(id: string): Promise<Receipt> {
  return {
    id,
    storeName: "Demo Store",
    totalAmount: 12.34,
    createdAt: new Date().toISOString(),
    ocrText: "Milk 2.99\nBread 3.49\n",
  };
}

export async function updateReceipt(
  id: string,
  patch: Partial<Pick<Receipt, "storeName" | "totalAmount" | "ocrText">>
): Promise<Receipt> {
  const current = await getReceipt(id);
  return { ...current, ...patch };
}
