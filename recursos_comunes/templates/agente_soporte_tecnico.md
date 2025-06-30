# Template: Agente de Soporte Técnico Universitario

## 🎯 Descripción
Template base para crear un agente de soporte técnico que puede manejar consultas comunes del servicio de informática universitario.

---

## 📋 Funcionalidades Incluidas

### ✅ Gestión de Consultas:
- Clasificación automática de tickets
- Respuestas a preguntas frecuentes
- Escalado inteligente a técnicos humanos

### ✅ Base de Conocimiento:
- FAQ sobre servicios IT universitarios
- Procedimientos paso a paso
- Información de contacto por áreas

### ✅ Integración con Sistemas:
- API mock para sistema de tickets
- Consulta de estado de servicios
- Logging de interacciones

---

## 🛠️ Código Base

### Archivo Principal: `agente_soporte.py`

```python
"""
Agente de Soporte Técnico Universitario
Desarrollado para el curso de Agentes con GitHub Copilot
"""
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('soporte_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Ticket:
    """Estructura de datos para tickets de soporte"""
    id: str
    usuario: str
    categoria: str
    descripcion: str
    estado: str
    prioridad: str
    fecha_creacion: datetime
    asignado_a: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'usuario': self.usuario,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'asignado_a': self.asignado_a
        }

class BaseDeDatos:
    """Simulador de base de datos para el agente"""
    
    def __init__(self):
        self.tickets = []
        self.faq = self._cargar_faq()
        self.servicios = self._cargar_estado_servicios()
    
    def _cargar_faq(self) -> List[Dict[str, str]]:
        """Carga las preguntas frecuentes"""
        return [
            {
                "pregunta": "¿Cómo restablezco mi contraseña universitaria?",
                "respuesta": "Puedes restablecer tu contraseña en https://password.universidad.edu o acudiendo presencialmente al Servicio de Informática con tu DNI.",
                "categoria": "cuentas"
            },
            {
                "pregunta": "¿Cómo me conecto a la WiFi de la universidad?",
                "respuesta": "Red: UNIV-WIFI, Usuario: tu email universitario, Contraseña: tu contraseña de cuenta. Si tienes problemas, verifica que tu dispositivo soporte WPA2-Enterprise.",
                "categoria": "conectividad"
            },
            {
                "pregunta": "¿Dónde puedo descargar software gratuito para estudiantes?",
                "respuesta": "Accede al portal de software en https://software.universidad.edu con tus credenciales universitarias. Disponemos de Office 365, Adobe Creative Suite, y más.",
                "categoria": "software"
            },
            {
                "pregunta": "¿Cómo accedo al campus virtual?",
                "respuesta": "El campus virtual está disponible en https://campus.universidad.edu. Usa las mismas credenciales que para el correo universitario.",
                "categoria": "plataformas"
            },
            {
                "pregunta": "¿Qué hago si mi correo universitario no funciona?",
                "respuesta": "Verifica tu conexión, prueba desde diferentes dispositivos. Si persiste el problema, puede ser mantenimiento programado. Consulta el estado en https://status.universidad.edu",
                "categoria": "correo"
            }
        ]
    
    def _cargar_estado_servicios(self) -> Dict[str, str]:
        """Simula el estado actual de los servicios"""
        return {
            "correo": "operativo",
            "wifi": "operativo", 
            "campus_virtual": "mantenimiento",
            "vpn": "operativo",
            "impresoras": "operativo",
            "laboratorios": "parcial"  # Algunos labs cerrados
        }
    
    def buscar_faq(self, consulta: str) -> List[Dict[str, str]]:
        """Busca en las FAQ basándose en palabras clave"""
        consulta_lower = consulta.lower()
        resultados = []
        
        # Buscar por palabras clave simples
        for faq in self.faq:
            if any(keyword in consulta_lower for keyword in 
                   faq["pregunta"].lower().split()):
                resultados.append(faq)
        
        return resultados[:3]  # Máximo 3 resultados
    
    def obtener_estado_servicio(self, servicio: str) -> str:
        """Obtiene el estado de un servicio específico"""
        return self.servicios.get(servicio.lower(), "desconocido")
    
    def crear_ticket(self, ticket: Ticket) -> str:
        """Crea un nuevo ticket en el sistema"""
        self.tickets.append(ticket)
        logger.info(f"Ticket creado: {ticket.id} para {ticket.usuario}")
        return ticket.id

class ClasificadorConsultas:
    """Clasifica consultas entrantes en categorías"""
    
    CATEGORIAS = {
        "cuentas": ["contraseña", "password", "cuenta", "usuario", "login", "acceso"],
        "conectividad": ["wifi", "internet", "conexión", "red", "vpn"],
        "software": ["programa", "aplicación", "office", "adobe", "licencia"],
        "correo": ["email", "correo", "outlook", "mail"],
        "hardware": ["ordenador", "impresora", "pantalla", "teclado", "ratón"],
        "plataformas": ["campus", "moodle", "blackboard", "plataforma"],
        "general": ["ayuda", "soporte", "problema", "error"]
    }
    
    def clasificar(self, consulta: str) -> str:
        """Clasifica una consulta en una categoría"""
        consulta_lower = consulta.lower()
        
        for categoria, palabras_clave in self.CATEGORIAS.items():
            if any(palabra in consulta_lower for palabra in palabras_clave):
                return categoria
        
        return "general"

class AgenteSoporteTecnico:
    """Agente principal de soporte técnico"""
    
    def __init__(self):
        self.bd = BaseDeDatos()
        self.clasificador = ClasificadorConsultas()
        self.contador_tickets = 1000  # Empezar en 1000 para IDs más realistas
        
    def procesar_consulta(self, usuario: str, consulta: str) -> Dict[str, Any]:
        """Procesa una consulta de usuario y genera respuesta"""
        logger.info(f"Procesando consulta de {usuario}: {consulta[:50]}...")
        
        # Clasificar la consulta
        categoria = self.clasificador.clasificar(consulta)
        
        # Buscar en FAQ primero
        resultados_faq = self.bd.buscar_faq(consulta)
        
        if resultados_faq:
            # Encontró respuesta en FAQ
            return {
                "tipo": "respuesta_directa",
                "categoria": categoria,
                "respuesta": resultados_faq[0]["respuesta"],
                "fuente": "FAQ",
                "respuestas_adicionales": resultados_faq[1:] if len(resultados_faq) > 1 else None
            }
        
        # Si no encuentra en FAQ, verificar si es consulta de estado
        if any(word in consulta.lower() for word in ["estado", "funciona", "disponible", "caído"]):
            return self._manejar_consulta_estado(consulta, categoria)
        
        # Si no puede resolver automáticamente, crear ticket
        return self._crear_ticket_automatico(usuario, consulta, categoria)
    
    def _manejar_consulta_estado(self, consulta: str, categoria: str) -> Dict[str, Any]:
        """Maneja consultas sobre el estado de servicios"""
        # Mapear categorías a servicios
        mapeo_servicios = {
            "correo": "correo",
            "conectividad": "wifi",
            "plataformas": "campus_virtual"
        }
        
        servicio = mapeo_servicios.get(categoria, "general")
        estado = self.bd.obtener_estado_servicio(servicio)
        
        estados_texto = {
            "operativo": "está funcionando correctamente",
            "mantenimiento": "está en mantenimiento programado",
            "parcial": "tiene funcionamiento limitado", 
            "caído": "está temporalmente fuera de servicio",
            "desconocido": "no tengo información actualizada"
        }
        
        return {
            "tipo": "estado_servicio",
            "categoria": categoria,
            "servicio": servicio,
            "estado": estado,
            "respuesta": f"El servicio de {servicio} {estados_texto[estado]}. "
                        f"Para más información, consulta https://status.universidad.edu"
        }
    
    def _crear_ticket_automatico(self, usuario: str, consulta: str, categoria: str) -> Dict[str, Any]:
        """Crea un ticket automáticamente cuando no puede resolver la consulta"""
        
        # Determinar prioridad basada en categoría
        prioridades = {
            "hardware": "alta",
            "conectividad": "media", 
            "cuentas": "media",
            "software": "baja",
            "general": "baja"
        }
        
        prioridad = prioridades.get(categoria, "baja")
        
        # Crear ticket
        ticket = Ticket(
            id=f"TICK-{self.contador_tickets}",
            usuario=usuario,
            categoria=categoria,
            descripcion=consulta,
            estado="nuevo",
            prioridad=prioridad,
            fecha_creacion=datetime.now()
        )
        
        self.contador_tickets += 1
        ticket_id = self.bd.crear_ticket(ticket)
        
        return {
            "tipo": "ticket_creado",
            "categoria": categoria,
            "ticket_id": ticket_id,
            "prioridad": prioridad,
            "respuesta": f"He creado el ticket {ticket_id} para tu consulta. "
                        f"Un técnico te contactará según la prioridad ({prioridad}). "
                        f"Puedes hacer seguimiento en https://tickets.universidad.edu/{ticket_id}"
        }
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Genera estadísticas de uso del agente"""
        total_tickets = len(self.bd.tickets)
        tickets_por_categoria = {}
        
        for ticket in self.bd.tickets:
            categoria = ticket.categoria
            tickets_por_categoria[categoria] = tickets_por_categoria.get(categoria, 0) + 1
        
        return {
            "total_tickets": total_tickets,
            "tickets_por_categoria": tickets_por_categoria,
            "servicios_monitorizados": len(self.bd.servicios),
            "faq_disponibles": len(self.bd.faq)
        }

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del agente
    agente = AgenteSoporteTecnico()
    
    # Ejemplos de consultas
    consultas_ejemplo = [
        ("juan.perez@alumnos.uni.edu", "¿Cómo cambio mi contraseña?"),
        ("maria.garcia@profesores.uni.edu", "No puedo conectarme al WiFi"),
        ("admin@uni.edu", "¿Está funcionando el correo?"),
        ("estudiante@uni.edu", "Mi ordenador no arranca en el laboratorio 3")
    ]
    
    print("=== AGENTE DE SOPORTE TÉCNICO UNIVERSITARIO ===\n")
    
    for usuario, consulta in consultas_ejemplo:
        print(f"👤 Usuario: {usuario}")
        print(f"❓ Consulta: {consulta}")
        
        respuesta = agente.procesar_consulta(usuario, consulta)
        
        print(f"🤖 Respuesta: {respuesta['respuesta']}")
        print(f"📋 Tipo: {respuesta['tipo']} | Categoría: {respuesta['categoria']}")
        print("-" * 80)
    
    # Mostrar estadísticas
    stats = agente.obtener_estadisticas()
    print("\n📊 ESTADÍSTICAS:")
    print(f"Total tickets creados: {stats['total_tickets']}")
    print(f"Tickets por categoría: {stats['tickets_por_categoria']}")
```

