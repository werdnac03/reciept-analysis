import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import {
  getReceipts,
  toggleReceiptStatus,
  deleteReceipt,
} from "../lib/api/receipts";

interface Receipt {
  receipt_id: number;
  store_name: string;
  status: string;
  date_modified?: string;
}

export default function ViewReceipts() {
  const { logout } = useAuth();
  const [receipts, setReceipts] = useState<Receipt[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [activeTab, setActiveTab] = useState<"active" | "archived">("active");
  const navigate = useNavigate();

  useEffect(() => {
    loadReceipts();
  }, []);

  async function loadReceipts() {
    try {
      const data = await getReceipts();
      setReceipts(data);
    } catch (err) {
      console.error("Failed to fetch receipts:", err);
    }
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0];
    if (selected) setFile(selected);
  }

  function handleAdd() {
    if (!file) return alert("Please select a file first.");
    const reader = new FileReader();
    reader.onload = () => {
      navigate("/create-receipt", { state: { imageBase64: reader.result } });
    };
    reader.readAsDataURL(file);
  }

  async function handleToggle(id: number) {
    await toggleReceiptStatus(id);
    loadReceipts();
  }

  async function handleDelete(id: number) {
    await deleteReceipt(id);
    loadReceipts();
  }

  // Filter receipts by activeTab
  const filtered = receipts.filter((r) => r.status === activeTab);

  return (
    <div className="container mt-4">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Your Receipts</h2>
        <button onClick={logout} className="btn btn-outline-danger btn-sm">
          Logout
        </button>
      </div>

      {/* File upload */}
      <div className="d-flex mb-4">
        <input
          type="file"
          accept="image/*"
          className="form-control me-2"
          onChange={handleFileChange}
        />
        <button onClick={handleAdd} className="btn btn-primary">
          Add
        </button>
      </div>

      {/* Tabs for Active / Archived */}
      <ul className="nav nav-tabs mb-3">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === "active" ? "active" : ""}`}
            onClick={() => setActiveTab("active")}
          >
            Active
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === "archived" ? "active" : ""}`}
            onClick={() => setActiveTab("archived")}
          >
            Archived
          </button>
        </li>
      </ul>

      {/* Table */}
      <table className="table table-hover">
        <thead>
          <tr>
            <th>Store</th>
            <th>Status</th>
            <th>Last Modified</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {filtered.length === 0 ? (
            <tr>
              <td colSpan={4} className="text-center text-muted">
                No {activeTab} receipts.
              </td>
            </tr>
          ) : (
            filtered.map((r) => (
              <tr key={r.receipt_id}>
                <td>
                  <a
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      navigate(`/receipt/${r.receipt_id}`);
                    }}
                    className="text-decoration-none fw-semibold"
                  >
                    {r.store_name}
                  </a>
                </td>

                <td>
                  <span
                    className={`badge ${
                      r.status === "archived"
                        ? "bg-secondary"
                        : "bg-success"
                    }`}
                  >
                    {r.status}
                  </span>
                </td>
                <td>
                  {r.date_modified
                    ? new Date(r.date_modified).toLocaleString()
                    : "—"}
                </td>
                <td>
                  <button
                    className="btn btn-sm btn-outline-secondary"
                    onClick={() => handleToggle(r.receipt_id)}
                  >
                    {r.status === "active" ? "Archive" : "Unarchive"}
                  </button>
                </td>
                <td>
                  <button
                    className="btn btn-sm btn-outline-primary"
                    onClick={() => handleDelete(r.receipt_id)}
                  >
                    {"Delete"}
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
