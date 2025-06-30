# Día 4: Integración MCP con Claude Desktop y Clientes Personalizados

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---------|-----------|----------|------|----------|
| 09:00-09:15 | Verificación servidores MCP del día 3 | 15min | Testing | `verificacion_servidores.md` |
| 09:15-10:45 | Integración avanzada con Claude Desktop | 1.5h | Práctico | `integracion_claude_desktop.md` |
| 10:45-11:00 | **DESCANSO** | 15min | - | - |
| 11:00-12:30 | Desarrollo de clientes MCP personalizados | 1.5h | Desarrollo | `clientes_personalizados.md` |
| 12:30-13:30 | **ALMUERZO** | 1h | - | - |
| 13:30-15:00 | Casos de uso complejos y workflows | 1.5h | Aplicación | `casos_uso_complejos.md` |
| 15:00-15:15 | **DESCANSO** | 15min | - | - |
| 15:15-16:45 | Automatización de workflows universitarios | 1.5h | Proyecto | `workflows_automatizados.md` |
| 16:45-17:00 | Demostración y evaluación del día | 15min | Demo | `demo_evaluacion.md` |

## 🎯 Objetivos del Día

1. ✅ **Integrar servidores MCP** avanzados con Claude Desktop
2. ✅ **Desarrollar clientes MCP** personalizados para casos específicos
3. ✅ **Implementar workflows** complejos multi-step
4. ✅ **Automatizar procesos** universitarios completos
5. ✅ **Optimizar la experiencia** de usuario final

## 🔧 Configuración Avanzada Claude Desktop

### Configuración Multi-Servidor

```json
{
  "mcpServers": {
    "university-academic": {
      "command": "python",
      "args": ["/path/to/academic_mcp_server.py"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/university_academic",
        "CACHE_ENABLED": "true",
        "LOG_LEVEL": "INFO"
      }
    },
    "university-it": {
      "command": "python", 
      "args": ["/path/to/it_support_mcp_server.py"],
      "env": {
        "LDAP_URL": "ldap://ldap.university.edu",
        "TICKET_SYSTEM_API": "https://tickets.university.edu/api",
        "MONITORING_ENABLED": "true"
      }
    },
    "university-library": {
      "command": "python",
      "args": ["/path/to/library_mcp_server.py"],
      "env": {
        "CATALOG_DB": "postgresql://user:pass@localhost/library",
        "DIGITAL_RESOURCES_API": "https://resources.library.edu/api"
      }
    },
    "university-admin": {
      "command": "python",
      "args": ["/path/to/admin_mcp_server.py"],
      "env": {
        "ERP_API_URL": "https://erp.university.edu/api",
        "SECURE_MODE": "true",
        "AUDIT_ENABLED": "true"
      }
    }
  },
  "mcpSettings": {
    "timeout": 30000,
    "maxConcurrentConnections": 10,
    "enableLogging": true,
    "logLevel": "INFO"
  }
}
```

### Configuración de Seguridad

```json
{
  "mcpSecurity": {
    "allowedDomains": ["*.university.edu", "localhost"],
    "requireAuthentication": true,
    "encryptCommunication": true,
    "auditTrail": true,
    "rateLimiting": {
      "enabled": true,
      "requestsPerMinute": 100,
      "burstLimit": 20
    }
  }
}
```

## 💻 Cliente MCP Personalizado

### Interfaz Web para Administradores

