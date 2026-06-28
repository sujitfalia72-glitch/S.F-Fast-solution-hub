from datetime import datetime, UTC

from extensions import db


class DoctorSchedule(db.Model):

    __tablename__ = "doctor_schedules"

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

    chamber_name = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    area = db.Column(
        db.String(150),
        nullable=False,
        index=True
    )

    address = db.Column(
        db.Text
    )

    phone = db.Column(
        db.String(20)
    )

    whatsapp = db.Column(
        db.String(20)
    )

    day = db.Column(
        db.String(50),
        nullable=False,
        index=True
    )

    start_time = db.Column(
        db.Time,
        nullable=False
    )

    end_time = db.Column(
        db.Time,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False
    )

    # ==========================
    # RELATIONSHIP
    # ==========================
    doctor = db.relationship(
        "Doctor",
        backref=db.backref(
            "schedules",
            lazy="dynamic",
            cascade="all, delete-orphan"
        )
    )

    # ==========================
    # INDEXES
    # ==========================
    __table_args__ = (
        db.Index(
            "idx_doctor_day",
            "doctor_id",
            "day"
        ),
    )

    def __repr__(self):
        return (
            f"<DoctorSchedule "
            f"doctor_id={self.doctor_id} "
            f"day={self.day}>"
        )