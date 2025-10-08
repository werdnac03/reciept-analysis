const API_URL = "/api";

const headers = () => ({
  "Content-Type": "application/json",
  Authorization: `Bearer ${localStorage.getItem("token")}`,
});

export async function getReceipts() {
  const res = await fetch(`${API_URL}/receipts`, { headers: headers() });
  return res.json();
}

export async function createReceipt(data: {
  store_name: string;
  total_amount?: string;
  image_base64?: string;
}) {
  const res = await fetch(`${API_URL}/receipts`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create receipt");
  return res.json();
}

export async function toggleReceiptStatus(id: number) {
  const res = await fetch(`${API_URL}/receipts/${id}/toggle_status`, {
    method: "POST",
    headers: headers(),
  });
  return res.json();
}

export async function getReceiptById(id: number) {
  const res = await fetch(`${API_URL}/receipts/${id}`, {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
  });
  if (!res.ok) throw new Error("Failed to fetch receipt");
  return res.json();
}

export async function deleteReceipt(id: number) {
  const res = await fetch(`${API_URL}/receipts/${id}`, {
    method: "DELETE",
    headers: headers(),
  });
  if (!res.ok) throw new Error("Failed to delete receipt");
  return res.json();
}