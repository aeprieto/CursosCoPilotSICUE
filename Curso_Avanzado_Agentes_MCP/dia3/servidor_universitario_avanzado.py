#!/usr/bin/env python3
"""
Servidor MCP Avanzado para Universidad - Día 3
Implementa conexión real a base de datos, caching y herramientas avanzadas
"""

import os
import json
import sys
import asyncio
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Estudiante:
    """Modelo de datos para estudiante"""
    id: str
    nombre: str
    email: str
    carrera: str
    año: int
    activo: bool
    fecha_ingreso: str
    creditos_completados: int = 0

@dataclass
class Curso:
    """Modelo de datos para curso"""
    codigo: str
    nombre: str
    profesor: str
    creditos: int
    max_estudiantes: int
    prerequisitos: List[str]
    activo: bool
    semestre: str

@dataclass
class Matricula:
    """Modelo de datos para matrícula"""
    id: int
    estudiante_id: str
    curso_codigo: str
    fecha_matricula: str
    calificacion: Optional[float] = None
    estado: str = "Matriculado"  # Matriculado, Aprobado, Reprobado, Retirado

class CacheSimple:
    """Cache simple en memoria para optimizar consultas"""
    
    def __init__(self, ttl_seconds: int = 300):  # 5 minutos por defecto
        self.cache = {}
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now().timestamp() - timestamp < self.ttl_seconds:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        self.cache[key] = (value, datetime.now().timestamp())
    
    def clear(self):
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_keys": len(self.cache),
            "cache_size_mb": sys.getsizeof(self.cache) / (1024 * 1024)
        }

