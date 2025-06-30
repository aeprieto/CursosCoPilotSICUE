# Introducción a Agentes Conversacionales

## 🎯 Objetivos de la Sesión (1.5 horas)

Al finalizar esta sesión, los participantes comprenderán:
- Qué son los agentes conversacionales y cómo funcionan
- Diferencias entre chatbots simples y agentes inteligentes
- Componentes clave: memoria, herramientas, y contexto
- Arquitectura básica de un sistema conversacional

---

## 🤖 ¿Qué es un Agente Conversacional?

### Definición
> Un agente conversacional es un sistema de IA que puede **mantener diálogos naturales** con usuarios humanos, **recordar el contexto** de la conversación, y **usar herramientas externas** para proporcionar información útil y realizar acciones.

### Evolución: De Chatbots a Agentes

```
Chatbots Básicos → Chatbots con IA → Agentes Conversacionales
     |                    |                      |
Respuestas fijas    Respuestas generadas    Acciones + Memoria
Sin contexto        Contexto limitado       Contexto persistente
Sin herramientas    Herramientas básicas    Herramientas complejas
```

---

## 🧩 Componentes Clave de un Agente Conversacional

### 1. 🧠 **Modelo de Lenguaje (LLM)**
**Función**: Núcleo de comprensión y generación de texto

**Características**:
- Comprende intención del usuario
- Genera respuestas coherentes
- Mantiene estilo conversacional

**Ejemplos**:
- **GPT-4**: Muy capaz, pero requiere API key
- **Claude**: Excelente para razonamiento
- **Llama 2**: Open source, puede ejecutarse localmente

### 2. 💾 **Sistema de Memoria**
**Función**: Mantener contexto y recordar información

**Tipos de Memoria**:
- **Memoria de Trabajo**: Conversación actual
- **Memoria Semántica**: Conocimientos generales
- **Memoria Episódica**: Interacciones anteriores específicas

**Ejemplo Práctico**:
```python
# Conversación sin memoria
Usuario: "¿Cuál es el horario de la biblioteca?"
Agente: "La biblioteca está abierta de 8:00 a 22:00"
Usuario: "¿Y los sábados?"
Agente: "¿Sobre qué necesitas información?" # ❌ Perdió contexto

# Conversación con memoria
Usuario: "¿Cuál es el horario de la biblioteca?"
Agente: "La biblioteca está abierta de 8:00 a 22:00"
Usuario: "¿Y los sábados?"
Agente: "Los sábados la biblioteca abre de 9:00 a 18:00" # ✅ Mantiene contexto
```

### 3. 🛠️ **Herramientas (Tools)**
**Función**: Capacidades para interactuar con el mundo exterior

**Ejemplos de Herramientas**:
- **Calculadora**: Para cálculos matemáticos
- **Búsqueda Web**: Para información actualizada
- **Base de Datos**: Para consultar datos específicos
- **API Externa**: Para servicios especializados
- **Envío de Email**: Para comunicación

**Patrón de Uso**:
```
Usuario: "¿Cuántos estudiantes hay matriculados este semestre?"
Agente: [Usa herramienta: consulta_bd_estudiantes()]
Agente: "Actualmente hay 18,247 estudiantes matriculados"
```

### 4. 🎯 **Sistema de Planificación**
**Función**: Decidir qué hacer y en qué orden

**Proceso de Decisión**:
1. **Analizar** la pregunta del usuario
2. **Determinar** qué herramientas necesita
3. **Planificar** secuencia de acciones
4. **Ejecutar** plan paso a paso
5. **Sintetizar** respuesta final

---

## 🏗️ Arquitectura de un Agente Conversacional

### Diagrama de Flujo Básico

```
[Usuario] → [Procesamiento de Entrada] → [Análisis de Intención]
                                              ↓
[Respuesta] ← [Síntesis de Respuesta] ← [Planificación de Acción]
     ↓                                        ↓
[Interfaz] ← [Formateo] ← [Memoria] ← [Ejecución de Herramientas]
```

### Ejemplo de Arquitectura en Código

