# 📋 Guía de Archivos del Proyecto

## 🎯 **¿Qué Necesito para Desarrollo Local?**

### ✅ **Archivos Esenciales**:
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

---

## 🌐 **Archivos Específicos de Vercel** (Puedes ignorar):

### ⚠️ **Solo para Deployment**:
```
├── vercel.json              # 🔧 Configuración de Vercel
├── requirements-vercel.txt  # 📦 Dependencias optimizadas para Vercel
├── .vercel/                 # 📁 Cache de Vercel
├── .vercelignore           # 🚫 Archivos ignorados en Vercel
├── api/                    # 🌍 Adaptador para serverless
│   ├── index.py            # 🎯 Punto de entrada para Vercel
│   └── requirements.txt    # 📦 Dependencias específicas de API
├── Procfile                # 🚀 Para despliegues en Heroku/similar
├── runtime.txt             # 🐍 Versión específica de Python
└── Aptfile                 # 📋 Paquetes del sistema para deployments
```

### 🎭 **Templates de Demo**:
- `Inventario/templates/Inventario/bienvenida_vercel.html` - Página específica de demo

---

## 🎯 **¿Qué Clono Entonces?**

### Para **Desarrollo Local**:
```bash
git clone https://github.com/EloyKarinR/Sistema_Inventario.git
cd Sistema_Inventario

# Solo necesitas estos comandos:
setup-local.bat  # Windows
# O
./setup-local.sh  # Linux/Mac
```

**Los archivos de Vercel no interfieren** con tu desarrollo local, simplemente los ignoras.

### Para **Deployment en Vercel**:
Clona todo el repositorio y conecta directamente con Vercel - los archivos de configuración ya están listos.

---

## 🧹 **¿Quieres un Repositorio "Limpio"?**

Si prefieres un repositorio solo con archivos de desarrollo local:

### Opción 1: Eliminar archivos de Vercel después de clonar
```bash
git clone https://github.com/EloyKarinR/Sistema_Inventario.git
cd Sistema_Inventario

# Eliminar archivos de Vercel (opcional)
rm -rf api/ vercel.json requirements-vercel.txt .vercelignore
rm Procfile runtime.txt Aptfile
```

### Opción 2: Fork y personalizar
1. Haz fork del repositorio
2. Elimina los archivos de Vercel que no necesites
3. Mantén solo lo esencial para tu desarrollo

---

## 💡 **Recomendación**

**Deja todos los archivos** - no estorban y permiten:
- ✅ Desarrollo local completo
- ✅ Opción de deployment futuro en Vercel
- ✅ Documentación completa
- ✅ Scripts de ayuda incluidos

Los archivos de Vercel ocupan menos de 1MB y no afectan el funcionamiento local.
