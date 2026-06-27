from datetime import datetime, UTC

from extensions import db


class ActivityLog(db.Model):

    __tablename__ = "activity_logs"

    id = db.Column(
        db.BigInteger,
        primary_key=True
    )

    # কে Action করলো
    actor_id = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    # কাকে Action করা হলো
    target_id = db.Column(
        db.Integer,
        nullable=True,
        index=True
    )

    # Action Type
    # login, logout, create_doctor,
    # delete_doctor, approve_application
    action = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    # User Role
    role = db.Column(
        db.String(30),
        nullable=True,
        index=True
    )

    # অতিরিক্ত তথ্য
    meta = db.Column(
        db.JSON,
        nullable=True
    )

    # Security Information
    ip_address = db.Column(
        db.String(45),
        nullable=True,
        index=True
    )

    user_agent = db.Column(
        db.String(500),
        nullable=True
    )

    # Timestamp
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True
    )

    # Performance Indexes
    __table_args__ = (

        db.Index(
            "idx_activity_actor_action",
            "actor_id",
            "action"
        ),

        db.Index(
            "idx_activity_target_action",
            "target_id",
            "action"
        ),

        db.Index(
            "idx_activity_role_created",
            "role",
            "created_at"
        ),

    )

    def to_dict(self):
        return {
            "id": self.id,
            "actor_id": self.actor_id,
            "target_id": self.target_id,
            "action": self.action,
            "role": self.role,
            "meta": self.meta,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
        }

    def __repr__(self):
        return (
            f"<ActivityLog "
            f"id={self.id} "
            f"actor_id={self.actor_id} "
            f"action='{self.action}'>"
        )