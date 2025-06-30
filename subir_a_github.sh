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
