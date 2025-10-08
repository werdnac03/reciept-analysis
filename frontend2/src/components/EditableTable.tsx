import React, { useState, useEffect } from "react";

interface Item {
  item_id: number;
  item_name: string;
  price: number;
  quantity: number;
}

interface Props {
  items: Item[];
  mode: "view" | "edit" | "select";
  onSave: (updated: Item[]) => void;
  onDeleteItems?: (ids: number[]) => Promise<void>;
  onSelectChange?: (itemId: number, qty: number, checked: boolean) => void;
  selectedItems?: Record<number, number>;
}

export default function EditableTable({
  items,
  mode,
  onSave,
  onDeleteItems,
  onSelectChange,
  selectedItems = {},
}: Props) {
  const [localItems, setLocalItems] = useState<Item[]>([]);
  const [deleteMode, setDeleteMode] = useState(false);
  const [itemsToDelete, setItemsToDelete] = useState<Set<number>>(new Set());

  useEffect(() => {
    setLocalItems(items);
  }, [items]);

  // Filter for view mode → only show selected items
  const displayedItems =
    mode === "view"
      ? localItems.filter((item) => selectedItems[item.item_id] !== undefined)
      : localItems;

  const handleChange = (
    idx: number,
    field: keyof Item,
    value: string | number
  ) => {
    const updated = [...localItems];
    updated[idx] = { ...updated[idx], [field]: value };
    setLocalItems(updated);
  };

  const handleAddItem = () => {
    const newItem: Item = {
      item_id: 0,
      item_name: "",
      price: 0,
      quantity: 1,
    };
    setLocalItems([...localItems, newItem]);
  };

  const handleToggleDeleteMode = () => {
    setDeleteMode(!deleteMode);
    setItemsToDelete(new Set());
  };

  const handleDeleteCheckbox = (itemId: number, checked: boolean) => {
    const updated = new Set(itemsToDelete);
    if (checked) updated.add(itemId);
    else updated.delete(itemId);
    setItemsToDelete(updated);
  };

  const handleSaveChanges = async () => {
    // Call delete API if delete mode active
    if (deleteMode && itemsToDelete.size > 0 && onDeleteItems) {
      await onDeleteItems(Array.from(itemsToDelete));
    }

    // Filter out deleted items locally
    const remainingItems = localItems.filter(
      (item) => !itemsToDelete.has(item.item_id)
    );

    onSave(remainingItems);
    setDeleteMode(false);
    setItemsToDelete(new Set());
  };

  return (
    <div className="table-responsive">
      <table className="table table-bordered table-hover table-sm align-middle">
        <thead className="table-light">
          <tr>
            {mode === "select" && <th style={{ width: "5%" }}>✔</th>}
            {deleteMode && mode === "edit" && <th style={{ width: "5%" }}>🗑</th>}
            <th>Name</th>
            <th style={{ width: "20%" }}>Price</th>
            <th style={{ width: "20%" }}>Qty</th>
            {mode === "view" && <th style={{ width: "20%" }}>TotalQty</th>}
          </tr>
        </thead>
        <tbody>
          {displayedItems.map((item, i) => {
            const selected = selectedItems[item.item_id] !== undefined;
            const markedForDeletion = itemsToDelete.has(item.item_id);

            return (
              <tr
                key={i}
                className={markedForDeletion ? "table-danger" : ""}
              >
                {mode === "select" && (
                  <td className="text-center">
                    <input
                      type="checkbox"
                      checked={selected}
                      onChange={(e) =>
                        onSelectChange?.(
                          item.item_id,
                          selectedItems[item.item_id] || 1,
                          e.target.checked
                        )
                      }
                    />
                  </td>
                )}

                {deleteMode && mode === "edit" && (
                  <td className="text-center">
                    <input
                      type="checkbox"
                      checked={markedForDeletion}
                      onChange={(e) =>
                        handleDeleteCheckbox(item.item_id, e.target.checked)
                      }
                    />
                  </td>
                )}

                <td>
                  {mode === "edit" && !deleteMode ? (
                    <input
                      type="text"
                      className="form-control form-control-sm"
                      placeholder="Item name"
                      value={item.item_name}
                      onChange={(e) =>
                        handleChange(i, "item_name", e.target.value)
                      }
                    />
                  ) : (
                    item.item_name
                  )}
                </td>

                <td>
                  {mode === "edit" && !deleteMode ? (
                    <input
                      type="number"
                      className="form-control form-control-sm"
                      value={item.price}
                      step="0.01"
                      min="0"
                      onChange={(e) =>
                        handleChange(i, "price", parseFloat(e.target.value))
                      }
                    />
                  ) : (
                    `$${Number(item.price).toFixed(2)}`
                  )}
                </td>

                <td>
                  {mode === "edit" && !deleteMode ? (
                    <input
                      type="number"
                      className="form-control form-control-sm"
                      value={item.quantity}
                      min="1"
                      onChange={(e) =>
                        handleChange(i, "quantity", parseInt(e.target.value))
                      }
                    />
                  ) : mode === "select" && selected ? (
                    <input
                      type="number"
                      min="1"
                      step="0.01"
                      className="form-control form-control-sm"
                      value={selectedItems[item.item_id] ?? 1}
                      onChange={(e) => {
                        const rawValue = parseFloat(e.target.value) || 0;
                        const clamped = Math.min(Math.max(rawValue, 0), item.quantity);
                        onSelectChange?.(item.item_id, clamped, true);
                      }}
                    />
                  ) : mode === "view" ? (
                    selectedItems[item.item_id] ?? 0
                  ) : (
                    item.quantity
                  )}
                </td>

                <td>
                  {mode === "view" && (
                    item.quantity
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {mode === "edit" && (
        <div className="d-flex justify-content-between mt-2">
          <div>
            {!deleteMode && (
              <button
                className="btn btn-outline-primary btn-sm me-2"
                onClick={handleAddItem}
              >
                + Add Item
              </button>
            )}
            <button
              className={`btn btn-outline-danger btn-sm ${
                deleteMode ? "active" : ""
              }`}
              onClick={handleToggleDeleteMode}
            >
              {deleteMode ? "Cancel Delete" : "🗑 Delete Items"}
            </button>
          </div>

          <button
            className="btn btn-success btn-sm"
            onClick={handleSaveChanges}
          >
            Save Changes
          </button>
        </div>
      )}
    </div>
  );
}
