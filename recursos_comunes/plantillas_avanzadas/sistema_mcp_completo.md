# Plantillas Avanzadas para Desarrollo de Agentes MCP

## Servidor MCP Base

### Estructura de Proyecto
```
mcp-server/
├── src/
│   ├── server.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── database_tools.py
│   │   └── api_tools.py
│   ├── resources/
│   │   ├── __init__.py
│   │   └── academic_resources.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── tests/
│   ├── test_server.py
│   └── test_tools.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Servidor MCP Básico
```python
# src/server.py
import asyncio
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    ReadResourceRequest,
    ReadResourceResult,
    Tool,
    Resource,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversityMCPServer:
    def __init__(self):
        self.server = Server("university-mcp-server")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configura los handlers del servidor MCP"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """Lista todas las herramientas disponibles"""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="search_courses",
                        description="Busca cursos en el catálogo académico",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Término de búsqueda"
                                },
                                "department": {
                                    "type": "string",
                                    "description": "Departamento específico"
                                },
                                "semester": {
                                    "type": "string",
                                    "description": "Semestre (ej: 2024-1)"
                                }
                            },
                            "required": ["query"]
                        }
                    ),
                    Tool(
                        name="get_student_info",
                        description="Obtiene información del estudiante",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "student_id": {
                                    "type": "string",
                                    "description": "ID del estudiante"
                                }
                            },
                            "required": ["student_id"]
                        }
                    ),
                    Tool(
                        name="reserve_resource",
                        description="Reserva un recurso universitario",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "resource_id": {
                                    "type": "string",
                                    "description": "ID del recurso"
                                },
                                "start_time": {
                                    "type": "string",
                                    "description": "Hora de inicio (ISO 8601)"
                                },
                                "end_time": {
                                    "type": "string",
                                    "description": "Hora de fin (ISO 8601)"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "ID del usuario"
                                }
                            },
                            "required": ["resource_id", "start_time", "end_time", "user_id"]
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> CallToolResult:
            """Maneja las llamadas a herramientas"""
            
            if name == "search_courses":
                return await self.search_courses(arguments)
            elif name == "get_student_info":
                return await self.get_student_info(arguments)
            elif name == "reserve_resource":
                return await self.reserve_resource(arguments)
            else:
                raise ValueError(f"Herramienta desconocida: {name}")
        
        @self.server.list_resources()
        async def handle_list_resources() -> ListResourcesResult:
            """Lista todos los recursos disponibles"""
            return ListResourcesResult(
                resources=[
                    Resource(
                        uri="university://academic-calendar",
                        name="Calendario Académico",
                        description="Calendario con fechas importantes del semestre",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="university://course-catalog",
                        name="Catálogo de Cursos",
                        description="Catálogo completo de cursos disponibles",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="university://facilities",
                        name="Instalaciones",
                        description="Información sobre instalaciones y recursos",
                        mimeType="application/json"
                    )
                ]
            )
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Lee el contenido de un recurso específico"""
            
            if uri == "university://academic-calendar":
                return await self.read_academic_calendar()
            elif uri == "university://course-catalog":
                return await self.read_course_catalog()
            elif uri == "university://facilities":
                return await self.read_facilities()
            else:
                raise ValueError(f"Recurso desconocido: {uri}")
    
    async def search_courses(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Implementa la búsqueda de cursos"""
        query = arguments.get("query", "")
        department = arguments.get("department")
        semester = arguments.get("semester")
        
        # Aquí iría la lógica real de búsqueda
        # Por ahora, retornamos datos simulados
        results = [
            {
                "code": "CS101",
                "name": "Introducción a la Programación",
                "department": "Ciencias de la Computación",
                "credits": 4,
                "professor": "Dr. García",
                "schedule": "Lun/Mié/Vie 10:00-11:00"
            },
            {
                "code": "CS201",
                "name": "Estructuras de Datos",
                "department": "Ciencias de la Computación",
                "credits": 4,
                "professor": "Dra. Rodríguez",
                "schedule": "Mar/Jue 14:00-15:30"
            }
        ]
        
        # Filtrar por departamento si se especifica
        if department:
            results = [r for r in results if department.lower() in r["department"].lower()]
        
        # Filtrar por query
        if query:
            results = [r for r in results if query.lower() in r["name"].lower() or query.lower() in r["code"].lower()]
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Encontrados {len(results)} cursos:\n\n" + 
                         "\n".join([
                             f"• {r['code']}: {r['name']}\n"
                             f"  Profesor: {r['professor']}\n"
                             f"  Horario: {r['schedule']}\n"
                             f"  Créditos: {r['credits']}\n"
                             for r in results
                         ])
                )
            ]
        )
    
    async def get_student_info(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Obtiene información del estudiante"""
        student_id = arguments.get("student_id")
        
        # Simulación de datos del estudiante
        student_data = {
            "id": student_id,
            "name": "Juan Pérez",
            "email": "juan.perez@universidad.edu",
            "program": "Ingeniería de Sistemas",
            "semester": 6,
            "gpa": 3.8,
            "credits_completed": 120,
            "status": "Activo"
        }
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Información del Estudiante {student_id}:\n\n"
                         f"Nombre: {student_data['name']}\n"
                         f"Email: {student_data['email']}\n"
                         f"Programa: {student_data['program']}\n"
                         f"Semestre: {student_data['semester']}\n"
                         f"GPA: {student_data['gpa']}\n"
                         f"Créditos Completados: {student_data['credits_completed']}\n"
                         f"Estado: {student_data['status']}"
                )
            ]
        )
    
    async def reserve_resource(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Reserva un recurso universitario"""
        resource_id = arguments.get("resource_id")
        start_time = arguments.get("start_time")
        end_time = arguments.get("end_time")
        user_id = arguments.get("user_id")
        
        # Simulación de reserva
        reservation_id = f"RES_{resource_id}_{user_id}_{start_time[:10]}"
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Reserva creada exitosamente:\n\n"
                         f"ID de Reserva: {reservation_id}\n"
                         f"Recurso: {resource_id}\n"
                         f"Usuario: {user_id}\n"
                         f"Inicio: {start_time}\n"
                         f"Fin: {end_time}\n\n"
                         f"Estado: Confirmada"
                )
            ]
        )
    
    async def read_academic_calendar(self) -> ReadResourceResult:
        """Lee el calendario académico"""
        calendar_data = {
            "semester": "2024-1",
            "important_dates": [
                {"date": "2024-01-15", "event": "Inicio de clases"},
                {"date": "2024-03-25", "event": "Semana Santa"},
                {"date": "2024-05-20", "event": "Fin de clases"},
                {"date": "2024-05-27", "event": "Exámenes finales"},
                {"date": "2024-06-03", "event": "Fin del semestre"}
            ]
        }
        
        return ReadResourceResult(
            contents=[
                TextContent(
                    type="text",
                    text=f"Calendario Académico {calendar_data['semester']}:\n\n" +
                         "\n".join([
                             f"• {event['date']}: {event['event']}"
                             for event in calendar_data['important_dates']
                         ])
                )
            ]
        )
    
    async def read_course_catalog(self) -> ReadResourceResult:
        """Lee el catálogo de cursos"""
        catalog_data = {
            "total_courses": 250,
            "departments": [
                "Ciencias de la Computación",
                "Ingeniería",
                "Matemáticas",
                "Física",
                "Química"
            ],
            "featured_courses": [
                {
                    "code": "CS101",
                    "name": "Introducción a la Programación",
                    "description": "Conceptos fundamentales de programación"
                },
                {
                    "code": "ENG201",
                    "name": "Circuitos Eléctricos",
                    "description": "Análisis de circuitos básicos"
                }
            ]
        }
        
        return ReadResourceResult(
            contents=[
                TextContent(
                    type="text",
                    text=f"Catálogo de Cursos:\n\n"
                         f"Total de cursos: {catalog_data['total_courses']}\n"
                         f"Departamentos: {', '.join(catalog_data['departments'])}\n\n"
                         f"Cursos destacados:\n" +
                         "\n".join([
                             f"• {course['code']}: {course['name']}\n"
                             f"  {course['description']}\n"
                             for course in catalog_data['featured_courses']
                         ])
                )
            ]
        )
    
    async def read_facilities(self) -> ReadResourceResult:
        """Lee información de instalaciones"""
        facilities_data = {
            "laboratories": [
                {"id": "LAB001", "name": "Laboratorio de Computación 1", "capacity": 30},
                {"id": "LAB002", "name": "Laboratorio de Física", "capacity": 20},
                {"id": "LAB003", "name": "Laboratorio de Química", "capacity": 25}
            ],
            "classrooms": [
                {"id": "AULA101", "name": "Aula Magna", "capacity": 200},
                {"id": "AULA201", "name": "Aula 201", "capacity": 50},
                {"id": "AULA301", "name": "Aula 301", "capacity": 40}
            ]
        }
        
        return ReadResourceResult(
            contents=[
                TextContent(
                    type="text",
                    text="Instalaciones Disponibles:\n\n"
                         "Laboratorios:\n" +
                         "\n".join([
                             f"• {lab['id']}: {lab['name']} (Capacidad: {lab['capacity']})"
                             for lab in facilities_data['laboratories']
                         ]) +
                         "\n\nAulas:\n" +
                         "\n".join([
                             f"• {room['id']}: {room['name']} (Capacidad: {room['capacity']})"
                             for room in facilities_data['classrooms']
                         ])
                )
            ]
        )
    
    async def run(self):
        """Ejecuta el servidor MCP"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, 
                write_stream, 
                InitializationOptions(
                    server_name="university-mcp-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities()
                )
            )

