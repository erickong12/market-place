from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import atexit

from app.database.session import SessionLocal
from datetime import timedelta

from app.models.order import Order
from app.utils.enums import OrderStatus


def auto_cancel_pending():
    db = SessionLocal()
    try:
        threshold = datetime.now() - timedelta(hours=24)
        pending = (
            db.query(Order)
            .filter(Order.status == OrderStatus.PENDING, Order.created_at < threshold)
            .all()
        )
        for o in pending:
            o.status = OrderStatus.AUTO_CANCELLED
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[Scheduler] Error auto-cancelling: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_cancel_pending, IntervalTrigger(minutes=1))
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
