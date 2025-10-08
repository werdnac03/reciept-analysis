from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.models import Item, Receipt, ItemOwnership
from app.utils.jwt_utils import token_required

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.route("/receipt/<int:receipt_id>", methods=["GET"])
@token_required
def list_items_for_receipt(current_user, receipt_id):
    """
    Get all items belonging to a specific receipt for the current user.
    """
    receipt = Receipt.query.filter_by(
        receipt_id=receipt_id, creator_id=current_user.user_id
    ).first_or_404()

    items = Item.query.filter_by(receipt_id=receipt.receipt_id).all()

    return jsonify([
        {
            "item_id": i.item_id,
            "item_name": i.item_name,
            "price": float(i.price or 0),
            "quantity": i.quantity,
        }
        for i in items
    ]), 200


@bp.route("/receipt/<int:receipt_id>", methods=["POST"])
@token_required
def create_item(current_user, receipt_id):
    """
    Create a new item under a given receipt.
    """
    receipt = Receipt.query.filter_by(
        receipt_id=receipt_id, creator_id=current_user.user_id
    ).first_or_404()

    data = request.get_json() or {}
    item_name = data.get("item_name")
    price = data.get("price", 0)
    quantity = data.get("quantity", 1)

    item = Item(
        receipt_id=receipt.receipt_id,
        item_name=item_name,
        price=price,
        quantity=quantity,
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({
        "message": "Item created",
        "item_id": item.item_id,
        "item_name": item.item_name,
        "price": float(item.price or 0),
        "quantity": item.quantity,
    }), 201


@bp.route("/<int:item_id>", methods=["PUT"])
@token_required
def update_item(current_user, item_id):
    """
    Update an existing item's name, price, or quantity.
    """
    item = (
        db.session.query(Item)
        .join(Receipt)
        .filter(Item.item_id == item_id, Receipt.creator_id == current_user.user_id)
        .first_or_404()
    )

    data = request.get_json() or {}

    if "item_name" in data:
        item.item_name = data["item_name"]
    if "price" in data:
        item.price = data["price"]
    if "quantity" in data:
        item.quantity = data["quantity"]

    db.session.commit()

    return jsonify({
        "item_id": item.item_id,
        "item_name": item.item_name,
        "price": float(item.price or 0),
        "quantity": item.quantity,
    }), 200


@bp.route("/<int:item_id>", methods=["DELETE"])
@token_required
def delete_item(current_user, item_id):
    """
    Delete an item under the current user's receipt.
    """
    item = (
        db.session.query(Item)
        .join(Receipt)
        .filter(Item.item_id == item_id, Receipt.creator_id == current_user.user_id)
        .first_or_404()
    )

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item deleted"}), 200


@bp.route("/ownership", methods=["POST"])
@token_required
def create_or_update_ownership(current_user):
    """
    Create or update ownership of an item for the current user.
    (Used in Select Mode on the frontend)
    """
    data = request.get_json() or {}
    item_id = data.get("item_id")
    receipt_id = data.get("receipt_id")
    quantity = data.get("quantity", 1)

    if not item_id or not receipt_id:
        return jsonify({"error": "Missing item_id or receipt_id"}), 400

    ownership = ItemOwnership.query.filter_by(
        item_id=item_id,
        user_id=current_user.user_id,
        receipt_id=receipt_id
    ).first()

    if ownership:
        ownership.quantity = quantity
    else:
        ownership = ItemOwnership(
            item_id=item_id,
            user_id=current_user.user_id,
            receipt_id=receipt_id,
            quantity=quantity
        )
        db.session.add(ownership)

    db.session.commit()

    return jsonify({
        "ownership_id": ownership.ownership_id,
        "item_id": ownership.item_id,
        "quantity": ownership.quantity,
    }), 200

@bp.route("/delete_items", methods=["DELETE"])
@token_required
def delete_items(current_user):
    """
    Delete all items given a list of item IDs.
    """
    item_ids = request.json.get("item_ids", [])
    for item_id in item_ids:
        item = (
            db.session.query(Item)
            .join(Receipt)
            .filter(Item.item_id == item_id, Receipt.creator_id == current_user.user_id)
            .first_or_404()
        )

        db.session.delete(item)
        db.session.commit()

    return jsonify({"message": "Items deleted"}), 200