class UniversidadMCPAvanzado:
    """Servidor MCP avanzado con base de datos real y caching"""
    
    def __init__(self, db_path: str = "universidad.db"):
        self.db_path = db_path
        self.cache = CacheSimple(ttl_seconds=300)  # 5 minutos
        self.tools = {
            "buscar_estudiantes": self.buscar_estudiantes,
            "gestionar_curso": self.gestionar_curso,
            "procesar_matricula": self.procesar_matricula,
            "analizar_rendimiento": self.analizar_rendimiento,
            "generar_dashboard": self.generar_dashboard,
            "exportar_datos": self.exportar_datos,
            "validar_prerequisitos": self.validar_prerequisitos,
            "simular_carga_academica": self.simular_carga_academica
        }
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con esquema avanzado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Esquema más completo
        schema_queries = [
            '''CREATE TABLE IF NOT EXISTS estudiantes (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                carrera TEXT NOT NULL,
                año INTEGER NOT NULL,
                activo BOOLEAN NOT NULL DEFAULT 1,
                fecha_ingreso TEXT NOT NULL,
                creditos_completados INTEGER DEFAULT 0,
                promedio_general REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )''',
            
            '''CREATE TABLE IF NOT EXISTS cursos (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                profesor TEXT NOT NULL,
                creditos INTEGER NOT NULL,
                max_estudiantes INTEGER NOT NULL,
                prerequisitos TEXT DEFAULT '[]',
                activo BOOLEAN NOT NULL DEFAULT 1,
                semestre TEXT NOT NULL,
                descripcion TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )''',
            
            '''CREATE TABLE IF NOT EXISTS matriculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante_id TEXT NOT NULL,
                curso_codigo TEXT NOT NULL,
                fecha_matricula TEXT NOT NULL,
                calificacion REAL,
                estado TEXT DEFAULT 'Matriculado',
                intentos INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                FOREIGN KEY (curso_codigo) REFERENCES cursos (codigo),
                UNIQUE(estudiante_id, curso_codigo, intentos)
            )''',
            
            '''CREATE TABLE IF NOT EXISTS log_actividad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tabla_afectada TEXT NOT NULL,
                accion TEXT NOT NULL,
                registro_id TEXT NOT NULL,
                datos_anteriores TEXT,
                datos_nuevos TEXT,
                usuario TEXT DEFAULT 'sistema',
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )'''
        ]
        
        for query in schema_queries:
            cursor.execute(query)
        
        # Insertar datos de ejemplo si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM estudiantes")
        if cursor.fetchone()[0] == 0:
            self._insertar_datos_ejemplo(cursor)
        
        conn.commit()
        conn.close()
        logger.info(f"Base de datos inicializada: {self.db_path}")
    
    def _insertar_datos_ejemplo(self, cursor):
        """Inserta datos de ejemplo más realistas"""
        estudiantes_ejemplo = [
            ("20240001", "Ana García López", "ana.garcia@univ.edu", "Ingeniería Informática", 3, True, "2022-09-01", 120, 8.5),
            ("20240002", "Carlos Martín Ruiz", "carlos.martin@univ.edu", "Matemáticas", 2, True, "2023-09-01", 80, 7.8),
            ("20240003", "María Rodríguez Sanz", "maria.rodriguez@univ.edu", "Física", 4, True, "2021-09-01", 180, 9.1),
            ("20240004", "David López Pérez", "david.lopez@univ.edu", "Ingeniería Informática", 1, True, "2024-09-01", 30, 7.2),
            ("20240005", "Elena Fernández Gil", "elena.fernandez@univ.edu", "Matemáticas", 3, True, "2022-09-01", 140, 8.9),
        ]
        
        cursor.executemany('''
            INSERT INTO estudiantes (id, nombre, email, carrera, año, activo, fecha_ingreso, creditos_completados, promedio_general) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', estudiantes_ejemplo)
        
        cursos_ejemplo = [
            ("INF101", "Programación I", "Dr. Juan Pérez", 6, 30, "[]", True, "2024S1", "Introducción a la programación"),
            ("INF201", "Estructuras de Datos", "Dr. Juan Pérez", 6, 25, '["INF101"]', True, "2024S2", "Algoritmos y estructuras"),
            ("INF301", "Bases de Datos", "Dra. Carmen Ruiz", 6, 20, '["INF101", "INF201"]', True, "2024S1", "Diseño de BD"),
            ("MAT101", "Cálculo I", "Dra. Elena Martín", 4, 40, "[]", True, "2024S1", "Límites y derivadas"),
            ("MAT201", "Álgebra Lineal", "Dra. Elena Martín", 4, 35, '["MAT101"]', True, "2024S2", "Matrices y vectores"),
            ("FIS101", "Física General", "Dr. Pedro Gómez", 5, 20, '["MAT101"]', True, "2024S1", "Mecánica clásica"),
        ]
        
        cursor.executemany('''
            INSERT INTO cursos (codigo, nombre, profesor, creditos, max_estudiantes, prerequisitos, activo, semestre, descripcion) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', cursos_ejemplo)
        
        # Algunas matrículas con calificaciones
        matriculas_ejemplo = [
            ("20240001", "INF101", "2022-09-15", 9.0, "Aprobado"),
            ("20240001", "INF201", "2023-02-01", 8.5, "Aprobado"),
            ("20240001", "MAT101", "2022-09-15", 8.0, "Aprobado"),
            ("20240002", "MAT101", "2023-09-15", 7.5, "Aprobado"),
            ("20240002", "MAT201", "2024-02-01", None, "Matriculado"),
            ("20240004", "INF101", "2024-09-15", None, "Matriculado"),
        ]
        
        cursor.executemany('''
            INSERT INTO matriculas (estudiante_id, curso_codigo, fecha_matricula, calificacion, estado) 
            VALUES (?, ?, ?, ?, ?)
        ''', matriculas_ejemplo)
    
    def _get_connection(self):
        """Obtiene conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def buscar_estudiantes(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Búsqueda avanzada de estudiantes con filtros múltiples"""
        try:
            filtros = args.get("filtros", {})
            orden = args.get("orden", "nombre")
            limite = args.get("limite", 50)
            
            # Crear clave de cache
            cache_key = f"buscar_estudiantes_{hash(str(sorted(filtros.items())))}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                logger.info("Resultado obtenido del cache")
                return cached_result
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Construir consulta dinámica
            where_clauses = []
            params = []
            
            if filtros.get("carrera"):
                where_clauses.append("carrera LIKE ?")
                params.append(f"%{filtros['carrera']}%")
            
            if filtros.get("año"):
                where_clauses.append("año = ?")
                params.append(filtros["año"])
            
            if filtros.get("activo") is not None:
                where_clauses.append("activo = ?")
                params.append(filtros["activo"])
            
            if filtros.get("promedio_min"):
                where_clauses.append("promedio_general >= ?")
                params.append(filtros["promedio_min"])
            
            where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
            
            query = f'''
                SELECT id, nombre, email, carrera, año, activo, fecha_ingreso, 
                       creditos_completados, promedio_general
                FROM estudiantes 
                WHERE {where_sql}
                ORDER BY {orden}
                LIMIT ?
            '''
            params.append(limite)
            
            cursor.execute(query, params)
            estudiantes = cursor.fetchall()
            
            # Obtener estadísticas adicionales
            cursor.execute(f"SELECT COUNT(*) FROM estudiantes WHERE {where_sql}", params[:-1])
            total_encontrados = cursor.fetchone()[0]
            
            resultado = {
                "success": True,
                "data": {
                    "estudiantes": [
                        {
                            "id": e[0], "nombre": e[1], "email": e[2], "carrera": e[3],
                            "año": e[4], "activo": bool(e[5]), "fecha_ingreso": e[6],
                            "creditos_completados": e[7], "promedio_general": e[8]
                        } for e in estudiantes
                    ],
                    "total_encontrados": total_encontrados,
                    "mostrando": len(estudiantes),
                    "filtros_aplicados": filtros
                }
            }
            
            conn.close()
            
            # Guardar en cache
            self.cache.set(cache_key, resultado)
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en buscar_estudiantes: {e}")
            return {"success": False, "error": str(e)}
    
    def gestionar_curso(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """CRUD completo para gestión de cursos"""
        try:
            accion = args.get("accion")  # crear, leer, actualizar, eliminar
            datos_curso = args.get("datos", {})
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if accion == "crear":
                curso = datos_curso
                cursor.execute('''
                    INSERT INTO cursos (codigo, nombre, profesor, creditos, max_estudiantes, 
                                      prerequisitos, semestre, descripcion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    curso["codigo"], curso["nombre"], curso["profesor"], 
                    curso["creditos"], curso["max_estudiantes"],
                    json.dumps(curso.get("prerequisitos", [])),
                    curso["semestre"], curso.get("descripcion", "")
                ))
                conn.commit()
                resultado = {"success": True, "message": f"Curso {curso['codigo']} creado"}
            
            elif accion == "leer":
                codigo = datos_curso.get("codigo")
                if codigo:
                    cursor.execute("SELECT * FROM cursos WHERE codigo = ?", (codigo,))
                    curso = cursor.fetchone()
                    if curso:
                        # Obtener estadísticas del curso
                        cursor.execute('''
                            SELECT COUNT(*) as matriculados,
                                   AVG(calificacion) as promedio,
                                   COUNT(CASE WHEN estado = 'Aprobado' THEN 1 END) as aprobados
                            FROM matriculas WHERE curso_codigo = ?
                        ''', (codigo,))
                        stats = cursor.fetchone()
                        
                        resultado = {
                            "success": True,
                            "data": {
                                "curso": {
                                    "codigo": curso[0], "nombre": curso[1], "profesor": curso[2],
                                    "creditos": curso[3], "max_estudiantes": curso[4],
                                    "prerequisitos": json.loads(curso[5]),
                                    "semestre": curso[7], "descripcion": curso[8]
                                },
                                "estadisticas": {
                                    "matriculados": stats[0],
                                    "promedio_calificaciones": round(stats[1], 2) if stats[1] else None,
                                    "aprobados": stats[2]
                                }
                            }
                        }
                else:
                    cursor.execute("SELECT * FROM cursos WHERE activo = 1")
                    cursos = cursor.fetchall()
                    resultado = {
                        "success": True,
                        "data": [
                            {
                                "codigo": c[0], "nombre": c[1], "profesor": c[2],
                                "creditos": c[3], "max_estudiantes": c[4],
                                "prerequisitos": json.loads(c[5]),
                                "semestre": c[7]
                            } for c in cursos
                        ]
                    }
            
            else:
                resultado = {"success": False, "error": f"Acción '{accion}' no soportada"}
            
            conn.close()
            return resultado
            
        except Exception as e:
            logger.error(f"Error en gestionar_curso: {e}")
            return {"success": False, "error": str(e)}
    
    def analizar_rendimiento(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis avanzado de rendimiento académico"""
        try:
            tipo_analisis = args.get("tipo", "general")  # general, por_carrera, por_curso
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            resultado = {"success": True, "data": {"tipo_analisis": tipo_analisis}}
            
            if tipo_analisis == "general":
                # Estadísticas generales del sistema
                queries = {
                    "total_estudiantes": "SELECT COUNT(*) FROM estudiantes WHERE activo = 1",
                    "promedio_sistema": "SELECT AVG(promedio_general) FROM estudiantes WHERE activo = 1 AND promedio_general > 0",
                    "total_cursos": "SELECT COUNT(*) FROM cursos WHERE activo = 1",
                    "total_matriculas": "SELECT COUNT(*) FROM matriculas",
                    "tasa_aprobacion": '''
                        SELECT 
                            COUNT(CASE WHEN estado = 'Aprobado' THEN 1 END) * 100.0 / COUNT(*) 
                        FROM matriculas 
                        WHERE calificacion IS NOT NULL
                    '''
                }
                
                for key, query in queries.items():
                    cursor.execute(query)
                    valor = cursor.fetchone()[0]
                    resultado["data"][key] = round(valor, 2) if valor else 0
                
                # Top estudiantes
                cursor.execute('''
                    SELECT nombre, carrera, promedio_general 
                    FROM estudiantes 
                    WHERE promedio_general > 0 
                    ORDER BY promedio_general DESC 
                    LIMIT 5
                ''')
                resultado["data"]["top_estudiantes"] = [
                    {"nombre": r[0], "carrera": r[1], "promedio": r[2]} 
                    for r in cursor.fetchall()
                ]
            
            elif tipo_analisis == "por_carrera":
                cursor.execute('''
                    SELECT carrera, 
                           COUNT(*) as total_estudiantes,
                           AVG(promedio_general) as promedio_carrera,
                           AVG(creditos_completados) as promedio_creditos
                    FROM estudiantes 
                    WHERE activo = 1 AND promedio_general > 0
                    GROUP BY carrera
                    ORDER BY promedio_carrera DESC
                ''')
                
                resultado["data"]["carreras"] = [
                    {
                        "carrera": r[0], "total_estudiantes": r[1],
                        "promedio_carrera": round(r[2], 2),
                        "promedio_creditos": round(r[3], 1)
                    } for r in cursor.fetchall()
                ]
            
            conn.close()
            return resultado
            
        except Exception as e:
            logger.error(f"Error en analizar_rendimiento: {e}")
            return {"success": False, "error": str(e)}
    
    def generar_dashboard(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Genera datos para dashboard administrativo"""
        try:
            cache_key = "dashboard_data"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Métricas principales
            cursor.execute('''
                SELECT 
                    (SELECT COUNT(*) FROM estudiantes WHERE activo = 1) as estudiantes_activos,
                    (SELECT COUNT(*) FROM cursos WHERE activo = 1) as cursos_activos,
                    (SELECT COUNT(*) FROM matriculas WHERE estado = 'Matriculado') as matriculas_activas,
                    (SELECT AVG(promedio_general) FROM estudiantes WHERE promedio_general > 0) as promedio_general
            ''')
            metricas = cursor.fetchone()
            
            # Distribución por año académico
            cursor.execute('''
                SELECT año, COUNT(*) as cantidad
                FROM estudiantes WHERE activo = 1
                GROUP BY año ORDER BY año
            ''')
            distribucion_años = cursor.fetchall()
            
            # Cursos con más demanda
            cursor.execute('''
                SELECT c.nombre, c.codigo, COUNT(m.id) as matriculados, c.max_estudiantes
                FROM cursos c
                LEFT JOIN matriculas m ON c.codigo = m.curso_codigo AND m.estado = 'Matriculado'
                WHERE c.activo = 1
                GROUP BY c.codigo, c.nombre, c.max_estudiantes
                ORDER BY matriculados DESC
                LIMIT 5
            ''')
            cursos_demanda = cursor.fetchall()
            
            resultado = {
                "success": True,
                "data": {
                    "metricas_principales": {
                        "estudiantes_activos": metricas[0],
                        "cursos_activos": metricas[1],
                        "matriculas_activas": metricas[2],
                        "promedio_general": round(metricas[3], 2) if metricas[3] else 0
                    },
                    "distribucion_años": [
                        {"año": r[0], "cantidad": r[1]} for r in distribucion_años
                    ],
                    "cursos_mas_demandados": [
                        {
                            "nombre": r[0], "codigo": r[1], "matriculados": r[2],
                            "max_estudiantes": r[3], "ocupacion_pct": round((r[2]/r[3])*100, 1)
                        } for r in cursos_demanda
                    ],
                    "cache_stats": self.cache.get_stats(),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            conn.close()
            self.cache.set(cache_key, resultado)
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en generar_dashboard: {e}")
            return {"success": False, "error": str(e)}
    
    # Implementar el resto de herramientas...
    def procesar_matricula(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa matrícula con validación de prerequisitos"""
        # Implementación similar pero más avanzada...
        return {"success": True, "message": "Matrícula procesada (implementar completamente)"}
    
    def exportar_datos(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Exporta datos en diferentes formatos"""
        return {"success": True, "message": "Exportación disponible (implementar completamente)"}
    
    def validar_prerequisitos(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Valida prerequisitos para un curso"""
        return {"success": True, "message": "Validación de prerequisitos (implementar completamente)"}
    
    def simular_carga_academica(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Simula diferentes escenarios de carga académica"""
        return {"success": True, "message": "Simulación de carga (implementar completamente)"}

def main():
    """Función principal con modo interactivo mejorado"""
    print("🚀 Servidor MCP Universitario Avanzado - Día 3", file=sys.stderr)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        server = UniversidadMCPAvanzado()
        
        print("\n🔧 Modo interactivo - Herramientas disponibles:")
        print("1. buscar_estudiantes({'filtros': {'carrera': 'Informática'}})")
        print("2. gestionar_curso({'accion': 'leer', 'datos': {}})")
        print("3. analizar_rendimiento({'tipo': 'general'})")
        print("4. generar_dashboard({})")
        
        while True:
            try:
                cmd = input("\n> ").strip()
                if cmd.lower() in ['exit', 'quit']:
                    break
                
                # Ejemplos rápidos
                if cmd == "1":
                    result = server.buscar_estudiantes({'filtros': {'carrera': 'Informática'}})
                elif cmd == "2":
                    result = server.gestionar_curso({'accion': 'leer', 'datos': {}})
                elif cmd == "3":
                    result = server.analizar_rendimiento({'tipo': 'general'})
                elif cmd == "4":
                    result = server.generar_dashboard({})
                else:
                    print("Comando no reconocido")
                    continue
                
                print(json.dumps(result, indent=2))
                
            except KeyboardInterrupt:
                break
    
    else:
        # Modo servidor MCP real
        server = UniversidadMCPAvanzado()
        print("Servidor MCP avanzado iniciado...", file=sys.stderr)

if __name__ == "__main__":
    main()
