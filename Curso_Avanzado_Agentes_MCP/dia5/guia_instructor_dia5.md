# Día 5: Agentes Multi-Sistema

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---|---|---|---|---|
| 09:00-09:15 | Repaso workflows del día 4 | 15min | Repaso | `repaso_workflows.md` |
| 09:15-11:15 | Orquestación de agentes y seguridad | 2h | Teórico-Práctico | `orquestacion_agentes.md` |
| 11:15-11:45 | **PAUSA - CAFÉ** | 30min | - | - |
| 11:45-14:00 | Taller: Integración, auditoría y compliance | 2.25h | Práctico | `integracion_empresarial.md` |

## 🎯 Objetivos del Día

1.  ✅ **Diseñar arquitecturas** de agentes distribuidos
2.  ✅ **Implementar orquestación** de múltiples agentes
3.  ✅ **Integrar con sistemas** empresariales (LDAP, ERP, CRM)
4.  ✅ **Aplicar governance** y políticas de seguridad
5.  ✅ **Implementar auditoría** y compliance completo

## 🏗️ Arquitectura de Agentes Multi-Sistema

### Patrón Orquestador Central

```python
"""
Sistema de Orquestación Central para Agentes Universitarios
Coordina múltiples agentes especializados
"""

import asyncio
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging

class AgentType(Enum):
    ACADEMIC = "academic"
    IT_SUPPORT = "it_support"
    LIBRARY = "library"
    ADMINISTRATION = "administration"
    FINANCIAL = "financial"

class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = ""
    description: str = ""
    priority: int = 5 # 1-10, 10 = máxima prioridad
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass 
class Agent:
    id: str
    type: AgentType
    name: str
    capabilities: List[str]
    max_concurrent_tasks: int = 5
    current_tasks: List[str] = field(default_factory=list)
    status: str = "active" # active, busy, offline, maintenance
    performance_metrics: Dict[str, float] = field(default_factory=dict)

class UniversityAgentOrchestrator:
    """Orquestador central para agentes universitarios"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []
        self.logger = logging.getLogger(__name__)
        
        # Registrar agentes especializados
        self._register_default_agents()
    
    def _register_default_agents(self):
        """Registrar agentes especializados por defecto"""
        
        # Agente Académico
        self.register_agent(Agent(
            id="academic-agent-01",
            type=AgentType.ACADEMIC,
            name="Asistente Académico Principal",
            capabilities=[
                "student_enrollment", "grade_management", "course_scheduling",
                "transcript_generation", "academic_planning"
            ],
            max_concurrent_tasks=10
        ))
        
        # Agente de Soporte IT
        self.register_agent(Agent(
            id="it-agent-01", 
            type=AgentType.IT_SUPPORT,
            name="Soporte Técnico Nivel 1",
            capabilities=[
                "password_reset", "account_management", "software_support",
                "hardware_diagnostics", "network_troubleshooting"
            ],
            max_concurrent_tasks=15
        ))
        
        # Agente de Biblioteca
        self.register_agent(Agent(
            id="library-agent-01",
            type=AgentType.LIBRARY,
            name="Asistente Bibliotecario",
            capabilities=[
                "catalog_search", "resource_reservation", "citation_help",
                "digital_access", "study_room_booking"
            ],
            max_concurrent_tasks=8
        ))
        
        # Agente Administrativo
        self.register_agent(Agent(
            id="admin-agent-01",
            type=AgentType.ADMINISTRATION,
            name="Asistente Administrativo",
            capabilities=[
                "document_processing", "application_review", "certification_issuing",
                "policy_information", "deadline_management"
            ],
            max_concurrent_tasks=12
        ))
    
    def register_agent(self, agent: Agent):
        """Registrar un nuevo agente en el sistema"""
        self.agents[agent.id] = agent
        self.logger.info(f"Agente registrado: {agent.name} ({agent.id})")
    
    async def submit_task(self, task_type: str, description: str, 
                         priority: int = 5, metadata: Dict[str, Any] = None) -> str:
        """Enviar nueva tarea al sistema"""
        
        task = Task(
            type=task_type,
            description=description,
            priority=priority,
            metadata=metadata or {}
        )
        
        self.tasks[task.id] = task
        self.task_queue.append(task.id)
        
        # Ordenar cola por prioridad
        self.task_queue.sort(key=lambda t_id: self.tasks[t_id].priority, reverse=True)
        
        self.logger.info(f"Tarea enviada: {task.id} - {description}")
        
        # Intentar asignación inmediata
        await self._try_assign_tasks()
        
        return task.id
    
    async def _try_assign_tasks(self):
        """Intentar asignar tareas pendientes a agentes disponibles"""
        
        for task_id in self.task_queue.copy():
            task = self.tasks[task_id]
            
            if task.status != TaskStatus.PENDING:
                continue
            
            # Encontrar agente capaz y disponible
            suitable_agent = self._find_suitable_agent(task)
            
            if suitable_agent:
                await self._assign_task_to_agent(task_id, suitable_agent.id)
                self.task_queue.remove(task_id)
    
    def _find_suitable_agent(self, task: Task) -> Optional[Agent]:
        """Encontrar agente más adecuado para una tarea"""
        
        suitable_agents = []
        
        for agent in self.agents.values():
            if (agent.status == "active" and 
                len(agent.current_tasks) < agent.max_concurrent_tasks and
                self._agent_can_handle_task(agent, task)):
                suitable_agents.append(agent)
        
        if not suitable_agents:
            return None
        
        # Seleccionar agente con menor carga actual
        return min(suitable_agents, key=lambda a: len(a.current_tasks))
    
    def _agent_can_handle_task(self, agent: Agent, task: Task) -> bool:
        """Verificar si un agente puede manejar una tarea específica"""
        
        # Mapeo de tipos de tarea a capacidades requeridas
        task_capability_map = {
            "student_query": ["student_enrollment", "grade_management"],
            "password_issue": ["password_reset", "account_management"],
            "library_search": ["catalog_search", "resource_reservation"],
            "document_request": ["document_processing", "certification_issuing"],
            "technical_support": ["software_support", "hardware_diagnostics"]
        }
        
        required_capabilities = task_capability_map.get(task.type, [])
        
        return any(cap in agent.capabilities for cap in required_capabilities)
    
    async def _assign_task_to_agent(self, task_id: str, agent_id: str):
        """Asignar tarea específica a agente específico"""
        
        task = self.tasks[task_id]
        agent = self.agents[agent_id]
        
        task.assigned_agent = agent_id
        task.status = TaskStatus.ASSIGNED
        agent.current_tasks.append(task_id)
        
        self.logger.info(f"Tarea {task_id} asignada a agente {agent.name}")
        
        # Ejecutar tarea de forma asíncrona
        asyncio.create_task(self._execute_task(task_id))
    
    async def _execute_task(self, task_id: str):
        """Ejecutar una tarea asignada"""
        
        task = self.tasks[task_id]
        agent = self.agents[task.assigned_agent]
        
        try:
            task.status = TaskStatus.IN_PROGRESS
            
            # Simular ejecución de tarea (en implementación real, llamaría al agente específico)
            await self._simulate_task_execution(task, agent)
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            # Actualizar métricas del agente
            self._update_agent_metrics(agent, success=True)
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self._update_agent_metrics(agent, success=False)
            
        finally:
            # Liberar agente
            agent.current_tasks.remove(task_id)
            
            # Intentar asignar más tareas
            await self._try_assign_tasks()
    
    async def _simulate_task_execution(self, task: Task, agent: Agent):
        """Simular ejecución de tarea (placeholder para implementación real)"""
        
        # Tiempo simulado basado en tipo de agente
        execution_times = {
            AgentType.ACADEMIC: 3,
            AgentType.IT_SUPPORT: 2,
            AgentType.LIBRARY: 1.5,
            AgentType.ADMINISTRATION: 4
        }
        
        await asyncio.sleep(execution_times.get(agent.type, 2))
        
        # Simular resultado
        task.result = {
            "success": True,
            "message": f"Tarea '{task.description}' completada por {agent.name}",
            "agent_id": agent.id,
            "execution_time": execution_times.get(agent.type, 2)
        }
    
    def _update_agent_metrics(self, agent: Agent, success: bool):
        """Actualizar métricas de rendimiento del agente"""
        
        if "tasks_completed" not in agent.performance_metrics:
            agent.performance_metrics["tasks_completed"] = 0
        if "tasks_failed" not in agent.performance_metrics:
            agent.performance_metrics["tasks_failed"] = 0
        
        if success:
            agent.performance_metrics["tasks_completed"] += 1
        else:
            agent.performance_metrics["tasks_failed"] += 1
        
        # Calcular tasa de éxito
        total_tasks = (agent.performance_metrics["tasks_completed"] + 
                      agent.performance_metrics["tasks_failed"])
        
        if total_tasks > 0:
            agent.performance_metrics["success_rate"] = (
                agent.performance_metrics["tasks_completed"] / total_tasks
            )
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Obtener estado general del sistema"""
        
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        failed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
        pending_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        
        active_agents = len([a for a in self.agents.values() if a.status == "active"])
        busy_agents = len([a for a in self.agents.values() if len(a.current_tasks) > 0])
        
        return {
            "timestamp": datetime.now().isoformat(),
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "failed": failed_tasks,
                "pending": pending_tasks,
                "in_queue": len(self.task_queue)
            },
            "agents": {
                "total": len(self.agents),
                "active": active_agents,
                "busy": busy_agents,
                "utilization": busy_agents / len(self.agents) if self.agents else 0
            },
            "performance": {
                "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
                "average_agent_performance": self._calculate_average_performance()
            }
        }
    
    def _calculate_average_performance(self) -> float:
        """Calcular rendimiento promedio de todos los agentes"""
        
        performances = [
            agent.performance_metrics.get("success_rate", 0)
            for agent in self.agents.values()
            if "success_rate" in agent.performance_metrics
        ]
        
        return sum(performances) / len(performances) if performances else 0

# Sistema de Governance y Políticas
class GovernanceEngine:
    """Motor de governance para sistemas de agentes"""
    
    def __init__(self):
        self.policies = {}
        self.audit_log = []
        self.compliance_rules = {}
    
    def register_policy(self, policy_name: str, policy_config: Dict[str, Any]):
        """Registrar política de governance"""
        self.policies[policy_name] = policy_config
    
    async def evaluate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluar solicitud contra políticas establecidas"""
        
        evaluation_result = {
            "approved": True,
            "reasons": [],
            "conditions": [],
            "risk_level": "low"
        }
        
        # Evaluar cada política
        for policy_name, policy in self.policies.items():
            policy_result = await self._evaluate_policy(policy, request)
            
            if not policy_result["passed"]:
                evaluation_result["approved"] = False
                evaluation_result["reasons"].append(policy_result["reason"])
                evaluation_result["risk_level"] = "high"
        
        # Registrar en audit log
        self._log_evaluation(request, evaluation_result)
        
        return evaluation_result
    
    async def _evaluate_policy(self, policy: Dict[str, Any], request: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluar una política específica"""
        
        # Implementar diferentes tipos de políticas
        policy_type = policy.get("type")
        
        if policy_type == "data_access":
            return await self._evaluate_data_access_policy(policy, request)
        elif policy_type == "rate_limiting":
            return await self._evaluate_rate_limiting_policy(policy, request)
        elif policy_type == "role_based":
            return await self._evaluate_role_based_policy(policy, request)
        
        return {"passed": True, "reason": "No policy evaluator found"}
    
    def _log_evaluation(self, request: Dict[str, Any], result: Dict[str, Any]):
        """Registrar evaluación en audit log"""
        
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "request_id": request.get("id", "unknown"),
            "user_id": request.get("user_id", "unknown"),
            "action": request.get("action", "unknown"),
            "approved": result["approved"],
            "risk_level": result["risk_level"],
            "reasons": result["reasons"]
        })

# Ejemplo de uso completo
async def demo_multi_agent_system():
    """Demostración del sistema multi-agente"""
    
    # Inicializar orquestador
    orchestrator = UniversityAgentOrchestrator()
    
    # Simular múltiples tareas concurrentes
    tasks = [
        ("student_query", "Consulta sobre horarios de Matemáticas", 8),
        ("password_issue", "Restablecer contraseña de juan.perez@uni.edu", 9),
        ("library_search", "Buscar libros sobre Machine Learning", 5),
        ("document_request", "Solicitar certificado de estudios", 7),
        ("technical_support", "Problema con impresora del laboratorio", 6)
    ]
    
    # Enviar tareas
    task_ids = []
    for task_type, description, priority in tasks:
        task_id = await orchestrator.submit_task(task_type, description, priority)
        task_ids.append(task_id)
    
    # Esperar un poco para que se procesen
    await asyncio.sleep(10)
    
    # Obtener estado del sistema
    status = await orchestrator.get_system_status()
    
    print("=== ESTADO DEL SISTEMA MULTI-AGENTE ===")
    print(f"Tareas completadas: {status['tasks']['completed']}/{status['tasks']['total']}")
    print(f"Agentes activos: {status['agents']['active']}")
    print(f"Utilización del sistema: {status['agents']['utilization']:.2%}")
    print(f"Tasa de éxito: {status['performance']['success_rate']:.2%}")
    
    return orchestrator

if __name__ == "__main__":
    asyncio.run(demo_multi_agent_system())
```

