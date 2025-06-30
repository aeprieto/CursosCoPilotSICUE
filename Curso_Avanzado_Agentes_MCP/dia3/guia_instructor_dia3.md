# Día 3: Desarrollo de Servidores MCP

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---|---|---|---|---|
| 09:00-09:15 | Repaso y verificación servidores día 2 | 15min | Verificación | `repaso_dia2.md` |
| 09:15-11:15 | Servidores MCP con bases de datos y herramientas avanzadas | 2h | Práctico | `servidores_bd_reales.md` |
| 11:15-11:45 | **PAUSA - CAFÉ** | 30min | - | - |
| 11:45-14:00 | Taller: Servidor MCP Universitario y gestión de recursos | 2.25h | Práctico | `servidor_universitario_completo.md` |

## 🎯 Objetivos del Día

1.  ✅ **Desarrollar servidores MCP** con integración real a bases de datos
2.  ✅ **Implementar herramientas avanzadas** (CRUD, búsqueda, análisis)
3.  ✅ **Gestionar recursos** de forma eficiente con caching
4.  ✅ **Crear servidor universitario** completo y funcional
5.  ✅ **Aplicar buenas prácticas** de desarrollo y seguridad

## 💻 Stack Técnico Avanzado

```bash
# Bases de datos y ORMs
pip install sqlalchemy alembic psycopg2-binary
pip install asyncpg # Para PostgreSQL asíncrono

# Caching y performance
pip install redis aioredis
pip install cachetools

# Validación y serialización
pip install pydantic
pip install marshmallow

# Autenticación y seguridad
pip install python-jose[cryptography]
pip install passlib[bcrypt]

# Monitorización
pip install prometheus-client
pip install structlog
```

## 🏗️ Arquitectura Avanzada MCP

### Servidor MCP Empresarial

```python
"""
Servidor MCP Avanzado para Universidad
Incluye: BD real, caching, autenticación, logging
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

# Core MCP
from mcp import Server, StdioServerTransport
from mcp.types import *

# Base de datos
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_, or_

# Caching
import aioredis
from cachetools import TTLCache

# Modelos de datos
from pydantic import BaseModel, Field
from datetime import datetime

# Configuración
from dataclasses import dataclass

# Configuración del servidor
@dataclass
class MCPConfig:
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/university")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    cache_ttl: int = int(os.getenv("CACHE_TTL", "300")) # 5 minutos
    max_cache_size: int = int(os.getenv("MAX_CACHE_SIZE", "1000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

# Modelos Pydantic para validación
class StudentModel(BaseModel):
    id: str
    name: str
    email: str
    department: str

## ✅ Finalización del curso

La finalización del curso se basa en la **asistencia**. No hay evaluación formal ni entrega de proyectos. El objetivo es **aprender haciendo** en un entorno práctico y colaborativo.
