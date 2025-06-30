# Día 4: Agentes para Soporte Técnico

## ⏰ Cronograma Detallado

| Horario | Actividad | Duración | Tipo | Material |
|---|---|---|---|---|
| 09:00-09:15 | Revisión del agente del día 3 | 15min | Demo | `revision_agente_dia3.md` |
| 09:15-11:15 | Casos de uso y sistemas universitarios | 2h | Teórico-Práctico | `casos_uso_universitarios.md` |
| 11:15-11:45 | **PAUSA - CAFÉ** | 30min | - | - |
| 11:45-14:00 | Taller: Agente de soporte y automatización | 2.25h | Práctico | `desarrollo_agente_soporte.md` |

## 🎯 Objetivos del Día

Al finalizar el día 4, los participantes podrán:

1.  ✅ **Identificar casos de uso** específicos del servicio de informática universitario
2.  ✅ **Integrar agentes** con sistemas académicos existentes (LDAP, bases de datos, APIs)
3.  ✅ **Desarrollar un agente** completo de soporte técnico funcional
4.  ✅ **Automatizar procesos** de gestión de tickets y workflows
5.  ✅ **Implementar buenas prácticas** de seguridad y logging

## 🏫 Enfoque: Servicio de Informática Universitario

### Contexto Real:
- **20,000 estudiantes** con necesidades diversas
- **Personal limitado** en el servicio de informática
- **Recursos económicos restringidos**
- **Múltiples sistemas** que mantener y soportar
- **Demanda 24/7** de soporte básico

### Oportunidades de Automatización:
- **80% de consultas** son repetitivas y automatizables
- **Gestión de usuarios** (altas, bajas, restablecimiento de contraseñas)
- **Monitorización de servicios** y alertas proactivas
- **Generación de reportes** automáticos

## 💻 Stack Técnico del Día

```bash
# Dependencias específicas para integración universitaria
pip install ldap3 # Para integración con Active Directory/LDAP
pip install sqlalchemy # Para bases de datos
pip install psycopg2-binary # PostgreSQL
pip install pymongo # MongoDB si se usa
pip install redis # Para caching y sesiones
pip install celery # Para tareas asíncronas
pip install fastapi uvicorn # Para crear APIs propias
pip install jinja2 # Para templates de respuestas
```

## 🎯 Ejercicios Principales del Día

### Ejercicio 1: Análisis de Casos de Uso (30 min)
**Objetivo**: Identificar y priorizar oportunidades de automatización
- Mapear procesos actuales del SI
- Identificar puntos de dolor
- Priorizar por impacto y facilidad de implementación

### Ejercicio 2: Integración con LDAP/AD (45 min)
**Objetivo**: Conectar agente con directorio de usuarios
- Consultar información de cuentas
- Validar credenciales
- Gestionar grupos y permisos

### Ejercicio 3: Agente de Soporte Completo (90 min)
**Objetivo**: Desarrollar agente funcional para el SI
- FAQ automatizada
- Gestión básica de tickets
- Integración con múltiples sistemas

### Ejercicio 4: Automatización de Workflows (60 min)
**Objetivo**: Automatizar procesos complejos
- Workflow de alta de usuario
- Proceso de resolución de incidencias
- Generación de reportes periódicos

## ✅ Finalización del curso

La finalización del curso se basa en la **asistencia**. No hay evaluación formal ni entrega de proyectos. El objetivo es **aprender haciendo** en un entorno práctico y colaborativo.
