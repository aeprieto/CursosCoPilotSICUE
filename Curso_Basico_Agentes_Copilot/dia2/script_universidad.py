# script_universidad.py
# Archivo para practicar el desarrollo asistido con Copilot en tareas universitarias.

# --- EJERCICIO 1: Generar Documentación (Docstrings) ---
# Pídele a Copilot que genere la documentación para la siguiente función.
# Pista: Escribe `"""` debajo de la línea de la función y espera a que Copilot sugiera.

def procesar_expediente(estudiante_id, accion="consultar"):
    # Código complejo de acceso a base de datos...
    if accion == "consultar":
        return {"id": estudiante_id, "nombre": "Ana Torres", "curso": "3º Grado en Informática"}
    elif accion == "actualizar":
        # Lógica para actualizar...
        return {"status": "actualizado"}
    return None

# --- EJERCICIO 2: Completar Código Complejo ---
# Tenemos una lista de diccionarios. Pídele a Copilot que complete la función
# para que filtre los estudiantes que pertenecen a un departamento específico.

lista_estudiantes = [
    {"id": "a123", "nombre": "Juan Pérez", "departamento": "Informática"},
    {"id": "b456", "nombre": "María López", "departamento": "Matemáticas"},
    {"id": "c789", "nombre": "Carlos García", "departamento": "Informática"}
]

def filtrar_por_departamento(estudiantes, departamento):
    # Escribe un comentario como: "crear una lista vacía y recorrer los estudiantes..."
    # Tu código aquí
    pass

# --- EJERCICIO 3: Generar Expresiones Regulares ---
# Pídele a Copilot que genere una expresión regular para validar un email universitario.
# El formato debe ser "letras_y_numeros@universidad.edu.es"
import re

def validar_email_universitario(email):
    # Escribe un comentario como: "regex para validar email con dominio universidad.edu.es"
    patron = ""
    if re.match(patron, email):
        return True
    return False

# --- EJERCICIO 4: Crear una Clase Simple ---
# Pídele a Copilot que cree una clase "Asignatura" con los atributos: nombre, creditos y profesor.
# Debe incluir un método para mostrar la información de la asignatura.

# Tu código aquí

