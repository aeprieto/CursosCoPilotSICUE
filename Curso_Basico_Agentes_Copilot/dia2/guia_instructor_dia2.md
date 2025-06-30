# Día 2: Desarrollo Asistido con Copilot

## ⏰ Cronograma Detallado (9:00 - 14:00)

| Horario     | Actividad                                       | Duración | Tipo              | Material                       |
|-------------|-------------------------------------------------|----------|-------------------|--------------------------------|
| 09:00-09:15 | Repaso del Día 1 y resolución de dudas          | 15min    | Plenario          | `repaso_dia1.md`               |
| 09:15-11:15 | Práctica: Técnicas Avanzadas de Prompting       | 2h       | Práctico Guiado   | `prompting_avanzado.md`        |
| 11:15-11:45 | **Pausa para el café**                          | 30min    | Descanso          | -                              |
| 11:45-13:45 | Taller: Automatización de Tareas Repetitivas    | 2h       | Práctico Intensivo| `automatizacion_tareas.md`     |
| 13:45-14:00 | Puesta en común y cierre de la sesión           | 15min    | Plenario          | `recapitulacion_dia2.md`       |

## 🎯 Objetivos del Día

Al finalizar el día 2, los participantes podrán:

1. ✅ Aplicar técnicas de ingeniería de prompts para obtener resultados más precisos.
2. ✅ Utilizar el contexto del código para guiar a Copilot de manera efectiva.
3. ✅ Automatizar tareas repetitivas (ej. renombrar archivos, procesar texto) mediante scripts generados con IA.
4. ✅ Desarrollar utilidades prácticas y personalizadas para el Servicio de Informática.
5. ✅ Generar documentación básica para sus propios scripts de forma automática.

## ✍️ Actividades Prácticas (Foco en "Aprender Haciendo")

### Taller 1: El Arte del Prompt (2h)
- **Context Priming**: Modificar comentarios y código existente para que Copilot genere funciones coherentes con el estilo del proyecto.
- **Few-Shot Examples**: Proporcionar ejemplos de entrada/salida en los comentarios para que Copilot genere la lógica correcta.
- **Role-Playing**: Asignar un rol a Copilot Chat (ej. "Eres un experto en ciberseguridad") para obtener respuestas especializadas.

### Taller 2: Creando tus Propias Herramientas (2h)
- **Objetivo**: Cada participante (o en parejas) identificará una tarea manual de su día a día y creará un script para automatizarla.
- **Ejemplos de Tareas**:
  - Un script que organiza los archivos de la carpeta "Descargas" en subcarpetas por tipo de archivo.
  - Una utilidad que revisa una lista de IPs y hace ping para verificar su estado.
  - Un programa que lee un archivo CSV y genera un resumen estadístico.
- **Metodología**: El instructor guiará el proceso, pero los participantes usarán Copilot para generar el 80-90% del código, enfocándose en la definición del problema y la validación del resultado.

**Nota:** El objetivo es la experimentación y el aprendizaje. No se espera que los scripts sean perfectos, sino que funcionen y demuestren la comprensión de los conceptos.

## 🔧 Troubleshooting Común

- **Copilot genera código con errores o alucinaciones**: Enseñar a los participantes a no confiar ciegamente, a depurar y a refinar el prompt para corregir el resultado.
- **Dependencias de librerías externas**: Guiar en el uso de `pip` para instalar las librerías que Copilot pueda sugerir (ej. `pandas`, `requests`).
- **Permisos del sistema**: Recordar que algunos scripts pueden necesitar permisos de administrador para ejecutarse, especialmente si interactúan con archivos del sistema.

## 📚 Material de Apoyo

- Repositorio con ejemplos de prompts efectivos.
- Lista de ideas para scripts de automatización.
- Guía rápida de las librerías estándar de Python más útiles (`os`, `sys`, `csv`, `json`).

---

**Próximo día**: Introducción a los Agentes Conversacionales y Conexión con APIs.
