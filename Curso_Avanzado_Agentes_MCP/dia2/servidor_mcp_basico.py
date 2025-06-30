#!/usr/bin/env python3
"""
Ejemplo básico de servidor MCP para el Día 2 del Curso Avanzado
Este servidor implementa herramientas simples para gestión universitaria
"""

import json
import sys
from typing import Dict, List, Any
import sqlite3
import os
from datetime import datetime

class UniversidadMCPServer:
    """
    Servidor MCP básico para gestión universitaria
    Implementa herramientas para consultar información de estudiantes y cursos
    """
    
    def __init__(self):
        self.tools = {
            "consultar_estudiante": self.consultar_estudiante,
            "listar_cursos": self.listar_cursos,
            "matricular_estudiante": self.matricular_estudiante,
            "generar_reporte": self.generar_reporte
        }
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con datos de ejemplo"""
        self.conn = sqlite3.connect(":memory:")  # Base de datos en memoria para la demo
        cursor = self.conn.cursor()
        
        # Crear tablas
        cursor.execute('''
            CREATE TABLE estudiantes (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                carrera TEXT NOT NULL,
                año INTEGER NOT NULL,
                activo BOOLEAN NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE cursos (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                profesor TEXT NOT NULL,
                creditos INTEGER NOT NULL,
                max_estudiantes INTEGER NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE matriculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante_id TEXT NOT NULL,
                curso_codigo TEXT NOT NULL,
                fecha_matricula TEXT NOT NULL,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                FOREIGN KEY (curso_codigo) REFERENCES cursos (codigo)
            )
        ''')
        
        # Insertar datos de ejemplo
        estudiantes = [
            ("20240001", "Ana García López", "ana.garcia@universidad.edu", "Informática", 3, True),
            ("20240002", "Carlos Martín Ruiz", "carlos.martin@universidad.edu", "Matemáticas", 2, True),
            ("20240003", "María Rodríguez Sanz", "maria.rodriguez@universidad.edu", "Física", 4, True),
            ("20240004", "David López Pérez", "david.lopez@universidad.edu", "Informática", 1, True),
        ]
        
        cursos = [
            ("INF101", "Programación I", "Dr. Juan Pérez", 6, 30),
            ("INF201", "Estructuras de Datos", "Dr. Juan Pérez", 6, 25),
            ("MAT101", "Cálculo I", "Dra. Elena Martín", 4, 40),
            ("MAT201", "Álgebra Lineal", "Dra. Elena Martín", 4, 35),
            ("FIS101", "Física General", "Dr. Pedro Gómez", 5, 20),
        ]
        
        cursor.executemany("INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?, ?)", estudiantes)
        cursor.executemany("INSERT INTO cursos VALUES (?, ?, ?, ?, ?)", cursos)
        
        # Algunas matrículas de ejemplo
        matriculas = [
            ("20240001", "INF101", "2024-01-15"),
            ("20240001", "MAT101", "2024-01-15"),
            ("20240002", "MAT101", "2024-01-16"),
            ("20240002", "MAT201", "2024-01-16"),
            ("20240004", "INF101", "2024-01-20"),
        ]
        
        cursor.executemany("INSERT INTO matriculas (estudiante_id, curso_codigo, fecha_matricula) VALUES (?, ?, ?)", matriculas)
        self.conn.commit()
    
    def consultar_estudiante(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Consulta información de un estudiante por ID o nombre"""
        try:
            query = args.get("query", "")
            cursor = self.conn.cursor()
            
            if query.startswith("2024"):  # Parece un ID
                cursor.execute("SELECT * FROM estudiantes WHERE id = ?", (query,))
            else:  # Buscar por nombre
                cursor.execute("SELECT * FROM estudiantes WHERE nombre LIKE ?", (f"%{query}%",))
            
            resultado = cursor.fetchone()
            
            if resultado:
                estudiante = {
                    "id": resultado[0],
                    "nombre": resultado[1],
                    "email": resultado[2],
                    "carrera": resultado[3],
                    "año": resultado[4],
                    "activo": bool(resultado[5])
                }
                
                # Obtener cursos matriculados
                cursor.execute("""
                    SELECT c.codigo, c.nombre, c.creditos 
                    FROM cursos c 
                    JOIN matriculas m ON c.codigo = m.curso_codigo 
                    WHERE m.estudiante_id = ?
                """, (estudiante["id"],))
                
                cursos = cursor.fetchall()
                estudiante["cursos_matriculados"] = [
                    {"codigo": c[0], "nombre": c[1], "creditos": c[2]} for c in cursos
                ]
                
                return {"success": True, "data": estudiante}
            else:
                return {"success": False, "error": "Estudiante no encontrado"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def listar_cursos(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Lista todos los cursos disponibles"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM cursos")
            cursos = cursor.fetchall()
            
            lista_cursos = []
            for curso in cursos:
                # Contar estudiantes matriculados
                cursor.execute("SELECT COUNT(*) FROM matriculas WHERE curso_codigo = ?", (curso[0],))
                matriculados = cursor.fetchone()[0]
                
                lista_cursos.append({
                    "codigo": curso[0],
                    "nombre": curso[1],
                    "profesor": curso[2],
                    "creditos": curso[3],
                    "max_estudiantes": curso[4],
                    "estudiantes_matriculados": matriculados,
                    "plazas_disponibles": curso[4] - matriculados
                })
            
            return {"success": True, "data": lista_cursos}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def matricular_estudiante(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Matricula un estudiante en un curso"""
        try:
            estudiante_id = args.get("estudiante_id")
            curso_codigo = args.get("curso_codigo")
            
            if not estudiante_id or not curso_codigo:
                return {"success": False, "error": "Se requiere estudiante_id y curso_codigo"}
            
            cursor = self.conn.cursor()
            
            # Verificar que el estudiante existe
            cursor.execute("SELECT id FROM estudiantes WHERE id = ?", (estudiante_id,))
            if not cursor.fetchone():
                return {"success": False, "error": "Estudiante no encontrado"}
            
            # Verificar que el curso existe
            cursor.execute("SELECT codigo, max_estudiantes FROM cursos WHERE codigo = ?", (curso_codigo,))
            curso = cursor.fetchone()
            if not curso:
                return {"success": False, "error": "Curso no encontrado"}
            
            # Verificar si ya está matriculado
            cursor.execute("SELECT id FROM matriculas WHERE estudiante_id = ? AND curso_codigo = ?", 
                         (estudiante_id, curso_codigo))
            if cursor.fetchone():
                return {"success": False, "error": "El estudiante ya está matriculado en este curso"}
            
            # Verificar plazas disponibles
            cursor.execute("SELECT COUNT(*) FROM matriculas WHERE curso_codigo = ?", (curso_codigo,))
            matriculados = cursor.fetchone()[0]
            if matriculados >= curso[1]:
                return {"success": False, "error": "No hay plazas disponibles en este curso"}
            
            # Realizar la matrícula
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO matriculas (estudiante_id, curso_codigo, fecha_matricula) VALUES (?, ?, ?)",
                         (estudiante_id, curso_codigo, fecha_actual))
            self.conn.commit()
            
            return {"success": True, "message": f"Estudiante {estudiante_id} matriculado en {curso_codigo}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generar_reporte(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Genera un reporte del estado del sistema"""
        try:
            cursor = self.conn.cursor()
            
            # Estadísticas generales
            cursor.execute("SELECT COUNT(*) FROM estudiantes WHERE activo = 1")
            estudiantes_activos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM cursos")
            total_cursos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM matriculas")
            total_matriculas = cursor.fetchone()[0]
            
            # Cursos más populares
            cursor.execute("""
                SELECT c.codigo, c.nombre, COUNT(m.id) as matriculas
                FROM cursos c
                LEFT JOIN matriculas m ON c.codigo = m.curso_codigo
                GROUP BY c.codigo, c.nombre
                ORDER BY matriculas DESC
                LIMIT 3
            """)
            cursos_populares = cursor.fetchall()
            
            # Estudiantes por carrera
            cursor.execute("""
                SELECT carrera, COUNT(*) as cantidad
                FROM estudiantes
                WHERE activo = 1
                GROUP BY carrera
                ORDER BY cantidad DESC
            """)
            estudiantes_por_carrera = cursor.fetchall()
            
            reporte = {
                "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "estadisticas_generales": {
                    "estudiantes_activos": estudiantes_activos,
                    "total_cursos": total_cursos,
                    "total_matriculas": total_matriculas,
                    "promedio_matriculas_por_curso": round(total_matriculas / total_cursos, 2) if total_cursos > 0 else 0
                },
                "cursos_mas_populares": [
                    {"codigo": c[0], "nombre": c[1], "matriculas": c[2]} for c in cursos_populares
                ],
                "estudiantes_por_carrera": [
                    {"carrera": c[0], "cantidad": c[1]} for c in estudiantes_por_carrera
                ]
            }
            
            return {"success": True, "data": reporte}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja las peticiones MCP entrantes"""
        try:
            method = request.get("method")
            
            if method == "tools/list":
                return {
                    "tools": [
                        {
                            "name": "consultar_estudiante",
                            "description": "Consulta información de un estudiante por ID o nombre",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "ID del estudiante o parte del nombre"}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "listar_cursos",
                            "description": "Lista todos los cursos disponibles con información de matrículas",
                            "inputSchema": {"type": "object", "properties": {}}
                        },
                        {
                            "name": "matricular_estudiante",
                            "description": "Matricula un estudiante en un curso específico",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "estudiante_id": {"type": "string", "description": "ID del estudiante"},
                                    "curso_codigo": {"type": "string", "description": "Código del curso"}
                                },
                                "required": ["estudiante_id", "curso_codigo"]
                            }
                        },
                        {
                            "name": "generar_reporte",
                            "description": "Genera un reporte completo del estado del sistema universitario",
                            "inputSchema": {"type": "object", "properties": {}}
                        }
                    ]
                }
            
            elif method == "tools/call":
                tool_name = request.get("params", {}).get("name")
                arguments = request.get("params", {}).get("arguments", {})
                
                if tool_name in self.tools:
                    result = self.tools[tool_name](arguments)
                    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                else:
                    return {"error": f"Herramienta desconocida: {tool_name}"}
            
            else:
                return {"error": f"Método no soportado: {method}"}
                
        except Exception as e:
            return {"error": str(e)}

def main():
    """Función principal para ejecutar el servidor MCP"""
    print("🚀 Servidor MCP Universitario - Día 2 Curso Avanzado", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    print("Este servidor implementa herramientas MCP básicas para:", file=sys.stderr)
    print("- Consultar información de estudiantes", file=sys.stderr)
    print("- Listar cursos disponibles", file=sys.stderr)
    print("- Matricular estudiantes", file=sys.stderr)
    print("- Generar reportes del sistema", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    server = UniversidadMCPServer()
    
    # Modo interactivo para testing
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        print("\n🔧 Modo interactivo activado")
        print("Ejemplos de uso:")
        print("1. Consultar estudiante: consultar_estudiante('Ana')")
        print("2. Listar cursos: listar_cursos()")
        print("3. Matricular: matricular_estudiante('20240004', 'MAT101')")
        print("4. Generar reporte: generar_reporte()")
        
        while True:
            try:
                entrada = input("\n> ").strip()
                if entrada.lower() in ['exit', 'quit', 'salir']:
                    break
                
                if entrada.startswith("consultar_estudiante"):
                    query = entrada.split("(")[1].split(")")[0].strip("'\"")
                    result = server.consultar_estudiante({"query": query})
                    print(json.dumps(result, indent=2))
                
                elif entrada == "listar_cursos()":
                    result = server.listar_cursos({})
                    print(json.dumps(result, indent=2))
                
                elif entrada.startswith("matricular_estudiante"):
                    # Parsear argumentos básico
                    args = entrada.split("(")[1].split(")")[0].split(",")
                    if len(args) == 2:
                        estudiante_id = args[0].strip("'\" ")
                        curso_codigo = args[1].strip("'\" ")
                        result = server.matricular_estudiante({
                            "estudiante_id": estudiante_id,
                            "curso_codigo": curso_codigo
                        })
                        print(json.dumps(result, indent=2))
                
                elif entrada == "generar_reporte()":
                    result = server.generar_reporte({})
                    print(json.dumps(result, indent=2))
                
                else:
                    print("Comando no reconocido. Usa los ejemplos mostrados arriba.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    else:
        # Modo servidor MCP (stdio)
        print("Servidor MCP listo para recibir peticiones...", file=sys.stderr)
        
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = server.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                error_response = {"error": f"JSON inválido: {str(e)}"}
                print(json.dumps(error_response))
                sys.stdout.flush()
            except Exception as e:
                error_response = {"error": f"Error del servidor: {str(e)}"}
                print(json.dumps(error_response))
                sys.stdout.flush()

if __name__ == "__main__":
    main()