# Punto de entrada principal
async def main():
    server = UniversityMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Archivo de Configuración
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "university-mcp-server"
version = "1.0.0"
description = "Servidor MCP para sistema universitario"
authors = [
    {name = "Universidad", email = "admin@universidad.edu"}
]
dependencies = [
    "mcp>=1.0.0",
    "pydantic>=2.0.0",
    "asyncio",
    "python-dotenv",
    "sqlalchemy>=2.0.0",
    "aiosqlite"
]
requires-python = ">=3.9"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio",
    "black",
    "flake8",
    "mypy"
]

[tool.setuptools]
packages = ["src"]

[tool.black]
line-length = 88
target-version = ['py39']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
```

### Tests de Ejemplo
```python
# tests/test_server.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.server import UniversityMCPServer

class TestUniversityMCPServer:
    @pytest.fixture
    def server(self):
        return UniversityMCPServer()
    
    @pytest.mark.asyncio
    async def test_search_courses_basic(self, server):
        """Test búsqueda básica de cursos"""
        arguments = {"query": "programación"}
        result = await server.search_courses(arguments)
        
        assert result.content is not None
        assert len(result.content) > 0
        assert "CS101" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_get_student_info(self, server):
        """Test obtención de información del estudiante"""
        arguments = {"student_id": "123456"}
        result = await server.get_student_info(arguments)
        
        assert result.content is not None
        assert "Juan Pérez" in result.content[0].text
        assert "123456" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_reserve_resource(self, server):
        """Test reserva de recurso"""
        arguments = {
            "resource_id": "LAB001",
            "start_time": "2024-03-15T10:00:00",
            "end_time": "2024-03-15T12:00:00",
            "user_id": "user123"
        }
        result = await server.reserve_resource(arguments)
        
        assert result.content is not None
        assert "RES_LAB001_user123_2024-03-15" in result.content[0].text
        assert "Confirmada" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_read_academic_calendar(self, server):
        """Test lectura del calendario académico"""
        result = await server.read_academic_calendar()
        
        assert result.contents is not None
        assert len(result.contents) > 0
        assert "2024-1" in result.contents[0].text
        assert "Inicio de clases" in result.contents[0].text
