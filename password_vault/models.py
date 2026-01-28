"""
Modelos de datos para entradas de un password vault sencillo.

Este módulo define la dataclass `EntradaVault`, que representa una entrada
individual en el gestor de contraseñas: servicio, usuario, contraseña y
notas opcionales asociadas.

Está pensado para ser usado junto con un vault cifrado (por ejemplo,
usando Fernet), donde una lista de estas entradas se serializa y se
guarda en disco de forma segura.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class EntradaVault:
    servicio: str
    usuario: str
    contrasena: str
    notas: Optional[str] = None