## 🔐 Integración Empresarial y Seguridad

### Integración con Active Directory/LDAP

```python
"""
Integración segura con sistemas empresariales
Active Directory, LDAP, ERP, CRM
"""

import ldap3
from ldap3 import Server, Connection, ALL, NTLM
import ssl
from typing import Dict, List, Optional, Any
import os
from cryptography.fernet import Fernet

class SecureUniversityIntegration:
    """Integración segura con sistemas universitarios"""
    
    def __init__(self):
        self.ldap_connection = None
        self.cipher_suite = Fernet(os.getenv('ENCRYPTION_KEY').encode())
        self.connections = {}
    
    async def authenticate_with_ldap(self, username: str, password: str) -> Dict[str, Any]:
        """Autenticación segura con LDAP/AD"""
        
        try:
            # Configuración LDAP segura
            server = Server(
                os.getenv('LDAP_SERVER'),
                port=636,  # Puerto LDAPS
                use_ssl=True,
                get_info=ALL
            )
            
            # Conexión con credenciales
            user_dn = f"{username}@{os.getenv('LDAP_DOMAIN')}"
            connection = Connection(
                server,
                user=user_dn,
                password=password,
                authentication=NTLM,
                auto_bind=True
            )
            
            # Buscar información del usuario
            search_filter = f"(sAMAccountName={username})"
            connection.search(
                search_base=os.getenv('LDAP_BASE_DN'),
                search_filter=search_filter,
                attributes=['cn', 'mail', 'department', 'title', 'memberOf']
            )
            
            if connection.entries:
                user_info = connection.entries[0]
                return {
                    "authenticated": True,
                    "user_info": {
                        "name": str(user_info.cn),
                        "email": str(user_info.mail),
                        "department": str(user_info.department),
                        "title": str(user_info.title),
                        "groups": [str(group) for group in user_info.memberOf]
                    }
                }
            
            return {"authenticated": False, "error": "User not found"}
            
        except Exception as e:
            return {"authenticated": False, "error": str(e)}
        
        finally:
            if connection:
                connection.unbind()
    
    async def get_user_permissions(self, username: str) -> List[str]:
        """Obtener permisos de usuario basados en grupos AD"""
        
        # Mapeo de grupos AD a permisos del sistema
        group_permission_map = {
            "CN=Estudiantes,OU=Grupos,DC=universidad,DC=edu": [
                "view_grades", "enroll_courses", "access_library"
            ],
            "CN=Profesores,OU=Grupos,DC=universidad,DC=edu": [
                "view_grades", "modify_grades", "create_courses", "access_library"
            ],
            "CN=Administradores,OU=Grupos,DC=universidad,DC=edu": [
                "full_access", "user_management", "system_configuration"
            ],
            "CN=IT_Support,OU=Grupos,DC=universidad,DC=edu": [
                "reset_passwords", "manage_accounts", "view_logs"
            ]
        }
        
        # Obtener grupos del usuario
        auth_result = await self.authenticate_with_ldap(username, "")
        if not auth_result["authenticated"]:
            return []
        
        user_groups = auth_result["user_info"]["groups"]
        
        # Compilar permisos
        permissions = set()
        for group in user_groups:
            if group in group_permission_map:
                permissions.update(group_permission_map[group])
        
        return list(permissions)
```

## 🎯 Ejercicios del Día

### Ejercicio 1: Diseño de Arquitectura Multi-Agente (45 min)
- Diseñar sistema de orquestación para tu universidad
- Definir agentes especializados necesarios
- Implementar cola de tareas prioritaria

### Ejercicio 2: Integración con LDAP/AD (60 min)
- Configurar conexión segura con directorio universitario
- Implementar autenticación y autorización
- Mapear grupos a permisos del sistema

### Ejercicio 3: Políticas de Governance (45 min)
- Definir políticas de acceso a datos
- Implementar evaluación de riesgos
- Crear sistema de audit trail

### Ejercicio 4: Monitorización y Alertas (45 min)
- Implementar métricas de rendimiento
- Configurar alertas automáticas
- Crear dashboard de monitorización

---

**Próximo día**: Proyecto Integral - Desarrollo supervisado de sistema completo multi-agente para universidad

## ✅ Finalización del curso

La finalización del curso se basa en la **asistencia**. No hay evaluación formal ni entrega de proyectos. El objetivo es **aprender haciendo** en un entorno práctico y colaborativo.
