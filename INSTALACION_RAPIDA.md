# 🚀 Instalación Rápida - Sistema de Inventario

## Requisitos Previos
- Python 3.13+ instalado
- Git instalado
- Conexión a internet

## ⚡ Instalación Automática (2 minutos)

### 1. Clonar y entrar al proyecto
```bash
git clone https://github.com/EloyKarinR/Sistema_Inventario.git
cd Sistema_Inventario
```

### 2. Ejecutar script de configuración

#### Windows:
```bash
setup-local.bat
```

#### Linux/Mac:
```bash
chmod +x setup-local.sh
./setup-local.sh
```

### 3. Crear administrador
```bash
python manage.py createsuperuser
```

### 4. Iniciar servidor
```bash
python manage.py runserver
```

## 📝 Instalación Manual (5 minutos)

### 1. Clonar y entrar al proyecto
```bash
git clone https://github.com/EloyKarinR/Sistema_Inventario.git
cd Sistema_Inventario
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac  
python3 -m venv env
source env/bin/activate
```

### 3. Instalar dependencias
```bash
# Para desarrollo local completo
pip install -r requirements-local.txt

# O usar el requirements.txt estándar (mismo contenido)
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
python manage.py migrate
```

### 5. Crear administrador
```bash
python manage.py createsuperuser
```
*Crea tu usuario y contraseña únicos*

### 6. Crear carpetas necesarias
```bash
mkdir media media\productos media\empresa media\profile_pics
```

### 7. Iniciar servidor
```bash
python manage.py runserver
```

## ✅ ¡Listo!

- **Aplicación**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/
- **Usuario**: El que acabas de crear

## 📝 Primeros Pasos

1. Ve al admin y configura tu empresa
2. Crea categorías de productos  
3. Añade productos con imágenes
4. ¡Comienza a usar tu sistema de inventario!

## ❗ ¿Problemas?

Ver archivo [README.md](README.md) para solución de problemas detallada.

---
**Funcionalidad completa solo en instalación local** - La demo online tiene limitaciones.
