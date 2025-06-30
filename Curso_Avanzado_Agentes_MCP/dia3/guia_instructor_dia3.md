# Día 3: Desarrollo de Servidores MCP

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---------|-----------|----------|------|----------|
| 09:00-09:15 | Repaso y verificación servidores día 2 | 15min | Verificación | `repaso_dia2.md` |
| 09:15-10:45 | Servidores MCP con bases de datos reales | 1.5h | Práctico | `servidores_bd_reales.md` |
| 10:45-11:00 | **DESCANSO** | 15min | - | - |
| 11:00-12:30 | Herramientas MCP avanzadas | 1.5h | Práctico | `herramientas_mcp_avanzadas.md` |
| 12:30-13:30 | **ALMUERZO** | 1h | - | - |
| 13:30-15:00 | Gestión de recursos y caching | 1.5h | Técnico | `recursos_caching.md` |
| 15:00-15:15 | **DESCANSO** | 15min | - | - |
| 15:15-16:45 | Proyecto: Servidor MCP Universitario Completo | 1.5h | Proyecto | `servidor_universitario_completo.md` |
| 16:45-17:00 | Demo y preparación día 4 | 15min | Presentación | `demo_dia3.md` |

## 🎯 Objetivos del Día

1. ✅ **Desarrollar servidores MCP** con integración real a bases de datos
2. ✅ **Implementar herramientas avanzadas** (CRUD, búsqueda, análisis)
3. ✅ **Gestionar recursos** de forma eficiente con caching
4. ✅ **Crear servidor universitario** completo y funcional
5. ✅ **Aplicar buenas prácticas** de desarrollo y seguridad

## 💻 Stack Técnico Avanzado

