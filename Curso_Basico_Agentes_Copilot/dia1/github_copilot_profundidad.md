# GitHub Copilot en Profundidad

## 🎯 Objetivos de la Sesión (1.5 horas)

Al finalizar esta sesión, los participantes podrán:
- Instalar y configurar GitHub Copilot correctamente
- Distinguir entre Copilot, Copilot Chat y Copilot CLI
- Aplicar mejores prácticas de prompting para código
- Utilizar las funciones avanzadas de Copilot

> **📁 Ejemplos Prácticos**: 
> - `ejemplo_funciones.py` - Funciones que construirás con ayuda de Copilot
> - `demo_conceptos_interactiva.py` - Demo práctica de todas las funcionalidades de Copilot

---

## 🛠️ ¿Qué es GitHub Copilot?

### Definición
> GitHub Copilot es un **asistente de programación con IA** que sugiere código y funciones completas en tiempo real desde el editor.

### Características Principales
- **Autocompletado inteligente**: Sugiere líneas completas o funciones
- **Comprensión contextual**: Entiende el código existente y el estilo
- **Multi-lenguaje**: Soporta Python, JavaScript, Java, C#, Go, Ruby, etc.
- **Integración nativa**: Funciona directamente en VS Code, JetBrains, etc.

### Historia y Tecnología
- **Desarrollado por**: GitHub + OpenAI
- **Basado en**: Codex (variante de GPT-3 especializada en código)
- **Entrenado con**: Miles de millones de líneas de código público
- **Lanzamiento**: 2021 (beta), 2022 (general)

---

## 🔧 Componentes del Ecosistema Copilot

### 1. 📝 GitHub Copilot (Extensión VS Code)
**Función**: Autocompletado de código en tiempo real

**Características**:
- Sugerencias inline mientras escribes
- Múltiples opciones de completado
- Adaptación al estilo de código existente

**Uso típico**:
```python
# Al escribir esta función...
def calculate_discount(price, percentage):
    # Copilot sugiere automáticamente:
    return price * (1 - percentage / 100)
```

### 2. 💬 GitHub Copilot Chat
**Función**: Asistente conversacional para programación

**Características**:
- Conversación en lenguaje natural sobre código
- Explicación de código existente
- Generación de código desde descripciones
- Depuración y optimización

**Uso típico**:
- "Explica qué hace esta función"
- "Crea una función que valide emails"
- "¿Cómo puedo optimizar este bucle?"

### 3. ⌨️ GitHub Copilot CLI (Avanzado)
**Función**: Asistente para comandos de terminal

**Características**:
- Sugerencias de comandos de shell
- Explicación de comandos complejos
- Conversión de lenguaje natural a comandos

**Uso típico**:
```bash
# Puedes escribir:
gh copilot suggest "find all python files modified in the last week"
# Y te sugiere:
find . -name "*.py" -mtime -7
```

---

## 🚀 Instalación Paso a Paso

### Paso 1: Verificar Prerrequisitos
- ✅ VS Code instalado (versión 1.74 o superior)
- ✅ Cuenta de GitHub activa
- ✅ Conexión a internet estable

