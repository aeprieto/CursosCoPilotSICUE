# Conceptos Fundamentales de IA y Agentes

## 🎯 Objetivos de la Sesión (1 hora)

Al finalizar esta sesión, los participantes comprenderán:
- Qué es la Inteligencia Artificial Generativa
- Diferencias entre chatbots, agentes y asistentes
- El panorama actual de herramientas de IA
- Aplicaciones específicas en entornos universitarios

> **📁 Ejemplos Prácticos**: 
> - `ejemplo_funciones.py` - Funciones básicas de IA para experimentar
> - `demo_conceptos_interactiva.py` - Demo interactiva de todos los conceptos explicados en esta sesión

---

## 🧠 ¿Qué es la Inteligencia Artificial Generativa?

### Definición Simple
> La IA Generativa es un tipo de inteligencia artificial capaz de **crear contenido nuevo** (texto, código, imágenes, etc.) basándose en patrones aprendidos de grandes cantidades de datos.

### Ejemplos Cotidianos
- **ChatGPT**: Genera texto conversacional
- **GitHub Copilot**: Genera código de programación  
- **DALL-E**: Genera imágenes desde texto
- **Claude**: Asistente conversacional avanzado

### ¿Cómo Funciona? (Simplificado)
1. **Entrenamiento**: Se alimenta con millones de ejemplos
2. **Patrones**: Aprende relaciones y estructuras
3. **Generación**: Predice qué viene después basándose en el contexto
4. **Refinamiento**: Se mejora con feedback humano

---

## 🤖 Taxonomía: Chatbots vs Agentes vs Asistentes

### 📱 Chatbots
**Definición**: Programas que simulan conversación humana de forma básica.

**Características**:
- Respuestas predefinidas o basadas en reglas simples
- Interacción principalmente reactiva
- Limitados a su dominio específico

**Ejemplos**:
- Bot de atención al cliente de una web
- FAQ automatizado
- Bot de reservas simple

**Casos de Uso Universitarios**:
- Información sobre horarios de biblioteca
- Consultas sobre matrículas básicas
- Estado de servicios IT

### 🧠 Agentes de IA
**Definición**: Sistemas que pueden **actuar de forma autónoma** para alcanzar objetivos específicos.

**Características**:
- Capacidad de **tomar decisiones**
- Pueden **usar herramientas** (APIs, bases de datos, etc.)
- **Planifican** secuencias de acciones
- **Aprenden** de la experiencia

**Ejemplos**:
- Agente que gestiona tickets de soporte automáticamente
- Sistema que optimiza horarios de clases
- Agente que monitoriza y repara problemas de red

**Casos de Uso Universitarios**:
- Gestión automática de incidencias IT
- Asignación inteligente de recursos
- Monitorización proactiva de sistemas

### 🎯 Asistentes Inteligentes
**Definición**: Combinan capacidades conversacionales con acceso a herramientas y datos.

**Características**:
- **Conversación natural** + **Acciones concretas**
- Acceso a múltiples fuentes de información
- Contextualización avanzada
- Interfaz unificada para múltiples tareas

**Ejemplos**:
- GitHub Copilot (asiste en programación)
- Claude con acceso a herramientas
- Asistentes empresariales con integración ERP

**Casos de Uso Universitarios**:
- Asistente integral para estudiantes
- Soporte técnico de nivel 1-2 automatizado
- Análisis de datos institucionales

---

## 🌍 Panorama Actual de Herramientas

### Principales Proveedores

| Empresa | Producto Principal | Fortalezas | Uso Típico |
|---------|-------------------|------------|------------|
| **OpenAI** | ChatGPT, GPT-4 | Conversación, creatividad | Chatbots, análisis de texto |
| **Anthropic** | Claude | Razonamiento, herramientas | Asistentes complejos, análisis |
| **Microsoft** | Copilot, Azure AI | Integración empresarial | Productividad, desarrollo |
| **Google** | Gemini, Bard | Multimodal, búsqueda | Investigación, análisis |
| **GitHub** | Copilot | Programación | Desarrollo de software |

