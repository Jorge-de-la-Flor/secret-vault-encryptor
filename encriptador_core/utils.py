"""
Helpers básicos para leer y escribir archivos binarios con pathlib.

Este módulo define funciones utilitarias mínimas para trabajar con rutas
de tipo `pathlib.Path` y manejar contenido en bytes de forma explícita.
Son convenientes para encapsular la lógica de E/S binaria en un solo lugar
y reutilizarla en otros módulos (por ejemplo, claves, tokens o blobs).

Las funciones no realizan validaciones avanzadas ni manejo complejo de
errores: se limitan a abrir el archivo en modo adecuado y devolver o
persistir los datos recibidos.
"""

from __future__ import annotations

from pathlib import Path


def leer_bytes(path: Path) -> bytes:
    """
    Lee el contenido binario completo de un archivo y lo devuelve como bytes.

    El parámetro `path` debe ser una ruta válida a un archivo existente.
    Lanza las excepciones de E/S estándar si el archivo no puede leerse.
    """
    with path.open("rb") as f:
        return f.read()


def escribir_bytes(path: Path, data: bytes) -> None:
    """
    Escribe datos binarios en la ruta indicada, creando directorios padres si hace falta.

    Si el archivo ya existe, su contenido se sobrescribe por completo.
    Se crean los directorios intermedios con `parents=True, exist_ok=True`.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(data)