```python
"""
Cliente MCP Web personalizado para administradores universitarios
Permite gestión visual de recursos y herramientas MCP
"""

import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
import streamlit as st
from mcp import ClientSession, StdioClientTransport
import subprocess
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class UniversityMCPClient:
    def __init__(self):
        self.sessions = {}
        self.server_configs = {
            "academic": {
                "command": ["python", "/path/to/academic_mcp_server.py"],
                "description": "Sistema Académico"
            },
            "it": {
                "command": ["python", "/path/to/it_mcp_server.py"], 
                "description": "Soporte IT"
            },
            "library": {
                "command": ["python", "/path/to/library_mcp_server.py"],
                "description": "Biblioteca"
            }
        }
    
    async def connect_to_server(self, server_name: str):
        """Conectar a un servidor MCP específico"""
        if server_name in self.sessions:
            return self.sessions[server_name]
        
        config = self.server_configs[server_name]
        
        # Iniciar proceso del servidor
        process = subprocess.Popen(
            config["command"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Crear sesión cliente
        transport = StdioClientTransport(process.stdin, process.stdout)
        session = ClientSession(transport)
        await session.initialize()
        
        self.sessions[server_name] = {
            "session": session,
            "process": process,
            "config": config
        }
        
        return self.sessions[server_name]
    
    async def list_all_resources(self) -> Dict[str, List[Dict]]:
        """Listar recursos de todos los servidores"""
        all_resources = {}
        
        for server_name in self.server_configs.keys():
            try:
                server_session = await self.connect_to_server(server_name)
                session = server_session["session"]
                
                resources = await session.list_resources()
                all_resources[server_name] = [
                    {
                        "uri": resource.uri,
                        "name": resource.name,
                        "description": resource.description,
                        "mimeType": resource.mimeType
                    }
                    for resource in resources.resources
                ]
            except Exception as e:
                st.error(f"Error conectando a {server_name}: {e}")
                all_resources[server_name] = []
        
        return all_resources
    
    async def execute_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]):
        """Ejecutar herramienta en servidor específico"""
        server_session = await self.connect_to_server(server_name)
        session = server_session["session"]
        
        result = await session.call_tool(tool_name, arguments)
        return result

# Interfaz Streamlit
class MCPDashboard:
    def __init__(self):
        self.client = UniversityMCPClient()
        st.set_page_config(
            page_title="Dashboard MCP Universidad",
            page_icon="🎓",
            layout="wide"
        )
    
    def run(self):
        """Ejecutar dashboard principal"""
        st.title("🎓 Dashboard MCP Universidad")
        st.sidebar.title("Navegación")
        
        page = st.sidebar.selectbox(
            "Seleccionar página",
            ["🏠 Inicio", "📊 Recursos", "🛠️ Herramientas", "📈 Métricas", "⚙️ Configuración"]
        )
        
        if page == "🏠 Inicio":
            self.show_home()
        elif page == "📊 Recursos":
            self.show_resources()
        elif page == "🛠️ Herramientas":
            self.show_tools()
        elif page == "📈 Métricas":
            self.show_metrics()
        elif page == "⚙️ Configuración":
            self.show_config()
    
    def show_home(self):
        """Página de inicio con resumen"""
        st.header("Panel de Control MCP")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Servidores Activos", "4", "+1")
        
        with col2:
            st.metric("Recursos Disponibles", "23", "+3")
        
        with col3:
            st.metric("Herramientas", "15", "+2")
        
        with col4:
            st.metric("Uptime", "99.8%", "+0.1%")
        
        # Gráfico de actividad
        st.subheader("Actividad Reciente")
        
        # Datos simulados de actividad
        activity_data = pd.DataFrame({
            'Hora': pd.date_range('2024-01-01 00:00', periods=24, freq='H'),
            'Consultas': [12, 8, 5, 3, 2, 4, 15, 25, 35, 42, 38, 45, 50, 48, 52, 49, 46, 43, 38, 32, 28, 22, 18, 15]
        })
        
        fig = px.line(activity_data, x='Hora', y='Consultas', title='Consultas por Hora')
        st.plotly_chart(fig, use_container_width=True)
    
    def show_resources(self):
        """Página de gestión de recursos"""
        st.header("📊 Gestión de Recursos MCP")
        
        # Selector de servidor
        server = st.selectbox(
            "Seleccionar servidor:",
            ["academic", "it", "library", "admin"]
        )
        
        if st.button("🔄 Actualizar Recursos"):
            with st.spinner("Cargando recursos..."):
                resources = asyncio.run(self.load_resources(server))
                st.session_state.resources = resources
        
        if hasattr(st.session_state, 'resources'):
            resources = st.session_state.resources
            
            # Mostrar recursos en tabla
            if resources:
                df = pd.DataFrame(resources)
                st.dataframe(df, use_container_width=True)
                
                # Permitir lectura de recursos
                selected_uri = st.selectbox(
                    "Seleccionar recurso para leer:",
                    [r['uri'] for r in resources]
                )
                
                if st.button("📖 Leer Recurso"):
                    content = asyncio.run(self.read_resource(server, selected_uri))
                    st.json(content)
    
    def show_tools(self):
        """Página de herramientas"""
        st.header("🛠️ Herramientas MCP")
        
        # Interfaz para ejecutar herramientas
        server = st.selectbox(
            "Servidor:",
            ["academic", "it", "library", "admin"],
            key="tools_server"
        )
        
        # Herramientas predefinidas
        tool_templates = {
            "search_students": {
                "name": "Buscar Estudiantes",
                "description": "Buscar estudiantes por criterios",
                "params": {
                    "name": {"type": "text", "label": "Nombre"},
                    "department": {"type": "text", "label": "Departamento"},
                    "year": {"type": "number", "label": "Año"}
                }
            },
            "create_ticket": {
                "name": "Crear Ticket IT",
                "description": "Crear nuevo ticket de soporte",
                "params": {
                    "title": {"type": "text", "label": "Título"},
                    "description": {"type": "textarea", "label": "Descripción"},
                    "priority": {"type": "select", "label": "Prioridad", "options": ["low", "medium", "high"]}
                }
            }
        }
        
        tool_name = st.selectbox(
            "Seleccionar herramienta:",
            list(tool_templates.keys())
        )
        
        tool = tool_templates[tool_name]
        st.subheader(tool["name"])
        st.write(tool["description"])
        
        # Generar formulario dinámico
        params = {}
        for param_name, param_config in tool["params"].items():
            if param_config["type"] == "text":
                params[param_name] = st.text_input(param_config["label"])
            elif param_config["type"] == "textarea":
                params[param_name] = st.text_area(param_config["label"])
            elif param_config["type"] == "number":
                params[param_name] = st.number_input(param_config["label"])
            elif param_config["type"] == "select":
                params[param_name] = st.selectbox(param_config["label"], param_config["options"])
        
        if st.button("▶️ Ejecutar Herramienta"):
            with st.spinner("Ejecutando..."):
                result = asyncio.run(self.client.execute_tool(server, tool_name, params))
                st.success("Herramienta ejecutada exitosamente")
                st.json(result)
    
    def show_metrics(self):
        """Página de métricas y análisis"""
        st.header("📈 Métricas y Análisis")
        
        # Métricas de rendimiento
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de uso por servidor
            server_usage = pd.DataFrame({
                'Servidor': ['Academic', 'IT', 'Library', 'Admin'],
                'Consultas': [150, 89, 67, 45],
                'Tiempo Respuesta (ms)': [245, 189, 156, 203]
            })
            
            fig1 = px.bar(server_usage, x='Servidor', y='Consultas', 
                         title='Consultas por Servidor')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Gráfico de tiempo de respuesta
            fig2 = px.bar(server_usage, x='Servidor', y='Tiempo Respuesta (ms)',
                         title='Tiempo de Respuesta Promedio')
            st.plotly_chart(fig2, use_container_width=True)
        
        # Tabla de errores recientes
        st.subheader("🚨 Errores Recientes")
        error_data = pd.DataFrame({
            'Timestamp': ['2024-01-01 10:30', '2024-01-01 11:15', '2024-01-01 12:45'],
            'Servidor': ['academic', 'it', 'library'],
            'Error': ['Connection timeout', 'Invalid auth', 'Resource not found'],
            'Severidad': ['Medium', 'High', 'Low']
        })
        st.dataframe(error_data, use_container_width=True)
    
    def show_config(self):
        """Página de configuración"""
        st.header("⚙️ Configuración")
        
        # Configuración de servidores
        st.subheader("Configuración de Servidores")
        
        for server_name, config in self.client.server_configs.items():
            with st.expander(f"Servidor: {config['description']}"):
                st.code(" ".join(config["command"]))
                
                # Estado del servidor
                status = st.radio(
                    f"Estado {server_name}:",
                    ["Activo", "Inactivo", "Mantenimiento"],
                    key=f"status_{server_name}"
                )
                
                # Configuración específica
                log_level = st.selectbox(
                    f"Nivel de log {server_name}:",
                    ["DEBUG", "INFO", "WARNING", "ERROR"],
                    index=1,
                    key=f"log_{server_name}"
                )
        
        # Configuración global
        st.subheader("Configuración Global")
        
        timeout = st.number_input("Timeout (segundos):", value=30, min_value=1, max_value=300)
        max_connections = st.number_input("Máx. conexiones:", value=10, min_value=1, max_value=100)
        enable_caching = st.checkbox("Habilitar cache", value=True)
        
        if st.button("💾 Guardar Configuración"):
            st.success("Configuración guardada exitosamente")
    
    async def load_resources(self, server_name: str):
        """Cargar recursos de un servidor"""
        all_resources = await self.client.list_all_resources()
        return all_resources.get(server_name, [])
    
    async def read_resource(self, server_name: str, uri: str):
        """Leer contenido de un recurso"""
        server_session = await self.client.connect_to_server(server_name)
        session = server_session["session"]
        
        result = await session.read_resource(uri)
        return result

# Ejecutar dashboard
if __name__ == "__main__":
    dashboard = MCPDashboard()
    dashboard.run()
```

