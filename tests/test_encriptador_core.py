"""
Tests básicos para el encriptador Fernet del módulo encriptador_core.

Este archivo verifica que el flujo de encriptar y luego desencriptar
una cadena con Encriptador preserva exactamente el texto original.
"""

from __future__ import annotations

from encriptador_core import Encriptador


def test_encriptar_y_desencriptar_str() -> None:
    clave = Encriptador.generar_clave()
    enc = Encriptador(clave)

    texto = "hola mundo"
    token = enc.encriptar_str(texto)
    recuperado = enc.desencriptar_str(token)

    assert recuperado == texto
