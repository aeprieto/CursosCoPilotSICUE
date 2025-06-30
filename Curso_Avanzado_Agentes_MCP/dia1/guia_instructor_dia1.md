# Día 1: Arquitecturas Avanzadas de Agentes

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---------|-----------|----------|------|----------|
| 09:00-09:30 | Bienvenida y evaluación de prerrequisitos | 30min | Evaluación | `evaluacion_inicial.md` |
| 09:30-11:00 | Arquitecturas de agentes: ReAct, CoT, ToT | 1.5h | Teórico | `arquitecturas_agentes.md` |
| 11:00-11:15 | **DESCANSO** | 15min | - | - |
| 11:15-12:45 | Frameworks avanzados: LangChain, CrewAI, AutoGen | 1.5h | Teórico-Práctico | `frameworks_avanzados.md` |
| 12:45-13:45 | **ALMUERZO** | 1h | - | - |
| 13:45-15:15 | Implementación práctica de agentes ReAct | 1.5h | Práctico | `implementacion_react.md` |
| 15:15-15:30 | **DESCANSO** | 15min | - | - |
| 15:30-16:45 | Diseño de sistemas multi-agente | 1.25h | Diseño | `sistemas_multiagente.md` |
| 16:45-17:00 | Recapitulación y preparación día 2 | 15min | Plenario | `recapitulacion_dia1.md` |

## 🎯 Objetivos del Día

Al finalizar el día 1, los participantes podrán:

1. ✅ **Distinguir entre arquitecturas** ReAct, Chain of Thought y Tree of Thoughts
2. ✅ **Implementar un agente ReAct** funcional con LangChain
3. ✅ **Comparar frameworks** LangChain vs CrewAI vs AutoGen
4. ✅ **Diseñar arquitecturas** para sistemas multi-agente
5. ✅ **Identificar patrones** de comunicación entre agentes

## 🧠 Conceptos Clave del Día

### Arquitecturas de Razonamiento:
- **ReAct**: Reasoning + Acting (Razonamiento + Acción)
- **Chain of Thought**: Razonamiento paso a paso
- **Tree of Thoughts**: Exploración de múltiples caminos de razonamiento

### Frameworks de Desarrollo:
- **LangChain**: Framework general para aplicaciones LLM
- **CrewAI**: Especializado en equipos de agentes
- **AutoGen**: Multi-agent conversations (Microsoft)

### Patrones de Arquitectura:
- **Pipeline**: Agentes en secuencia
- **Orchestrator**: Agente coordinador central
- **Mesh**: Comunicación directa entre agentes
- **Hierarchical**: Estructura jerárquica de agentes

## 💻 Stack Técnico del Día

```bash
# Instalar dependencias para el día 1
pip install langchain langchain-openai langchain-community
pip install crewai
pip install pyautogen
pip install streamlit  # Para interfaces rápidas
pip install python-dotenv  # Para variables de entorno
```

## 🎯 Ejercicios Principales

### Ejercicio 1: Agente ReAct Básico (45 min)
**Objetivo**: Implementar un agente que puede razonar y actuar
```python
# Template del ejercicio
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

# Los participantes implementarán:
# 1. Definir herramientas (calculadora, búsqueda, etc.)
# 2. Configurar el agente ReAct
# 3. Probar con diferentes tipos de preguntas
```

### Ejercicio 2: Comparativa de Frameworks (60 min)
**Objetivo**: Implementar el mismo caso de uso con 3 frameworks diferentes
- **LangChain**: Agente de soporte técnico
- **CrewAI**: Equipo de agentes colaborativos
- **AutoGen**: Conversación multi-agente

### Ejercicio 3: Diseño de Arquitectura (45 min)
**Objetivo**: Diseñar sistema multi-agente para caso universitario
- Identificar agentes necesarios
- Definir responsabilidades
- Diseñar flujos de comunicación
- Crear diagrama de arquitectura

