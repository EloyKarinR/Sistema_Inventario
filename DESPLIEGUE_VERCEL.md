## Despliegue en Vercel

### Configuración del Proyecto

Tu sistema de inventario está ahora configurado para desplegarse en Vercel con los siguientes archivos:

- `vercel.json` - Configuración de despliegue para Vercel
- `build.sh` - Script de construcción para preparar el proyecto
- Configuración específica de Vercel en `settings.py`

### Pasos para el Despliegue

1. **Crear cuenta en Vercel**
   - Ve a https://vercel.com
   - Regístrate con tu cuenta de GitHub

2. **Subir el proyecto a GitHub**
   ```bash
   git add .
   git commit -m "Configuración para Vercel"
   git push origin main
   ```

3. **Conectar con Vercel**
   - En Vercel, selecciona "New Project"
   - Importa tu repositorio de GitHub
   - Vercel detectará automáticamente la configuración

4. **Variables de Entorno (opcionales)**
   - `DJANGO_SECRET_KEY` - Para mayor seguridad
   - `DEBUG` - Mantener como False en producción

### Características de la Configuración

✅ **Base de datos**: SQLite en memoria (para demo)
✅ **Archivos estáticos**: Configurados para servirse desde `/static/`
✅ **Archivos multimedia**: Configurados para servirse desde `/media/`
✅ **Seguridad**: HTTPS y configuraciones de cookies seguras
✅ **Migraciones**: Automáticas durante el build

### Notas Importantes

- Esta configuración usa SQLite en memoria, ideal para demos
- Para producción real, considera usar PostgreSQL
- Los archivos multimedia se servirán desde el proyecto (limitaciones de Vercel)

### Después del Despliegue

Una vez desplegado, podrás:
- Gestionar inventario de productos
- Registrar ventas y compras
- Generar reportes
- Administrar clientes y proveedores

¡Tu sistema estará disponible en una URL de Vercel como `tu-proyecto.vercel.app`!