```bash
# Bases de datos y ORMs
pip install sqlalchemy alembic psycopg2-binary
pip install asyncpg  # Para PostgreSQL asíncrono

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
    cache_ttl: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutos
    max_cache_size: int = int(os.getenv("MAX_CACHE_SIZE", "1000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

# Modelos Pydantic para validación
class StudentModel(BaseModel):
    id: str
    name: str
    email: str
    department: str
    year: int
    enrollment_date: datetime
    active: bool = True

class CourseModel(BaseModel):
    code: str
    name: str
    credits: int
    department: str
    professor: Optional[str] = None
    capacity: int
    enrolled: int = 0

class EnrollmentModel(BaseModel):
    student_id: str
    course_code: str
    semester: str
    grade: Optional[float] = None
    enrollment_date: datetime

class AdvancedUniversityMCPServer:
    def __init__(self, config: MCPConfig):
        self.config = config
        self.server = Server("advanced-university-system")
        self.cache = TTLCache(maxsize=config.max_cache_size, ttl=config.cache_ttl)
        self.redis_client = None
        self.db_engine = None
        self.db_session = None
        
        # Configurar logging
        logging.basicConfig(
            level=getattr(logging, config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self._setup_handlers()
    
    async def initialize(self):
        """Inicializar conexiones a BD y Redis"""
        try:
            # Configurar base de datos
            self.db_engine = create_async_engine(
                self.config.database_url,
                echo=True if self.config.log_level == "DEBUG" else False
            )
            self.db_session = sessionmaker(
                self.db_engine, 
                class_=AsyncSession, 
                expire_on_commit=False
            )
            
            # Configurar Redis
            self.redis_client = await aioredis.from_url(self.config.redis_url)
            
            self.logger.info("Servidor MCP inicializado correctamente")
            
        except Exception as e:
            self.logger.error(f"Error inicializando servidor: {e}")
            raise
    
    def _setup_handlers(self):
        """Configurar todos los manejadores MCP"""
        
        @self.server.list_resources()
        async def list_resources() -> ListResourcesResult:
            """Lista recursos universitarios disponibles"""
            return ListResourcesResult(
                resources=[
                    Resource(
                        uri="university://students/all",
                        name="Todos los Estudiantes",
                        description="Lista completa de estudiantes activos",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="university://courses/catalog",
                        name="Catálogo de Cursos",
                        description="Catálogo completo de cursos disponibles",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="university://enrollments/current",
                        name="Matriculaciones Actuales",
                        description="Matriculaciones del semestre actual",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="university://statistics/dashboard",
                        name="Dashboard de Estadísticas",
                        description="Métricas y estadísticas universitarias",
                        mimeType="application/json"
                    )
                ]
            )
        
        @self.server.read_resource()
        async def read_resource(request: ReadResourceRequest) -> ReadResourceResult:
            """Lee recursos específicos con caching"""
            uri = request.uri
            
            # Check cache primero
            cached_result = await self._get_from_cache(uri)
            if cached_result:
                return cached_result
            
            # Generar contenido
            if uri == "university://students/all":
                content = await self._get_all_students()
            elif uri == "university://courses/catalog":
                content = await self._get_course_catalog()
            elif uri == "university://enrollments/current":
                content = await self._get_current_enrollments()
            elif uri == "university://statistics/dashboard":
                content = await self._generate_statistics()
            else:
                raise ValueError(f"Recurso no encontrado: {uri}")
            
            result = ReadResourceResult(
                contents=[TextContent(type="text", text=content)]
            )
            
            # Guardar en cache
            await self._save_to_cache(uri, result)
            
            return result
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """Lista herramientas avanzadas disponibles"""
            return [
                Tool(
                    name="search_students",
                    description="Búsqueda avanzada de estudiantes con filtros múltiples",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Nombre o parte del nombre"},
                            "department": {"type": "string", "description": "Departamento"},
                            "year": {"type": "integer", "description": "Año académico"},
                            "active_only": {"type": "boolean", "default": True},
                            "limit": {"type": "integer", "default": 50}
                        }
                    }
                ),
                Tool(
                    name="create_student",
                    description="Crear nuevo estudiante en el sistema",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "department": {"type": "string"},
                            "year": {"type": "integer"}
                        },
                        "required": ["name", "email", "department", "year"]
                    }
                ),
                Tool(
                    name="enroll_student",
                    description="Matricular estudiante en un curso",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "student_id": {"type": "string"},
                            "course_code": {"type": "string"},
                            "semester": {"type": "string"}
                        },
                        "required": ["student_id", "course_code", "semester"]
                    }
                ),
                Tool(
                    name="analyze_enrollments",
                    description="Análisis avanzado de matriculaciones por departamento",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "department": {"type": "string"},
                            "semester": {"type": "string"},
                            "include_trends": {"type": "boolean", "default": True}
                        }
                    }
                ),
                Tool(
                    name="generate_report",
                    description="Generar reportes personalizados",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["enrollment", "academic", "statistical"]
                            },
                            "format": {
                                "type": "string", 
                                "enum": ["json", "csv", "html"],
                                "default": "json"
                            },
                            "filters": {"type": "object"}
                        },
                        "required": ["type"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(request: CallToolRequest) -> CallToolResult:
            """Ejecuta herramientas con manejo avanzado"""
            tool_name = request.params.name
            arguments = request.params.arguments or {}
            
            try:
                self.logger.info(f"Ejecutando herramienta: {tool_name}")
                
                if tool_name == "search_students":
                    result = await self._search_students_advanced(arguments)
                elif tool_name == "create_student":
                    result = await self._create_student(arguments)
                elif tool_name == "enroll_student":
                    result = await self._enroll_student(arguments)
                elif tool_name == "analyze_enrollments":
                    result = await self._analyze_enrollments(arguments)
                elif tool_name == "generate_report":
                    result = await self._generate_report(arguments)
                else:
                    raise ValueError(f"Herramienta no encontrada: {tool_name}")
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result)]
                )
                
            except Exception as e:
                self.logger.error(f"Error ejecutando {tool_name}: {e}")
                return CallToolResult(
                    content=[TextContent(
                        type="text", 
                        text=f"Error: {str(e)}"
                    )],
                    isError=True
                )
    
    async def _get_from_cache(self, key: str) -> Optional[ReadResourceResult]:
        """Obtener resultado del cache"""
        try:
            if self.redis_client:
                cached = await self.redis_client.get(f"mcp:{key}")
                if cached:
                    import json
                    data = json.loads(cached)
                    return ReadResourceResult(**data)
        except Exception as e:
            self.logger.warning(f"Error accediendo cache: {e}")
        return None
    
    async def _save_to_cache(self, key: str, result: ReadResourceResult):
        """Guardar resultado en cache"""
        try:
            if self.redis_client:
                import json
                data = result.dict()
                await self.redis_client.setex(
                    f"mcp:{key}", 
                    self.config.cache_ttl, 
                    json.dumps(data)
                )
        except Exception as e:
            self.logger.warning(f"Error guardando en cache: {e}")
    
    async def _search_students_advanced(self, args: Dict[str, Any]) -> str:
        """Búsqueda avanzada de estudiantes"""
        async with self.db_session() as session:
            query = select(Student)
            
            # Aplicar filtros
            if args.get("name"):
                query = query.where(Student.name.ilike(f"%{args['name']}%"))
            
            if args.get("department"):
                query = query.where(Student.department == args["department"])
            
            if args.get("year"):
                query = query.where(Student.year == args["year"])
            
            if args.get("active_only", True):
                query = query.where(Student.active == True)
            
            # Limitar resultados
            limit = args.get("limit", 50)
            query = query.limit(limit)
            
            result = await session.execute(query)
            students = result.scalars().all()
            
            return json.dumps([
                StudentModel.from_orm(student).dict() 
                for student in students
            ], indent=2, default=str)
    
    async def _create_student(self, args: Dict[str, Any]) -> str:
        """Crear nuevo estudiante"""
        async with self.db_session() as session:
            # Validar datos
            student_data = StudentModel(**args)
            
            # Crear registro
            new_student = Student(
                id=generate_student_id(),
                **student_data.dict(exclude={"id"})
            )
            
            session.add(new_student)
            await session.commit()
            
            # Invalidar cache
            await self._invalidate_cache_pattern("university://students/*")
            
            return json.dumps({
                "success": True,
                "student_id": new_student.id,
                "message": f"Estudiante {args['name']} creado exitosamente"
            })
    
    async def _generate_report(self, args: Dict[str, Any]) -> str:
        """Generar reportes personalizados"""
        report_type = args["type"]
        format_type = args.get("format", "json")
        filters = args.get("filters", {})
        
        if report_type == "enrollment":
            data = await self._enrollment_report(filters)
        elif report_type == "academic":
            data = await self._academic_report(filters)
        elif report_type == "statistical":
            data = await self._statistical_report(filters)
        
        # Formatear según tipo solicitado
        if format_type == "csv":
            return self._format_as_csv(data)
        elif format_type == "html":
            return self._format_as_html(data)
        else:
            return json.dumps(data, indent=2, default=str)
    
    async def run(self):
        """Ejecutar servidor MCP"""
        await self.initialize()
        transport = StdioServerTransport()
        await self.server.run(transport)

# Configuración y ejecución
async def main():
    config = MCPConfig()
    server = AdvancedUniversityMCPServer(config)
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🎯 Ejercicios del Día

### Ejercicio 1: Integración con Base de Datos Real (60 min)
- Configurar PostgreSQL local
- Crear schema universitario
- Implementar modelos SQLAlchemy
- Probar queries básicas

### Ejercicio 2: Sistema de Caching (45 min)
- Configurar Redis
- Implementar cache para consultas frecuentes
- Estrategias de invalidación
- Monitorizar performance

### Ejercicio 3: Herramientas CRUD Completas (60 min)
- Create: Estudiantes, cursos, matriculaciones
- Read: Búsquedas avanzadas
- Update: Modificación de datos
- Delete: Eliminación segura

### Ejercicio 4: Análisis y Reportes (45 min)
- Generar estadísticas universitarias
- Reportes en múltiples formatos
- Análisis de tendencias
- Exportación de datos

---

**Próximo día**: Integración MCP con Claude Desktop y desarrollo de clientes personalizados