```python
class AgenteConversacional:
    def __init__(self):
        self.llm = ChatOpenAI()  # Modelo de lenguaje
        self.memory = ConversationBufferMemory()  # Sistema de memoria
        self.tools = [
            calculadora_tool,
            consulta_bd_tool,
            envio_email_tool
        ]
        self.agent = create_agent(self.llm, self.tools, self.memory)
    
    def procesar_mensaje(self, mensaje_usuario):
        # 1. Analizar entrada
        intencion = self.analizar_intencion(mensaje_usuario)
        
        # 2. Planificar respuesta
        plan = self.planificar_accion(intencion)
        
        # 3. Ejecutar herramientas si es necesario
        resultados = self.ejecutar_herramientas(plan)
        
        # 4. Generar respuesta
        respuesta = self.generar_respuesta(resultados)
        
        # 5. Actualizar memoria
        self.memory.save_context({"input": mensaje_usuario}, {"output": respuesta})
        
        return respuesta
```

---

## 🎯 Casos de Uso Universitarios Específicos

### 1. 🎓 **Asistente Académico**
**Funcionalidades**:
- Consultar horarios de clases
- Información sobre profesores y asignaturas
- Fechas de exámenes y entregas
- Requisitos de matriculación

**Herramientas Necesarias**:
- API del sistema académico
- Base de datos de profesores
- Calendario académico
- Sistema de notas

### 2. 🔧 **Agente de Soporte IT**
**Funcionalidades**:
- Resolver problemas técnicos comunes
- Gestionar tickets de soporte
- Información sobre servicios IT
- Guías de troubleshooting

**Herramientas Necesarias**:
- Base de conocimiento IT
- Sistema de tickets
- Monitor de servicios
- Scripts de diagnóstico

### 3. 📚 **Asistente de Biblioteca**
**Funcionalidades**:
- Búsqueda de recursos bibliográficos
- Reserva de espacios de estudio
- Información sobre servicios
- Ayuda con citas bibliográficas

**Herramientas Necesarias**:
- Catálogo bibliográfico
- Sistema de reservas
- Generador de citas
- API de bases de datos académicas

### 4. 🏢 **Asistente Administrativo**
**Funcionalidades**:
- Trámites administrativos
- Información sobre becas
- Consultas sobre normativas
- Gestión de documentos

**Herramientas Necesarias**:
- Sistema de gestión académica
- Base de datos de becas
- Repositorio de normativas
- Generador de documentos

---

## 🔄 Flujos de Conversación Típicos

### Flujo 1: Consulta Simple
```
Usuario: "¿Cuál es el horario de atención del decanato?"
   ↓
Agente: [Consulta base de datos] → "El decanato atiende de lunes a viernes de 9:00 a 14:00"
```

### Flujo 2: Consulta Compleja con Seguimiento
```
Usuario: "Necesito información sobre la asignatura de Bases de Datos"
   ↓
Agente: [Consulta académica] → "La asignatura tiene 6 créditos, profesor Juan Pérez..."
   ↓
Usuario: "¿Cuáles son los horarios?"
   ↓
Agente: [Memoria: recordar asignatura] + [Consulta horarios] → "Los horarios son..."
```

### Flujo 3: Acción con Confirmación
```
Usuario: "Quiero reservar una sala de estudio"
   ↓
Agente: "¿Para qué fecha y hora?" 
   ↓
Usuario: "Mañana a las 15:00"
   ↓
Agente: [Consulta disponibilidad] → "Hay disponibilidad. ¿Confirmas la reserva?"
   ↓
Usuario: "Sí"
   ↓
Agente: [Ejecuta reserva] → "Reserva confirmada. Código: R12345"
```

---

## ⚡ Actividad Práctica: Diseño de Agente (30 minutos)

### Ejercicio: Diseñar tu Agente Universitario

**Instrucciones**:
1. **Elegir un área** (IT, académica, biblioteca, administración)
2. **Definir 5 funcionalidades** principales
3. **Identificar herramientas** necesarias
4. **Diseñar 3 flujos** de conversación típicos
5. **Presentar** diseño al grupo (5 min por equipo)

### Plantilla de Diseño:

