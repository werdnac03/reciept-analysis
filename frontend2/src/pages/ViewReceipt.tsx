import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getReceiptById } from "../lib/api/receipts";
import { getReceiptItems, updateItem, createItem, deleteItems} from "../lib/api/item";
import EditableTable from "../components/EditableTable";

interface Receipt {
  receipt_id: number;
  store_name: string;
  total_amount: string;
  status: string;
  image_base64?: string;
  ocr_text?: string;
  date_modified?: string;
}

interface Item {
  item_id: number;
  item_name: string;
  price: number;
  quantity: number;
}

export default function ViewReceipt() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [receipt, setReceipt] = useState<Receipt | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const [mode, setMode] = useState<"view" | "edit" | "select">("view");
  const [selectedItems, setSelectedItems] = useState<Record<number, number>>({});

  useEffect(() => {
    if (id) {
      loadReceipt(parseInt(id));
      loadItems(parseInt(id));
    }
  }, [id]);

  async function loadReceipt(receiptId: number) {
    try {
      const data = await getReceiptById(receiptId);
      setReceipt(data);
    } catch (err) {
      console.error("Failed to load receipt:", err);
    }
  }

  async function loadItems(receiptId: number) {
    try {
      const data = await getReceiptItems(receiptId);
      setItems(data);
    } catch (err) {
      console.error("Failed to load items:", err);
    }
  }

  async function handleSave(updatedItems: Item[]) {
    for (const item of updatedItems) {
      if (item.item_id === 0) {
        // new item → POST
        await createItem(receipt!.receipt_id, item);
      } else {
        // existing item → PUT
        await updateItem(item.item_id, item);
      }
    }
  
    // refresh items after saving
    await loadItems(receipt!.receipt_id);
    setMode("view");
  }

  async function handleDeleteItems(ids: number[]) {
    await deleteItems(ids);
    // Refresh items after deletion
    await loadItems(receipt!.receipt_id);
    setMode("view");
  }

  function handleSelectChange(itemId: number, qty: number, checked: boolean) {
    setSelectedItems((prev) => {
      const updated = { ...prev };
      if (checked) updated[itemId] = qty;
      else delete updated[itemId];
      return updated;
    });
  }

  if (!receipt) return <div className="container mt-4">Loading...</div>;

  return (
    <div className="container mt-4">
      <button
        className="btn btn-outline-secondary mb-3"
        onClick={() => navigate("/view-receipts")}
      >
        ← Back
      </button>

      <h2>{receipt.store_name}</h2>
      <p className="text-muted">
        {receipt.status === "archived" ? "Archived" : "Active"} • Last updated{" "}
        {receipt.date_modified
          ? new Date(receipt.date_modified).toLocaleString()
          : "N/A"}
      </p>

      <div className="row mt-3">
        {/* Left side: receipt image */}
        <div className="col-md-6">
          {receipt.image_base64 ? (
            <img
              src={receipt.image_base64}
              alt="Receipt"
              className="img-fluid rounded shadow-sm"
            />
          ) : (
            <div className="text-muted">No image uploaded</div>
          )}
        </div>

        {/* Right side: table + mode switch */}
        <div className="col-md-6">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <h5 className="mb-0">Items</h5>
            <div className="btn-group btn-group-sm">
              <button
                className={`btn ${
                  mode === "view" ? "btn-primary" : "btn-outline-primary"
                }`}
                onClick={() => setMode("view")}
              >
                View
              </button>
              <button
                className={`btn ${
                  mode === "edit" ? "btn-primary" : "btn-outline-primary"
                }`}
                onClick={() => setMode("edit")}
              >
                Edit
              </button>
              <button
                className={`btn ${
                  mode === "select" ? "btn-primary" : "btn-outline-primary"
                }`}
                onClick={() => setMode("select")}
              >
                Select
              </button>
            </div>
          </div>

          <EditableTable
            items={items}
            mode={mode}
            onSave={handleSave}
            onDeleteItems={handleDeleteItems}
            onSelectChange={handleSelectChange}
            selectedItems={selectedItems}
          />
        </div>
      </div>
    </div>
  );
}
