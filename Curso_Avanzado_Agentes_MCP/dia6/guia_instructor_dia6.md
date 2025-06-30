# Día 6: Desarrollo de Proyectos Integrados y Casos Prácticos Complejos

## Objetivos del Día

- Integrar todos los conceptos aprendidos en proyectos complejos
- Desarrollar sistemas multi-agente completos para casos reales
- Implementar arquitecturas escalables y robustas
- Aplicar mejores prácticas de desarrollo, testing y documentación
- Resolver casos prácticos específicos del entorno universitario

## Cronograma del Día

### Sesión 1: Arquitecturas de Sistema Integradas (9:00-10:30)

#### Objetivos de la Sesión
- Diseñar arquitecturas completas de sistemas multi-agente
- Comprender patrones de integración avanzados
- Implementar comunicación entre múltiples componentes MCP

#### Contenido

**1. Patrones de Arquitectura Avanzados (30 min)**
- Arquitectura por capas en sistemas multi-agente
- Microservicios con MCP
- Event-driven architecture
- Patrones de orquestación vs coreografía

**2. Diseño de Sistema Completo (45 min)**
- Análisis de requisitos para sistema universitario
- Identificación de agentes necesarios
- Definición de interfaces MCP
- Estrategias de escalabilidad

**3. Implementación Práctica (15 min)**
- Setup del proyecto integrado
- Configuración de la arquitectura base

#### Lista de Verificación del Instructor
- [ ] Diagramas de arquitectura preparados
- [ ] Ejemplos de código de integración
- [ ] Template de proyecto base configurado
- [ ] Herramientas de diagramado disponibles

#### Ejercicio Práctico
**Sistema de Gestión Académica Inteligente**
```
Requisitos:
- Agente de soporte estudiantil
- Agente de gestión de recursos
- Agente de análisis académico
- Agente de comunicaciones
- Dashboard de monitorización

Implementar:
1. Arquitectura del sistema
2. Definición de interfaces MCP
3. Plan de integración
```

### DESCANSO (10:30-11:00)

### Sesión 2: Desarrollo del Proyecto Principal (11:00-12:30)

#### Objetivos de la Sesión
- Desarrollar un sistema completo paso a paso
- Implementar cada componente del sistema
- Integrar todos los agentes desarrollados

#### Contenido

**1. Agente de Soporte Estudiantil (30 min)**
```python
# Ejemplo de implementación
class StudentSupportAgent:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.knowledge_base = self.load_university_kb()
    
    async def handle_student_query(self, query):
        # Análisis de la consulta
        intent = await self.classify_intent(query)
        
        # Routing basado en intención
        if intent == "academic_info":
            return await self.handle_academic_query(query)
        elif intent == "technical_support":
            return await self.handle_tech_support(query)
        elif intent == "administrative":
            return await self.escalate_to_admin(query)
        
        return await self.generic_response(query)
    
    async def handle_academic_query(self, query):
        # Consulta a base de conocimiento académico
        context = await self.mcp_client.call_tool(
            "academic_search", {"query": query}
        )
        
        # Generación de respuesta contextual
        response = await self.generate_response(query, context)
        
        # Log para análisis posterior
        await self.log_interaction(query, response, "academic")
        
        return response
```

**2. Agente de Gestión de Recursos (30 min)**
```python
class ResourceManagementAgent:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.resource_db = self.connect_resource_db()
    
    async def check_availability(self, resource_type, date_range):
        # Consulta disponibilidad en tiempo real
        availability = await self.mcp_client.call_tool(
            "check_resources", {
                "type": resource_type,
                "start_date": date_range["start"],
                "end_date": date_range["end"]
            }
        )
        
        return availability
    
    async def make_reservation(self, user_id, resource_id, datetime):
        # Validación de permisos
        if not await self.validate_user_permissions(user_id, resource_id):
            return {"error": "Permission denied"}
        
        # Realizar reserva
        reservation = await self.mcp_client.call_tool(
            "create_reservation", {
                "user_id": user_id,
                "resource_id": resource_id,
                "datetime": datetime
            }
        )
        
        # Notificación automática
        await self.send_confirmation(user_id, reservation)
        
        return reservation
```

**3. Integración de Componentes (30 min)**
- Configuración de comunicación entre agentes
- Implementación de middleware de coordinación
- Testing de integración

#### Ejercicio Práctico
Cada equipo implementa un componente completo del sistema y lo integra con los demás.

### ALMUERZO (12:30-13:30)

### Sesión 3: Testing y Validación Avanzada (13:30-15:00)

