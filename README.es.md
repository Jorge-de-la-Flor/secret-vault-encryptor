README en [inglés](README.md)

# Secret Vault Encryptor

**Secret Vault Encryptor** es un proyecto en Python diseñado para proteger información sensible en disco mediante **cifrado simétrico autenticado** con Fernet y una **arquitectura basada en master password + KDF** para gestión de contraseñas.

El repositorio se organiza en dos componentes principales:

- `encriptador_core`: módulo genérico de cifrado con Fernet para cadenas y datos sensibles.
- `password_vault`: gestor de contraseñas local que utiliza master password, derivación de claves y cifrado autenticado para proteger un vault en disco.

---

## Características principales

- **Cifrado simétrico autenticado (Fernet)**  
  - Basado en el paquete `cryptography`, que implementa el estándar Fernet (AES + HMAC) para garantizar confidencialidad e integridad del dato cifrado.  

- **Módulo de cifrado reutilizable** (`encriptador_core`)  
  - API sencilla para encriptar y desencriptar cadenas UTF-8.
  - Adecuado para proteger tokens de API, claves de acceso, configuraciones sensibles y otros secretos en disco.

- **Password Vault local** (`password_vault`)  
  - Master password introducida por el usuario.  
  - Derivación de clave a partir de la master password mediante KDF (PBKDF2 con múltiples iteraciones).
  - Uso de Fernet para cifrar y descifrar el archivo de credenciales.
  - Modelo de datos simple: servicio, usuario, contraseña y notas.

- **Calidad de código y mantenibilidad**  
  - Estructura de proyecto clara, separando core criptográfico, vault, ejemplos y tests.  
  - Tests automatizados con `pytest` para el encriptador y el vault.

---

## Arquitectura del proyecto

```text
secret_vault_encryptor/
├─ README.md
├─ pyproject.toml
├─ encriptador_core/
│  ├─ __init__.py
│  ├─ encriptador.py          # Encriptador genérico (Fernet)
│  └─ utils.py                # Helpers para E/S de bytes
│
├─ password_vault/
│  ├─ __init__.py
│  ├─ kdf.py                  # KDF (PBKDF2) para derivar clave desde master password
│  ├─ vault.py                # Lógica de leer/escribir el archivo cifrado
│  ├─ cli.py                  # CLI (crear vault, añadir, listar, etc.)
│  └─ models.py               # Modelo: servicio, usuario, contraseña, notas
│
├─ examples/
│  ├─ usar_encriptador_core.py
│  └─ usar_password_vault.py
│
└─ tests/
   ├─ test_encriptador_core.py
   └─ test_password_vault.py
```

Esta organización permite reutilizar el **core criptográfico** en otros proyectos (gestores de API keys, cifrado de configs, etc.) y, al mismo tiempo, ofrecer un caso de uso completo de gestor de contraseñas.

---

## Instalación

Requisitos:

- Python 3.12+
- `cryptography`
- `pytest` (para ejecutar tests)

Con `uv`:

```bash
uv sync
```

Con `pip` (si exportas requisitos):

```bash
pip install -r requirements.txt
```

## Uso del encriptador core

El módulo `encriptador_core` expone una clase `Encriptador` basada en Fernet.

Ejemplo rápido:

```python
from encriptador_core import Encriptador

# Generar una nueva clave Fernet
clave = Encriptador.generar_clave()
enc = Encriptador(clave)

texto = "secreto super sensible"
token = enc.encriptar_str(texto)
print("Token:", token)

original = enc.desencriptar_str(token)
print("Original:", original)
```

Casos de uso típicos:

- Almacenar tokens de API cifrados en disco.
- Cifrar configuraciones sensibles (credenciales de BBDD, claves de terceros).  
- Proteger pequeños archivos o blobs de texto.

También puedes ejecutar el ejemplo incluido:

```bash
uv run python examples/usar_encriptador_core.py
```

## Uso del Password Vault

El componente `password_vault` implementa un vault local cifrado, protegido por una master password.

### Flujo criptográfico

1. El usuario introduce una **master password**.  
2. Se deriva una clave binaria mediante **PBKDF2-HMAC-SHA256** con sal y un número elevado de iteraciones.
3. Esa clave derivada se transforma en una clave Fernet válida (32 bytes codificados en base64 url-safe).
4. Se crea una instancia de `Encriptador` con dicha clave.  
5. El contenido del vault (lista de entradas) se serializa como JSON y se cifra con Fernet antes de escribirse a disco.  

### CLI

Ejecutar el CLI de ejemplo:

```bash
uv run python examples/usar_password_vault.py
```

Opciones básicas:

- **Listar entradas** del vault.  
- **Agregar nuevas entradas** con servicio, usuario, contraseña y notas.

La ruta del archivo del vault y la del salt se gestionan en código y pueden ajustarse según el entorno o las preferencias de despliegue.

---

## Tests

Para ejecutar todos los tests:

```bash
uv run python -m pytest
```

Se cubren:

- Cifrado y descifrado básico del `Encriptador`.  
- Operaciones fundamentales del vault (agregar y listar entradas).

Esto permite validar el comportamiento core antes de extender funcionalidades.

---

## Decisiones de diseño

- **Fernet como esquema de cifrado**  
  - Ofrece cifrado simétrico autenticado de alto nivel y fácil de usar en Python.
  - Evita errores comunes de implementación manual de AES (IV, padding, MAC, etc.).

- **KDF basado en PBKDF2**
  - Uso de múltiples iteraciones para hacer costosos los ataques offline sobre la master password.
  - KDF separado del cifrado, lo que facilita la futura sustitución por Argon2 o scrypt si se desea endurecer aún más el esquema.

- **Separación entre core y vault**  
  - El módulo de cifrado (`encriptador_core`) es agnóstico al contexto.  
  - El vault (`password_vault`) encapsula las decisiones de modelo de datos, formato de archivo y UX de CLI.

---

## Roadmap (visión)

Algunas líneas naturales de evolución del proyecto:

- Integrar un TUI/GUI para gestionar el vault de forma más amigable.  
- Añadir búsqueda, filtrado y etiquetas para las entradas.  
- Soportar distintos backends de almacenamiento (archivo local, repositorios Git, WebDAV, etc.).
- Explorar KDFs más avanzados (Argon2id, scrypt) y configuración dinámica de parámetros.
- Documentación ampliada y ejemplos adicionales de integración en otros proyectos.

---

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

La licencia MIT es permisiva y permite usar, modificar y distribuir el código, tanto en proyectos personales como comerciales, fomentando la colaboración y la adopción en la comunidad.