---

## 🎯 Ejercicios Propuestos

### Ejercicio 1: Personalización Básica (30 min)
**Objetivo**: Adaptar el agente a tu universidad específica

**Tareas**:
1. Modificar las FAQ con información real de tu universidad
2. Actualizar las URLs y contactos
3. Añadir 3 categorías nuevas específicas de tu contexto

### Ejercicio 2: Mejora con Copilot (45 min)
**Objetivo**: Usar GitHub Copilot para añadir funcionalidades

**Tareas**:
1. Añadir función de detección de idioma (español/inglés)
2. Implementar respuestas automáticas por email
3. Crear función de análisis de sentimiento básico

### Ejercicio 3: Integración Avanzada (60 min)
**Objetivo**: Conectar con APIs reales

**Tareas**:
1. Integrar con API de estado de servicios real
2. Conectar con sistema de tickets existente
3. Añadir autenticación básica

### Ejercicio 4: Interface de Usuario (45 min)
**Objetivo**: Crear una interfaz simple con Streamlit

**Tareas**:
1. Crear interfaz web básica
2. Mostrar historial de conversación
3. Añadir panel de estadísticas

---

## 📝 Guía para el Instructor

### Puntos Clave a Enfatizar:
1. **Modularidad**: Cada componente tiene responsabilidad específica
2. **Logging**: Importancia de rastrear interacciones
3. **Escalabilidad**: Cómo crece el sistema con más usuarios
4. **Mantenimiento**: Actualización de FAQ y conocimiento

