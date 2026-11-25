"""Configuracion de la API de usuarios.

Los valores sensibles se leen de variables de entorno. En desarrollo se
cargan desde un archivo .env local, que esta en .gitignore y NO se sube.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Base de datos MySQL/MariaDB de XAMPP (puerto 3350 en esta laptop)
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3350"))
    DB_NAME = os.getenv("DB_NAME", "lab_usuarios")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASS = os.getenv("DB_PASS", "")

    # Autenticacion
    JWT_SECRET = os.getenv("JWT_SECRET", "")
    JWT_EXPIRA_MIN = int(os.getenv("JWT_EXPIRA_MIN", "60"))

    # Servicios externos (ficticios)
    MAIL_API_KEY = os.getenv("MAIL_API_KEY", "")
    PAGOS_API_KEY = os.getenv("PAGOS_API_KEY", "")
