# utils/activity_logger.py

import logging
from flask import request

logger = logging.getLogger(__name__)


def log_activity(
    actor_id=None,
    target_id=None,
    action="",
    role=None,
    meta=None
):
    """
    Production Activity Logger
    """

    try:
        logger.info(
            {
                "actor_id": actor_id,
                "target_id": target_id,
                "role": role,
                "action": action,
                "meta": meta or {},
                "ip": request.remote_addr,
                "method": request.method,
                "path": request.path,
                "user_agent": request.headers.get("User-Agent"),
            }
        )

    except Exception as e:
        logger.exception(f"Activity Logger Error: {e}")
