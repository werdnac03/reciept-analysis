from flask import Blueprint, request, jsonify
from ..models.internal_testing import Dummy

bp = Blueprint("testing_internal", __name__)


@bp.post("/")
def test_postgres_connection():
    dummy = Dummy.query.first()
    if dummy:
        return jsonify({
            "ok": True,
            "message": "internal testing route works!",
            "name": dummy.name
        }), 200
    else:
        return jsonify({
            "ok": False,
            "message": "no Dummy rows found"
        }), 404