"""
CLI mínima para gestionar un password vault cifrado con Fernet.

Este módulo ofrece una interfaz de línea de comandos sencilla para
listar y agregar entradas en un vault de contraseñas almacenado en
un archivo cifrado en el directorio del usuario.

La clave de cifrado se deriva en cada ejecución a partir de una
master password introducida por consola, usando una función KDF
(`derivar_clave_fernet_desde_master`) que produce una clave válida
para el `Encriptador` del core.
"""

from __future__ import annotations

import getpass
from pathlib import Path

from encriptador_core import Encriptador
from .kdf import derivar_clave_fernet_desde_master
from .models import EntradaVault
from .vault import PasswordVault


RUTA_VAULT = Path.home() / ".mi_encriptador" / "vault.jafa"


def _crear_encriptador_desde_master() -> Encriptador:
    master = getpass.getpass("Master password: ")
    clave_fernet, _salt = derivar_clave_fernet_desde_master(master)
    return Encriptador(clave_fernet)


def comando_listar() -> None:
    encriptador = _crear_encriptador_desde_master()
    vault = PasswordVault(RUTA_VAULT, encriptador)
    entradas = vault.listar()

    if not entradas:
        print("No hay entradas en el vault.")
        return

    for i, e in enumerate(entradas, start=1):
        print(f"{i}. {e.servicio} - {e.usuario}")


def comando_agregar() -> None:
    encriptador = _crear_encriptador_desde_master()
    vault = PasswordVault(RUTA_VAULT, encriptador)

    servicio = input("Servicio: ").strip()
    usuario = input("Usuario: ").strip()
    contrasena = getpass.getpass("Contraseña: ")
    notas = input("Notas (opcional): ").strip() or None

    entrada = EntradaVault(
        servicio=servicio,
        usuario=usuario,
        contrasena=contrasena,
        notas=notas,
    )
    vault.agregar(entrada)
    print("Entrada agregada correctamente.")


def main() -> None:
    print("Password Vault")
    print("1) Listar")
    print("2) Agregar")
    opcion = input("Opción: ").strip()

    if opcion == "1":
        comando_listar()
    elif opcion == "2":
        comando_agregar()
    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()