#### Objetivos de la Sesión
- Implementar estrategias de testing comprehensivas
- Validar el funcionamiento del sistema integrado
- Establecer métricas de calidad y rendimiento

#### Contenido

**1. Testing de Sistemas Multi-Agente (45 min)**
```python
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

class TestIntegratedSystem:
    @pytest.fixture
    async def system_setup(self):
        # Setup del sistema completo para testing
        mcp_mock = AsyncMock()
        student_agent = StudentSupportAgent(mcp_mock)
        resource_agent = ResourceManagementAgent(mcp_mock)
        
        return {
            "student_agent": student_agent,
            "resource_agent": resource_agent,
            "mcp_client": mcp_mock
        }
    
    async def test_student_academic_query(self, system_setup):
        # Test de consulta académica
        agents = system_setup
        
        # Mock de respuesta de MCP
        agents["mcp_client"].call_tool.return_value = {
            "results": ["Curso de Python disponible", "Horarios: L-V 9-11"]
        }
        
        # Ejecutar consulta
        response = await agents["student_agent"].handle_student_query(
            "¿Cuándo es el curso de Python?"
        )
        
        # Validaciones
        assert "Python" in response
        assert "L-V 9-11" in response
        agents["mcp_client"].call_tool.assert_called_once()
    
    async def test_resource_reservation_flow(self, system_setup):
        # Test de flujo completo de reserva
        agents = system_setup
        
        # Mock de disponibilidad
        agents["mcp_client"].call_tool.return_value = {
            "available": True,
            "resource_id": "lab_001"
        }
        
        # Test de reserva
        result = await agents["resource_agent"].make_reservation(
            "user_123", "lab_001", "2024-03-15T10:00:00"
        )
        
        assert result is not None
        assert "error" not in result
    
    async def test_agent_coordination(self, system_setup):
        # Test de coordinación entre agentes
        agents = system_setup
        
        # Simular escenario de coordinación
        query = "Necesito reservar un laboratorio para el curso de Python"
        
        # El agente de soporte debe coordinarse con el de recursos
        response = await agents["student_agent"].handle_student_query(query)
        
        # Verificar que se llamó al agente de recursos
        assert agents["mcp_client"].call_tool.call_count >= 1
```

**2. Métricas y Monitorización (30 min)**
```python
class SystemMetrics:
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "success_rates": {},
            "error_counts": {},
            "user_satisfaction": []
        }
    
    async def track_response_time(self, agent_name, start_time, end_time):
        duration = end_time - start_time
        self.metrics["response_times"].append({
            "agent": agent_name,
            "duration": duration,
            "timestamp": end_time
        })
    
    async def track_success_rate(self, agent_name, success):
        if agent_name not in self.metrics["success_rates"]:
            self.metrics["success_rates"][agent_name] = {
                "total": 0, "successful": 0
            }
        
        self.metrics["success_rates"][agent_name]["total"] += 1
        if success:
            self.metrics["success_rates"][agent_name]["successful"] += 1
    
    def generate_report(self):
        report = {
            "avg_response_time": sum(
                m["duration"] for m in self.metrics["response_times"]
            ) / len(self.metrics["response_times"]),
            "success_rates": {
                agent: data["successful"] / data["total"]
                for agent, data in self.metrics["success_rates"].items()
            }
        }
        return report
```

**3. Validación de Rendimiento (15 min)**
- Load testing con múltiples usuarios concurrentes
- Análisis de bottlenecks
- Optimización de consultas MCP

#### Ejercicio Práctico
Implementar suite completa de tests para el sistema desarrollado.

### DESCANSO (15:00-15:30)

### Sesión 4: Despliegue y Configuración de Producción (15:30-17:00)

#### Objetivos de la Sesión
- Preparar el sistema para entorno de producción
- Configurar monitorización y logging
- Establecer procedimientos de mantenimiento

#### Contenido

**1. Configuración de Producción (45 min)**
```yaml
# docker-compose.yml para el sistema completo
version: '3.8'
services:
  student-support-agent:
    build: ./agents/student-support
    environment:
      - MCP_SERVER_URL=http://mcp-server:8000
      - LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://user:pass@db:5432/university
    depends_on:
      - mcp-server
      - database
    networks:
      - agent-network
  
  resource-management-agent:
    build: ./agents/resource-management
    environment:
      - MCP_SERVER_URL=http://mcp-server:8000
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mcp-server
      - redis
    networks:
      - agent-network
  
  mcp-server:
    build: ./mcp-server
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/university
    networks:
      - agent-network
  
  database:
    image: postgres:15
    environment:
      - POSTGRES_DB=university
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - agent-network
  
  redis:
    image: redis:7-alpine
    networks:
      - agent-network
  
  monitoring:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - agent-network

networks:
  agent-network:
    driver: bridge

volumes:
  postgres_data:
  grafana_data:
```

