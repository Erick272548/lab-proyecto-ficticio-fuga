# API de usuarios (proyecto ficticio de laboratorio)

> Repositorio de **práctica académica** (pruebas de caja blanca). Todas las
> credenciales que aparecen en su historial son **ficticias** y fueron
> filtradas a propósito para demostrar cómo un bot captura secretos.

API REST en Flask con MySQL (XAMPP, puerto 3350).

| Método | Ruta | Token |
|---|---|---|
| GET | `/salud` | no |
| POST | `/usuarios` (registro) | no |
| POST | `/login` | no |
| GET | `/usuarios` | sí |
| GET | `/usuarios/<id>` | sí |
| DELETE | `/usuarios/<id>` | sí |

```
pip install -r requirements.txt
python app.py      # http://127.0.0.1:5001
```

Las variables (`DB_USER`, `DB_PASS`, `JWT_SECRET`, ...) se leen del entorno
o de un `.env` local que no se versiona.
