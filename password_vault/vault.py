"""
Implementación de un vault de contraseñas cifrado sobre archivo JSON.

Este módulo define la clase `PasswordVault`, que gestiona una colección
de entradas (`EntradaVault`) almacenadas en un archivo JSON cifrado
mediante un `Encriptador` basado en Fernet.

El vault se encarga de leer y escribir la estructura de datos en disco
(creando el directorio padre si es necesario), mientras que el cifrado
y descifrado del contenido se delega por completo en el encriptador
inyectado en el constructor.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from encriptador_core import Encriptador
from .models import EntradaVault


class PasswordVault:
    """
    Vault de contraseñas cifrado con Fernet.
    Guarda un listado de entradas en un archivo JSON cifrado.
    """

    def __init__(self, ruta_vault: Path, encriptador: Encriptador) -> None:
        self._ruta_vault = ruta_vault
        self._encriptador = encriptador

    def _leer_entradas(self) -> List[EntradaVault]:
        if not self._ruta_vault.exists():
            return []
        data_cifrada = self._ruta_vault.read_bytes()
        json_str = self._encriptador.desencriptar_str(data_cifrada)
        items = json.loads(json_str)
        return [EntradaVault(**item) for item in items]

    def _guardar_entradas(self, entradas: List[EntradaVault]) -> None:
        items = [asdict(e) for e in entradas]
        json_str = json.dumps(items, ensure_ascii=False, indent=2)
        data_cifrada = self._encriptador.encriptar_str(json_str)
        self._ruta_vault.parent.mkdir(parents=True, exist_ok=True)
        self._ruta_vault.write_bytes(data_cifrada)

    def listar(self) -> List[EntradaVault]:
        return self._leer_entradas()

    def agregar(self, entrada: EntradaVault) -> None:
        entradas = self._leer_entradas()
        entradas.append(entrada)
        self._guardar_entradas(entradas)
