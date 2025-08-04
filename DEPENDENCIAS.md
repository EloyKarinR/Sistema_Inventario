# 📦 Estrategia de Dependencias

## Archivos de Dependencias

### `requirements.txt` (Principal)
- **Uso**: Desarrollo local completo
- **Contenido**: Todas las dependencias incluidas reportlab y chardet
- **Características**: Funcionalidad 100% completa

### `requirements-vercel.txt` (Optimizado)
- **Uso**: Deployment en Vercel
- **Contenido**: Solo dependencias esenciales para web
- **Características**: Reducido para evitar límites de Vercel

### `requirements-local.txt` (Respaldo)
- **Uso**: Copia de seguridad de dependencias completas
- **Contenido**: Idéntico a requirements.txt
- **Características**: Para casos donde se necesite especificar

## Manejo Inteligente de Dependencias

El sistema está diseñado para funcionar con o sin ciertas dependencias:

### PDF Generation (reportlab)
```python
try:
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
```

**Comportamiento**:
- ✅ **Con reportlab**: Genera PDFs completos
- ⚠️ **Sin reportlab**: Muestra mensaje amigable y redirecciona

### Character Detection (chardet)
- **Uso**: Detección automática de encoding
- **Fallback**: Python usa encoding por defecto

## Beneficios de Esta Estrategia

### 🚀 **Para Vercel**:
- Instalación más rápida
- Menor uso de memoria
- Evita dependencias pesadas innecesarias
- Reduce posibilidad de errores de build

### 💻 **Para Local**:
- Funcionalidad 100% completa
- Todas las características disponibles
- Desarrollo sin limitaciones

### 🔄 **Compatibilidad**:
- El mismo código funciona en ambos entornos
- Degradación elegante de funcionalidades
- Mensajes claros al usuario sobre limitaciones

## Configuración Automática

### Vercel Build
```json
{
  "config": {
    "installCommand": "pip install -r requirements-vercel.txt"
  }
}
```

### Local Development
```bash
pip install -r requirements.txt
```

## Verificación del Entorno

El sistema detecta automáticamente el entorno:
- Variable `VERCEL=1` → Modo demo con limitaciones
- Modo local → Funcionalidad completa

Esta estrategia asegura que **Vercel funcione de manera óptima** mientras que **localhost tenga todas las funcionalidades**.
