# ejemplo_funciones.py
# Archivo para practicar las funciones básicas de GitHub Copilot.

# --- EJERCICIO 1: Generar Código ---
# Pídele a Copilot que complete la siguiente función para que calcule el área de un círculo.
# Pista: Puedes empezar a escribir "radio_al_cuadrado = ..."
import math

def calcular_area_circulo(radio):
    # Tu código aquí
    pass

# --- EJERCICIO 2: Explicar Código ---
# Selecciona la función de abajo y pídele a Copilot que te la explique ("Copilot: Explain this").

def fibonacci(n):
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

# --- EJERCICIO 3: Corregir Errores (Debug) ---
# La siguiente función tiene un error. ¿Puedes usar Copilot para encontrarlo y arreglarlo?
# Pista: Pregúntale a Copilot "cómo soluciono este error" o usa la funcionalidad de "Fix this".

def sumar_lista(numeros):
    total = 0
    for i in range(len(numeros)):
        total += numeros[i+1] # ¡Cuidado con el índice!
    return total

# --- EJERCICIO 4: Crear Código a partir de un Comentario ---
# Escribe un comentario que diga: "crea una función que reciba una lista de strings y devuelva la más larga".
# Observa cómo Copilot genera el código por ti.

# Tu comentario y código aquí

