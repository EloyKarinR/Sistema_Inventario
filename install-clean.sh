#!/bin/bash
# Script para instalar solo archivos necesarios para desarrollo local

echo "🧹 Instalación Limpia - Solo Desarrollo Local"
echo "Este script eliminará archivos específicos de Vercel deployment"
echo ""

read -p "¿Continuar? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelado"
    exit 1
fi

echo "🗑️ Eliminando archivos de Vercel..."

# Eliminar archivos de Vercel
rm -f vercel.json
rm -f requirements-vercel.txt
rm -f .vercelignore
rm -f Procfile
rm -f runtime.txt
rm -f Aptfile

# Eliminar directorio api
rm -rf api/

# Eliminar template específico de Vercel
rm -f Inventario/templates/Inventario/bienvenida_vercel.html

echo "✅ Archivos de Vercel eliminados"
echo ""
echo "📦 Archivos restantes son solo para desarrollo local:"
echo "   ✅ Django proyecto completo"
echo "   ✅ Requirements.txt para local"
echo "   ✅ Scripts de setup automático"
echo "   ✅ Documentación"
echo ""
echo "🚀 Ahora ejecuta: ./setup-local.sh"
