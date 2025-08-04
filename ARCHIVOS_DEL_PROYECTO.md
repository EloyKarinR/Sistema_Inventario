# 📋 Guía de Archivos del Proyecto

## � **Estrategia de Ramas**

Este repositorio usa **ramas separadas** para diferentes propósitos:

### 💻 **Rama `main` (Esta rama)**
**Solo desarrollo local - Sin archivos de deployment**

## 🎯 **¿Qué Contiene Esta Rama?**

### ✅ **Archivos Esenciales para Desarrollo Local**:
```
Sistema_Inventario/
├── manage.py                 # ⚡ Script principal de Django
├── requirements.txt          # 📦 Dependencias para local
├── db.sqlite3               # 💾 Base de datos (se crea automáticamente)
├── SistemaInventario/       # ⚙️ Configuración del proyecto
├── Inventario/              # 🏢 Aplicación principal
├── media/                   # 🖼️ Archivos subidos (se crea automáticamente)
├── static/                  # 🎨 Archivos estáticos
├── staticfiles/             # 📁 Archivos compilados (se crea automáticamente)
└── env/                     # 🐍 Entorno virtual (se crea automáticamente)
```

### 🚀 **Scripts de Ayuda**:
- `setup-local.bat` / `setup-local.sh` - Instalación automática
- `INSTALACION_RAPIDA.md` - Guía paso a paso

### 📚 **Documentación**:
- `README.md` - Guía principal
- `DEPENDENCIAS.md` - Estrategia de dependencias  
- `ESTRATEGIA_RAMAS.md` - Explicación de ramas
- `ARCHIVOS_DEL_PROYECTO.md` - Este archivo

---

## 🌐 **¿Qué NO Contiene Esta Rama?**

### ❌ **Archivos de Vercel** (Están en rama `vercel-deploy`):
```
├── vercel.json              # 🔧 Configuración de Vercel
├── requirements-vercel.txt  # 📦 Dependencias optimizadas para Vercel
├── .vercel/                 # 📁 Cache de Vercel
├── .vercelignore           # 🚫 Archivos ignorados en Vercel
├── api/                    # 🌍 Adaptador para serverless
├── Procfile                # 🚀 Para despliegues en Heroku/similar
├── runtime.txt             # 🐍 Versión específica de Python
└── Aptfile                 # 📋 Paquetes del sistema para deployments
```

---

## 🎯 **¿Cómo Usar Esta Rama?**

### Para **Desarrollo Local**:
```bash
git clone https://github.com/EloyKarinR/Sistema_Inventario.git
cd Sistema_Inventario

# Instalación automática
setup-local.bat  # Windows
./setup-local.sh  # Linux/Mac
```

### Para **Deployment en Vercel**:
```bash
# Cambiar a rama de deployment
git clone -b vercel-deploy https://github.com/EloyKarinR/Sistema_Inventario.git
```

O conectar Vercel directamente a la rama `vercel-deploy`.

---

## 💡 **Beneficios de Esta Estrategia**

### ✅ **Para Desarrolladores**:
- **Repositorio limpio**: Solo archivos necesarios
- **Setup más rápido**: Sin archivos de deployment innecesarios  
- **Menor confusión**: Enfoque claro en desarrollo local
- **Clonación más rápida**: Menos archivos

### ✅ **Para el Proyecto**:
- **Separación clara**: Development vs Production
- **Mantenimiento fácil**: Cada rama tiene propósito específico
- **Escalabilidad**: Fácil añadir nuevas ramas para otros deployments

---

## � **Cambios entre Ramas**

Para ver archivos de deployment:
```bash
git checkout vercel-deploy
```

Para regresar a desarrollo local:
```bash
git checkout main
```

**Esta estrategia asegura que obtengas exactamente lo que necesitas para tu propósito específico.** 🎯