**2. Logging y Monitorización (30 min)**
```python
import logging
import structlog
from opentelemetry import trace, metrics

# Configuración de logging estructurado
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

class AgentMonitoring:
    def __init__(self, agent_name):
        self.logger = structlog.get_logger(agent_name)
        self.tracer = trace.get_tracer(agent_name)
        self.meter = metrics.get_meter(agent_name)
        
        # Métricas personalizadas
        self.request_counter = self.meter.create_counter(
            name="agent_requests_total",
            description="Total requests processed by agent"
        )
        
        self.response_time_histogram = self.meter.create_histogram(
            name="agent_response_time_seconds",
            description="Response time distribution"
        )
    
    async def log_request(self, request_data, user_id=None):
        with self.tracer.start_as_current_span("process_request") as span:
            span.set_attribute("user.id", user_id or "anonymous")
            span.set_attribute("request.type", request_data.get("type", "unknown"))
            
            self.logger.info(
                "Processing request",
                user_id=user_id,
                request_type=request_data.get("type"),
                request_size=len(str(request_data))
            )
            
            self.request_counter.add(1, {"user_type": "student" if user_id else "anonymous"})
    
    async def log_response(self, response_data, processing_time):
        self.logger.info(
            "Request completed",
            response_size=len(str(response_data)),
            processing_time=processing_time,
            success=response_data.get("success", True)
        )
        
        self.response_time_histogram.record(processing_time)
```

**3. Procedimientos de Mantenimiento (15 min)**
- Scripts de backup automático
- Procedimientos de actualización
- Monitorización de salud del sistema

#### Lista de Verificación del Instructor
- [ ] Entorno Docker configurado
- [ ] Scripts de despliegue preparados
- [ ] Dashboard de monitorización funcional
- [ ] Documentación de procedimientos lista

#### Ejercicio Final del Día
Desplegar el sistema completo en un entorno de prueba y validar su funcionamiento.

## Resolución de Problemas Comunes

### Problema: Errores de Comunicación entre Agentes
**Síntomas:** Timeouts, respuestas vacías, errores de conexión
**Solución:**
1. Verificar configuración de red
2. Comprobar logs de MCP server
3. Validar autenticación entre servicios

### Problema: Rendimiento Degradado
**Síntomas:** Respuestas lentas, alta utilización de CPU/memoria
**Solución:**
1. Análisis de métricas de rendimiento
2. Optimización de consultas a base de datos
3. Implementación de cache

### Problema: Fallos en Testing de Integración
**Síntomas:** Tests inconsistentes, falsos positivos/negativos
**Solución:**
1. Revisión de mocks y fixtures
2. Verificación de orden de ejecución
3. Limpieza de estado entre tests

## Recursos Adicionales

### Documentación
- Guías de arquitectura de sistemas distribuidos
- Best practices para testing de sistemas complejos
- Documentación de Docker y orquestación

### Herramientas
- Docker Desktop
- Grafana para monitorización
- pytest para testing
- structlog para logging

### Referencias
- Patterns of Enterprise Application Architecture (Martin Fowler)
- Building Event-Driven Microservices (Adam Bellemare)
- Testing Distributed Systems (Kyle Kingsbury)

## Evaluación del Día

### Criterios de Evaluación
1. **Diseño de Arquitectura (25%)**
   - Correcta identificación de componentes
   - Definición apropiada de interfaces
   - Consideración de escalabilidad

2. **Implementación Técnica (35%)**
   - Código funcional y bien estructurado
   - Integración exitosa de componentes
   - Manejo apropiado de errores

3. **Testing y Validación (25%)**
   - Cobertura adecuada de tests
   - Tests de integración funcionales
   - Validación de métricas

4. **Despliegue y Configuración (15%)**
   - Configuración correcta del entorno
   - Procedimientos documentados
   - Monitorización implementada

### Entregables
1. Código fuente completo del sistema
2. Suite de tests implementada
3. Configuración de despliegue
4. Documentación técnica
5. Dashboard de monitorización

## Preparación para el Día 7
- Revisión de sistemas desarrollados
- Identificación de mejoras potenciales
- Preparación de presentaciones finales
- Planificación de proyectos futuros
