"""
Ejemplo mínimo de uso del encriptador Fernet.

Este módulo genera una clave nueva en memoria, crea una instancia de
`Encriptador` y muestra por consola cómo encriptar y desencriptar
una cadena de texto sencilla en un flujo completo de ida y vuelta.

Está pensado como script de demostración o ejemplo rápido dentro del
proyecto, no como gestor de claves persistentes: la clave se pierde
al terminar el programa y el token solo es válido durante esta ejecución.
"""

from __future__ import annotations

from encriptador_core import Encriptador


def main() -> None:
    clave = Encriptador.generar_clave()
    enc = Encriptador(clave)

    texto = "secreto super sensible"
    token = enc.encriptar_str(texto)
    print("Token:", token)

    original = enc.desencriptar_str(token)
    print("Original:", original)


if __name__ == "__main__":
    main()