### Herramientas Open Source

| Herramienta | Descripción | Ventajas para Universidades |
|-------------|-------------|----------------------------|
| **LangChain** | Framework para desarrollar aplicaciones LLM | Gratuito, flexible, gran comunidad |
| **CrewAI** | Plataforma para agentes colaborativos | Especializado en multi-agentes |
| **Ollama** | LLMs locales | Sin envío de datos a terceros |
| **AutoGen** | Framework de Microsoft para agentes | Integración con ecosistema Microsoft |

---

## 🏫 Aplicaciones en Entornos Universitarios

### 🔧 Servicio de Informática

#### Casos de Uso Inmediatos:
1. **Automatización de Tickets**
   - Clasificación automática por urgencia
   - Respuestas automáticas para problemas comunes
   - Escalado inteligente a técnicos especializados

2. **Gestión de Usuarios**
   - Creación/eliminación masiva de cuentas
   - Restablecimiento de contraseñas automatizado
   - Auditoría de permisos

3. **Monitorización Proactiva**
   - Detección temprana de problemas
   - Análisis de logs automatizado
   - Informes de rendimiento automáticos

#### Casos de Uso Avanzados:
1. **Asistente IT Integral**
   - Soporte multi-idioma para estudiantes internacionales
   - Integración con sistemas académicos
   - Análisis predictivo de incidencias

2. **Optimización de Recursos**
   - Gestión inteligente de laboratorios
   - Planificación de mantenimientos
   - Análisis de uso de software/licencias

### 📚 Otros Departamentos Universitarios

#### Biblioteca:
- Asistente de búsqueda bibliográfica
- Catalogación automática
- Recomendaciones personalizadas

#### Administración:
- Chatbot para consultas administrativas
- Automatización de procesos burocráticos
- Análisis de satisfacción estudiantil

#### Académico:
- Asistentes para creación de contenidos
- Corrección automática (nivel básico)
- Análisis de rendimiento académico

---

## ⚡ Actividad Práctica (15 minutos)

### Ejercicio: Identifica el Tipo

**Instrucciones**: Para cada escenario, identifica si es un **Chatbot**, **Agente** o **Asistente**:

1. **Escenario A**: Un sistema que responde "Los horarios de biblioteca son de 8:00 a 22:00" cuando preguntas por horarios.
   - **Respuesta**: _Chatbot_ (respuesta predefinida)

2. **Escenario B**: Un sistema que detecta que un servidor está sobrecargado, automáticamente escala recursos, y notifica al administrador.
   - **Respuesta**: _Agente_ (acción autónoma)

3. **Escenario C**: Un sistema con el que puedes conversar en lenguaje natural, que puede consultar tu expediente académico, hacer cálculos, y enviarte emails con resúmenes.
   - **Respuesta**: _Asistente_ (conversación + herramientas)

### Reflexión en Grupos (10 minutos)
**Pregunta**: ¿Qué tipo de herramienta sería más útil para vuestro trabajo diario en el Servicio de Informática? ¿Por qué?

---

## 📝 Puntos Clave para Recordar

1. **La IA Generativa** es la base tecnológica que permite todas estas herramientas
2. **Los Agentes** son más que chatbots: pueden actuar y tomar decisiones
3. **GitHub Copilot** es un asistente especializado en programación
4. **En entornos universitarios** hay múltiples oportunidades de aplicación
5. **Empezar con casos simples** y evolucionar hacia soluciones más complejas

---

## 🔗 Referencias y Lecturas Adicionales

- [IBM: ¿Qué es la IA Generativa?](https://www.ibm.com/es-es/topics/generative-ai)
- [Microsoft: Introduction to AI Agents](https://docs.microsoft.com/en-us/azure/cognitive-services/)
- [LangChain Documentation](https://python.langchain.com/)
- [GitHub Copilot: Getting Started](https://docs.github.com/en/copilot)

---

**Siguiente tema**: GitHub Copilot en Profundidad - Instalación, configuración y primeros pasos
