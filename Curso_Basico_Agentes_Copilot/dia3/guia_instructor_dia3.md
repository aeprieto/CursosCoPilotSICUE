# Día 3: Agentes Simples y APIs

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---|---|---|---|---|
| 09:00-09:15 | Repaso días anteriores y dudas | 15min | Plenario | `repaso_dias_anteriores.md` |
| 09:15-11:15 | Introducción a agentes conversacionales y LangChain | 2h | Teórico-Práctico | `introduccion_agentes_conversacionales.md` |
| 11:15-11:45 | **PAUSA - CAFÉ** | 30min | - | - |
| 11:45-14:00 | Taller práctico: Creación de un agente con APIs REST | 2.25h | Práctico | `integracion_apis.md` |

## 🎯 Objetivos del Día

Al finalizar el día 3, los participantes podrán:

1.  ✅ **Entender los conceptos** básicos de agentes conversacionales
2.  ✅ **Usar LangChain** para crear agentes simples
3.  ✅ **Integrar agentes** con APIs REST externas
4.  ✅ **Desarrollar un agente** que responda preguntas usando datos externos
5.  ✅ **Manejar errores** y casos edge en la comunicación con APIs

## 🧠 Conceptos Clave del Día

### Agentes Conversacionales:
- **Memory**: Mantener contexto entre interacciones
- **Tools**: Herramientas que el agente puede usar
- **Chains**: Secuencias de operaciones conectadas
- **Prompts**: Templates para guiar el comportamiento

### LangChain Básico:
- **LLMs**: Modelos de lenguaje
- **Chat Models**: Modelos optimizados para conversación
- **Agents**: Entidades que pueden usar herramientas
- **Retrievers**: Sistemas de búsqueda de información

### Integración APIs:
- **REST APIs**: Protocolo estándar de comunicación
- **Authentication**: Manejo de tokens y credenciales
- **Error Handling**: Gestión robusta de fallos
- **Rate Limiting**: Respeto a límites de uso

## 💻 Stack Técnico del Día

```bash
# Instalar dependencias adicionales para el día 3
pip install langchain langchain-openai langchain-community
pip install requests beautifulsoup4
pip install python-dotenv
pip install streamlit # Para crear interfaces rápidas
pip install httpx # Cliente HTTP asíncrono
```

## 🔧 Configuración del Entorno

### Variables de Entorno (.env):
```bash
# APIs de LLM (usar al menos una)
OPENAI_API_KEY=tu_clave_openai
ANTHROPIC_API_KEY=tu_clave_claude

# APIs universitarias simuladas
UNIVERSITY_API_URL=http://localhost:8000
UNIVERSITY_API_KEY=demo_key_12345

# Configuración del agente
AGENT_NAME=AgenteSI_Universidad
DEFAULT_LANGUAGE=es
MAX_TOKENS=1000
```

## 🎯 Ejercicios Principales del Día

### Ejercicio 1: Primer Agente con LangChain (45 min)
**Objetivo**: Crear un agente básico que puede usar herramientas simples

### Ejercicio 2: Agente con Memoria (30 min)
**Objetivo**: Añadir capacidad de recordar conversaciones anteriores

### Ejercicio 3: Integración con API Universitaria (60 min)
**Objetivo**: Conectar agente con API de información estudiantil

### Ejercicio 4: Agente de Consulta Integral (45 min)
**Objetivo**: Combinar múltiples fuentes de datos en un solo agente

## ✅ Finalización del curso

La finalización del curso se basa en la **asistencia**. No hay evaluación formal ni entrega de proyectos. El objetivo es **aprender haciendo** en un entorno práctico y colaborativo.

## 📚 Material para Casa

- **Lectura**: `recursos/langchain_advanced_concepts.pdf`
- **Práctica**: Extender el agente con una API adicional
- **Preparación**: Pensar en caso de uso específico para día 4

## 📞 Contacto y Dudas

- Canal Slack: `#curso-dia3`
- Email instructor: [correo]
- Office hours: Mañana 10:00-11:00

---

**Próximo día**: Agentes para Soporte Técnico - Aplicación práctica en el contexto del Servicio de Informática
