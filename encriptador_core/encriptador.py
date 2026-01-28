"""
Utilidades de encriptación simétrica basadas en Fernet.

Este módulo expone la clase `Encriptador`, un wrapper sencillo sobre
`cryptography.fernet.Fernet` para encriptar y desencriptar cadenas de texto.
La clave simétrica se recibe externamente, lo que permite integrarlo con
distintas fuentes de secretos (variables de entorno, archivos seguros, KMS,
vaults, etc.).

Casos de uso habituales:
- Guardar credenciales o tokens en disco de forma segura.
- Encriptar configuraciones sensibles antes de persistirlas.
- Implementar pequeños “password vaults” o helpers de cifrado en aplicaciones.

Ejemplo básico de uso:

    from cryptography.fernet import Fernet
    from encriptador import Encriptador

    # Generar y guardar la clave por tu cuenta
    clave = Encriptador.generar_clave()
    encr = Encriptador(clave)

    token = encr.encriptar_str("secreto")
    texto = encr.desencriptar_str(token)

Requiere el paquete `cryptography` y usa Fernet, que provee cifrado
simétrico autenticado (confidencialidad + integridad del mensaje).
"""

from __future__ import annotations

from cryptography.fernet import Fernet


class Encriptador:
    """
    Encriptador de cadenas usando Fernet (encriptación simétrica autenticada).

    Este encriptador es genérico: recibe la clave en el __init__ para poder
    reutilizarlo en distintos contextos (APIs, configs, password vault, etc.).
    """

    def __init__(self, clave_fernet: bytes) -> None:
        self._fernet = Fernet(clave_fernet)

    @staticmethod
    def generar_clave() -> bytes:
        """
        Genera una nueva clave Fernet (32 bytes codificados en base64 url-safe).
        """
        return Fernet.generate_key()

    def encriptar_str(self, texto_plano: str) -> bytes:
        """
        Encripta un string en UTF-8 y devuelve el token en bytes.
        """
        return self._fernet.encrypt(texto_plano.encode("utf-8"))

    def desencriptar_str(self, texto_encriptado: bytes) -> str:
        """
        Desencripta un token en bytes y devuelve el string en UTF-8.
        """
        return self._fernet.decrypt(texto_encriptado).decode("utf-8")
