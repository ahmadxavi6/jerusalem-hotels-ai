import os
import requests
from functools import wraps
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
)
from supabase import create_client
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

admin_bp = Blueprint("admin", __name__)

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_embedding(text):
    return get_model().encode(text).tolist()


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/")
@admin_required
def dashboard():
    hotels = (
        supabase.table("hotels")
        .select("id, name, neighborhood, stars, price_min, price_max")
        .execute()
    )
    return render_template("admin/dashboard.html", hotels=hotels.data)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == os.getenv("ADMIN_PASSWORD", "admin123"):
            session["is_admin"] = True
            return redirect(url_for("admin.dashboard"))
        return render_template("admin/login.html", error="Wrong password")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/add", methods=["GET", "POST"])
@admin_required
def add_hotel():
    if request.method == "POST":
        hotel = {
            "name": request.form.get("name"),
            "location": request.form.get("location"),
            "neighborhood": request.form.get("neighborhood"),
            "stars": int(request.form.get("stars")),
            "price_min": int(request.form.get("price_min")),
            "price_max": int(request.form.get("price_max")),
            "amenities": request.form.get("amenities"),
            "nearby": request.form.get("nearby"),
            "description": request.form.get("description"),
        }
        text = f"{hotel['name']} {hotel['neighborhood']} {hotel['amenities']} {hotel['nearby']} {hotel['description']}"
        hotel["embedding"] = get_embedding(text)
        supabase.table("hotels").insert(hotel).execute()
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add.html")


@admin_bp.route("/edit/<int:hotel_id>", methods=["GET", "POST"])
@admin_required
def edit_hotel(hotel_id):
    if request.method == "POST":
        hotel = {
            "name": request.form.get("name"),
            "location": request.form.get("location"),
            "neighborhood": request.form.get("neighborhood"),
            "stars": int(request.form.get("stars")),
            "price_min": int(request.form.get("price_min")),
            "price_max": int(request.form.get("price_max")),
            "amenities": request.form.get("amenities"),
            "nearby": request.form.get("nearby"),
            "description": request.form.get("description"),
        }
        text = f"{hotel['name']} {hotel['neighborhood']} {hotel['amenities']} {hotel['nearby']} {hotel['description']}"
        hotel["embedding"] = get_embedding(text)
        supabase.table("hotels").update(hotel).eq("id", hotel_id).execute()
        return redirect(url_for("admin.dashboard"))

    hotel = supabase.table("hotels").select("*").eq("id", hotel_id).execute()
    return render_template("admin/edit.html", hotel=hotel.data[0])


@admin_bp.route("/delete/<int:hotel_id>", methods=["POST"])
@admin_required
def delete_hotel(hotel_id):
    supabase.table("hotels").delete().eq("id", hotel_id).execute()
    return redirect(url_for("admin.dashboard"))