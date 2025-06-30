# Día 2: Model Context Protocol (MCP) - Fundamentos

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---|---|---|---|---|
| 09:00-09:15 | Repaso arquitecturas del día 1 | 15min | Repaso | `repaso_arquitecturas.md` |
| 09:15-11:15 | Fundamentos de MCP: ¿Qué es y cómo funciona? | 2h | Teórico-Técnico | `introduccion_mcp.md` |
| 11:15-11:45 | **PAUSA - CAFÉ** | 30min | - | - |
| 11:45-14:00 | Taller: Configuración del entorno y primer servidor MCP | 2.25h | Práctico | `primer_servidor_mcp.md` |

## 🎯 Objetivos del Día

Al finalizar el día 2, los participantes podrán:

1.  ✅ **Comprender qué es MCP** y cómo funciona realmente
2.  ✅ **Distinguir MCP** de otros protocolos y APIs
3.  ✅ **Configurar entorno** para desarrollo MCP
4.  ✅ **Implementar servidor MCP** básico funcional
5.  ✅ **Conectar Claude Desktop** con servidor MCP propio

## 📚 Corrección de Conceptos Erróneos

### ❌ **Mito**: MCP = "Multi-Agent Collaboration Patterns"
### ✅ **Realidad**: MCP = **Model Context Protocol**

MCP es un **protocolo estándar** desarrollado por **Anthropic** para permitir que herramientas de IA accedan de forma segura a datos y funcionalidades externas.

### ¿Por qué la Confusión?
- **Nombre similar** a conceptos de multi-agentes
- **Documentación limitada** en español
- **Protocolo relativamente nuevo** (2024)
- **Falta de ejemplos** prácticos en contextos universitarios

---

## 🔍 ¿Qué es MCP Realmente?

### Definición Técnica
> **Model Context Protocol (MCP)** es un protocolo de comunicación que permite a modelos de IA acceder de forma segura y estructurada a recursos y herramientas externas, extendiendo sus capacidades más allá de su conocimiento base.

### Analogía Simple
Imagina MCP como un **"sistema de enchufes"** estándar:
- **El modelo de IA** es como un dispositivo eléctrico
- **Los servidores MCP** son como diferentes tipos de enchufes especializados
- **El protocolo MCP** es el estándar que asegura que todo funcione junto

### Componentes Principales

#### 1. **🖥️ Cliente MCP**
- **Ejemplo**: Claude Desktop, VS Code con extensión MCP
- **Función**: Interfaz que el usuario utiliza
- **Responsabilidad**: Mostrar resultados y gestionar interacciones

#### 2. **🔌 Servidor MCP**
- **Ejemplo**: Servidor que accede a base de datos universitaria
- **Función**: Proporciona herramientas y recursos específicos
- **Responsabilidad**: Ejecutar acciones y devolver datos

#### 3. **🌐 Protocolo MCP**
- **Función**: Especificación de comunicación
- **Características**: JSON-RPC sobre diferentes transportes
- **Seguridad**: Autenticación y autorización incorporadas

---

## 🏗️ Arquitectura MCP Detallada

### Diagrama de Componentes

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente MCP   │    │  Protocolo MCP  │    │  Servidor MCP   │
│  (Claude App)   │◄──►│   (JSON-RPC)    │◄──►│ (Tu Aplicación) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interfaz de   │    │   Transporte    │    │   Recursos      │
│     Usuario     │    │ (stdio/socket)  │    │ (DB, APIs, etc) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flujo de Comunicación

1. **Usuario** hace una pregunta en Claude Desktop
2. **Cliente MCP** (Claude) identifica que necesita información externa
3. **Protocolo MCP** envía solicitud al servidor apropiado
4. **Servidor MCP** ejecuta la acción (consulta BD, llama API, etc.)
5. **Servidor MCP** devuelve resultados estructurados
6. **Cliente MCP** integra resultados en la respuesta
7. **Usuario** recibe respuesta completa y contextualizada

### Ejemplo Práctico: Consulta de Estudiante