## 🔄 Workflows Automatizados

### Workflow: Proceso de Matriculación Completo

```python
"""
Workflow automatizado para proceso de matriculación
Integra múltiples servidores MCP para proceso completo
"""

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowStep:
    name: str
    server: str
    tool: str
    arguments: Dict[str, Any]
    required: bool = True
    retry_count: int = 3

class EnrollmentWorkflow:
    def __init__(self, mcp_client):
        self.client = mcp_client
        self.status = WorkflowStatus.PENDING
        self.results = {}
        self.errors = []
    
    async def execute_enrollment(self, student_id: str, course_code: str, semester: str):
        """Ejecutar workflow completo de matriculación"""
        
        steps = [
            WorkflowStep(
                name="validate_student",
                server="academic",
                tool="get_student_info",
                arguments={"student_id": student_id}
            ),
            WorkflowStep(
                name="check_prerequisites",
                server="academic", 
                tool="check_course_prerequisites",
                arguments={"student_id": student_id, "course_code": course_code}
            ),
            WorkflowStep(
                name="verify_capacity",
                server="academic",
                tool="check_course_capacity",
                arguments={"course_code": course_code, "semester": semester}
            ),
            WorkflowStep(
                name="calculate_fees",
                server="admin",
                tool="calculate_enrollment_fees",
                arguments={"student_id": student_id, "course_code": course_code}
            ),
            WorkflowStep(
                name="create_enrollment",
                server="academic",
                tool="enroll_student",
                arguments={"student_id": student_id, "course_code": course_code, "semester": semester}
            ),
            WorkflowStep(
                name="generate_invoice",
                server="admin",
                tool="generate_invoice",
                arguments={"student_id": student_id, "enrollment_id": "{{create_enrollment.enrollment_id}}"}
            ),
            WorkflowStep(
                name="send_confirmation",
                server="it",
                tool="send_email",
                arguments={
                    "to": "{{validate_student.email}}",
                    "template": "enrollment_confirmation",
                    "data": {
                        "course_code": course_code,
                        "semester": semester
                    }
                },
                required=False
            ),
            WorkflowStep(
                name="update_library_access",
                server="library",
                tool="update_student_access",
                arguments={"student_id": student_id, "course_code": course_code},
                required=False
            )
        ]
        
        self.status = WorkflowStatus.RUNNING
        
        try:
            for step in steps:
                result = await self._execute_step(step)
                
                if result["success"]:
                    self.results[step.name] = result["data"]
                elif step.required:
                    self.status = WorkflowStatus.FAILED
                    self.errors.append(f"Error en paso requerido {step.name}: {result['error']}")
                    return False
                else:
                    # Paso opcional falló, continuar
                    self.errors.append(f"Warning en paso opcional {step.name}: {result['error']}")
            
            self.status = WorkflowStatus.COMPLETED
            return True
            
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            self.errors.append(f"Error inesperado: {str(e)}")
            return False
    
    async def _execute_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Ejecutar un paso individual del workflow"""
        
        # Resolver argumentos con resultados anteriores
        resolved_args = self._resolve_arguments(step.arguments)
        
        for attempt in range(step.retry_count):
            try:
                result = await self.client.execute_tool(
                    step.server, 
                    step.tool, 
                    resolved_args
                )
                
                return {
                    "success": True,
                    "data": result,
                    "attempt": attempt + 1
                }
                
            except Exception as e:
                if attempt == step.retry_count - 1:
                    return {
                        "success": False,
                        "error": str(e),
                        "attempts": step.retry_count
                    }
                
                # Esperar antes del siguiente intento
                await asyncio.sleep(2 ** attempt)
    
    def _resolve_arguments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Resolver argumentos con referencias a resultados anteriores"""
        resolved = {}
        
        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                # Referencia a resultado anterior
                reference = value[2:-2]  # Remover {{ }}
                
                if "." in reference:
                    step_name, field = reference.split(".", 1)
                    if step_name in self.results:
                        resolved[key] = self.results[step_name].get(field, value)
                    else:
                        resolved[key] = value
                else:
                    resolved[key] = self.results.get(reference, value)
            else:
                resolved[key] = value
        
        return resolved

# Uso del workflow
async def demo_enrollment_workflow():
    """Demostración del workflow de matriculación"""
    
    client = UniversityMCPClient()
    workflow = EnrollmentWorkflow(client)
    
    # Ejecutar matriculación
    success = await workflow.execute_enrollment(
        student_id="12345",
        course_code="CS201", 
        semester="2024-2"
    )
    
    if success:
        print("✅ Matriculación completada exitosamente")
        print("Resultados:", workflow.results)
    else:
        print("❌ Error en la matriculación")
        print("Errores:", workflow.errors)
    
    print(f"Estado final: {workflow.status.value}")

if __name__ == "__main__":
    asyncio.run(demo_enrollment_workflow())
```

## 🎯 Ejercicios del Día

### Ejercicio 1: Configuración Avanzada Claude Desktop (30 min)
- Configurar múltiples servidores MCP
- Implementar configuración de seguridad
- Probar conectividad y rendimiento

### Ejercicio 2: Cliente Web Personalizado (60 min)
- Desarrollar interfaz Streamlit
- Integrar con servidores MCP
- Crear dashboard de monitorización

### Ejercicio 3: Workflow de Proceso Universitario (90 min)
- Elegir proceso específico de tu universidad
- Diseñar workflow multi-paso
- Implementar con manejo de errores
- Probar con datos reales

### Ejercicio 4: Optimización y Monitorización (30 min)
- Implementar métricas de rendimiento
- Configurar alertas y logs
- Optimizar tiempos de respuesta

---

**Próximo día**: Agentes Multi-Sistema - Orquestación de agentes, integración empresarial y governance avanzada
