import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { createReceipt } from "../lib/api/receipts";

export default function CreateReceipt() {
  const location = useLocation();
  const navigate = useNavigate();
  const { imageBase64 } = (location.state || {}) as { imageBase64?: string };

  const [storeName, setStoreName] = useState("");
  const [total, setTotal] = useState("");

  async function handleSave() {
    if (!storeName) return alert("Store name required.");
    await createReceipt({
      store_name: storeName,
      total_amount: total,
      image_base64: imageBase64,
    });
    navigate("/view-receipts");
  }

  return (
    <div className="container mt-4">
      <h2>Create Receipt</h2>
      <div className="row mt-3">
        <div className="col-md-6">
          {imageBase64 ? (
            <img
              src={imageBase64}
              alt="Uploaded receipt"
              className="img-fluid rounded shadow-sm"
            />
          ) : (
            <p>No image uploaded.</p>
          )}
        </div>
        <div className="col-md-6">
          <div className="mb-3">
            <label className="form-label">Store Name</label>
            <input
              type="text"
              className="form-control"
              value={storeName}
              onChange={(e) => setStoreName(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Total Amount</label>
            <input
              type="number"
              step="0.01"
              className="form-control"
              value={total}
              onChange={(e) => setTotal(e.target.value)}
            />
          </div>
          <button className="btn btn-primary" onClick={handleSave}>
            Save
          </button>
          <button
            className="btn btn-outline-secondary ms-2"
            onClick={() => navigate("/view-receipts")}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
