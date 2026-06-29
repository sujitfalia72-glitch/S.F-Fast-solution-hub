from extensions import db
from datetime import datetime, UTC


class Profile(db.Model):

    __tablename__ = "profile"

    # ================= PRIMARY KEY =================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ================= USER LINK =================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=True,
        nullable=False,
        index=True
    )

    user = db.relationship(
        "User",
        back_populates="profile",
        lazy="joined"
    )
    # ================= BASIC INFO =================

    name = db.Column(
        db.String(100),
        default=""
    )

    address = db.Column(
        db.String(200),
        default=""
    )

    age = db.Column(
        db.Integer
    )

    education = db.Column(
        db.String(100),
        default=""
    )

    area = db.Column(
        db.String(100),
        default=""
    )

    gender = db.Column(
        db.String(20),
        default=""
    )

    religion = db.Column(
        db.String(50),
        default=""
    )

    country = db.Column(
        db.String(50),
        default=""
    )

    # ================= WORK INFO =================

    work_desc = db.Column(
        db.Text,
        default=""
    )

    # ================= IMAGES =================

    profile_img = db.Column(
        db.String(1000),
        default=""
    )

    cover_img = db.Column(
        db.String(1000),
        default=""
    )

    # Gallery stored as JSON string

    gallery = db.Column(
        db.Text,
        default="[]"
    )

    # ================= TIMESTAMP =================

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

    # ================= DEBUG =================

    def __repr__(self):

        return (
            f"<Profile "
            f"id={self.id} "
            f"name='{self.name}' "
            f"user_id={self.user_id}>"
        )