```
Usuario: "¿Cuántos estudiantes hay matriculados en Informática?"

Claude Desktop (Cliente MCP):
  ↓ Detecta necesidad de datos externos
  ↓ Envía solicitud MCP

Servidor MCP Universitario:
  ↓ Recibe solicitud
  ↓ Consulta base de datos académica
  ↓ SELECT COUNT(*) FROM estudiantes WHERE carrera = 'Informática'
  ↓ Devuelve resultado: {"count": 342}

Claude Desktop:
  ↓ Recibe datos
  ↓ Genera respuesta natural
  ↓ "Actualmente hay 342 estudiantes matriculados en Informática"

Usuario: Recibe respuesta completa
```

---

## 🔧 Especificación Técnica MCP

### Protocolo Base: JSON-RPC 2.0

#### Estructura de Mensaje
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "method": "resource/read",
  "params": {
    "uri": "university://students/count",
    "arguments": {
      "department": "computer-science"
    }
  }
}
```

#### Respuesta Estándar
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "result": {
    "contents": [
      {
        "uri": "university://students/count",
        "mimeType": "application/json",
        "text": "{\"count\": 342, \"department\": \"computer-science\"}"
      }
    ]
  }
}
```

### Tipos de Recursos MCP

#### 1. **🛠️ Tools (Herramientas)**
**Función**: Acciones que el modelo puede ejecutar
```json
{
  "name": "query_student_database",
  "description": "Consulta información de estudiantes",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query_type": {"type": "string"},
      "filters": {"type": "object"}
    }
  }
}
```

#### 2. **📄 Resources (Recursos)**
**Función**: Datos que el modelo puede leer
```json
{
  "uri": "university://courses/schedule",
  "name": "Horarios de Cursos",
  "description": "Horarios actualizados de todas las asignaturas",
  "mimeType": "application/json"
}
```

#### 3. **🔗 Prompts (Plantillas)**
**Función**: Templates reutilizables para el modelo
```json
{
  "name": "student_support_prompt",
  "description": "Plantilla para soporte estudiantil",
  "arguments": [
    {
      "name": "student_id",
      "description": "ID del estudiante",
      "required": true
    }
  ]
}
```

### Transportes Soportados

#### 1. **📡 stdio (Standard Input/Output)**
**Uso**: Desarrollo local, testing
```bash
# Ejecutar servidor MCP
python mcp_server.py

# Cliente se conecta via stdin/stdout
```

#### 2. **🌐 HTTP/WebSocket**
**Uso**: Producción, servidores remotos
```python
# Servidor HTTP MCP
from mcp import Server
server = Server("university-mcp")
server.run(host="0.0.0.0", port=8080)
```

#### 3. **🔌 Named Pipes/Sockets**
**Uso**: Integración con sistemas existentes
```python
# Conexión via socket
import socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/mcp-server.sock")
```

---

## 💻 Configuración del Entorno MCP

### Requisitos del Sistema

#### Software Base:
```bash
# Python 3.9+ (requerido)
python --version  # Debe ser 3.9 o superior

# Node.js 18+ (para algunos servidores MCP)
node --version    # Debe ser 18.0 o superior

# Claude Desktop (cliente MCP)
# Descargar desde: https://claude.ai/download
```

#### Librerías Python:
```bash
# Instalar SDK de MCP
pip install mcp

# Librerías adicionales para servidores universitarios
pip install sqlalchemy psycopg2-binary
pip install fastapi uvicorn
pip install python-ldap
pip install redis
```

### Configuración de Claude Desktop

#### Archivo de Configuración: `claude_desktop_config.json`

**Ubicación por SO**:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Ejemplo de Configuración:
```json
{
  "mcpServers": {
    "university-system": {
      "command": "python",
      "args": ["/path/to/university_mcp_server.py"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/university",
        "LDAP_URL": "ldap://ldap.university.edu"
      }
    },
    "file-system": {
      "command": "python",
      "args": ["/path/to/filesystem_mcp_server.py"],
      "env": {
        "ALLOWED_DIRECTORIES": "/home/user/documents,/var/log"
      }
    }
  }
}
```

### Verificación de Instalación

#### Test de Conectividad:
```bash
# Verificar que Claude Desktop detecta servidores MCP
# Abrir Claude Desktop y escribir:
# "List available MCP servers"

# Debería mostrar los servidores configurados
```

---

## 🔨 Implementación: Primer Servidor MCP

