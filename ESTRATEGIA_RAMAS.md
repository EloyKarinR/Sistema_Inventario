# 🌿 Estrategia de Ramas

Este repositorio utiliza una estrategia de **ramas separadas** para mantener el código organizado según su propósito:

## 🏗️ **Estructura de Ramas**

### 💻 **`main`** - Desarrollo Local
**Propósito**: Desarrollo local limpio y optimizado

**Contenido**:
- ✅ Código Django completo
- ✅ `requirements.txt` para desarrollo local
- ✅ Scripts de setup automático
- ✅ Documentación completa
- ❌ Sin archivos de deployment
- ❌ Sin configuraciones de Vercel

**Para usar**:
```bash
git clone https://github.com/EloyKarinR/Sistema_Inventario.git
cd Sistema_Inventario
setup-local.bat  # Windows
./setup-local.sh  # Linux/Mac
```

---

### 🌐 **`vercel-deploy`** - Deployment en Vercel
**Propósito**: Deployment y configuración para producción

**Contenido adicional**:
- ✅ Todo el contenido de `main`
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `api/` - Adaptador serverless
- ✅ `requirements-vercel.txt` - Dependencias optimizadas
- ✅ `Procfile`, `runtime.txt`, `Aptfile` - Archivos de deployment
- ✅ Templates específicos de demo

**Para deployment**:
1. Conecta Vercel directamente a la rama `vercel-deploy`
2. Vercel usará automáticamente la configuración optimizada

---

## 🎯 **Beneficios de Esta Estrategia**

### 👨‍💻 **Para Desarrolladores**:
- **Repositorio limpio**: Solo archivos necesarios
- **Setup rápido**: Sin archivos innecesarios que confundan
- **Menor tamaño**: Clonación más rápida
- **Enfoque claro**: Solo desarrollo local

### 🚀 **Para Deployment**:
- **Configuración completa**: Todo listo para producción
- **Optimizaciones específicas**: Para entorno serverless
- **Separación de concerns**: Development vs Production

### 🔄 **Para Mantenimiento**:
- **Cambios específicos**: Modificaciones según propósito
- **Menos conflictos**: Archivos separados por función
- **Historial claro**: Commits organizados por propósito

---

## 🛠️ **Flujo de Trabajo**

### Desarrollo Local:
1. Clonar `main`
2. Desarrollar localmente
3. Commit a `main`

### Deployment:
1. Merge cambios de `main` a `vercel-deploy`
2. Vercel detecta cambios automáticamente
3. Deploy automático

### Sincronización:
```bash
# Actualizar vercel-deploy con cambios de main
git checkout vercel-deploy
git merge main
git push origin vercel-deploy
```

---

## 🎉 **Resultado**

- ✅ **Desarrolladores**: Experiencia limpia y rápida
- ✅ **Deployment**: Optimizado y automático  
- ✅ **Usuarios**: Pueden elegir exactamente lo que necesitan
- ✅ **Mantenimiento**: Organizado y escalable

Esta estrategia asegura que cada usuario obtenga exactamente lo que necesita, sin archivos innecesarios.
