# Estructura 4: Base de datos

Scripts SQL del sistema **EcoLogística Lima** según la estructura requerida del PFA.

## Contenidos

| Artefacto | Descripción |
| :--- | :--- |
| `esquema.sql` | DDL completo del esquema PostgreSQL (versionado). Generado a partir de los modelos SQLAlchemy. **No editar a mano.** |

## Origen del esquema

El proyecto **no usa migraciones** (no hay Alembic): las tablas se crean al iniciar
la aplicación desde los modelos ORM (`Base.metadata.create_all`, ver
`src/backend/app/core/database.py`). El archivo `esquema.sql` es la representación
SQL versionada de esos mismos modelos, generada con la herramienta de la nota al pie.

Fuentes de la definición de datos:

- Modelos ORM: `src/backend/app/models/__init__.py`
- Diseño e ingeniería de datos: `docs/inicio/11. Base de datos V_1_0_0.md`

> Regenerar después de cambiar `app/models`:
>
> ```bash
> cd src/backend
> python -c "..."   # compila CREATE TABLE de Base.metadata con dialecto postgresql
> ```