### Adaptaciones Posibles:
- **Nivel Básico**: Usar solo FAQ estática
- **Nivel Intermedio**: Añadir clasificación automática
- **Nivel Avanzado**: Integración con LangChain para NLP

### Extensiones Sugeridas:
- Integración con ChatGPT/Claude para respuestas más naturales
- Base de datos real (PostgreSQL/MySQL)
- Notificaciones por Slack/Teams
- Dashboard de métricas en tiempo real

---

## 🔧 Instalación y Configuración

### Dependencias:
```bash
pip install streamlit pandas python-dotenv requests
```

### Variables de Entorno (.env):
```bash
# Configuración del agente
UNIVERSIDAD_NOMBRE="Universidad Ejemplo"
UNIVERSIDAD_DOMINIO="universidad.edu"
TICKETS_BASE_URL="https://tickets.universidad.edu"
STATUS_API_URL="https://status.universidad.edu/api"

# APIs opcionales
OPENAI_API_KEY="tu_clave_si_usas_gpt"
SMTP_SERVER="smtp.universidad.edu"
SMTP_PORT="587"
```

### Ejecución:
```bash
# Modo consola
python agente_soporte.py

# Interfaz web (si implementas Streamlit)
streamlit run interfaz_web.py
```

---

*Este template proporciona una base sólida para desarrollar agentes de soporte técnico adaptados a entornos universitarios. Úsalo como punto de partida y personalízalo según las necesidades específicas de tu institución.*
