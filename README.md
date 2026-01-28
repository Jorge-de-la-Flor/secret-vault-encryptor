README in [Spanish](README.es.md)

# Secret Vault Encryptor

Secret Vault Encryptor is a Python project designed to protect sensitive information on disk using authenticated symmetric encryption with Fernet and a master password + KDF-based architecture for password management.

The repository is organized into two main components:

- `encriptador_core`: a generic encryption module using Fernet for strings and sensitive data.
- `password_vault`: a local password manager that uses a master password, key derivation, and authenticated encryption to protect a vault on disk.

---

## Main Features

- Authenticated Symmetric Encryption (Fernet)
  - Based on the `cryptography` package, which implements the Fernet standard (AES + HMAC) to guarantee the confidentiality and integrity of the encrypted data.

- **Reusable Encryption Module** (`encriptador_core`)
  - Simple API for encrypting and decrypting UTF-8 strings.
  - Suitable for protecting API tokens, access keys, sensitive configurations, and other secrets on disk.

- **Local Password Vault** (`password_vault`)
  - Master password entered by the user.
  - Key derivation from the master password using KDF (PBKDF2 with multiple iterations).
  - Use of Fernet to encrypt and decrypt the credentials file.
  - Simple data model: service, user, password, and notes.

- **Code Quality and Maintainability**
  - Clear project structure, separating the cryptographic core, vault, examples, and tests.
  - Automated tests with `pytest` for the encryptor and vault.

---

## Project Architecture

```text
secret_vault_encryptor/
├─ README.md
├─ pyproject.toml
├─ encriptador_core/
│  ├─ __init__.py
│  ├─ encriptador.py          # Generic Encryptor (Fernet)
│  └─ utils.py                # Helpers for Byte I/O
│
├─ password_vault/
│  ├─ __init__.py
│  ├─ kdf.py                  # KDF (PBKDF2) to derive the key from the master
│  ├─ vault.py                # Logic for reading/writing the encrypted file
│  ├─ cli.py                  # CLI (create vault, add, list, etc.)
│  └─ models.py               # Model: service, user, password, notes
│
├─ examples/
│  ├─ usar_encriptador_core.py
│  └─ usar_password_vault.py
│
└─ tests/
   ├─ test_encriptador_core.py
   └─ test_password_vault.py
```

This organization allows reusing the **cryptographic core** in other projects (API key managers, config encryption, etc.) while simultaneously providing a complete password manager use case.

---

## Installation

Requirements:

- Python 3.12+
- `cryptography`
- `pytest` (to run tests)

With `uv`:

```bash
uv sync
```

With `pip` (if you export requirements):

```bash
pip install -r requirements.txt
```

## Using the core encryptor

The `encriptador_core` module exposes a `Encriptador` class based on Fernet.

Quick Example:

```python
from encriptador_core import Encriptador

# Generate a new Fernet key
clave = Encriptador.generar_clave()
enc = Encriptador(clave)

texto = "secreto super sensible"
token = enc.encriptar_str(texto)
print("Token:", token)

original = enc.desencriptar_str(token)
print("Original:", original)
```

Typical use cases:

- Store encrypted API tokens on disk.
- Encrypt sensitive configurations (database credentials, third-party keys).
- Protect small files or text blobs.

You can also run the included example:

```bash
uv run python examples/use_encriptador_core.py
```

## Using the Password Vault

The `password_vault` component implements a local encrypted vault, protected by a master password.

### Cryptographic Flow

1. The user enters a **master password**.
2. A binary key is derived using **PBKDF2-HMAC-SHA256** with a salt and a large number of iterations.
3. This derived key is transformed into a valid Fernet key (32 bytes encoded in base64 URL-safe).
4. An instance of `Encriptador` is created with this key.
5. The vault contents (list of entries) are serialized as JSON and encrypted with Fernet before being written to disk.

### CLI

Run the example CLI:

```bash
uv run python examples/usar_password_vault.py
```

Basic options:

- **List entries** in the vault.
- **Add new entries** with service, username, password, and notes.

The vault file path and salt path are managed in code and can be adjusted according to the environment or deployment preferences.

--

## Tests

To run all tests:

```bash
uv run python -m pytest
```

The following are covered:

- Basic encryption and decryption of the `Encriptador`.

- Fundamental vault operations (adding and listing entries).

This allows you to validate the core behavior before extending functionality.

--

## Design Decisions

- **Fernet as an encryption scheme**
  - Offers high-level, authenticated, and easy-to-use symmetric encryption in Python.
  - Avoids common errors in manual AES implementations (IV, padding, MAC, etc.).

- **KDF based on PBKDF2**
  - Uses multiple iterations to make offline attacks on the master password costly.
  - KDF is separate from the encryption, facilitating future replacement with Argon2 or scrypt if further hardening of the scheme is desired.

- **Separation between core and vault**
  - The encryption module (`encriptador_core`) is context-agnostic.
  - The vault (`password_vault`) encapsulates the data model, file format, and CLI UX decisions.

---

## Roadmap (vision)

Some natural lines of project evolution:

- Integrate a TUI/GUI to manage the vault more user-friendly. - Add search, filtering, and tags for entries.
- Support for various storage backends (local file, Git repositories, WebDAV, etc.).
- Explore more advanced KDFs (Argon2id, scrypt) and dynamic parameter configuration.
- Extended documentation and additional integration examples for other projects.

---

## License

This project is distributed under the **MIT** license.

The MIT license is permissive and allows you to use, modify, and distribute the code in both personal and commercial projects, encouraging collaboration and adoption within the community.