## 📊 Evaluación del Día

### Quiz Técnico (15 min):
1. **¿Cuándo usar ReAct vs Chain of Thought?**
2. **¿Qué ventajas tiene CrewAI sobre LangChain para multi-agentes?**
3. **¿Cómo manejar la coordinación en un sistema mesh?**

### Evaluación Práctica (30 min):
- Implementar un agente ReAct que pueda:
  - Responder preguntas de cálculo
  - Buscar información en una base de datos simulada
  - Tomar decisiones basadas en criterios dados

### Criterios de Evaluación:
- **Comprensión técnica (40%)**
- **Implementación funcional (35%)**
- **Diseño de arquitectura (25%)**

## 🔧 Setup Técnico del Día

### Variables de Entorno Necesarias:
```bash
# Crear archivo .env
OPENAI_API_KEY=tu_clave_aqui  # Si usas OpenAI
ANTHROPIC_API_KEY=tu_clave_aqui  # Si usas Claude
LANGCHAIN_API_KEY=tu_clave_aqui  # Para LangSmith (opcional)
```

### Estructura de Carpetas:
```
dia1/
├── ejercicios/
│   ├── react_basico/
│   ├── comparativa_frameworks/
│   └── diseno_arquitectura/
├── ejemplos/
├── recursos/
└── resultados/
```

## 🚨 Troubleshooting Común

### Problemas de API:
- **Error de API Key**: Verificar variables de entorno
- **Rate limiting**: Usar delays entre llamadas
- **Costs concerns**: Usar modelos más baratos para pruebas

### Problemas de Código:
- **Imports fallando**: Verificar instalaciones de pip
- **Agentes no responden**: Revisar prompts y herramientas
- **Errores de formato**: Validar entrada/salida de herramientas

### Soluciones Preparadas:
1. **Mock APIs** para casos sin acceso a servicios reales
2. **Código de ejemplo** funcionando para cada ejercicio
3. **Documentación offline** de frameworks principales

## 📚 Material de Referencia del Día

### Documentación Esencial:
- [LangChain Agent Documentation](https://python.langchain.com/docs/modules/agents/)
- [CrewAI Official Docs](https://docs.crewai.com/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)

### Papers Académicos:
- **ReAct**: "ReAct: Synergizing Reasoning and Acting in Language Models"
- **Chain of Thought**: "Chain-of-Thought Prompting Elicits Reasoning"
- **Tree of Thoughts**: "Tree of Thoughts: Deliberate Problem Solving"

### Recursos Adicionales:
- Comparison matrix de frameworks
- Architectural patterns cheat sheet
- Decision tree para elegir arquitectura

## 📋 Checklist del Instructor

### Antes de la Sesión:
- [ ] Verificar que todos tienen las APIs configuradas
- [ ] Preparar ejemplos en vivo funcionando
- [ ] Configurar entorno de demostración
- [ ] Revisar tiempo estimado para cada ejercicio

### Durante la Sesión:
- [ ] Tomar attendance y evaluar nivel inicial
- [ ] Adaptar profundidad según nivel del grupo
- [ ] Documentar preguntas técnicas interesantes
- [ ] Asegurar que todos completan ejercicio mínimo

### Después de la Sesión:
- [ ] Compartir código de soluciones
- [ ] Enviar material de referencia adicional
- [ ] Preparar ajustes para día 2 basados en feedback

## 🎯 Preparación para Día 2

### Conceptos a Revisar:
- Repasar implementaciones del día 1
- Leer introducción al Model Context Protocol
- Instalar Claude Desktop

### Material para Casa:
- **Lectura**: `recursos/introduccion_mcp.pdf`
- **Práctica**: Completar ejercicio de arquitectura iniciado
- **Instalación**: Claude Desktop y configuración inicial

---

**Próximo día**: Model Context Protocol (MCP) - Fundamentos - Introducción al protocolo que permite extender las capacidades de Claude y otros LLMs
