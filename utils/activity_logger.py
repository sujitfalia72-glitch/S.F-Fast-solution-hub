# utils/activity_logger.py

import logging
from flask import request, session

logger = logging.getLogger(__name__)


def log_activity(action, details=None):
    """
    Log user activity safely.

    Example:
        log_activity("Delete User")
        log_activity("Approve Booking", {"booking_id": 12})
    """

    try:
        user_id = session.get("user_id")
        role = session.get("role")

        logger.info(
            {
                "user_id": user_id,
                "role": role,
                "action": action,
                "details": details,
                "ip": request.remote_addr,
                "method": request.method,
                "path": request.path,
            }
        )

    except Exception as e:
        logger.error(f"Activity Logger Error: {e}")
