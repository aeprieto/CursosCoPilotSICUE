# Guía de Configuración del Entorno

## 🎯 Objetivo
Preparar el entorno de desarrollo completo para trabajar con GitHub Copilot y desarrollo de agentes básicos.

---

## 💻 Prerrequisitos de Sistema

### Sistemas Operativos Soportados:
- ✅ **Windows 10/11** (recomendado: versión 21H2 o superior)  
- ✅ **macOS** (recomendado: 10.15 Catalina o superior)
- ✅ **Linux** (Ubuntu 18.04+, Fedora 32+, CentOS 8+)

### Requisitos de Hardware:
- **RAM**: 8GB mínimo (16GB recomendado)
- **Almacenamiento**: 10GB libres
- **Procesador**: Intel i5 o equivalente AMD
- **Conexión**: Internet estable (mínimo 10 Mbps)

---

## 🛠️ Instalación Paso a Paso

### 1. Visual Studio Code

#### Windows:
```bash
# Opción 1: Descarga directa
# Ve a https://code.visualstudio.com/
# Descarga "Windows x64 User Installer"

# Opción 2: Winget (Windows Package Manager)
winget install Microsoft.VisualStudioCode
```

#### macOS:
```bash
# Opción 1: Descarga directa
# Ve a https://code.visualstudio.com/
# Descarga "macOS Universal"

# Opción 2: Homebrew
brew install --cask visual-studio-code
```

#### Linux (Ubuntu/Debian):
```bash
# Añadir repositorio de Microsoft
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'

# Instalar
sudo apt update
sudo apt install code
```

### 2. Python 3.9+

#### Windows:
```bash
# Opción 1: Descarga desde python.org
# Ve a https://www.python.org/downloads/
# Descarga Python 3.11.x (recomendado)
# ¡IMPORTANTE! Marcar "Add Python to PATH"

# Opción 2: Microsoft Store
# Buscar "Python 3.11" en Microsoft Store

# Verificar instalación
python --version
pip --version
```

#### macOS:
```bash
# Opción 1: Homebrew (recomendado)
brew install python@3.11

# Opción 2: Descarga directa
# Ve a https://www.python.org/downloads/mac-osx/

# Verificar instalación
python3 --version
pip3 --version
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv

# Fedora
sudo dnf install python3.11 python3.11-pip

# Verificar instalación
python3 --version
pip3 --version
```

### 3. Git

#### Windows:
```bash
# Opción 1: Git para Windows
# Ve a https://git-scm.com/download/win
# Descarga e instala con configuración por defecto

# Opción 2: Winget
winget install Git.Git

# Verificar
git --version
```

#### macOS:
```bash
# Git ya viene instalado, pero instalar versión más reciente:
brew install git

# Verificar
git --version
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt install git

# Fedora
sudo dnf install git

# Verificar
git --version
```

### 4. Node.js (Para ejercicios avanzados)

#### Todas las plataformas:
```bash
# Ve a https://nodejs.org/
# Descarga la versión LTS (Long Term Support)
# Instala con configuración por defecto

# Verificar
node --version
npm --version
```

---

## 🔌 Extensiones de VS Code

### Extensiones Obligatorias:

1. **GitHub Copilot**
   - ID: `GitHub.copilot`
   - Función: Asistente de código con IA

2. **GitHub Copilot Chat**
   - ID: `GitHub.copilot-chat`
   - Función: Chat conversacional para programación

3. **Python**
   - ID: `ms-python.python`
   - Función: Soporte completo para Python

4. **Pylance**
   - ID: `ms-python.vscode-pylance`
   - Función: IntelliSense avanzado para Python

### Extensiones Recomendadas:

5. **GitLens**
   - ID: `eamodio.gitlens`
   - Función: Mejoras para Git integrado

6. **Code Spell Checker**
   - ID: `streetsidesoftware.code-spell-checker`
   - Función: Corrector ortográfico en código

7. **Prettier**
   - ID: `esbenp.prettier-vscode`
   - Función: Formateador de código

8. **Thunder Client** (Opcional)
   - ID: `rangav.vscode-thunder-client`
   - Función: Cliente REST para probar APIs

### Instalación de Extensiones:

#### Método 1: Interfaz Gráfica
1. Abrir VS Code
2. Presionar `Ctrl+Shift+X` (o `Cmd+Shift+X` en Mac)
3. Buscar cada extensión por nombre
4. Hacer clic en "Install"

#### Método 2: Línea de Comandos
```bash
# Instalar todas las extensiones esenciales de una vez
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension eamodio.gitlens
code --install-extension streetsidesoftware.code-spell-checker
```

---

## 🐍 Configuración de Python

### 1. Verificar Instalación
```bash
# Verificar Python
python --version
# Debería mostrar: Python 3.9.x o superior

# Verificar pip
pip --version
# Debería mostrar información de pip
```

### 2. Actualizar pip
```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
pip3 install --upgrade pip
```

### 3. Instalar Librerías Básicas
```bash
# Instalar librerías que usaremos en el curso
pip install requests pandas python-dotenv

# Para desarrollo de agentes (más adelante)
pip install langchain langchain-openai

# Para trabajar con APIs
pip install fastapi uvicorn

# Para análisis de datos
pip install matplotlib seaborn jupyter
```

