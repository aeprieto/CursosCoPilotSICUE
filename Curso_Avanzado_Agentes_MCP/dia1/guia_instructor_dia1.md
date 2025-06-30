# Día 1: Arquitecturas Avanzadas de Agentes

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---|---|---|---|---|
| 09:00-09:15 | Bienvenida y objetivos del curso | 15min | Plenario | `bienvenida.md` |
| 09:15-11:15 | Arquitecturas de agentes y frameworks avanzados | 2h | Teórico-Práctico | `arquitecturas_agentes.md` |
| 11:15-11:45 | **PAUSA - CAFÉ** | 30min | - | - |
| 11:45-14:00 | Taller: Implementación de agentes ReAct y sistemas multi-agente | 2.25h | Práctico | `implementacion_react.md` |

## 🎯 Objetivos del Día

Al finalizar el día 1, los participantes podrán:

1.  ✅ **Distinguir entre arquitecturas** ReAct, Chain of Thought y Tree of Thoughts
2.  ✅ **Implementar un agente ReAct** funcional con LangChain
3.  ✅ **Comparar frameworks** LangChain vs CrewAI vs AutoGen
4.  ✅ **Diseñar arquitecturas** para sistemas multi-agente
5.  ✅ **Identificar patrones** de comunicación entre agentes

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
pip install streamlit # Para interfaces rápidas
pip install python-dotenv # Para variables de entorno
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

## ✅ Finalización del curso

La finalización del curso se basa en la **asistencia**. No hay evaluación formal ni entrega de proyectos. El objetivo es **aprender haciendo** en un entorno práctico y colaborativo.
