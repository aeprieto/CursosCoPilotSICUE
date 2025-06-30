# agente_simple.py
# Archivo para construir un agente conversacional simple con LangChain.

# --- PREPARACIÓN ---
# 1. Asegúrate de tener un fichero .env en esta carpeta con tu OPENAI_API_KEY
#    OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# 2. Ejecuta `pip install langchain langchain-openai python-dotenv`

import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# --- EJERCICIO 1: Definir Herramientas ---
# Crea dos herramientas simples que el agente pueda usar.

@tool
def obtener_hora_actual():
    """Devuelve la hora actual."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

@tool
def buscar_info_universidad(termino: str):
    """Busca información simulada sobre la universidad.""" 
    # En un caso real, aquí llamaríamos a una API o base de datos.
    base_de_datos_simulada = {
        "horario de secretaría": "Lunes a Viernes de 9:00 a 14:00",
        "biblioteca": "Abierta de 8:30 a 21:00",
        "cafetería": "Abierta de 8:00 a 18:00"
    }
    return base_de_datos_simulada.get(termino.lower(), "No se encontró información sobre ese término.")

# --- EJERCICIO 2: Crear el Agente ---
# Configura el prompt, el modelo y el agente.

# 2.1. Define el prompt para que el agente sepa cómo comportarse.
# Pista: El sistema debe saber que tiene herramientas a su disposición.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente universitario muy útil. Tienes acceso a herramientas para responder preguntas."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 2.2. Inicializa el modelo de lenguaje.
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# 2.3. Junta las herramientas que creaste.
tools = [obtener_hora_actual, buscar_info_universidad]

# 2.4. Crea el agente y el ejecutor.
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- EJERCICIO 3: Probar el Agente ---
# Llama al agente con diferentes preguntas para ver cómo usa las herramientas.

if __name__ == "__main__":
    print("¡Hola! Soy tu asistente universitario. ¿En qué puedo ayudarte?")
    
    # Prueba 1: Usar la herramienta de la hora
    # agent_executor.invoke({"input": "¿Qué hora es?"})

    # Prueba 2: Usar la herramienta de información
    # agent_executor.invoke({"input": "¿Cuál es el horario de la biblioteca?"})

    # Prueba 3: Pregunta general (sin herramientas)
    # agent_executor.invoke({"input": "Explícame qué es la inteligencia artificial."})

    # Prueba interactiva
    while True:
        pregunta = input("> ")
        if pregunta.lower() in ["salir", "exit"]:
            break
        result = agent_executor.invoke({"input": pregunta})
        print(result["output"])