### 4. Crear Entorno Virtual (Recomendado)
```bash
# Crear entorno virtual para el curso
python -m venv curso-agentes-env

# Activar entorno virtual
# Windows:
curso-agentes-env\Scripts\activate

# macOS/Linux:
source curso-agentes-env/bin/activate

# Instalar librerías en el entorno
pip install -r requirements.txt
```

---

## 🔐 Configuración de GitHub

### 1. Crear/Verificar Cuenta GitHub
- Ve a [github.com](https://github.com)
- Crea una cuenta si no tienes una
- Verifica tu email

### 2. Configurar Git Localmente
```bash
# Configurar nombre y email
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@universidad.edu"

# Verificar configuración
git config --list
```

### 3. Solicitar GitHub Copilot
```bash
# Opción 1: Cuenta educativa
# Ve a https://education.github.com/
# Solicita GitHub Student Pack (incluye Copilot gratis)

# Opción 2: Prueba gratuita
# Ve a https://github.com/features/copilot
# Inicia prueba gratuita de 30 días
```

---

## ⚙️ Configuración de VS Code

### 1. Configuración Básica
Crear archivo `settings.json` en VS Code:

```json
{
    "python.defaultInterpreterPath": "python",
    "python.terminal.activateEnvironment": true,
    "editor.fontSize": 14,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": true,
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 2000,
    "terminal.integrated.fontSize": 12
}
```

### 2. Configuración de Copilot
```json
{
    "github.copilot.enable": {
        "*": true,
        "yaml": true,
        "plaintext": false,
        "markdown": true
    },
    "github.copilot.advanced": {
        "length": 500,
        "temperature": 0.1
    }
}
```

### 3. Configuración de Python
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.analysis.typeCheckingMode": "basic"
}
```

---

## 📁 Estructura de Workspace

### Crear Carpeta de Trabajo
```bash
# Crear carpeta principal
mkdir curso-agentes-copilot
cd curso-agentes-copilot

# Crear subcarpetas
mkdir dia1 dia2 dia3 dia4 dia5
mkdir recursos ejemplos proyectos

# Estructura final:
# curso-agentes-copilot/
# ├── dia1/
# ├── dia2/
# ├── dia3/
# ├── dia4/
# ├── dia5/
# ├── recursos/
# ├── ejemplos/
# └── proyectos/
```

### Archivo requirements.txt
```txt
# Librerías básicas
requests>=2.31.0
pandas>=2.0.0
python-dotenv>=1.0.0

# Para desarrollo de agentes
langchain>=0.1.0
langchain-openai>=0.1.0

# Para APIs
fastapi>=0.104.0
uvicorn>=0.24.0

# Para análisis y visualización
matplotlib>=3.7.0
seaborn>=0.12.0
jupyter>=1.0.0

# Utilidades
python-dateutil>=2.8.0
PyYAML>=6.0.0
```

---

## ✅ Lista de Verificación Final

### Antes de Empezar el Curso:
- [ ] VS Code instalado y funcionando
- [ ] Python 3.9+ instalado y en PATH
- [ ] Git instalado y configurado
- [ ] Cuenta GitHub creada y verificada
- [ ] GitHub Copilot activado y funcionando
- [ ] Extensiones de VS Code instaladas
- [ ] Librerías Python instaladas
- [ ] Workspace creado y organizado
- [ ] Conexión a internet estable

### Test de Verificación:
```python
# Crear archivo test_setup.py y ejecutar:
import sys
import requests
import pandas as pd

print(f"Python version: {sys.version}")
print("Requests:", requests.__version__)
print("Pandas:", pd.__version__)
print("✅ Setup completo!")
```

---

## 🚨 Troubleshooting

### Problemas Comunes:

#### Python no se encuentra:
```bash
# Windows: Verificar PATH
echo $env:PATH

# Agregar Python al PATH manualmente:
# Panel de Control > Sistema > Variables de entorno
# Agregar ruta de Python (ej: C:\Python311\)
```

#### VS Code no encuentra Python:
1. Abrir VS Code
2. `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Seleccionar la versión correcta de Python

#### Copilot no funciona:
1. Verificar que estás logueado en GitHub
2. `Ctrl+Shift+P` → "GitHub Copilot: Sign in"
3. Reiniciar VS Code

#### Permisos en Linux/Mac:
```bash
# Si hay problemas de permisos con pip:
pip install --user [paquete]

# O usar entorno virtual:
python -m venv venv
source venv/bin/activate
```

---

## 📞 Soporte Técnico

### Durante el Curso:
- **Instructor**: Disponible durante todas las sesiones
- **Compañeros**: Trabajo en parejas para resolver problemas
- **Documentación**: Enlaces a recursos oficiales

### Recursos Online:
- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Python.org](https://www.python.org/doc/)
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Stack Overflow](https://stackoverflow.com) para problemas específicos

---

*Configuración completada. ¡Listo para empezar el desarrollo con agentes!*
