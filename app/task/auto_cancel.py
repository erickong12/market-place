from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.order import Order, OrderStatus


def auto_cancel_pending():
    db: Session = SessionLocal()
    threshold = datetime.now() - timedelta(hours=24)
    pending = (
        db.query(Order)
        .filter(Order.status == OrderStatus.PENDING, Order.created_at < threshold)
        .all()
    )
    for o in pending:
        o.status = OrderStatus.AUTO_CANCELLED
    db.commit()
    db.close()
