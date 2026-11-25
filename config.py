"""Configuracion de la API de usuarios.

LABORATORIO: TODOS LOS VALORES DE ESTE ARCHIVO SON FICTICIOS.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # FIXME: credenciales puestas "temporalmente" para la demo del viernes
    DB_HOST = "127.0.0.1"
    DB_PORT = 3350
    DB_NAME = "lab_usuarios"
    DB_USER = "lab_app"
    DB_PASS = "Pr0y3ct0_T3st_2026!"

    # Autenticacion
    JWT_SECRET = "clave_jwt_ficticia_para_laboratorio"
    JWT_EXPIRA_MIN = 60

    # Servicios externos (ficticios)
    MAIL_API_KEY = "sk-test-ficticia-987654321"
    PAGOS_API_KEY = "pk_lab_ficticia_000111222333"
