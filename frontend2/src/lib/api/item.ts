const API_URL = "/api";

const headers = () => ({
  "Content-Type": "application/json",
  Authorization: `Bearer ${localStorage.getItem("token")}`,
});

export async function getReceiptItems(receiptId: number) {
  const res = await fetch(`${API_URL}/items/receipt/${receiptId}`, { headers: headers() });
  return res.json();
}

export async function updateItem(itemId: number, data: any) {
  const res = await fetch(`${API_URL}/items/${itemId}`, {
    method: "PUT",
    headers: headers(),
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function createItem(receiptId: number, data: any) {
  const res = await fetch(`/api/items/receipt/${receiptId}`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function deleteItems(itemIds: number[]) {
  const res = await fetch(`${API_URL}/items/delete_items`, {
    method: "DELETE",
    headers: headers(),
    body: JSON.stringify({ item_ids: itemIds }),
  });
  if (!res.ok) throw new Error(`Failed to delete items: ${res.status}`);
  return res.json();
}