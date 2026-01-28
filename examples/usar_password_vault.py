"""
Ejemplo de punto de entrada para ejecutar el password vault desde `password_vault.cli`.

Este módulo actúa como wrapper mínimo: simplemente importa la función
`main` del módulo `password_vault.cli` y la ejecuta cuando se invoca
el archivo directamente como script (`python -m ...` o similar).
"""

from __future__ import annotations

from password_vault.cli import main


if __name__ == "__main__":
    main()
