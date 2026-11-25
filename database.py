"""Acceso a la base de datos MySQL (XAMPP) con PyMySQL."""
import pymysql
from pymysql.cursors import DictCursor

from config import Config


def get_connection(con_base=True):
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASS,
        database=Config.DB_NAME if con_base else None,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True,
    )


def init_db():
    """Crea la base y la tabla de usuarios si no existen."""
    with get_connection(con_base=False) as conn, conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4")
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def listar_usuarios():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, nombre, email, creado_en FROM usuarios ORDER BY id")
        return cur.fetchall()


def obtener_usuario(usuario_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, nombre, email, creado_en FROM usuarios WHERE id = %s", (usuario_id,))
        return cur.fetchone()


def buscar_por_email(email):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        return cur.fetchone()


def crear_usuario(nombre, email, password_hash):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)",
            (nombre, email, password_hash),
        )
        return cur.lastrowid


def eliminar_usuario(usuario_id):
    with get_connection() as conn, conn.cursor() as cur:
        return cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