### Paso 2: Solicitar Acceso (Si es necesario)
1. Ve a [github.com/features/copilot](https://github.com/features/copilot)
2. Si eres estudiante/educador: Solicita acceso gratuito
3. Si no: Inicia prueba gratuita de 30 días

### Paso 3: Instalar Extensiones en VS Code

#### Extensiones Requeridas:
1. **GitHub Copilot** (ID: `GitHub.copilot`)
2. **GitHub Copilot Chat** (ID: `GitHub.copilot-chat`)

#### Proceso de Instalación:
1. Abrir VS Code
2. Ir a Extensions (Ctrl+Shift+X)
3. Buscar "GitHub Copilot"
4. Instalar ambas extensiones
5. Reiniciar VS Code

### Paso 4: Autenticación
1. Al abrir VS Code, aparecerá notificación de autenticación
2. Hacer clic en "Sign in to GitHub"
3. Autorizar en el navegador
4. Volver a VS Code y confirmar

### Paso 5: Verificación
```python
# Crea un archivo test.py y escribe:
def hello_
# Copilot debería sugiere completar con "world():"
```

---

## 💡 Mejores Prácticas de Prompting

### 1. 📝 Comentarios Descriptivos
**Mala práctica**:
```python
# función
def calc():
```

**Buena práctica**:
```python
# Calcula el descuento aplicado a un precio base
# considerando el porcentaje de descuento y un mínimo aplicable
def calculate_discount_with_minimum(base_price, discount_percent, minimum_discount):
```

### 2. 🎯 Nombres de Variables Descriptivos
**Mala práctica**:
```python
def proc(x, y):
    return x * y
```

**Buena práctica**:
```python
def calculate_area_rectangle(width_meters, height_meters):
    # Copilot entenderá mejor el contexto
    return width_meters * height_meters
```

### 3. 📋 Especificar Tipos y Formatos
```python
# Función que valida un email usando regex
# Retorna True si es válido, False si no
# Input: string con el email a validar
# Output: boolean
def validate_email(email_address):
```

### 4. 🔧 Proporcionar Contexto
```python
# Para una aplicación universitaria de gestión de estudiantes
# Esta función busca estudiantes por número de expediente
def find_student_by_id(student_id):
```

### 5. 📊 Ejemplos y Casos de Uso
```python
# Convierte temperaturas de Celsius a Fahrenheit
# Ejemplo: celsius_to_fahrenheit(25) -> 77.0
# Ejemplo: celsius_to_fahrenheit(0) -> 32.0
def celsius_to_fahrenheit(celsius):
```

---

## ⚡ Funciones Avanzadas

### 1. 🔄 Múltiples Sugerencias
- **Atajo**: `Alt + ]` (siguiente sugerencia)
- **Atajo**: `Alt + [` (sugerencia anterior)
- **Uso**: Ver diferentes enfoques para el mismo problema

### 2. 💬 Copilot Chat Integrado
- **Activar**: `Ctrl + Shift + I` o hacer clic en el icono de chat
- **Comandos útiles**:
  - `/explain`: Explica el código seleccionado
  - `/fix`: Sugiere correcciones
  - `/optimize`: Propone optimizaciones
  - `/generate`: Genera código desde descripción

### 3. 🎯 Copilot Labs (Experimental)
Funciones experimentales como:
- **Explicar código** en lenguaje natural
- **Traducir código** entre lenguajes
- **Generar tests** automáticamente

### 4. 📄 Generación de Documentación
```python
def complex_calculation(data, filters, options):
    """
    # Al presionar Enter aquí, Copilot puede generar automáticamente:
    Performs complex calculation on the provided data.
    
    Args:
        data (list): Input data to process
        filters (dict): Filtering criteria
        options (dict): Additional processing options
        
    Returns:
        dict: Processed results with metadata
    """
```

---

## 🛠️ Configuración Avanzada

### Configuración de VS Code
```json
// settings.json
{
    "github.copilot.enable": {
        "*": true,
        "yaml": false,
        "plaintext": false
    },
    "github.copilot.advanced": {
        "length": 500,
        "temperature": 0.1
    }
}
```

### Deshabilitar en Archivos Específicos
```json
// Para archivos sensibles
{
    "github.copilot.enable": {
        "*.env": false,
        "*.key": false,
        "*.secret": false
    }
}
```

---

## 🚨 Limitaciones y Consideraciones

### Limitaciones Técnicas
- **No es 100% preciso**: Siempre revisar el código generado
- **Puede generar código obsoleto**: Verificar versiones de librerías
- **Dependiente del contexto**: Mejor con archivos bien estructurados
- **Sesgos de entrenamiento**: Basado en código público existente

### Consideraciones de Seguridad
- **No incluir datos sensibles** en comentarios
- **Revisar dependencias** sugeridas
- **Validar lógica de negocio** crítica
- **Cumplir políticas** institucionales de seguridad

### Consideraciones Legales
- **Licencias de código**: Verificar compatibilidad
- **Propiedad intelectual**: Revisar políticas institucionales
- **Código público**: Copilot aprende de repositorios públicos

---

## 🎯 Ejercicio Práctico (30 minutos)

### Parte 1: Configuración (10 min)
1. Verificar que Copilot está funcionando
2. Probar diferentes tipos de sugerencias
3. Configurar preferencias básicas

### Parte 2: Práctica Guiada (20 min)

#### Ejercicio A: Función de Validación
```python
# Crea una función que valide si una contraseña cumple los criterios:
# - Al menos 8 caracteres
# - Al menos una mayúscula
# - Al menos una minúscula  
# - Al menos un número
# - Al menos un carácter especial
def validate_password(password):
    # Deja que Copilot complete la función
```

#### Ejercicio B: Script de Automatización
```python
# Script para limpiar archivos temporales del sistema
# Debe buscar archivos .tmp, .log más antiguos de 7 días
# y eliminarlos de forma segura
import os
import time
from datetime import datetime, timedelta

def clean_temp_files(directory_path):
    # Implementa con ayuda de Copilot
```

#### Ejercicio C: API Helper
```python
# Cliente simple para consultar información de estudiantes
# desde una API REST universitaria
import requests
import json

class StudentAPI:
    def __init__(self, base_url, api_key):
        # Inicializar cliente API
        
    def get_student_info(self, student_id):
        # Obtener información de estudiante
        
    def update_student_email(self, student_id, new_email):
        # Actualizar email de estudiante
```

---

## 📊 Evaluación de la Sesión

### Checklist de Comprensión
- [ ] Copilot instalado y funcionando
- [ ] Entiende la diferencia entre Copilot y Copilot Chat
- [ ] Puede generar código usando comentarios descriptivos
- [ ] Sabe cómo ver múltiples sugerencias
- [ ] Comprende las limitaciones y consideraciones de seguridad

### Mini-Quiz (5 minutos)
1. **¿Cuál es la mejor manera de obtener código específico de Copilot?**
   - a) Escribir código parcial y esperar
   - b) Usar comentarios descriptivos detallados ✅
   - c) Escribir nombres de variables cortos

2. **¿Qué deberías hacer SIEMPRE con el código generado por Copilot?**
   - a) Usarlo directamente sin cambios
   - b) Revisarlo y validarlo ✅
   - c) Reescribirlo completamente

---

## 🔗 Recursos Adicionales

- [Documentación oficial de GitHub Copilot](https://docs.github.com/en/copilot)
- [GitHub Copilot: Getting Started](https://github.com/features/copilot)
- [Best Practices for Copilot](https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/)
- [VS Code Copilot Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)

---

**Siguiente tema**: Configuración del Entorno de Desarrollo - Preparando el workspace para el desarrollo con agentes
