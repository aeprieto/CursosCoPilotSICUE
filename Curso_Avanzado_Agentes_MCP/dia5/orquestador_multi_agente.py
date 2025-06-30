#!/usr/bin/env python3
"""
Sistema de Orquestación Multi-Agente para Universidad - Día 5
Implementa arquitectura distribuida con governance y seguridad
"""

import asyncio
import uuid
import json
import logging
import sys
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
import hashlib
from pathlib import Path
import sqlite3

# JWT simplificado para la demo (en producción usar PyJWT)
class SimpleJWT:
    @staticmethod
    def encode(payload, secret, algorithm="HS256"):
        import base64
        import hmac
        header = {"alg": algorithm, "typ": "JWT"}
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        message = f"{header_b64}.{payload_b64}"
        signature = base64.urlsafe_b64encode(
            hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        ).decode().rstrip('=')
        return f"{message}.{signature}"
    
    @staticmethod
    def decode(token, secret, algorithms=None):
        import base64
        import hmac
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Token inválido")
        header_b64, payload_b64, signature_b64 = parts
        
        # Verificar firma
        message = f"{header_b64}.{payload_b64}"
        expected_sig = base64.urlsafe_b64encode(
            hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        ).decode().rstrip('=')
        
        if signature_b64 != expected_sig:
            raise ValueError("Firma inválida")
        
        # Decodificar payload
        payload_json = base64.urlsafe_b64decode(payload_b64 + '===').decode()
        payload = json.loads(payload_json)
        
        # Verificar expiración
        if 'exp' in payload:
            if datetime.utcnow().timestamp() > payload['exp']:
                raise ValueError("Token expirado")
        
        return payload

jwt = SimpleJWT()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TipoAgente(Enum):
    """Tipos de agentes en el ecosistema universitario"""
    ACADEMICO = "academico"
    SOPORTE_IT = "soporte_it"
    BIBLIOTECA = "biblioteca"
    ADMINISTRACION = "administracion"
    FINANCIERO = "financiero"
    SEGURIDAD = "seguridad"

class EstadoTarea(Enum):
    """Estados posibles de una tarea"""
    PENDIENTE = "pendiente"
    ASIGNADA = "asignada"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    FALLIDA = "fallida"
    CANCELADA = "cancelada"

class NivelPrioridad(Enum):
    """Niveles de prioridad para tareas"""
    BAJA = 1
    NORMAL = 2
    ALTA = 3
    CRITICA = 4
    EMERGENCIA = 5

@dataclass
class TareaOrquestada:
    """Representa una tarea en el sistema de orquestación"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tipo: str = ""
    descripcion: str = ""
    agente_requerido: TipoAgente = TipoAgente.ACADEMICO
    prioridad: NivelPrioridad = NivelPrioridad.NORMAL
    estado: EstadoTarea = EstadoTarea.PENDIENTE
    datos_entrada: Dict[str, Any] = field(default_factory=dict)
    resultado: Optional[Dict[str, Any]] = None
    agente_asignado: Optional[str] = None
    tiempo_creacion: datetime = field(default_factory=datetime.now)
    tiempo_asignacion: Optional[datetime] = None
    tiempo_completado: Optional[datetime] = None
    intentos: int = 0
    max_intentos: int = 3
    dependencias: List[str] = field(default_factory=list)
    metadatos: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegistroAuditoria:
    """Registro de auditoría para compliance"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    usuario: str = ""
    accion: str = ""
    recurso: str = ""
    resultado: str = ""
    ip_origen: str = ""
    agente_usuario: str = ""
    datos_adicionales: Dict[str, Any] = field(default_factory=dict)

