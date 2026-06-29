from datetime import datetime, UTC
from extensions import db


class DoctorRating(db.Model):
    __tablename__ = "doctor_ratings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "doctors.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    rating = db.Column(
        db.SmallInteger,
        nullable=False
    )

    ip_address = db.Column(
        db.String(45),   # IPv4 + IPv6 support
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True
    )

    # =========================
    # RELATIONSHIP
    # =========================
    doctor = db.relationship(
        "Doctor",
        back_populates="ratings"
    )

    # =========================
    # VALIDATION
    # =========================
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not 1 <= self.rating <= 5:
            raise ValueError(
                "Rating must be between 1 and 5"
            )

    # =========================
    # REPRESENTATION
    # =========================
    def __repr__(self):
        return (
            f"<DoctorRating "
            f"doctor_id={self.doctor_id} "
            f"rating={self.rating}>"
        )