```
ÁREA ELEGIDA: _________________

FUNCIONALIDADES:
1. ________________________
2. ________________________
3. ________________________
4. ________________________
5. ________________________

HERRAMIENTAS NECESARIAS:
- _______________________
- _______________________
- _______________________

FLUJO DE CONVERSACIÓN EJEMPLO:
Usuario: "________________"
Agente: "________________"
Usuario: "________________"
Agente: "________________"
```

### Criterios de Evaluación:
- **Utilidad práctica** (¿Resuelve problemas reales?)
- **Viabilidad técnica** (¿Es implementable?)
- **Experiencia de usuario** (¿Es fácil de usar?)

---

## 🔍 Comparación: Agentes vs Alternativas

### vs. Formularios Web Tradicionales

| Aspecto | Formularios Web | Agentes Conversacionales |
|---------|-----------------|---------------------------|
| **Interfaz** | Campos fijos | Lenguaje natural |
| **Flexibilidad** | Limitada | Alta |
| **Accesibilidad** | Requiere conocimiento previo | Intuitivo |
| **Mantenimiento** | Alto (cada cambio = nuevo formulario) | Bajo (se adapta automáticamente) |
| **Casos complejos** | Requiere múltiples formularios | Un solo flujo |

### vs. Sistemas de Tickets Tradicionales

| Aspecto | Tickets Tradicionales | Agentes Inteligentes |
|---------|----------------------|---------------------|
| **Tiempo de respuesta** | Horas/días | Instantáneo |
| **Disponibilidad** | Horario laboral | 24/7 |
| **Escalabilidad** | Limitada por personal | Ilimitada |
| **Consistencia** | Varía por técnico | Siempre consistente |
| **Aprendizaje** | Manual | Automático |

---

## 🎯 Métricas de Éxito para Agentes

### Métricas Técnicas:
- **Tiempo de respuesta**: < 3 segundos
- **Precisión de respuestas**: > 85%
- **Disponibilidad**: > 99%
- **Tasa de error**: < 5%

### Métricas de Usuario:
- **Satisfacción**: > 4.0/5.0
- **Resolución en primera interacción**: > 70%
- **Adopción**: > 60% de usuarios objetivo
- **Reducción de tickets**: > 30%

### Métricas de Negocio:
- **Ahorro de costes**: Medible en horas de personal
- **Mejora en tiempos**: Medible en tiempo de resolución
- **Escalabilidad**: Capacidad de manejar más usuarios sin más personal

---

## 🔗 Frameworks y Herramientas Principales

### 1. **LangChain** 🦜
**Pros**: Muy completo, gran ecosistema, bien documentado
**Cons**: Curva de aprendizaje, puede ser complejo
**Mejor para**: Aplicaciones complejas con múltiples integraciones

### 2. **Rasa** 🤖
**Pros**: Open source, muy personalizable, control total
**Cons**: Requiere más desarrollo, setup complejo
**Mejor para**: Casos que requieren privacidad total de datos

### 3. **Botpress** 💬
**Pros**: Interfaz visual, fácil de usar, deployment sencillo
**Cons**: Menos flexible para casos complejos
**Mejor para**: Prototipos rápidos y casos de uso simples

### 4. **Microsoft Bot Framework** 🏢
**Pros**: Integración con ecosistema Microsoft, enterprise-ready
**Cons**: Vendor lock-in, requiere Azure
**Mejor para**: Organizaciones ya en ecosistema Microsoft

---

## 📝 Puntos Clave para Recordar

1. **Los agentes conversacionales** son más que chatbots: tienen memoria, herramientas y capacidad de planificación
2. **La memoria es crucial** para mantener conversaciones naturales
3. **Las herramientas permiten** que el agente interactúe con el mundo real
4. **El diseño del flujo conversacional** es tan importante como la tecnología
5. **Empezar simple** e iterar basándose en feedback real de usuarios

---

## 🔗 Referencias y Lecturas Adicionales

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction.html)
- [Conversational AI Best Practices](https://www.rasa.com/docs/rasa/conversation-driven-development/)
- [Building Chatbots with Python](https://realpython.com/build-a-chatbot-python-chatterbot/)
- [Microsoft Bot Framework](https://docs.microsoft.com/en-us/azure/bot-service/)

---

**Siguiente tema**: LangChain Básico - Instalación, configuración y creación del primer agente funcional
