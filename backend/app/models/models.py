from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

share_receipts = db.Table(
    "share_receipts",
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE")),
    db.Column("receipt_id", db.Integer, db.ForeignKey("receipts.receipt_id", ondelete="CASCADE")),
    UniqueConstraint("user_id", "receipt_id", name="uq_share_user_receipt"),
)

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.Text, nullable=False)

    receipts_created = db.relationship("Receipt", back_populates="creator")
    shared_receipts = db.relationship("Receipt", secondary=share_receipts, back_populates="shared_with_users")
    item_ownerships = db.relationship("ItemOwnership", back_populates="user")
    transactions_sent = db.relationship("Transaction", foreign_keys="Transaction.from_user_id", back_populates="from_user")
    transactions_received = db.relationship("Transaction", foreign_keys="Transaction.to_user_id", back_populates="to_user")
    notifications_sent = db.relationship("Notification", foreign_keys="Notification.from_user_id", back_populates="from_user")
    notifications_received = db.relationship("Notification", foreign_keys="Notification.to_user_id", back_populates="to_user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Receipt(db.Model):
    __tablename__ = "receipts"

    receipt_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="SET NULL"), index=True)
    store_name = db.Column(db.String(255))
    total_amount = db.Column(db.Numeric(12, 2))
    image_base64 = db.Column(db.Text)
    ocr_text = db.Column(db.Text)

    creator = db.relationship("User", back_populates="receipts_created")
    items = db.relationship("Item", back_populates="receipt")
    shared_with_users = db.relationship("User", secondary=share_receipts, back_populates="shared_receipts")
    item_ownerships = db.relationship("ItemOwnership", back_populates="receipt")
    transactions = db.relationship("Transaction", back_populates="receipt")


class Item(db.Model):
    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey("receipts.receipt_id", ondelete="CASCADE"), index=True, nullable=False)
    item_name = db.Column(db.String(255))
    price = db.Column(db.Numeric(12, 2))
    quantity = db.Column(db.Integer, default=1, nullable=False)

    receipt = db.relationship("Receipt", back_populates="items")
    owners = db.relationship("ItemOwnership", back_populates="item")


class ItemOwnership(db.Model):
    __tablename__ = "item_ownerships"

    ownership_id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey("receipts.receipt_id", ondelete="CASCADE"), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), index=True, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id", ondelete="CASCADE"), index=True, nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    receipt = db.relationship("Receipt", back_populates="item_ownerships")
    user = db.relationship("User", back_populates="item_ownerships")
    item = db.relationship("Item", back_populates="owners")


class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="SET NULL"), index=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="SET NULL"), index=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey("receipts.receipt_id", ondelete="SET NULL"), index=True)
    amount = db.Column(db.Numeric(12, 2))
    status = db.Column(db.String(255), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    from_user = db.relationship("User", foreign_keys=[from_user_id], back_populates="transactions_sent")
    to_user = db.relationship("User", foreign_keys=[to_user_id], back_populates="transactions_received")
    receipt = db.relationship("Receipt", back_populates="transactions")


class Notification(db.Model):
    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="SET NULL"), index=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="SET NULL"), index=True)
    message = db.Column(db.Text)
    status = db.Column(db.String(255))

    from_user = db.relationship("User", foreign_keys=[from_user_id], back_populates="notifications_sent")
    to_user = db.relationship("User", foreign_keys=[to_user_id], back_populates="notifications_received")