```

## Agente Cliente MCP

### Cliente MCP Base
```python
# client/mcp_client.py
import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class UniversityMCPClient:
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.session: Optional[ClientSession] = None
    
    async def connect(self):
        """Conecta al servidor MCP"""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        
        self.session = await stdio_client(server_params)
        await self.session.initialize()
    
    async def disconnect(self):
        """Desconecta del servidor MCP"""
        if self.session:
            await self.session.close()
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Lista todas las herramientas disponibles"""
        if not self.session:
            await self.connect()
        
        result = await self.session.list_tools()
        return [tool.model_dump() for tool in result.tools]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Llama a una herramienta específica"""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(name, arguments)
        return {
            "content": [content.model_dump() for content in result.content],
            "isError": result.isError
        }
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """Lista todos los recursos disponibles"""
        if not self.session:
            await self.connect()
        
        result = await self.session.list_resources()
        return [resource.model_dump() for resource in result.resources]
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Lee un recurso específico"""
        if not self.session:
            await self.connect()
        
        result = await self.session.read_resource(uri)
        return {
            "contents": [content.model_dump() for content in result.contents]
        }

# Ejemplo de uso del cliente
class UniversityAssistant:
    def __init__(self, mcp_client: UniversityMCPClient):
        self.mcp_client = mcp_client
    
    async def search_courses_for_student(self, query: str, department: Optional[str] = None):
        """Busca cursos para un estudiante"""
        arguments = {"query": query}
        if department:
            arguments["department"] = department
        
        result = await self.mcp_client.call_tool("search_courses", arguments)
        return result
    
    async def get_student_schedule(self, student_id: str):
        """Obtiene el horario de un estudiante"""
        # Primero obtener info del estudiante
        student_info = await self.mcp_client.call_tool(
            "get_student_info", 
            {"student_id": student_id}
        )
        
        # Luego buscar sus cursos actuales
        # (esto requeriría una herramienta adicional en el servidor)
        return {
            "student_info": student_info,
            "schedule": "Horario no disponible aún"
        }
    
    async def make_room_reservation(self, user_id: str, room_id: str, start_time: str, end_time: str):
        """Hace una reserva de sala"""
        arguments = {
            "resource_id": room_id,
            "start_time": start_time,
            "end_time": end_time,
            "user_id": user_id
        }
        
        result = await self.mcp_client.call_tool("reserve_resource", arguments)
        return result
    
    async def get_academic_calendar(self):
        """Obtiene el calendario académico"""
        result = await self.mcp_client.read_resource("university://academic-calendar")
        return result

# Ejemplo de uso
async def main():
    # Crear cliente MCP
    client = UniversityMCPClient("../server/src/server.py")
    
    # Crear asistente
    assistant = UniversityAssistant(client)
    
    try:
        # Buscar cursos
        courses = await assistant.search_courses_for_student("programación")
        print("Cursos encontrados:", courses)
        
        # Obtener calendario
        calendar = await assistant.get_academic_calendar()
        print("Calendario académico:", calendar)
        
        # Hacer reserva
        reservation = await assistant.make_room_reservation(
            "user123", "AULA101", "2024-03-15T10:00:00", "2024-03-15T12:00:00"
        )
        print("Reserva realizada:", reservation)
        
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Sistema Multi-Agente

### Orquestador de Agentes
```python
# orchestrator/agent_orchestrator.py
import asyncio
import logging
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class AgentType(Enum):
    ACADEMIC_SUPPORT = "academic_support"
    RESOURCE_MANAGEMENT = "resource_management"
    STUDENT_SERVICES = "student_services"
    TECHNICAL_SUPPORT = "technical_support"

@dataclass
class AgentCapability:
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]

@dataclass
class AgentInfo:
    id: str
    type: AgentType
    name: str
    capabilities: List[AgentCapability]
    mcp_client: Any
    status: str = "active"
    last_heartbeat: datetime = None

class AgentOrchestrator:
    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}
        self.routing_rules: Dict[str, List[str]] = {}
        self.logger = logging.getLogger(__name__)
    
    async def register_agent(self, agent_info: AgentInfo):
        """Registra un nuevo agente en el orquestador"""
        self.agents[agent_info.id] = agent_info
        self.logger.info(f"Agente registrado: {agent_info.id} ({agent_info.type.value})")
    
    async def unregister_agent(self, agent_id: str):
        """Desregistra un agente"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.logger.info(f"Agente desregistrado: {agent_id}")
    
    async def route_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Rutea una solicitud al agente apropiado"""
        intent = await self.classify_intent(request)
        suitable_agents = await self.find_suitable_agents(intent)
        
        if not suitable_agents:
            return {
                "error": "No se encontró un agente adecuado",
                "intent": intent
            }
        
        # Seleccionar el mejor agente
        selected_agent = await self.select_best_agent(suitable_agents, request)
        
        # Ejecutar la solicitud
        try:
            result = await self.execute_request(selected_agent, request)
            return {
                "success": True,
                "result": result,
                "agent_used": selected_agent.id
            }
        except Exception as e:
            self.logger.error(f"Error ejecutando solicitud: {e}")
            return {
                "error": str(e),
                "agent_used": selected_agent.id
            }
    
    async def classify_intent(self, request: Dict[str, Any]) -> str:
        """Clasifica la intención de la solicitud"""
        text = request.get("text", "").lower()
        
        # Clasificación simple basada en palabras clave
        if any(word in text for word in ["curso", "materia", "horario", "profesor"]):
            return "academic_query"
        elif any(word in text for word in ["reservar", "sala", "laboratorio", "aula"]):
            return "resource_reservation"
        elif any(word in text for word in ["matrícula", "inscripción", "certificado"]):
            return "student_services"
        elif any(word in text for word in ["problema", "error", "ayuda técnica"]):
            return "technical_support"
        else:
            return "general_query"
    
    async def find_suitable_agents(self, intent: str) -> List[AgentInfo]:
        """Encuentra agentes adecuados para una intención"""
        intent_to_agent_type = {
            "academic_query": AgentType.ACADEMIC_SUPPORT,
            "resource_reservation": AgentType.RESOURCE_MANAGEMENT,
            "student_services": AgentType.STUDENT_SERVICES,
            "technical_support": AgentType.TECHNICAL_SUPPORT
        }
        
        target_type = intent_to_agent_type.get(intent)
        if not target_type:
            # Para consultas generales, devolver todos los agentes activos
            return [agent for agent in self.agents.values() if agent.status == "active"]
        
        return [
            agent for agent in self.agents.values() 
            if agent.type == target_type and agent.status == "active"
        ]
    
    async def select_best_agent(self, agents: List[AgentInfo], request: Dict[str, Any]) -> AgentInfo:
        """Selecciona el mejor agente para una solicitud"""
        # Por ahora, selecciona el primero disponible
        # En una implementación real, consideraría carga, performance, etc.
        return agents[0]
    
    async def execute_request(self, agent: AgentInfo, request: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta una solicitud en un agente específico"""
        # Determinar qué herramienta usar basado en el request
        tool_name = await self.determine_tool(agent, request)
        
        # Preparar argumentos
        arguments = await self.prepare_arguments(request, tool_name)
        
        # Llamar al agente
        result = await agent.mcp_client.call_tool(tool_name, arguments)
        
        return result
    
    async def determine_tool(self, agent: AgentInfo, request: Dict[str, Any]) -> str:
        """Determina qué herramienta usar para una solicitud"""
        # Lógica simplificada
        if agent.type == AgentType.ACADEMIC_SUPPORT:
            return "search_courses"
        elif agent.type == AgentType.RESOURCE_MANAGEMENT:
            return "reserve_resource"
        elif agent.type == AgentType.STUDENT_SERVICES:
            return "get_student_info"
        else:
            return "general_query"
    
    async def prepare_arguments(self, request: Dict[str, Any], tool_name: str) -> Dict[str, Any]:
        """Prepara los argumentos para una herramienta"""
        if tool_name == "search_courses":
            return {"query": request.get("text", "")}
        elif tool_name == "get_student_info":
            return {"student_id": request.get("student_id", "")}
        elif tool_name == "reserve_resource":
            return {
                "resource_id": request.get("resource_id", ""),
                "start_time": request.get("start_time", ""),
                "end_time": request.get("end_time", ""),
                "user_id": request.get("user_id", "")
            }
        else:
            return {}
    
    async def health_check(self) -> Dict[str, Any]:
        """Verifica el estado de todos los agentes"""
        health_status = {}
        
        for agent_id, agent in self.agents.items():
            try:
                # Intentar una operación simple
                tools = await agent.mcp_client.list_tools()
                health_status[agent_id] = {
                    "status": "healthy",
                    "tools_count": len(tools),
                    "last_check": datetime.now().isoformat()
                }
            except Exception as e:
                health_status[agent_id] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
        
        return health_status
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas del sistema"""
        return {
            "total_agents": len(self.agents),
            "active_agents": len([a for a in self.agents.values() if a.status == "active"]),
            "agents_by_type": {
                agent_type.value: len([a for a in self.agents.values() if a.type == agent_type])
                for agent_type in AgentType
            },
            "last_updated": datetime.now().isoformat()
        }

# Ejemplo de uso del orquestador
async def setup_orchestrator():
    """Configura el orquestador con agentes"""
    orchestrator = AgentOrchestrator()
    
    # Simular registro de agentes
    from ..client.mcp_client import UniversityMCPClient
    
    # Agente de soporte académico
    academic_client = UniversityMCPClient("../server/src/server.py")
    await academic_client.connect()
    
    academic_agent = AgentInfo(
        id="academic_agent_001",
        type=AgentType.ACADEMIC_SUPPORT,
        name="Asistente Académico",
        capabilities=[
            AgentCapability(
                name="search_courses",
                description="Busca cursos en el catálogo",
                input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
                output_schema={"type": "object"}
            )
        ],
        mcp_client=academic_client
    )
    
    await orchestrator.register_agent(academic_agent)
    
    return orchestrator

# Función de prueba
async def test_orchestrator():
    orchestrator = await setup_orchestrator()
    
    # Probar ruteo de solicitudes
    academic_request = {
        "text": "Busco cursos de programación",
        "user_id": "student123"
    }
    
    result = await orchestrator.route_request(academic_request)
    print("Resultado de solicitud académica:", result)
    
    # Verificar salud del sistema
    health = await orchestrator.health_check()
    print("Estado de salud:", health)
    
    # Obtener métricas
    metrics = await orchestrator.get_system_metrics()
    print("Métricas del sistema:", metrics)

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
```

## Configuración de Despliegue

### Docker Compose para Producción
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Servidor MCP Principal
  mcp-server:
    build:
      context: ./server
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://mcpuser:mcppass@postgres:5432/mcpdb
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=info
    ports:
      - "8001:8000"
    depends_on:
      - postgres
      - redis
    networks:
      - mcp-network
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Orquestador de Agentes
  agent-orchestrator:
    build:
      context: ./orchestrator
      dockerfile: Dockerfile
    environment:
      - MCP_SERVER_URL=http://mcp-server:8000
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=info
    ports:
      - "8002:8000"
    depends_on:
      - mcp-server
      - redis
    networks:
      - mcp-network
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  # Agente de Soporte Académico
  academic-agent:
    build:
      context: ./agents/academic
      dockerfile: Dockerfile
    environment:
      - MCP_SERVER_URL=http://mcp-server:8000
      - ORCHESTRATOR_URL=http://agent-orchestrator:8000
      - DATABASE_URL=postgresql://mcpuser:mcppass@postgres:5432/mcpdb
    depends_on:
      - mcp-server
      - agent-orchestrator
    networks:
      - mcp-network
    restart: unless-stopped

  # Agente de Gestión de Recursos
  resource-agent:
    build:
      context: ./agents/resources
      dockerfile: Dockerfile
    environment:
      - MCP_SERVER_URL=http://mcp-server:8000
      - ORCHESTRATOR_URL=http://agent-orchestrator:8000
      - DATABASE_URL=postgresql://mcpuser:mcppass@postgres:5432/mcpdb
    depends_on:
      - mcp-server
      - agent-orchestrator
    networks:
      - mcp-network
    restart: unless-stopped

  # Base de Datos
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mcpdb
      - POSTGRES_USER=mcpuser
      - POSTGRES_PASSWORD=mcppass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - mcp-network
    restart: unless-stopped

  # Cache Redis
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - mcp-network
    restart: unless-stopped

  # Monitorización
  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    networks:
      - mcp-network
    restart: unless-stopped

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - mcp-network
    restart: unless-stopped

  # Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - mcp-server
      - agent-orchestrator
      - grafana
    networks:
      - mcp-network
    restart: unless-stopped

networks:
  mcp-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  grafana_data:
  prometheus_data:
```

### Configuración de Monitorización
```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, start_http_server
import time
import logging
from functools import wraps

# Métricas personalizadas
REGISTRY = CollectorRegistry()

# Contadores
REQUEST_COUNT = Counter(
    'mcp_requests_total',
    'Total de solicitudes MCP',
    ['agent_type', 'tool_name', 'status'],
    registry=REGISTRY
)

# Histogramas para tiempo de respuesta
REQUEST_DURATION = Histogram(
    'mcp_request_duration_seconds',
    'Duración de las solicitudes MCP',
    ['agent_type', 'tool_name'],
    registry=REGISTRY
)

# Gauges para métricas de sistema
ACTIVE_AGENTS = Gauge(
    'mcp_active_agents',
    'Número de agentes activos',
    ['agent_type'],
    registry=REGISTRY
)

SYSTEM_HEALTH = Gauge(
    'mcp_system_health',
    'Estado de salud del sistema (1=saludable, 0=no saludable)',
    registry=REGISTRY
)

class MetricsCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def track_request(self, agent_type: str, tool_name: str, status: str):
        """Rastrea una solicitud"""
        REQUEST_COUNT.labels(
            agent_type=agent_type,
            tool_name=tool_name,
            status=status
        ).inc()
    
    def track_duration(self, agent_type: str, tool_name: str, duration: float):
        """Rastrea la duración de una solicitud"""
        REQUEST_DURATION.labels(
            agent_type=agent_type,
            tool_name=tool_name
        ).observe(duration)
    
    def update_active_agents(self, agent_type: str, count: int):
        """Actualiza el número de agentes activos"""
        ACTIVE_AGENTS.labels(agent_type=agent_type).set(count)
    
    def update_system_health(self, is_healthy: bool):
        """Actualiza el estado de salud del sistema"""
        SYSTEM_HEALTH.set(1 if is_healthy else 0)

# Decorador para métricas automáticas
def track_metrics(agent_type: str, tool_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "success"
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                raise e
            finally:
                duration = time.time() - start_time
                
                # Registrar métricas
                metrics = MetricsCollector()
                metrics.track_request(agent_type, tool_name, status)
                metrics.track_duration(agent_type, tool_name, duration)
        
        return wrapper
    return decorator

# Ejemplo de uso
class MonitoredMCPAgent:
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.metrics = MetricsCollector()
    
    @track_metrics("academic", "search_courses")
    async def search_courses(self, query: str):
        # Simular trabajo
        await asyncio.sleep(0.1)
        return f"Cursos para: {query}"
    
    @track_metrics("resource", "reserve_room")
    async def reserve_room(self, room_id: str):
        # Simular trabajo
        await asyncio.sleep(0.2)
        return f"Reserva para: {room_id}"

# Servidor de métricas
def start_metrics_server(port: int = 8000):
    """Inicia el servidor de métricas de Prometheus"""
    start_http_server(port, registry=REGISTRY)
    logging.info(f"Servidor de métricas iniciado en puerto {port}")
```

### Scripts de Utilidad
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "🚀 Iniciando despliegue del sistema MCP..."

# Verificar dependencias
echo "📋 Verificando dependencias..."
command -v docker >/dev/null 2>&1 || { echo "❌ Docker no está instalado"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose no está instalado"; exit 1; }

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p logs
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/prometheus
mkdir -p nginx/ssl

# Generar certificados SSL si no existen
if [ ! -f nginx/ssl/server.crt ]; then
    echo "🔐 Generando certificados SSL..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/server.key \
        -out nginx/ssl/server.crt \
        -subj "/C=CO/ST=Bogota/L=Bogota/O=Universidad/CN=localhost"
fi

# Construir imágenes
echo "🏗️ Construyendo imágenes Docker..."
docker-compose -f docker-compose.prod.yml build

# Iniciar servicios
echo "▶️ Iniciando servicios..."
docker-compose -f docker-compose.prod.yml up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
echo "✅ Verificando estado de los servicios..."
docker-compose -f docker-compose.prod.yml ps

# Ejecutar pruebas de salud
echo "🔍 Ejecutando pruebas de salud..."
curl -f http://localhost:8001/health || echo "⚠️ MCP Server no responde"
curl -f http://localhost:8002/health || echo "⚠️ Orchestrator no responde"
curl -f http://localhost:3000/api/health || echo "⚠️ Grafana no responde"

echo "✅ Despliegue completado!"
echo "📊 Grafana: http://localhost:3000 (admin/admin123)"
echo "📈 Prometheus: http://localhost:9090"
echo "🔧 MCP Server: http://localhost:8001"
echo "🎯 Orchestrator: http://localhost:8002"
```

```bash
#!/bin/bash
# scripts/backup.sh

set -e

BACKUP_DIR="/backup/mcp-$(date +%Y%m%d_%H%M%S)"
echo "📦 Creando backup en: $BACKUP_DIR"

# Crear directorio de backup
mkdir -p "$BACKUP_DIR"

# Backup de base de datos
echo "💾 Respaldando base de datos..."
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U mcpuser mcpdb > "$BACKUP_DIR/database.sql"

# Backup de configuraciones
echo "⚙️ Respaldando configuraciones..."
cp -r nginx/ "$BACKUP_DIR/"
cp -r monitoring/ "$BACKUP_DIR/"
cp docker-compose.prod.yml "$BACKUP_DIR/"

# Backup de logs
echo "📄 Respaldando logs..."
cp -r logs/ "$BACKUP_DIR/"

# Crear archivo tar
echo "🗜️ Comprimiendo backup..."
tar -czf "$BACKUP_DIR.tar.gz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"

# Limpiar directorio temporal
rm -rf "$BACKUP_DIR"

echo "✅ Backup completado: $BACKUP_DIR.tar.gz"
```

Estas plantillas proporcionan una base sólida para desarrollar sistemas MCP complejos con capacidades de monitorización, escalabilidad y mantenimiento en producción. Los participantes pueden usar estos ejemplos como punto de partida para sus propios proyectos.
