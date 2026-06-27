from functools import wraps

from flask import (
    Blueprint,
    request,
    render_template,
    session,
    abort
)

from services.search_service import (
    search_users,
    search_workers,
    search_bookings,
    search_works
)

search = Blueprint("search", __name__)


# ==========================================================
# ACCESS CONTROL
# ==========================================================
def search_access_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if session.get("role") not in (
            "owner",
            "admin",
            "super_admin"
        ):
            abort(403)

        return f(*args, **kwargs)

    return decorated


# ==========================================================
# USER SEARCH
# ==========================================================
@search.route("/search/users")
@search_access_required
def users_search():

    users = search_users(
        query=request.args.get("q", "").strip(),
        area=request.args.get("area", "").strip(),
        skill=request.args.get("skill", "").strip()
    )

    return render_template(
        "search_users.html",
        users=users
    )


# ==========================================================
# WORKER SEARCH
# ==========================================================
@search.route("/search/workers")
@search_access_required
def workers_search():

    workers = search_workers(
        query=request.args.get("q", "").strip(),
        area=request.args.get("area", "").strip(),
        skill=request.args.get("skill", "").strip()
    )

    return render_template(
        "search_workers.html",
        workers=workers
    )


# ==========================================================
# BOOKING SEARCH
# ==========================================================
@search.route("/search/bookings")
@search_access_required
def bookings_search():

    bookings = search_bookings(
        query=request.args.get("q", "").strip(),
        status=request.args.get("status", "").strip()
    )

    return render_template(
        "search_bookings.html",
        bookings=bookings
    )


# ==========================================================
# WORK SEARCH
# ==========================================================
@search.route("/search/works")
@search_access_required
def works_search():

    works = search_works(
        query=request.args.get("q", "").strip(),
        area=request.args.get("area", "").strip()
    )

    return render_template(
        "search_works.html",
        works=works
    )