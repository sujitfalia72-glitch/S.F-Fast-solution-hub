from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    session,
    flash,
    url_for
)

from datetime import datetime, timedelta

from extensions import db
from models.user import User
from models.verification_request import VerificationRequest
from utils.decorators import (
    login_required,
    admin_required
)

verification = Blueprint(
    "verification",
    __name__,
    url_prefix="/verification"
)


# =====================================================
# USER REQUEST VERIFICATION
# =====================================================

@verification.route(
    "/request",
    methods=["GET", "POST"]
)
@login_required
def request_verification():

    user = User.query.get_or_404(
        session["user_id"]
    )

    if user.is_verified:
        flash(
            "Your profile is already verified.",
            "warning"
        )
        return redirect(
            url_for("verification.my_requests")
        )

    existing_request = (
        VerificationRequest.query.filter_by(
            user_id=user.id,
            status="pending"
        ).first()
    )

    if existing_request:
        flash(
            "A verification request is already pending.",
            "warning"
        )
        return redirect(
            url_for("verification.my_requests")
        )

    if request.method == "POST":

        try:
            plan_months = int(
                request.form.get(
                    "plan_months",
                    1
                )
            )
        except (
            TypeError,
            ValueError
        ):
            flash(
                "Invalid verification plan.",
                "danger"
            )
            return redirect(
                url_for(
                    "verification.request_verification"
                )
            )

        if plan_months not in (
            1,
            6
        ):
            flash(
                "Invalid verification plan.",
                "danger"
            )
            return redirect(
                url_for(
                    "verification.request_verification"
                )
            )

        amount = (
            500
            if plan_months == 6
            else 100
        )

        verification_request = (
            VerificationRequest(
                user_id=user.id,
                plan_months=plan_months,
                amount=amount,
                payment_status="pending",
                status="pending"
            )
        )

        db.session.add(
            verification_request
        )
        db.session.commit()

        flash(
            "Verification request submitted successfully.",
            "success"
        )

        return redirect(
            url_for(
                "verification.my_requests"
            )
        )

    return render_template(
        "verification/request.html",
        user=user
    )


# =====================================================
# USER REQUEST HISTORY
# =====================================================

@verification.route("/my-requests")
@login_required
def my_requests():

    requests = (
        VerificationRequest.query.filter_by(
            user_id=session["user_id"]
        )
        .order_by(
            VerificationRequest.created_at.desc()
        )
        .all()
    )

    return render_template(
        "verification/my_requests.html",
        requests=requests
    )
    
    # =====================================================
# ADMIN PANEL
# =====================================================

@verification.route("/admin/requests")
@admin_required
def admin_requests():

    requests = (
        VerificationRequest.query
        .order_by(
            VerificationRequest.created_at.desc()
        )
        .all()
    )

    pending_count = sum(
        r.status == "pending"
        for r in requests
    )

    approved_count = sum(
        r.status == "approved"
        for r in requests
    )

    rejected_count = sum(
        r.status == "rejected"
        for r in requests
    )

    return render_template(
        "owner/verification_requests.html",
        requests=requests,
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count
    )


# =====================================================
# APPROVE REQUEST
# =====================================================

@verification.route(
    "/admin/approve/<int:request_id>",
    methods=["POST"]
)
@admin_required
def approve_verification(request_id):

    verification_request = (
        VerificationRequest.query.get_or_404(
            request_id
        )
    )

    if verification_request.status != "pending":

        flash(
            "Request has already been processed.",
            "warning"
        )

        return redirect(
            url_for(
                "verification.admin_requests"
            )
        )

    user = User.query.get_or_404(
        verification_request.user_id
    )

    days = (
        180
        if verification_request.plan_months == 6
        else 30
    )

    user.is_verified = True
    user.verification_expiry = (
        datetime.utcnow()
        + timedelta(days=days)
    )

    verification_request.status = "approved"
    verification_request.payment_status = "paid"
    verification_request.reviewed_at = (
        datetime.utcnow()
    )

    db.session.commit()

    flash(
        "Verification approved successfully.",
        "success"
    )

    return redirect(
        url_for(
            "verification.admin_requests"
        )
    )


# =====================================================
# REJECT REQUEST
# =====================================================

@verification.route(
    "/admin/reject/<int:request_id>",
    methods=["POST"]
)
@admin_required
def reject_verification(request_id):

    verification_request = (
        VerificationRequest.query.get_or_404(
            request_id
        )
    )

    if verification_request.status != "pending":

        flash(
            "Request has already been processed.",
            "warning"
        )

        return redirect(
            url_for(
                "verification.admin_requests"
            )
        )

    verification_request.status = "rejected"

    verification_request.rejection_reason = (
        request.form.get(
            "reason",
            "Rejected by admin"
        ).strip()
    )

    verification_request.reviewed_at = (
        datetime.utcnow()
    )

    db.session.commit()

    flash(
        "Verification request rejected.",
        "success"
    )

    return redirect(
        url_for(
            "verification.admin_requests"
        )
    )


# =====================================================
# REMOVE VERIFICATION
# =====================================================

@verification.route(
    "/admin/remove/<int:user_id>",
    methods=["POST"]
)
@admin_required
def remove_verification(user_id):

    user = User.query.get_or_404(
        user_id
    )

    if not user.is_verified:

        flash(
            "User is not verified.",
            "warning"
        )

        return redirect(
            url_for(
                "verification.admin_requests"
            )
        )

    user.is_verified = False
    user.verification_expiry = None

    db.session.commit()

    flash(
        "Verification removed successfully.",
        "success"
    )

    return redirect(
        url_for(
            "verification.admin_requests"
        )
    )