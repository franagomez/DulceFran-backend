# DulceFran - Backend (Parcial 3, DSY1104)

API en **FastAPI** para la tienda DulceFran. Reemplaza los datos que antes
vivían en `localStorage` (productos, usuarias, mensajes) por una base de
datos real (`dulcefran.db`, SQLite), con login y permisos por rol usando
**JWT**.

## Cómo levantarla (primera vez)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Cargar datos iniciales (mismo catálogo y las mismas 2 cuentas de prueba
#    que ya tenías en productos.js / usuarios.js)
python seed.py

# 3. Levantar el servidor
uvicorn main:app --reload
```

Después de eso:

- **Swagger (documentación interactiva):** http://127.0.0.1:8000/docs
- **API:** http://127.0.0.1:8000

Las siguientes veces solo necesitas el paso 3 (`uvicorn main:app --reload`).
No vuelvas a correr `seed.py` salvo que borres `dulcefran.db` — si la base
ya tiene datos, el script no duplica nada.

## Cuentas de prueba

| Correo | Contraseña | Rol |
|---|---|---|
| panchita@gmail.com | admin123 | Administrador |
| repostera@gmail.com | vende123 | Vendedor |

También puedes crear una cuenta de Cliente nueva con `POST /auth/registro`.

## Endpoints

| Método | Ruta | Quién puede | Qué hace |
|---|---|---|---|
| POST | `/auth/login` | Cualquiera | Devuelve un JWT + los datos de la usuaria |
| POST | `/auth/registro` | Cualquiera | Crea una cuenta nueva (rol Cliente) |
| GET | `/productos/` | Cualquiera | Lista el catálogo |
| GET | `/productos/{codigo}` | Cualquiera | Un producto |
| POST | `/productos/` | Administrador, Vendedor | Crear producto |
| PUT | `/productos/{codigo}` | Administrador, Vendedor | Editar producto |
| DELETE | `/productos/{codigo}` | Administrador, Vendedor | Eliminar producto |
| GET/POST/PUT/DELETE | `/usuarios/...` | Solo Administrador | CRUD de usuarias |
| POST | `/mensajes/` | Cualquiera | Enviar mensaje desde el formulario de Contacto |
| GET | `/mensajes/` | Administrador, Vendedor | Leer los mensajes recibidos |

## Cómo se protege cada ruta (JWT)

1. `POST /auth/login` valida correo+contraseña y devuelve un `token`.
2. El frontend guarda ese token y lo manda en cada petición protegida como
   header: `Authorization: Bearer <token>`.
3. Cada ruta protegida usa `seguridad.requiere_rol(...)` como dependencia de
   FastAPI — valida el token y el rol *antes* de ejecutar la función. Si
   falta el token o es inválido: `401`. Si el rol no tiene permiso: `403`.

Para probar una ruta protegida desde Swagger: botón **Authorize** (arriba a
la derecha) → pega el `token` que te devolvió `/auth/login` (sin la palabra
"Bearer") → Authorize.

## Estructura

```
main.py          -> arma la app, CORS, conecta las rutas
database.py      -> configuración de SQLite/SQLAlchemy
models.py        -> tablas (Producto, Usuario, MensajeContacto)
schemas.py       -> formas de entrada/salida (Pydantic)
seguridad.py      -> hash de contraseñas + creación/validación de JWT
seed.py           -> carga los datos iniciales
routes/
  auth.py         -> login, registro
  productos.py     -> CRUD productos
  usuarios.py      -> CRUD usuarias (solo admin)
  mensajes.py      -> mensajes de contacto
```

## Siguiente paso: conectar con el frontend React

Falta reemplazar en DulceFran (React) las funciones de `src/data/*.js` que
leen/escriben `localStorage` por llamadas `fetch`/`axios` a esta API, y
guardar el `token` del login en `localStorage` o `sessionStorage` para
mandarlo en cada petición protegida. Eso se ve en la siguiente sesión.
