"""
Derivación de claves Fernet a partir de una master password usando PBKDF2.

Este módulo proporciona utilidades para obtener una clave simétrica apta
para Fernet partiendo de una contraseña maestra, aplicando un KDF
(PBKDF2 con SHA-256) y un salt almacenado en disco.

El salt se guarda en la ruta definida por `RUTA_SALT`, de modo que
la derivación sea reproducible entre ejecuciones en la misma máquina.
En un entorno real se recomienda gestionar el salt de forma más flexible
(por ejemplo, guardándolo junto al vault o permitiendo rotación).
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Tuple

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


RUTA_SALT = Path.home() / ".mi_encriptador_salt"  # ejemplo sencillo


def _obtener_o_crear_salt() -> bytes:
    if RUTA_SALT.exists():
        return RUTA_SALT.read_bytes()
    salt = os.urandom(16)
    RUTA_SALT.write_bytes(salt)
    return salt


def derivar_clave_fernet_desde_master(master_password: str) -> Tuple[bytes, bytes]:
    """
    Deriva una clave Fernet desde la master password usando PBKDF2.

    Devuelve (clave_fernet, salt_usada).

    En un producto real, puedes guardar el salt junto al vault, o
    permitir rotación de salt/clave.
    """
    salt = _obtener_o_crear_salt()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,            # 32 bytes para Fernet
        salt=salt,
        iterations=390_000,   # valor recomendado/alto para PBKDF2
    )
    key = kdf.derive(master_password.encode("utf-8"))
    clave_fernet = base64.urlsafe_b64encode(key)
    return clave_fernet, salt
