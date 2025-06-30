import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
import json
import requests

# Cargar variables de entorno
load_dotenv()

class CalculadoraTool(BaseTool):
    """Herramienta simple de calculadora para demostrar ReAct"""
    name = "calculadora"
    description = "Útil para hacer cálculos matemáticos básicos. Input debe ser una expresión matemática válida."
    
    def _run(self, query: str) -> str:
        try:
            # Por seguridad, evaluamos solo expresiones básicas
            allowed_chars = "0123456789+-*/(). "
            if all(c in allowed_chars for c in query):
                result = eval(query)
                return f"El resultado de {query} es {result}"
            else:
                return "Error: Solo se permiten operaciones matemáticas básicas"
        except Exception as e:
            return f"Error al calcular: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("Esta herramienta no soporta ejecución asíncrona")

class ConsultorBaseDatosTool(BaseTool):
    """Simulador de consulta a base de datos universitaria"""
    name = "consultor_bd_universidad"
    description = "Consulta información de estudiantes, profesores y cursos de la universidad"
    
    # Datos simulados para la demo
    datos_universidad = {
        "estudiantes": [
            {"id": "12345", "nombre": "Ana García", "carrera": "Informática", "año": 3, "activo": True},
            {"id": "67890", "nombre": "Carlos López", "carrera": "Matemáticas", "año": 2, "activo": True},
            {"id": "11111", "nombre": "María Ruiz", "carrera": "Física", "año": 4, "activo": False}
        ],
        "profesores": [
            {"id": "prof001", "nombre": "Dr. Juan Pérez", "departamento": "Informática", "activo": True},
            {"id": "prof002", "nombre": "Dra. Elena Martín", "departamento": "Matemáticas", "activo": True}
        ],
        "cursos": [
            {"codigo": "INF101", "nombre": "Programación I", "profesor": "Dr. Juan Pérez", "creditos": 6},
            {"codigo": "MAT201", "nombre": "Álgebra Lineal", "profesor": "Dra. Elena Martín", "creditos": 4}
        ]
    }
    
    def _run(self, query: str) -> str:
        query_lower = query.lower()
        
        if "estudiante" in query_lower:
            if "ana" in query_lower or "12345" in query:
                return json.dumps(self.datos_universidad["estudiantes"][0], indent=2)
            elif "carlos" in query_lower or "67890" in query:
                return json.dumps(self.datos_universidad["estudiantes"][1], indent=2)
            elif "maría" in query_lower or "11111" in query:
                return json.dumps(self.datos_universidad["estudiantes"][2], indent=2)
            else:
                return "Estudiante no encontrado. Prueba con Ana García (12345), Carlos López (67890) o María Ruiz (11111)"
        
        elif "profesor" in query_lower:
            return json.dumps(self.datos_universidad["profesores"], indent=2)
        
        elif "curso" in query_lower:
            return json.dumps(self.datos_universidad["cursos"], indent=2)
        
        else:
            return "Consulta no reconocida. Puedes preguntar por estudiantes, profesores o cursos."
    
    def _arun(self, query: str):
        raise NotImplementedError("Esta herramienta no soporta ejecución asíncrona")

def crear_agente_react():
    """
    Crea un agente ReAct con herramientas personalizadas
    
    El patrón ReAct combina:
    - Reasoning (Razonamiento): El agente piensa sobre qué hacer
    - Acting (Acción): El agente ejecuta herramientas
    - Observing (Observación): El agente analiza los resultados
    """
    
    # Inicializar el LLM
    llm = OpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Definir herramientas disponibles
    tools = [
        CalculadoraTool(),
        ConsultorBaseDatosTool()
    ]
    
    # Configurar memoria para mantener contexto
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Crear el agente ReAct
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.REACT_DOCSTORE_SINGLE_INPUT,
        memory=memory,
        verbose=True,  # Para ver el proceso de razonamiento
        handle_parsing_errors=True
    )
    
    return agent

def demostrar_react():
    """Función de demostración del patrón ReAct"""
    
    print("🤖 DEMO: Agente ReAct - Día 1 Curso Avanzado")
    print("=" * 50)
    print("Este agente demuestra el patrón ReAct:")
    print("- Reasoning: Piensa qué herramienta usar")
    print("- Acting: Ejecuta la herramienta")
    print("- Observing: Analiza el resultado")
    print("=" * 50)
    
    # Verificar API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ATENCIÓN: No se encontró OPENAI_API_KEY")
        print("Para ejecutar este ejemplo, necesitas:")
        print("1. Crear un archivo .env con tu clave de OpenAI")
        print("2. Añadir: OPENAI_API_KEY=tu_clave_aqui")
        print("\nPor ahora, mostraré la estructura del agente...")
        return
    
    try:
        # Crear el agente
        agent = crear_agente_react()
        
        # Ejemplos de consultas que demuestran ReAct
        consultas_ejemplo = [
            "Calcula cuántos estudiantes hay en total si Ana tiene 3 años de carrera y Carlos tiene 2",
            "¿Quién es el profesor del curso INF101 y cuántos créditos tiene?",
            "Si un estudiante toma INF101 y MAT201, ¿cuántos créditos totales obtiene?"
        ]
        
        print("\n📝 Consultas de ejemplo disponibles:")
        for i, consulta in enumerate(consultas_ejemplo, 1):
            print(f"{i}. {consulta}")
        
        print("\n¿Quieres ejecutar alguna consulta? (1-3) o escribe tu propia pregunta:")
        print("(Presiona Enter para salir)")
        
        while True:
            entrada = input("\n> ").strip()
            
            if not entrada:
                break
                
            if entrada.isdigit() and 1 <= int(entrada) <= len(consultas_ejemplo):
                consulta = consultas_ejemplo[int(entrada) - 1]
            else:
                consulta = entrada
            
            print(f"\n🔍 Procesando: {consulta}")
            print("-" * 40)
            
            try:
                resultado = agent.run(consulta)
                print(f"\n✅ Resultado: {resultado}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            print("-" * 40)
    
    except Exception as e:
        print(f"❌ Error al crear el agente: {str(e)}")
        print("Verifica tu configuración de OpenAI API key")

if __name__ == "__main__":
    # Mostrar información sobre el patrón ReAct
    print("""
🧠 PATRÓN ReAct - Reasoning + Acting

El patrón ReAct combina razonamiento y acción en un bucle:

1. THOUGHT (Pensamiento): ¿Qué necesito hacer?
2. ACTION (Acción): Ejecutar herramienta específica
3. OBSERVATION (Observación): Analizar resultado
4. THOUGHT (Pensamiento): ¿Necesito más información?
5. ... (repetir hasta completar la tarea)

Este patrón es especialmente útil para:
- Tareas que requieren múltiples pasos
- Integración con herramientas externas
- Razonamiento complejo sobre datos
""")
    
    demostrar_react()
