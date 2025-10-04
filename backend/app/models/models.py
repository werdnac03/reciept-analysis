from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from ..extensions import db


class User(db.Model):
    __tablename__ = "Users"

    user_id = db.Column("UserID", db.Integer, primary_key=True)
    email = db.Column("Email", db.String(255), unique=True, nullable=False)
    username = db.Column("Username", db.String(100))
    password_hash = db.Column("PasswordHash", db.Text, nullable=False)

    receipts_created = db.relationship("Receipt", back_populates="creator")
    shared_receipts = db.relationship("Receipt", secondary="ShareReceipts", back_populates="shared_with_users")
    item_ownerships = db.relationship("ItemOwnership", back_populates="user")
    transactions_sent = db.relationship("Transaction", foreign_keys="Transaction.from_user_id", back_populates="from_user")
    transactions_received = db.relationship("Transaction", foreign_keys="Transaction.to_user_id", back_populates="to_user")
    notifications_sent = db.relationship("Notification", foreign_keys="Notification.from_user_id", back_populates="from_user")
    notifications_received = db.relationship("Notification", foreign_keys="Notification.to_user_id", back_populates="to_user")


class Receipt(db.Model):
    __tablename__ = "Receipts"

    receipt_id = db.Column("ReceiptID", db.Integer, primary_key=True)
    creator_id = db.Column("CreatorID", db.Integer, db.ForeignKey("Users.UserID", ondelete="SET NULL"), index=True)
    store_name = db.Column("StoreName", db.String(255))
    total_amount = db.Column("TotalAmount", db.Numeric(12, 2))
    image_base64 = db.Column("ImageBase64", db.Text)
    ocr_text = db.Column("OCRText", db.Text)

    creator = db.relationship("User", back_populates="receipts_created")
    items = db.relationship("Item", back_populates="receipt")
    shared_with_users = db.relationship("User", secondary="ShareReceipts", back_populates="shared_receipts")
    item_ownerships = db.relationship("ItemOwnership", back_populates="receipt")
    transactions = db.relationship("Transaction", back_populates="receipt")


class ShareReceipt(db.Model):
    __tablename__ = "ShareReceipts"
    __table_args__ = (UniqueConstraint("UserID", "ReceiptID", name="uq_share_user_receipt"),)

    share_id = db.Column("ShareID", db.Integer, primary_key=True)
    user_id = db.Column("UserID", db.Integer, db.ForeignKey("Users.UserID", ondelete="CASCADE"), index=True)
    receipt_id = db.Column("ReceiptID", db.Integer, db.ForeignKey("Receipts.ReceiptID", ondelete="CASCADE"), index=True)

    user = db.relationship("User", backref="share_links")
    receipt = db.relationship("Receipt", backref="share_links")


class Item(db.Model):
    __tablename__ = "Item"

    item_id = db.Column("ItemID", db.Integer, primary_key=True)
    receipt_id = db.Column("ReceiptID", db.Integer, db.ForeignKey("Receipts.ReceiptID", ondelete="CASCADE"), index=True, nullable=False)
    item_name = db.Column("ItemName", db.String(255))
    price = db.Column("Price", db.Numeric(12, 2))
    quantity = db.Column("Quantity", db.Integer, default=1, nullable=False)

    receipt = db.relationship("Receipt", back_populates="items")
    owners = db.relationship("ItemOwnership", back_populates="item")


class ItemOwnership(db.Model):
    __tablename__ = "ItemOwnership"

    ownership_id = db.Column("OwnershipID", db.Integer, primary_key=True)
    receipt_id = db.Column("ReceiptID", db.Integer, db.ForeignKey("Receipts.ReceiptID", ondelete="CASCADE"), index=True, nullable=False)
    user_id = db.Column("UserID", db.Integer, db.ForeignKey("Users.UserID", ondelete="CASCADE"), index=True, nullable=False)
    item_id = db.Column("ItemID", db.Integer, db.ForeignKey("Item.ItemID", ondelete="CASCADE"), index=True, nullable=False)
    quantity = db.Column("Quantity", db.Integer, default=1, nullable=False)

    receipt = db.relationship("Receipt", back_populates="item_ownerships")
    user = db.relationship("User", back_populates="item_ownerships")
    item = db.relationship("Item", back_populates="owners")


class Transaction(db.Model):
    __tablename__ = "Transactions"

    transaction_id = db.Column("TransactionID", db.Integer, primary_key=True)
    from_user_id = db.Column("FromUserID", db.Integer, db.ForeignKey("Users.UserID", ondelete="SET NULL"), index=True)
    to_user_id = db.Column("ToUserID", db.Integer, db.ForeignKey("Users.UserID", ondelete="SET NULL"), index=True)
    receipt_id = db.Column("ReceiptID", db.Integer, db.ForeignKey("Receipts.ReceiptID", ondelete="SET NULL"), index=True)
    amount = db.Column("Amount", db.Numeric(12, 2))
    status = db.Column("Status", db.String(255), default="pending", nullable=False)
    created_at = db.Column("CreatedAt", db.DateTime, server_default=db.func.current_timestamp())

    from_user = db.relationship("User", foreign_keys=[from_user_id], back_populates="transactions_sent")
    to_user = db.relationship("User", foreign_keys=[to_user_id], back_populates="transactions_received")
    receipt = db.relationship("Receipt", back_populates="transactions")


class Notification(db.Model):
    __tablename__ = "Notification"

    notification_id = db.Column("NotificationID", db.Integer, primary_key=True)
    from_user_id = db.Column("FromUserID", db.Integer, db.ForeignKey("Users.UserID", ondelete="SET NULL"), index=True)
    to_user_id = db.Column("ToUserID", db.Integer, db.ForeignKey("Users.UserID", ondelete="SET NULL"), index=True)
    message = db.Column("Message", db.Text)
    status = db.Column("Status", db.String(255))

    from_user = db.relationship("User", foreign_keys=[from_user_id], back_populates="notifications_sent")
    to_user = db.relationship("User", foreign_keys=[to_user_id], back_populates="notifications_received")
