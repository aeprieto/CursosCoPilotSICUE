#!/bin/bash

# 🚀 Script para Subir el Proyecto a GitHub
# Ejecuta este script para configurar y subir tu repositorio automáticamente

set -e

echo "🎓 Configurando repositorio: Plan de Formación en Agentes de IA"
echo "================================================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar si estamos en el directorio correcto
if [ ! -f "PROYECTO_COMPLETADO.md" ]; then
    print_error "No estás en el directorio correcto. Navega a /Users/alvaroeprieto/Desarrollo/CursosCoPIlotSICUE"
    exit 1
fi

print_status "Directorio correcto encontrado"

# Paso 1: Configurar Git (si no está configurado)
echo
print_info "Paso 1: Configurando Git..."

# Verificar si Git está configurado
if ! git config user.name > /dev/null 2>&1; then
    print_warning "Git no está configurado. Por favor, ingresa tu información:"
    
    read -p "Tu nombre completo: " git_name
    read -p "Tu email de GitHub: " git_email
    
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    
    print_status "Git configurado con nombre: $git_name y email: $git_email"
else
    current_name=$(git config user.name)
    current_email=$(git config user.email)
    print_status "Git ya configurado: $current_name <$current_email>"
fi

# Paso 2: Inicializar repositorio (si no existe)
echo
print_info "Paso 2: Inicializando repositorio Git..."

if [ ! -d ".git" ]; then
    git init
    print_status "Repositorio Git inicializado"
else
    print_status "Repositorio Git ya existe"
fi

# Paso 3: Añadir archivos
echo
print_info "Paso 3: Añadiendo archivos al repositorio..."

git add .
print_status "Archivos añadidos al staging area"

# Mostrar status
echo
print_info "Estado del repositorio:"
git status --short

# Paso 4: Crear commit inicial
echo
print_info "Paso 4: Creando commit inicial..."

git commit -m "Initial commit: Complete AI Agent Training Program for University Staff

✅ Features included:
- Basic Course: GitHub Copilot & Conversational Agents (5 days)
- Advanced Course: MCP Development & Multi-Agent Systems (7 days)  
- 60+ hours of structured educational content
- 40+ documentation files and instructor guides
- 25+ reusable templates and code examples
- 60+ practical exercises with real university use cases
- Docker deployment configurations
- Complete evaluation and certification system

🎯 Ready for immediate implementation in university environments"

print_status "Commit inicial creado"

# Paso 5: Instrucciones para GitHub
echo
print_info "🎉 ¡Repositorio local listo!"
echo
print_warning "PRÓXIMOS PASOS PARA SUBIR A GITHUB:"
echo
echo "1️⃣  Ve a https://github.com/new"
echo "2️⃣  Crea un nuevo repositorio con el nombre: CursosCoPIlotSICUE"
echo "3️⃣  NO inicialices con README, .gitignore o LICENSE (ya los tenemos)"
echo "4️⃣  Copia la URL del repositorio (algo como: https://github.com/tu-usuario/CursosCoPIlotSICUE.git)"
echo "5️⃣  Ejecuta estos comandos en la terminal:"
echo
echo "     git remote add origin https://github.com/TU-USUARIO/CursosCoPIlotSICUE.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo
print_info "También puedes usar el script siguiente paso: ./subir_a_github.sh"

# Crear script para el siguiente paso
cat > subir_a_github.sh << 'EOF'
#!/bin/bash

# Script para conectar con GitHub (ejecutar después de crear el repo en GitHub)

echo "🔗 Conectando repositorio local con GitHub..."

# Solicitar URL del repositorio
read -p "Pega la URL de tu repositorio de GitHub: " repo_url

# Validar URL
if [[ ! $repo_url =~ ^https://github\.com/.+/CursosCoPIlotSICUE\.git$ ]]; then
    echo "⚠️  Asegúrate de que la URL termine en .git"
    echo "   Ejemplo: https://github.com/tu-usuario/CursosCoPIlotSICUE.git"
    exit 1
fi

# Configurar remote
git remote add origin "$repo_url"
git branch -M main

# Subir a GitHub
echo "⬆️  Subiendo archivos a GitHub..."
git push -u origin main

echo "🎉 ¡Listo! Tu repositorio está en GitHub:"
echo "   $repo_url"
echo
echo "🔧 Próximos pasos recomendados en GitHub:"
echo "   - Añadir descripción del repositorio"
echo "   - Configurar GitHub Pages (si quieres)"
echo "   - Añadir topics: ai, education, university, github-copilot, mcp"
echo "   - Invitar colaboradores si es necesario"
EOF

chmod +x subir_a_github.sh

print_status "Script 'subir_a_github.sh' creado"

echo
print_status "🎯 Repositorio local preparado exitosamente"
print_info "Archivos en el repositorio:"
echo
git ls-files | head -20
echo "... y $(git ls-files | wc -l | tr -d ' ') archivos en total"

echo
print_warning "Recuerda: Después de crear el repo en GitHub, ejecuta:"
echo "          ./subir_a_github.sh"
