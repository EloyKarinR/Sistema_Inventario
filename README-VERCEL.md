# 🌐 Rama Vercel Deploy

Esta es la rama específica para **deployment en Vercel**. Contiene todos los archivos necesarios para desplegar el Sistema de Inventario en la plataforma Vercel.

## 🎯 **Propósito de Esta Rama**

- ✅ **Deployment automático** en Vercel
- ✅ **Configuración optimizada** para serverless
- ✅ **Archivos específicos** de deployment
- ✅ **Todo listo** para producción

## 📁 **Archivos Adicionales en Esta Rama**

Además de todo el contenido de `main`, esta rama incluye:

### 🔧 **Configuración de Vercel**:
- `vercel.json` - Configuración principal
- `requirements-vercel.txt` - Dependencias optimizadas
- `.vercelignore` - Archivos a ignorar

### 🌍 **Adaptador Serverless**:
- `api/index.py` - Punto de entrada
- `api/requirements.txt` - Dependencias API

### 🚀 **Archivos de Deployment**:
- `Procfile` - Para otros servicios
- `runtime.txt` - Versión de Python
- `Aptfile` - Paquetes del sistema

### 🎭 **Demo Específico**:
- `bienvenida_vercel.html` - Template de demo

## 🔄 **Cómo Usar Esta Rama**

### Para Vercel (Automático):
1. Conecta tu repositorio a Vercel
2. Selecciona la rama `vercel-deploy`
3. Vercel detecta automáticamente la configuración
4. ¡Deploy automático!

### Para otros servicios:
Puedes usar los archivos de configuración incluidos para desplegar en:
- Heroku (usando `Procfile`)
- Railway
- Render
- Y otros servicios similares

## 🔄 **Sincronización con Main**

Esta rama se mantiene sincronizada con `main`:

```bash
# Actualizar con cambios de main
git checkout vercel-deploy
git merge main
git push origin vercel-deploy
```

## 💡 **¿Por Qué Esta Estrategia?**

### ✅ **Ventajas**:
- **Main limpia**: Desarrolladores solo ven archivos necesarios
- **Deploy optimizado**: Configuración específica para producción
- **Separación clara**: Development vs Production
- **Mantenimiento fácil**: Cambios específicos por propósito

### 🎯 **Resultado**:
- Desarrolladores clonan `main` (limpio y rápido)
- Vercel usa `vercel-deploy` (completo y optimizado)
- Todos contentos! 🎉

---

**Para desarrollo local, usa la rama `main`. Para deployment, esta rama tiene todo listo.** 🚀