class GestorSeguridad:
    """Gestiona autenticación, autorización y auditoría"""
    
    def __init__(self, clave_secreta: str):
        self.clave_secreta = clave_secreta
        self.permisos_rol = self._cargar_permisos()
        self.registros_auditoria = []
    
    def _cargar_permisos(self) -> Dict[str, List[str]]:
        """Carga la matriz de permisos por rol"""
        return {
            "admin_sistema": ["*"],  # Acceso completo
            "decano": ["academico.*", "administracion.reportes", "financiero.consultas"],
            "director_it": ["soporte_it.*", "seguridad.*"],
            "bibliotecario": ["biblioteca.*"],
            "profesor": ["academico.consultas", "biblioteca.consultas"],
            "estudiante": ["academico.consultas_propias", "biblioteca.servicios"],
            "personal_admin": ["administracion.*", "financiero.basico"]
        }
    
    def generar_token(self, usuario: str, rol: str, duracion_horas: int = 8) -> str:
        """Genera token JWT para autenticación"""
        payload = {
            "usuario": usuario,
            "rol": rol,
            "exp": datetime.utcnow() + timedelta(hours=duracion_horas),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.clave_secreta, algorithm="HS256")
    
    def validar_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Valida token JWT"""
        try:
            payload = jwt.decode(token, self.clave_secreta, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado")
            return None
        except (jwt.InvalidTokenError, ValueError):
            logger.warning("Token inválido")
            return None
    
    def autorizar_accion(self, usuario: str, rol: str, accion: str) -> bool:
        """Verifica si un usuario tiene permisos para una acción"""
        permisos_usuario = self.permisos_rol.get(rol, [])
        
        # Acceso completo
        if "*" in permisos_usuario:
            return True
        
        # Verificar permisos específicos
        for permiso in permisos_usuario:
            if permiso.endswith("*"):
                if accion.startswith(permiso[:-1]):
                    return True
            elif permiso == accion:
                return True
        
        return False
    
    def registrar_auditoria(self, usuario: str, accion: str, recurso: str, 
                          resultado: str, **kwargs):
        """Registra evento para auditoría"""
        registro = RegistroAuditoria(
            usuario=usuario,
            accion=accion,
            recurso=recurso,
            resultado=resultado,
            ip_origen=kwargs.get("ip_origen", "desconocida"),
            agente_usuario=kwargs.get("agente_usuario", "sistema"),
            datos_adicionales=kwargs.get("datos_adicionales", {})
        )
        
        self.registros_auditoria.append(registro)
        logger.info(f"Auditoría: {usuario} - {accion} - {resultado}")
    
    def generar_reporte_auditoria(self, fecha_inicio: datetime, 
                                fecha_fin: datetime) -> List[Dict[str, Any]]:
        """Genera reporte de auditoría para compliance"""
        registros_periodo = [
            r for r in self.registros_auditoria
            if fecha_inicio <= r.timestamp <= fecha_fin
        ]
        
        return [asdict(r) for r in registros_periodo]

class AgenteEspecializado:
    """Clase base para agentes especializados"""
    
    def __init__(self, tipo: TipoAgente, nombre: str, capacidades: List[str]):
        self.id = str(uuid.uuid4())
        self.tipo = tipo
        self.nombre = nombre
        self.capacidades = capacidades
        self.estado = "disponible"  # disponible, ocupado, mantenimiento
        self.tareas_en_proceso = []
        self.estadisticas = {
            "tareas_completadas": 0,
            "tareas_fallidas": 0,
            "tiempo_promedio_respuesta": 0.0
        }
    
    async def procesar_tarea(self, tarea: TareaOrquestada) -> Dict[str, Any]:
        """Procesa una tarea asignada"""
        self.estado = "ocupado"
        inicio = datetime.now()
        
        try:
            # Simulación de procesamiento específico por tipo
            resultado = await self._ejecutar_tarea_especializada(tarea)
            
            # Actualizar estadísticas
            tiempo_procesamiento = (datetime.now() - inicio).total_seconds()
            self.estadisticas["tareas_completadas"] += 1
            self._actualizar_tiempo_promedio(tiempo_procesamiento)
            
            self.estado = "disponible"
            return resultado
            
        except Exception as e:
            self.estadisticas["tareas_fallidas"] += 1
            self.estado = "disponible"
            raise e
    
    async def _ejecutar_tarea_especializada(self, tarea: TareaOrquestada) -> Dict[str, Any]:
        """Implementación específica según el tipo de agente"""
        # Simular diferentes tiempos de procesamiento
        await asyncio.sleep(0.5)  # Simular trabajo
        
        if self.tipo == TipoAgente.ACADEMICO:
            return await self._procesar_tarea_academica(tarea)
        elif self.tipo == TipoAgente.SOPORTE_IT:
            return await self._procesar_tarea_it(tarea)
        elif self.tipo == TipoAgente.BIBLIOTECA:
            return await self._procesar_tarea_biblioteca(tarea)
        elif self.tipo == TipoAgente.ADMINISTRACION:
            return await self._procesar_tarea_administrativa(tarea)
        elif self.tipo == TipoAgente.FINANCIERO:
            return await self._procesar_tarea_financiera(tarea)
        else:
            return {"success": False, "error": "Tipo de agente no implementado"}
    
    async def _procesar_tarea_academica(self, tarea: TareaOrquestada) -> Dict[str, Any]:
        """Procesa tareas académicas"""
        if tarea.tipo == "matricula":
            return {
                "success": True,
                "data": {
                    "estudiante_matriculado": True,
                    "cursos_asignados": tarea.datos_entrada.get("cursos", []),
                    "creditos_totales": len(tarea.datos_entrada.get("cursos", [])) * 4
                }
            }
        elif tarea.tipo == "calificaciones":
            return {
                "success": True,
                "data": {
                    "calificaciones_procesadas": True,
                    "promedio_calculado": 8.5
                }
            }
        return {"success": True, "data": {"procesado": True}}
    
    async def _procesar_tarea_it(self, tarea: TareaOrquestada) -> Dict[str, Any]:
        """Procesa tareas de soporte IT"""
        if tarea.tipo == "crear_usuario":
            return {
                "success": True,
                "data": {
                    "usuario_creado": True,
                    "credenciales": {
                        "usuario": tarea.datos_entrada.get("nombre_usuario", "user123"),
                        "password_temporal": "temp_" + str(uuid.uuid4())[:8]
                    }
                }
            }
        elif tarea.tipo == "resolver_incidencia":
            return {
                "success": True,
                "data": {
                    "incidencia_resuelta": True,
                    "tiempo_resolucion": "15 minutos",
                    "ticket_cerrado": True
                }
            }
        return {"success": True, "data": {"procesado": True}}
    
    async def _procesar_tarea_biblioteca(self, tarea: TareaOrquestada) -> Dict[str, Any]:
        """Procesa tareas de biblioteca"""
        if tarea.tipo == "reservar_recurso":
            return {
                "success": True,
                "data": {
                    "reserva_confirmada": True,
                    "recurso": tarea.datos_entrada.get("recurso", "Sala de estudio"),
                    "fecha_reserva": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
            }
        return {"success": True, "data": {"procesado": True}}
    
    async def _procesar_tarea_administrativa(self, tarea: TareaOrquestada) -> Dict[str, Any]:
        """Procesa tareas administrativas"""
        if tarea.tipo == "generar_certificado":
            return {
                "success": True,
                "data": {
                    "certificado_generado": True,
                    "numero_certificado": f"CERT-{datetime.now().year}-{uuid.uuid4().hex[:8].upper()}"
                }
            }
        return {"success": True, "data": {"procesado": True}}
    
    async def _procesar_tarea_financiera(self, tarea: TareaOrquestada) -> Dict[str, Any]:
        """Procesa tareas financieras"""
        if tarea.tipo == "procesar_pago":
            return {
                "success": True,
                "data": {
                    "pago_procesado": True,
                    "numero_transaccion": f"TXN-{uuid.uuid4().hex[:12].upper()}",
                    "monto": tarea.datos_entrada.get("monto", 0)
                }
            }
        return {"success": True, "data": {"procesado": True}}
    
    def _actualizar_tiempo_promedio(self, nuevo_tiempo: float):
        """Actualiza el tiempo promedio de respuesta"""
        total_tareas = self.estadisticas["tareas_completadas"]
        if total_tareas == 1:
            self.estadisticas["tiempo_promedio_respuesta"] = nuevo_tiempo
        else:
            tiempo_actual = self.estadisticas["tiempo_promedio_respuesta"]
            self.estadisticas["tiempo_promedio_respuesta"] = (
                (tiempo_actual * (total_tareas - 1) + nuevo_tiempo) / total_tareas
            )

class OrquestadorCentral:
    """Orquestador central que coordina todos los agentes"""
    
    def __init__(self, gestor_seguridad: GestorSeguridad):
        self.agentes: Dict[str, AgenteEspecializado] = {}
        self.cola_tareas: List[TareaOrquestada] = []
        self.tareas_activas: Dict[str, TareaOrquestada] = {}
        self.historial_tareas: List[TareaOrquestada] = []
        self.gestor_seguridad = gestor_seguridad
        self.configuracion = self._cargar_configuracion()
        self.metricas_sistema = {
            "tareas_totales": 0,
            "tareas_exitosas": 0,
            "tareas_fallidas": 0,
            "tiempo_promedio_cola": 0.0
        }
    
    def _cargar_configuracion(self) -> Dict[str, Any]:
        """Carga configuración del sistema"""
        return {
            "max_tareas_por_agente": 5,
            "timeout_tarea_segundos": 300,
            "reintento_automatico": True,
            "notificaciones_activas": True,
            "modo_debug": True
        }
    
    def registrar_agente(self, agente: AgenteEspecializado):
        """Registra un nuevo agente en el sistema"""
        self.agentes[agente.id] = agente
        logger.info(f"Agente registrado: {agente.nombre} ({agente.tipo.value})")
    
    async def enviar_tarea(self, tarea: TareaOrquestada, token_usuario: str = None) -> str:
        """Envía una nueva tarea al sistema"""
        # Validar autorización si se proporciona token
        if token_usuario:
            payload = self.gestor_seguridad.validar_token(token_usuario)
            if not payload:
                raise PermissionError("Token inválido o expirado")
            
            accion_requerida = f"{tarea.agente_requerido.value}.{tarea.tipo}"
            if not self.gestor_seguridad.autorizar_accion(
                payload["usuario"], payload["rol"], accion_requerida
            ):
                self.gestor_seguridad.registrar_auditoria(
                    payload["usuario"], accion_requerida, tarea.id, "DENEGADO"
                )
                raise PermissionError("Sin permisos para esta acción")
            
            # Registrar en auditoría
            self.gestor_seguridad.registrar_auditoria(
                payload["usuario"], accion_requerida, tarea.id, "AUTORIZADO"
            )
        
        # Añadir a la cola
        self.cola_tareas.append(tarea)
        self.metricas_sistema["tareas_totales"] += 1
        
        logger.info(f"Tarea enviada: {tarea.id} - {tarea.tipo}")
        
        # Procesar cola de forma asíncrona
        asyncio.create_task(self._procesar_cola())
        
        return tarea.id
    
    async def _procesar_cola(self):
        """Procesa la cola de tareas asignando a agentes disponibles"""
        while self.cola_tareas:
            tarea = self.cola_tareas.pop(0)
            
            # Verificar dependencias
            if not self._dependencias_completadas(tarea):
                # Reencolar al final
                self.cola_tareas.append(tarea)
                continue
            
            # Buscar agente disponible
            agente_disponible = self._encontrar_agente_disponible(tarea.agente_requerido)
            
            if agente_disponible:
                # Asignar tarea
                tarea.estado = EstadoTarea.ASIGNADA
                tarea.agente_asignado = agente_disponible.id
                tarea.tiempo_asignacion = datetime.now()
                
                self.tareas_activas[tarea.id] = tarea
                
                # Procesar de forma asíncrona
                asyncio.create_task(self._ejecutar_tarea(agente_disponible, tarea))
            else:
                # No hay agentes disponibles, reencolar
                self.cola_tareas.append(tarea)
                break
    
    def _dependencias_completadas(self, tarea: TareaOrquestada) -> bool:
        """Verifica si las dependencias de una tarea están completadas"""
        for dep_id in tarea.dependencias:
            # Buscar en historial
            tarea_dep = next(
                (t for t in self.historial_tareas if t.id == dep_id),
                None
            )
            if not tarea_dep or tarea_dep.estado != EstadoTarea.COMPLETADA:
                return False
        return True
    
    def _encontrar_agente_disponible(self, tipo_requerido: TipoAgente) -> Optional[AgenteEspecializado]:
        """Encuentra un agente disponible del tipo requerido"""
        agentes_tipo = [
            a for a in self.agentes.values()
            if a.tipo == tipo_requerido and a.estado == "disponible"
        ]
        
        if not agentes_tipo:
            return None
        
        # Seleccionar el agente con menos carga
        return min(agentes_tipo, key=lambda a: len(a.tareas_en_proceso))
    
    async def _ejecutar_tarea(self, agente: AgenteEspecializado, tarea: TareaOrquestada):
        """Ejecuta una tarea en un agente específico"""
        try:
            tarea.estado = EstadoTarea.EN_PROCESO
            agente.tareas_en_proceso.append(tarea.id)
            
            # Ejecutar tarea
            resultado = await agente.procesar_tarea(tarea)
            
            # Completar tarea
            tarea.resultado = resultado
            tarea.estado = EstadoTarea.COMPLETADA
            tarea.tiempo_completado = datetime.now()
            
            # Limpiar referencias
            agente.tareas_en_proceso.remove(tarea.id)
            del self.tareas_activas[tarea.id]
            self.historial_tareas.append(tarea)
            
            # Actualizar métricas
            self.metricas_sistema["tareas_exitosas"] += 1
            
            logger.info(f"Tarea completada: {tarea.id}")
            
        except Exception as e:
            # Manejar fallo
            tarea.estado = EstadoTarea.FALLIDA
            tarea.resultado = {"success": False, "error": str(e)}
            tarea.intentos += 1
            
            agente.tareas_en_proceso.remove(tarea.id)
            
            # Reintentar si es posible
            if (tarea.intentos < tarea.max_intentos and 
                self.configuracion.get("reintento_automatico", True)):
                
                tarea.estado = EstadoTarea.PENDIENTE
                self.cola_tareas.append(tarea)
                logger.warning(f"Reintentando tarea: {tarea.id} (intento {tarea.intentos})")
            else:
                del self.tareas_activas[tarea.id]
                self.historial_tareas.append(tarea)
                self.metricas_sistema["tareas_fallidas"] += 1
                logger.error(f"Tarea fallida definitivamente: {tarea.id}")
            
        # Continuar procesando la cola
        await self._procesar_cola()
    
    def obtener_estado_sistema(self) -> Dict[str, Any]:
        """Obtiene el estado completo del sistema"""
        return {
            "agentes_registrados": len(self.agentes),
            "agentes_por_tipo": {
                tipo.value: len([a for a in self.agentes.values() if a.tipo == tipo])
                for tipo in TipoAgente
            },
            "tareas_en_cola": len(self.cola_tareas),
            "tareas_activas": len(self.tareas_activas),
            "tareas_completadas": len(self.historial_tareas),
            "metricas": self.metricas_sistema,
            "timestamp": datetime.now().isoformat()
        }
    
    async def generar_reporte_rendimiento(self) -> Dict[str, Any]:
        """Genera reporte detallado de rendimiento"""
        # Métricas por agente
        metricas_agentes = {}
        for agente in self.agentes.values():
            metricas_agentes[agente.nombre] = {
                "tipo": agente.tipo.value,
                "estado": agente.estado,
                "estadisticas": agente.estadisticas,
                "carga_actual": len(agente.tareas_en_proceso)
            }
        
        # Análisis de tareas
        tareas_por_estado = {}
        for estado in EstadoTarea:
            count = len([t for t in self.historial_tareas if t.estado == estado])
            tareas_por_estado[estado.value] = count
        
        return {
            "resumen_sistema": self.obtener_estado_sistema(),
            "metricas_agentes": metricas_agentes,
            "distribucion_tareas": tareas_por_estado,
            "rendimiento_temporal": self._calcular_metricas_temporales(),
            "recomendaciones": self._generar_recomendaciones_rendimiento()
        }
    
    def _calcular_metricas_temporales(self) -> Dict[str, Any]:
        """Calcula métricas temporales del sistema"""
        if not self.historial_tareas:
            return {}
        
        tiempos_completado = []
        for tarea in self.historial_tareas:
            if (tarea.tiempo_completado and tarea.tiempo_creacion and 
                tarea.estado == EstadoTarea.COMPLETADA):
                tiempo_total = (tarea.tiempo_completado - tarea.tiempo_creacion).total_seconds()
                tiempos_completado.append(tiempo_total)
        
        if not tiempos_completado:
            return {}
        
        return {
            "tiempo_promedio_completado": sum(tiempos_completado) / len(tiempos_completado),
            "tiempo_minimo": min(tiempos_completado),
            "tiempo_maximo": max(tiempos_completado),
            "total_tareas_medidas": len(tiempos_completado)
        }
    
    def _generar_recomendaciones_rendimiento(self) -> List[str]:
        """Genera recomendaciones para mejorar el rendimiento"""
        recomendaciones = []
        
        # Analizar cola
        if len(self.cola_tareas) > 10:
            recomendaciones.append("Considerar añadir más agentes - cola excesiva")
        
        # Analizar distribución de agentes
        tipos_agentes = {}
        for agente in self.agentes.values():
            tipos_agentes[agente.tipo] = tipos_agentes.get(agente.tipo, 0) + 1
        
        if len(tipos_agentes) < len(TipoAgente):
            recomendaciones.append("Faltan tipos de agentes especializados")
        
        # Analizar tasa de fallos
        if self.metricas_sistema["tareas_fallidas"] > 0:
            tasa_fallo = (self.metricas_sistema["tareas_fallidas"] / 
                         self.metricas_sistema["tareas_totales"])
            if tasa_fallo > 0.1:  # Más del 10% de fallos
                recomendaciones.append("Tasa de fallos alta - revisar configuración de agentes")
        
        return recomendaciones

async def demo_sistema_completo():
    """Demo completa del sistema de orquestación"""
    print("🚀 Sistema de Orquestación Multi-Agente Universitario")
    print("=" * 60)
    
    # Inicializar componentes
    gestor_seguridad = GestorSeguridad("clave_secreta_universidad_2024")
    orquestador = OrquestadorCentral(gestor_seguridad)
    
    # Crear y registrar agentes
    agentes = [
        AgenteEspecializado(TipoAgente.ACADEMICO, "Agente Académico Principal", 
                          ["matriculas", "calificaciones", "certificados"]),
        AgenteEspecializado(TipoAgente.SOPORTE_IT, "Agente IT Support", 
                          ["usuarios", "incidencias", "infraestructura"]),
        AgenteEspecializado(TipoAgente.BIBLIOTECA, "Agente Biblioteca Digital", 
                          ["reservas", "catalogos", "recursos"]),
        AgenteEspecializado(TipoAgente.ADMINISTRACION, "Agente Administrativo", 
                          ["certificados", "tramites", "documentos"]),
        AgenteEspecializado(TipoAgente.FINANCIERO, "Agente Financiero", 
                          ["pagos", "becas", "facturacion"])
    ]
    
    for agente in agentes:
        orquestador.registrar_agente(agente)
    
    print(f"✅ {len(agentes)} agentes registrados")
    
    # Generar token de autenticación para admin
    token_admin = gestor_seguridad.generar_token("admin", "admin_sistema")
    print("✅ Token de administrador generado")
    
    # Crear tareas de ejemplo
    tareas_ejemplo = [
        TareaOrquestada(
            tipo="matricula",
            descripcion="Matricular estudiante nuevo",
            agente_requerido=TipoAgente.ACADEMICO,
            prioridad=NivelPrioridad.ALTA,
            datos_entrada={"estudiante_id": "20240001", "cursos": ["INF101", "MAT101"]}
        ),
        TareaOrquestada(
            tipo="crear_usuario",
            descripcion="Crear credenciales IT",
            agente_requerido=TipoAgente.SOPORTE_IT,
            prioridad=NivelPrioridad.NORMAL,
            datos_entrada={"nombre_usuario": "estudiante20240001", "tipo": "estudiante"}
        ),
        TareaOrquestada(
            tipo="reservar_recurso",
            descripción="Reservar sala de estudio",
            agente_requerido=TipoAgente.BIBLIOTECA,
            prioridad=NivelPrioridad.BAJA,
            datos_entrada={"recurso": "Sala Estudio Grupal 1", "fecha": "2024-12-01"}
        ),
        TareaOrquestada(
            tipo="generar_certificado",
            descripcion="Generar certificado de estudios",
            agente_requerido=TipoAgente.ADMINISTRACION,
            prioridad=NivelPrioridad.NORMAL,
            datos_entrada={"estudiante_id": "20240001", "tipo_certificado": "estudios"}
        )
    ]
    
    # Enviar tareas
    print("\n📤 Enviando tareas al sistema...")
    for tarea in tareas_ejemplo:
        tarea_id = await orquestador.enviar_tarea(tarea, token_admin)
        print(f"   Tarea enviada: {tarea.tipo} -> {tarea_id[:8]}")
    
    # Esperar procesamiento
    print("\n⏳ Procesando tareas...")
    await asyncio.sleep(3)  # Esperar que se procesen las tareas
    
    # Mostrar estado del sistema
    estado = orquestador.obtener_estado_sistema()
    print("\n📊 Estado del Sistema:")
    print(f"   Agentes registrados: {estado['agentes_registrados']}")
    print(f"   Tareas completadas: {estado['tareas_completadas']}")
    print(f"   Tareas en cola: {estado['tareas_en_cola']}")
    
    # Generar reporte de rendimiento
    reporte = await orquestador.generar_reporte_rendimiento()
    print("\n📈 Reporte de rendimiento generado")
    if reporte.get("recomendaciones"):
        print("   Recomendaciones:")
        for rec in reporte["recomendaciones"]:
            print(f"   - {rec}")
    
    # Mostrar registros de auditoría
    registros = gestor_seguridad.generar_reporte_auditoria(
        datetime.now() - timedelta(hours=1),
        datetime.now()
    )
    print(f"\n🔍 Registros de auditoría: {len(registros)} eventos")
    
    print("\n✨ Demo completada exitosamente")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        asyncio.run(demo_sistema_completo())
    else:
        print("🏗️ Sistema de Orquestación Multi-Agente - Día 5")
        print("=" * 50)
        print("Este sistema implementa:")
        print("- Orquestación centralizada de agentes especializados")
        print("- Gestión de seguridad y autorización con JWT")
        print("- Auditoría completa para compliance")
        print("- Métricas y monitorización en tiempo real")
        print("- Manejo de dependencias entre tareas")
        print("- Balanceado de carga automático")
        print("\nEjecuta con --demo para ver una demostración completa")