### Servidor MCP Básico para Universidad

```python
#!/usr/bin/env python3
"""
Servidor MCP Básico para Sistema Universitario
Proporciona herramientas para consultar información académica
"""

import json
import sys
import asyncio
from typing import Any, Dict, List, Optional
from mcp import Server, StdioServerTransport
from mcp.types import (
    Resource, Tool, TextContent, 
    CallToolRequest, CallToolResult,
    ListResourcesRequest, ListResourcesResult,
    ReadResourceRequest, ReadResourceResult
)

# Simulación de base de datos universitaria
UNIVERSITY_DATA = {
    "students": [
        {"id": "12345", "name": "Juan Pérez", "department": "Informática", "year": 3},
        {"id": "12346", "name": "María García", "department": "Matemáticas", "year": 2},
        {"id": "12347", "name": "Carlos López", "department": "Informática", "year": 4}
    ],
    "courses": [
        {"code": "CS101", "name": "Introducción a la Programación", "credits": 6},
        {"code": "CS201", "name": "Estructuras de Datos", "credits": 6},
        {"code": "MATH101", "name": "Cálculo I", "credits": 6}
    ],
    "enrollments": [
        {"student_id": "12345", "course_code": "CS201", "semester": "2024-1"},
        {"student_id": "12346", "course_code": "MATH101", "semester": "2024-1"},
        {"student_id": "12347", "course_code": "CS101", "semester": "2024-1"}
    ]
}

class UniversityMCPServer:
    def __init__(self):
        self.server = Server("university-system")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Configurar manejadores para el servidor MCP"""
        
        @self.server.list_resources()
        async def list_resources() -> ListResourcesResult:
            """Lista recursos disponibles en el sistema universitario"""
            return ListResourcesResult(
                resources=[
                    Resource(
                        uri="university://students",
                        name="Lista de Estudiantes",
                        description="Información completa de estudiantes matriculados",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="university://courses",
                        name="Catálogo de Cursos",
                        description="Información de todos los cursos disponibles",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="university://enrollments",
                        name="Matriculaciones",
                        description="Información de matriculaciones actuales",
                        mimeType="application/json"
                    )
                ]
            )
        
        @self.server.read_resource()
        async def read_resource(request: ReadResourceRequest) -> ReadResourceResult:
            """Lee un recurso específico"""
            uri = request.uri
            
            if uri == "university://students":
                content = json.dumps(UNIVERSITY_DATA["students"], indent=2)
            elif uri == "university://courses":
                content = json.dumps(UNIVERSITY_DATA["courses"], indent=2)
            elif uri == "university://enrollments":
                content = json.dumps(UNIVERSITY_DATA["enrollments"], indent=2)
            else:
                raise ValueError(f"Recurso no encontrado: {uri}")
            
            return ReadResourceResult(
                contents=[
                    TextContent(
                        type="text",
                        text=content
                    )
                ]
            )
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """Lista herramientas disponibles"""
            return [
                Tool(
                    name="query_students",
                    description="Consulta estudiantes por departamento o año",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "department": {
                                "type": "string",
                                "description": "Departamento a consultar"
                            },
                            "year": {
                                "type": "integer",
                                "description": "Año académico"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_student_info",
                    description="Obtiene información detallada de un estudiante",
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
                    name="count_enrollments",
                    description="Cuenta matriculaciones por curso",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "course_code": {
                                "type": "string",
                                "description": "Código del curso"
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(request: CallToolRequest) -> CallToolResult:
            """Ejecuta una herramienta específica"""
            tool_name = request.params.name
            arguments = request.params.arguments or {}
            
            if tool_name == "query_students":
                return await self._query_students(arguments)
            elif tool_name == "get_student_info":
                return await self._get_student_info(arguments)
            elif tool_name == "count_enrollments":
                return await self._count_enrollments(arguments)
            else:
                raise ValueError(f"Herramienta no encontrada: {tool_name}")
    
    async def _query_students(self, args: Dict[str, Any]) -> CallToolResult:
        """Consulta estudiantes con filtros"""
        students = UNIVERSITY_DATA["students"]
        
        # Aplicar filtros
        if "department" in args:
            students = [s for s in students if s["department"] == args["department"]]
        
        if "year" in args:
            students = [s for s in students if s["year"] == args["year"]]
        
        result = {
            "total": len(students),
            "students": students
        }
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        )
    
    async def _get_student_info(self, args: Dict[str, Any]) -> CallToolResult:
        """Obtiene información de un estudiante específico"""
        student_id = args["student_id"]
        
        # Buscar estudiante
        student = next(
            (s for s in UNIVERSITY_DATA["students"] if s["id"] == student_id), 
            None
        )
        
        if not student:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Estudiante con ID {student_id} no encontrado"
                    )
                ]
            )
        
        # Buscar matriculaciones del estudiante
        enrollments = [
            e for e in UNIVERSITY_DATA["enrollments"] 
            if e["student_id"] == student_id
        ]
        
        # Obtener detalles de cursos matriculados
        enrolled_courses = []
        for enrollment in enrollments:
            course = next(
                (c for c in UNIVERSITY_DATA["courses"] 
                 if c["code"] == enrollment["course_code"]), 
                None
            )
            if course:
                enrolled_courses.append({
                    **course,
                    "semester": enrollment["semester"]
                })
        
        result = {
            "student": student,
            "enrolled_courses": enrolled_courses,
            "total_credits": sum(c["credits"] for c in enrolled_courses)
        }
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        )
    
    async def _count_enrollments(self, args: Dict[str, Any]) -> CallToolResult:
        """Cuenta matriculaciones por curso"""
        course_code = args.get("course_code")
        
        if course_code:
            # Contar para un curso específico
            count = len([
                e for e in UNIVERSITY_DATA["enrollments"] 
                if e["course_code"] == course_code
            ])
            
            # Obtener información del curso
            course = next(
                (c for c in UNIVERSITY_DATA["courses"] if c["code"] == course_code), 
                None
            )
            
            result = {
                "course_code": course_code,
                "course_name": course["name"] if course else "Desconocido",
                "enrollment_count": count
            }
        else:
            # Contar para todos los cursos
            course_counts = {}
            for enrollment in UNIVERSITY_DATA["enrollments"]:
                code = enrollment["course_code"]
                course_counts[code] = course_counts.get(code, 0) + 1
            
            result = {
                "total_enrollments": len(UNIVERSITY_DATA["enrollments"]),
                "by_course": course_counts
            }
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        )
    
    async def run(self):
        """Ejecuta el servidor MCP"""
        transport = StdioServerTransport()
        await self.server.run(transport)

# Función principal
async def main():
    server = UniversityMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Configuración en Claude Desktop

```json
{
  "mcpServers": {
    "university-system": {
      "command": "python",
      "args": ["/path/to/university_mcp_server.py"]
    }
  }
}
```

### Pruebas del Servidor

#### En Claude Desktop, probar:
```
1. "List available MCP resources"
2. "How many students are in the Computer Science department?"
3. "Show me information about student 12345"
4. "Count enrollments for course CS101"
```

---

## 🎯 Ejercicio Práctico (45 minutos)

### Objetivo: Adaptar el Servidor MCP a tu Universidad

#### Parte 1: Personalización (20 min)
1. **Modificar datos** con información realista de tu universidad
2. **Añadir nuevos recursos** (profesores, horarios, etc.)
3. **Crear herramientas específicas** para tu contexto

#### Parte 2: Testing (15 min)
1. **Configurar Claude Desktop** con tu servidor
2. **Probar diferentes consultas**
3. **Verificar respuestas** y funcionamiento

#### Parte 3: Documentación (10 min)
1. **Documentar tu servidor** MCP
2. **Crear guía de uso** para colegas
3. **Identificar mejoras** para mañana

## 📚 Material para Casa

- **Lectura**: `recursos/mcp_advanced_patterns.pdf`
- **Práctica**: Extender servidor con datos reales
- **Preparación**: Instalar herramientas para desarrollo día 3

---

## ✅ Finalización del curso

La finalización del curso se basa en la **asistencia**. No hay evaluación formal ni entrega de proyectos. El objetivo es **aprender haciendo** en un entorno práctico y colaborativo.

**Próximo día**: Desarrollo de Servidores MCP - Implementación avanzada con bases de datos reales e integración con sistemas universitarios
