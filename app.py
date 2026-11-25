"""API REST de gestion de usuarios (Flask + MySQL de XAMPP)."""
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
import pymysql
from flask import Flask, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

import database
from config import Config

app = Flask(__name__)


def requiere_token(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        cabecera = request.headers.get("Authorization", "")
        if not cabecera.startswith("Bearer "):
            return jsonify(error="Falta el token Bearer"), 401
        try:
            g.usuario = jwt.decode(cabecera[7:], Config.JWT_SECRET, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify(error="Token invalido o expirado"), 401
        return vista(*args, **kwargs)

    return envoltura


@app.get("/salud")
def salud():
    return jsonify(estado="ok", servicio="api-usuarios")


@app.post("/usuarios")
def registrar():
    datos = request.get_json(silent=True) or {}
    if not all(datos.get(campo) for campo in ("nombre", "email", "password")):
        return jsonify(error="nombre, email y password son obligatorios"), 400
    try:
        nuevo_id = database.crear_usuario(
            datos["nombre"], datos["email"], generate_password_hash(datos["password"])
        )
    except pymysql.err.IntegrityError:
        return jsonify(error="El email ya esta registrado"), 409
    return jsonify(id=nuevo_id, nombre=datos["nombre"], email=datos["email"]), 201


@app.post("/login")
def login():
    datos = request.get_json(silent=True) or {}
    usuario = database.buscar_por_email(datos.get("email", ""))
    if not usuario or not check_password_hash(usuario["password_hash"], datos.get("password", "")):
        return jsonify(error="Credenciales incorrectas"), 401
    carga = {
        "sub": str(usuario["id"]),
        "email": usuario["email"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=Config.JWT_EXPIRA_MIN),
    }
    return jsonify(token=jwt.encode(carga, Config.JWT_SECRET, algorithm="HS256"))


@app.get("/usuarios")
@requiere_token
def listar():
    return jsonify(database.listar_usuarios())


@app.get("/usuarios/<int:usuario_id>")
@requiere_token
def detalle(usuario_id):
    usuario = database.obtener_usuario(usuario_id)
    return (jsonify(usuario), 200) if usuario else (jsonify(error="No encontrado"), 404)


@app.delete("/usuarios/<int:usuario_id>")
@requiere_token
def eliminar(usuario_id):
    if not database.eliminar_usuario(usuario_id):
        return jsonify(error="No encontrado"), 404
    return "", 204


if __name__ == "__main__":
    database.init_db()
    app.run(host="127.0.0.1", port=5001, debug=False)
