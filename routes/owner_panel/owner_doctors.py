from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from extensions import db
from models.doctor import Doctor
from utils.decorators import owner_required


owner_doctors = Blueprint(
    "owner_doctors",
    __name__,
    url_prefix="/owner/doctors"
)


# ==========================================
# ALL DOCTORS
# ==========================================

@owner_doctors.route("/")
@owner_required
def doctors_list():

    search = request.args.get("search", "").strip()

    query = Doctor.query

    if search:
        query = query.filter(
            Doctor.name.ilike(f"%{search}%")
        )

    doctors = query.order_by(
        Doctor.id.desc()
    ).all()

    return render_template(
        "owner/doctors.html",
        doctors=doctors,
        search=search
    )


# ==========================================
# DOCTOR DETAILS
# ==========================================

@owner_doctors.route("/<int:doctor_id>")
@owner_required
def doctor_details(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    return render_template(
        "owner/doctor_details.html",
        doctor=doctor
    )


# ==========================================
# EDIT DOCTOR
# ==========================================

@owner_doctors.route(
    "/<int:doctor_id>/edit",
    methods=["GET", "POST"]
)
@owner_required
def edit_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    if request.method == "POST":

        doctor.name = request.form.get(
            "name",
            doctor.name
        )

        doctor.degree = request.form.get(
            "degree",
            doctor.degree
        )

        doctor.specialization = request.form.get(
            "specialization",
            doctor.specialization
        )

        doctor.hospital = request.form.get(
            "hospital",
            doctor.hospital
        )

        doctor.experience = request.form.get(
            "experience",
            doctor.experience
        )

        doctor.about = request.form.get(
            "about",
            doctor.about
        )

        doctor.profile_photo = request.form.get(
            "profile_photo",
            doctor.profile_photo
        )

        doctor.cover_photo = request.form.get(
            "cover_photo",
            doctor.cover_photo
        )

        fee = request.form.get(
            "consultation_fee"
        )

        if fee:
            doctor.consultation_fee = int(fee)

        db.session.commit()

        flash(
            "Doctor updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "owner_doctors.doctor_details",
                doctor_id=doctor.id
            )
        )

    return render_template(
        "owner/edit_doctor.html",
        doctor=doctor
    )


# ==========================================
# VERIFY DOCTOR
# ==========================================

@owner_doctors.route(
    "/<int:doctor_id>/verify"
)
@owner_required
def verify_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    doctor.verified = True

    db.session.commit()

    flash(
        "Doctor verified successfully.",
        "success"
    )

    return redirect(
        url_for(
            "owner_doctors.doctor_details",
            doctor_id=doctor.id
        )
    )


# ==========================================
# UNVERIFY DOCTOR
# ==========================================

@owner_doctors.route(
    "/<int:doctor_id>/unverify"
)
@owner_required
def unverify_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    doctor.verified = False

    db.session.commit()

    flash(
        "Doctor verification removed.",
        "warning"
    )

    return redirect(
        url_for(
            "owner_doctors.doctor_details",
            doctor_id=doctor.id
        )
    )


# ==========================================
# DELETE DOCTOR
# ==========================================

@owner_doctors.route(
    "/<int:doctor_id>/delete"
)
@owner_required
def delete_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    chamber_id = doctor.chamber_id

    db.session.delete(doctor)

    db.session.commit()

    flash(
        "Doctor deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "owner_chambers.chamber_details",
            chamber_id=chamber_id
        )
    )
