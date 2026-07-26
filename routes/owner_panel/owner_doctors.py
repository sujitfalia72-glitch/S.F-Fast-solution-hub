from flask import Blueprint, render_template, redirect, url_for, flash
from extensions import db
from models.doctor import Doctor
from utils.decorators import owner_required

owner_doctors = Blueprint(
    "owner_doctors",
    __name__,
    url_prefix="/owner/doctors"
)


# ===============================
# ALL DOCTORS
# ===============================
@owner_doctors.route("/")
@owner_required
def doctors_list():

    doctors = Doctor.query.order_by(
        Doctor.id.desc()
    ).all()

    return render_template(
        "owner/doctors.html",
        doctors=doctors
    )


# ===============================
# DOCTOR DETAILS
# ===============================
@owner_doctors.route("/<int:doctor_id>")
@owner_required
def doctor_details(doctor_id):

    doctor = Doctor.query.get_or_404(doctor_id)

    return render_template(
        "owner/doctor_details.html",
        doctor=doctor
    )


# ===============================
# EDIT DOCTOR
# ===============================
@owner_doctors.route("/<int:doctor_id>/edit")
@owner_required
def edit_doctor(doctor_id):

    flash(
        "Edit Doctor page is under development.",
        "info"
    )

    return redirect(
        url_for(
            "owner_doctors.doctor_details",
            doctor_id=doctor_id
        )
    )


# ===============================
# DELETE DOCTOR
# ===============================
@owner_doctors.route("/<int:doctor_id>/delete")
@owner_required
def delete_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(
        doctor_id
    )

    db.session.delete(doctor)

    db.session.commit()

    flash(
        "Doctor deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "owner_doctors.doctors_list"
        )
  )
