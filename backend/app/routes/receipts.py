from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.models import Receipt
from app.utils.jwt_utils import token_required
from app.services.receipt_service import process_receipt_image_pil

bp = Blueprint("receipts", __name__, url_prefix="/receipts")


@bp.route("", methods=["GET"])
@token_required
def list_receipts(current_user):
    receipts = (
        Receipt.query.filter_by(creator_id=current_user.user_id)
        .order_by(Receipt.date_modified.desc())
        .all()
    )
    return jsonify([
        {
            "receipt_id": r.receipt_id,
            "store_name": r.store_name,
            "total_amount": str(r.total_amount or 0),
            "status": r.status,
            "date_modified": r.date_modified.isoformat() if r.date_modified else None,
        }
        for r in receipts
    ]), 200


@bp.route("", methods=["POST"])
@token_required
def create_receipt(current_user):
    data = request.get_json() or {}
    store_name = data.get("store_name")
    image_base64 = data.get("image_base64")
    total_amount = data.get("total_amount")

    receipt = Receipt(
        creator_id=current_user.user_id,
        store_name=store_name,
        image_base64=image_base64,
        total_amount=total_amount,
    )
    db.session.add(receipt)
    db.session.commit()

    receipt, parsed_data = process_receipt_image_pil(receipt.receipt_id, image_base64)

    return jsonify({"message": "Receipt created", "receipt_id": receipt.receipt_id}), 201


@bp.route("/<int:receipt_id>", methods=["GET"])
@token_required
def get_receipt(current_user, receipt_id):
    receipt = Receipt.query.filter_by(
        receipt_id=receipt_id, creator_id=current_user.user_id
    ).first_or_404()
    return jsonify({
        "receipt_id": receipt.receipt_id,
        "store_name": receipt.store_name,
        "total_amount": str(receipt.total_amount or 0),
        "status": receipt.status,
        "ocr_text": receipt.ocr_text,
        "image_base64": receipt.image_base64,
    }), 200


@bp.route("/<int:receipt_id>", methods=["PUT"])
@token_required
def update_receipt(current_user, receipt_id):
    receipt = Receipt.query.filter_by(
        receipt_id=receipt_id, creator_id=current_user.user_id
    ).first_or_404()
    data = request.get_json() or {}
    receipt.store_name = data.get("store_name", receipt.store_name)
    receipt.total_amount = data.get("total_amount", receipt.total_amount)
    receipt.status = data.get("status", receipt.status)
    db.session.commit()
    return jsonify({"message": "Receipt updated"}), 200


@bp.route("/<int:receipt_id>", methods=["DELETE"])
@token_required
def delete_receipt(current_user, receipt_id):
    receipt = Receipt.query.filter_by(
        receipt_id=receipt_id, creator_id=current_user.user_id
    ).first_or_404()
    db.session.delete(receipt)
    db.session.commit()
    return jsonify({"message": "Receipt deleted"}), 200


@bp.route("/<int:receipt_id>/toggle_status", methods=["POST"])
@token_required
def toggle_status(current_user, receipt_id):
    receipt = Receipt.query.filter_by(
        receipt_id=receipt_id, creator_id=current_user.user_id
    ).first_or_404()
    if receipt.status == "active":
        receipt.status = "archived"
    else:
        receipt.status = "active"
    db.session.commit()
    return jsonify({"message": f"Receipt marked as {receipt.status}"}), 200


