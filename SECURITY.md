# 🚨 INSTRUCCIONES DE SEGURIDAD CRÍTICAS

## ⚠️ ANTES DE USAR EN PRODUCCIÓN

### 1. Generar nueva SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Configurar variables de entorno
```bash
# En el servidor, establecer estas variables:
export SECRET_KEY="tu-nueva-secret-key-aqui"
export DEBUG="False"
export ALLOWED_HOSTS="tu-dominio.com,www.tu-dominio.com"
```

### 3. O usar archivo .env (recomendado para desarrollo)
```bash
cp .env.example .env
# Editar .env con tus valores reales
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🔒 Archivos protegidos por .gitignore
- `.env` - Variables de entorno
- `db.sqlite3` - Base de datos de desarrollo
- `media/` - Archivos de usuario
- `staticfiles/` - Archivos estáticos compilados

## 🚫 NUNCA subir a Git
- Credenciales de base de datos
- SECRET_KEY de producción
- Archivos .env
- Tokens de API
- Contraseñas

## ✅ Seguridad implementada
- SECRET_KEY removida del código
- Variables de entorno configuradas
- .gitignore actualizado
- Configuración de producción separada
