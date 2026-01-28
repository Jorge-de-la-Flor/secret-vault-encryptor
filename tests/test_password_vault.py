"""
Tests de integración sencilla para el PasswordVault.

Este archivo verifica que un vault nuevo puede agregar una entrada y
luego recuperarla correctamente mediante `listar`, usando una clave
derivada con la KDF y un directorio temporal de pytest.
"""

from __future__ import annotations

from pathlib import Path

from encriptador_core import Encriptador
from password_vault.kdf import derivar_clave_fernet_desde_master
from password_vault.models import EntradaVault
from password_vault.vault import PasswordVault


def test_vault_agregar_y_listar(tmp_path: Path) -> None:
    ruta_vault = tmp_path / "vault.jafa"
    clave_fernet, _ = derivar_clave_fernet_desde_master("master-test")
    enc = Encriptador(clave_fernet)

    vault = PasswordVault(ruta_vault, enc)

    entrada = EntradaVault(
        servicio="github",
        usuario="user",
        contrasena="pass123",
        notas="test",
    )
    vault.agregar(entrada)

    entradas = vault.listar()
    assert len(entradas) == 1
    assert entradas[0].servicio == "github"
