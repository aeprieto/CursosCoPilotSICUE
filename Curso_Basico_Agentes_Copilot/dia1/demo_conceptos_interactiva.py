#!/usr/bin/env python3
"""
Ejemplos Interactivos de Conceptos Fundamentales - Día 1 Curso Básico
Demostración práctica de diferencias entre chatbots, agentes y asistentes
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re

class ChatbotBasico:
    """
    Ejemplo de chatbot simple con respuestas predefinidas
    Muestra las limitaciones de los sistemas basados en reglas
    """
    
    def __init__(self):
        self.respuestas_predefinidas = {
            "horario biblioteca": "La biblioteca está abierta de lunes a viernes de 8:00 a 22:00, sábados de 9:00 a 18:00.",
            "matricula": "El período de matrícula es del 1 al 15 de septiembre. Contacta con secretaría para más información.",
            "wifi": "La red WiFi de la universidad es 'UNIV-WiFi'. Usa tus credenciales de estudiante para conectarte.",
            "cafeteria": "La cafetería está abierta de 8:00 a 17:00. Menú del día disponible en la web principal.",
            "ayuda": "Puedo ayudarte con: horarios, matrícula, wifi, cafetería. ¿Sobre qué quieres información?"
        }
        
        self.palabras_clave = {
            "horario biblioteca": ["horario", "biblioteca", "abierto", "cerrado"],
            "matricula": ["matricula", "inscribir", "curso", "asignatura"],
            "wifi": ["wifi", "internet", "conexion", "red"],
            "cafeteria": ["cafeteria", "comida", "menu", "almuerzo"],
            "ayuda": ["ayuda", "help", "que puedes", "opciones"]
        }
    
    def procesar_mensaje(self, mensaje: str) -> str:
        """Procesa mensaje del usuario usando coincidencia de palabras clave"""
        mensaje_lower = mensaje.lower().strip()
        
        # Buscar coincidencias exactas primero
        for tema, respuesta in self.respuestas_predefinidas.items():
            if tema in mensaje_lower:
                return f"🤖 Chatbot: {respuesta}"
        
        # Buscar por palabras clave
        for tema, palabras in self.palabras_clave.items():
            if any(palabra in mensaje_lower for palabra in palabras):
                return f"🤖 Chatbot: {self.respuestas_predefinidas[tema]}"
        
        # Respuesta por defecto
        return "🤖 Chatbot: Lo siento, no entiendo tu consulta. Escribe 'ayuda' para ver qué puedo hacer."

class AgenteUniversitario:
    """
    Ejemplo de agente que puede realizar acciones y tiene memoria
    Muestra capacidades más avanzadas que un chatbot simple
    """
    
    def __init__(self):
        self.memoria_conversacion = []
        self.estado_usuario = {}
        self.base_datos_simulada = {
            "estudiantes": {
                "12345": {"nombre": "Ana García", "carrera": "Informática", "año": 3},
                "67890": {"nombre": "Carlos López", "carrera": "Matemáticas", "año": 2}
            },
            "cursos": {
                "INF101": {"nombre": "Programación I", "creditos": 6, "plazas": 30, "ocupadas": 25},
                "MAT101": {"nombre": "Cálculo I", "creditos": 4, "plazas": 40, "ocupadas": 38}
            },
            "reservas_biblioteca": []
        }
        self.herramientas_disponibles = [
            "consultar_estudiante",
            "consultar_curso", 
            "reservar_sala",
            "calcular_creditos",
            "generar_horario"
        ]
    
    def procesar_mensaje(self, mensaje: str, id_usuario: str = "invitado") -> str:
        """Procesa mensaje con capacidades de agente: memoria, acciones, razonamiento"""
        # Guardar en memoria
        self.memoria_conversacion.append({
            "timestamp": datetime.now(),
            "usuario": id_usuario,
            "mensaje": mensaje
        })
        
        # Analizar intención del usuario
        intencion = self._analizar_intencion(mensaje)
        
        # Ejecutar acção según la intención
        if intencion == "consultar_estudiante":
            return self._consultar_estudiante(mensaje, id_usuario)
        elif intencion == "consultar_curso":
            return self._consultar_curso(mensaje)
        elif intencion == "reservar_sala":
            return self._reservar_sala(mensaje, id_usuario)
        elif intencion == "calcular_creditos":
            return self._calcular_creditos(mensaje, id_usuario)
        elif intencion == "conversacion_general":
            return self._responder_contextual(mensaje, id_usuario)
        else:
            return self._respuesta_con_herramientas(mensaje)
    
    def _analizar_intencion(self, mensaje: str) -> str:
        """Analiza la intención del usuario usando patrones simples"""
        mensaje_lower = mensaje.lower()
        
        patrones_intencion = {
            "consultar_estudiante": ["mi perfil", "mis datos", "mi información", "estudiante"],
            "consultar_curso": ["curso", "asignatura", "materia", "plazas disponibles"],
            "reservar_sala": ["reservar", "sala", "espacio", "aula"],
            "calcular_creditos": ["creditos", "cálculo", "cuantos creditos"],
            "conversacion_general": ["hola", "gracias", "adios", "como estas"]
        }
        
        for intencion, patrones in patrones_intencion.items():
            if any(patron in mensaje_lower for patron in patrones):
                return intencion
        
        return "desconocida"
    
    def _consultar_estudiante(self, mensaje: str, id_usuario: str) -> str:
        """Simula consulta de datos del estudiante"""
        if id_usuario in self.base_datos_simulada["estudiantes"]:
            estudiante = self.base_datos_simulada["estudiantes"][id_usuario]
            return f"""🤖 Agente: Aquí tienes tu información académica:
            
📚 Perfil Académico:
• Nombre: {estudiante['nombre']}
• Carrera: {estudiante['carrera']}
• Año actual: {estudiante['año']}

¿Necesitas que consulte algo más específico?"""
        else:
            return "🤖 Agente: No encuentro tu perfil de estudiante. ¿Podrías proporcionar tu número de estudiante?"
    
    def _consultar_curso(self, mensaje: str) -> str:
        """Consulta información de cursos"""
        # Buscar códigos de curso en el mensaje
        codigos_encontrados = re.findall(r'[A-Z]{3}\d{3}', mensaje.upper())
        
        if codigos_encontrados:
            info_cursos = []
            for codigo in codigos_encontrados:
                if codigo in self.base_datos_simulada["cursos"]:
                    curso = self.base_datos_simulada["cursos"][codigo]
                    plazas_libres = curso["plazas"] - curso["ocupadas"]
                    info_cursos.append(f"""
📖 {codigo} - {curso['nombre']}
• Créditos: {curso['creditos']}
• Plazas disponibles: {plazas_libres}/{curso['plazas']}
• Estado: {'Disponible' if plazas_libres > 0 else 'Completo'}""")
            
            if info_cursos:
                return f"🤖 Agente: Información de cursos solicitados:{''.join(info_cursos)}"
        
        # Mostrar todos los cursos disponibles
        cursos_info = []
        for codigo, curso in self.base_datos_simulada["cursos"].items():
            plazas_libres = curso["plazas"] - curso["ocupadas"]
            cursos_info.append(f"• {codigo}: {curso['nombre']} ({plazas_libres} plazas libres)")
        
        return f"🤖 Agente: Cursos disponibles:\n" + "\n".join(cursos_info)
    
    def _reservar_sala(self, mensaje: str, id_usuario: str) -> str:
        """Simula reserva de sala"""
        # Generar ID de reserva
        reserva_id = f"RES{random.randint(1000, 9999)}"
        fecha_reserva = datetime.now() + timedelta(days=1)
        
        reserva = {
            "id": reserva_id,
            "usuario": id_usuario,
            "fecha": fecha_reserva.strftime("%Y-%m-%d %H:%M"),
            "sala": "Sala de Estudio 1",
            "duracion": "2 horas"
        }
        
        self.base_datos_simulada["reservas_biblioteca"].append(reserva)
        
        return f"""🤖 Agente: ¡Reserva confirmada!

📅 Detalles de tu reserva:
• ID: {reserva_id}
• Sala: {reserva['sala']}
• Fecha: {reserva['fecha']}
• Duración: {reserva['duracion']}

Recuerda llevar tu tarjeta universitaria. ¿Necesitas algo más?"""
    
    def _calcular_creditos(self, mensaje: str, id_usuario: str) -> str:
        """Calcula créditos basándose en cursos mencionados"""
        codigos_encontrados = re.findall(r'[A-Z]{3}\d{3}', mensaje.upper())
        
        if not codigos_encontrados:
            return "🤖 Agente: Para calcular créditos, menciona los códigos de curso (ej: INF101, MAT101)"
        
        total_creditos = 0
        detalle_cursos = []
        
        for codigo in codigos_encontrados:
            if codigo in self.base_datos_simulada["cursos"]:
                curso = self.base_datos_simulada["cursos"][codigo]
                total_creditos += curso["creditos"]
                detalle_cursos.append(f"• {codigo}: {curso['creditos']} créditos")
        
        if detalle_cursos:
            return f"""🤖 Agente: Cálculo de créditos:

{chr(10).join(detalle_cursos)}

📊 Total: {total_creditos} créditos
📚 Carga académica: {'Normal' if total_creditos <= 20 else 'Alta' if total_creditos <= 25 else 'Muy alta'}"""
        
        return "🤖 Agente: No encontré cursos válidos para calcular créditos."
    
    def _responder_contextual(self, mensaje: str, id_usuario: str) -> str:
        """Responde usando contexto de la conversación"""
        contexto = len(self.memoria_conversacion)
        
        if "hola" in mensaje.lower():
            if contexto > 1:
                return f"🤖 Agente: ¡Hola de nuevo! Veo que hemos hablado antes. ¿En qué más puedo ayudarte?"
            else:
                return f"🤖 Agente: ¡Hola! Soy tu agente universitario. Puedo ayudarte con consultas académicas, reservas y más. ¿Qué necesitas?"
        
        elif "gracias" in mensaje.lower():
            return f"🤖 Agente: ¡De nada! Ha sido un placer ayudarte. Si necesitas algo más, aquí estaré."
        
        elif "adios" in mensaje.lower():
            return f"🤖 Agente: ¡Hasta luego! Que tengas un buen día. Recuerda que puedes consultarme cuando necesites."
        
        return f"🤖 Agente: Entiendo. ¿Hay algo específico en lo que pueda ayudarte hoy?"
    
    def _respuesta_con_herramientas(self, mensaje: str) -> str:
        """Respuesta cuando no se identifica intención clara"""
        return f"""🤖 Agente: No estoy seguro de entender completamente tu consulta. 

🔧 Puedo ayudarte con:
• Consultar tu perfil de estudiante
• Información sobre cursos y plazas
• Reservar salas de estudio
• Calcular créditos académicos
• Consultas generales universitarias

¿Podrías ser más específico sobre lo que necesitas?"""
    
    def obtener_historial(self) -> List[Dict[str, Any]]:
        """Devuelve el historial de conversación"""
        return self.memoria_conversacion
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Devuelve estadísticas del agente"""
        return {
            "total_conversaciones": len(self.memoria_conversacion),
            "herramientas_disponibles": len(self.herramientas_disponibles),
            "estudiantes_en_bd": len(self.base_datos_simulada["estudiantes"]),
            "cursos_disponibles": len(self.base_datos_simulada["cursos"]),
            "reservas_activas": len(self.base_datos_simulada["reservas_biblioteca"])
        }

class AsistenteInteligente:
    """
    Ejemplo de asistente más avanzado que puede razonar y adaptarse
    Muestra las capacidades más sofisticadas de los sistemas modernos
    """
    
    def __init__(self):
        self.contexto_sesion = {}
        self.preferencias_usuario = {}
        self.conocimiento_dinamico = {}
        self.conversacion_activa = []
    
    def procesar_mensaje(self, mensaje: str, id_usuario: str = "usuario") -> str:
        """Procesa mensaje con capacidades de asistente inteligente"""
        # Actualizar contexto
        self._actualizar_contexto(mensaje, id_usuario)
        
        # Razonamiento contextual
        respuesta = self._generar_respuesta_inteligente(mensaje, id_usuario)
        
        # Aprender de la interacción
        self._aprender_de_interaccion(mensaje, respuesta, id_usuario)
        
        return respuesta
    
    def _actualizar_contexto(self, mensaje: str, id_usuario: str):
        """Actualiza el contexto de la conversación"""
        timestamp = datetime.now()
        
        if id_usuario not in self.contexto_sesion:
            self.contexto_sesion[id_usuario] = {
                "inicio_sesion": timestamp,
                "mensajes": [],
                "temas_discutidos": [],
                "estado_emocional": "neutral"
            }
        
        self.contexto_sesion[id_usuario]["mensajes"].append({
            "timestamp": timestamp,
            "mensaje": mensaje,
            "sentimiento": self._analizar_sentimiento(mensaje)
        })
    
    def _analizar_sentimiento(self, mensaje: str) -> str:
        """Análisis básico de sentimiento"""
        palabras_positivas = ["gracias", "excelente", "perfecto", "genial", "bueno"]
        palabras_negativas = ["problema", "error", "mal", "horrible", "difícil"]
        palabras_neutras = ["información", "consulta", "pregunta", "datos"]
        
        mensaje_lower = mensaje.lower()
        
        score_positivo = sum(1 for palabra in palabras_positivas if palabra in mensaje_lower)
        score_negativo = sum(1 for palabra in palabras_negativas if palabra in mensaje_lower)
        
        if score_positivo > score_negativo:
            return "positivo"
        elif score_negativo > score_positivo:
            return "negativo"
        else:
            return "neutral"
    
    def _generar_respuesta_inteligente(self, mensaje: str, id_usuario: str) -> str:
        """Genera respuesta contextual e inteligente"""
        contexto = self.contexto_sesion.get(id_usuario, {})
        historial = contexto.get("mensajes", [])
        
        # Análisis del mensaje actual
        es_pregunta = any(palabra in mensaje.lower() for palabra in ["qué", "cómo", "cuándo", "dónde", "por qué", "cuánto"])
        es_solicitud = any(palabra in mensaje.lower() for palabra in ["puedes", "podrías", "necesito", "quiero", "ayuda"])
        
        # Respuesta adaptativa basada en historial
        if len(historial) == 1:
            return self._respuesta_primera_interaccion(mensaje, id_usuario)
        else:
            return self._respuesta_contextual_avanzada(mensaje, id_usuario, historial)
    
    def _respuesta_primera_interaccion(self, mensaje: str, id_usuario: str) -> str:
        """Respuesta especializada para primera interacción"""
        sentimiento = self._analizar_sentimiento(mensaje)
        
        if "hola" in mensaje.lower() or "buenos" in mensaje.lower():
            return f"""🧠 Asistente: ¡Hola! Soy tu asistente universitario inteligente. 

🎯 Me adapto a tu forma de comunicarte y aprendo de nuestras conversaciones para ayudarte mejor cada vez.

✨ Puedo entender contexto, recordar nuestra conversación anterior, y personalizar mis respuestas según tus necesidades.

¿En qué puedo ayudarte hoy? Puedes preguntarme sobre cualquier tema universitario."""
        
        elif sentimiento == "negativo":
            return f"""🧠 Asistente: Percibo que puedes estar experimentando alguna dificultad. 

🤝 Estoy aquí para ayudarte a resolver cualquier problema universitario que tengas. 

📋 Puedo asistirte con:
• Problemas académicos o administrativos
• Navegación por sistemas universitarios
• Información detallada y personalizada
• Seguimiento de tus consultas

¿Podrías contarme más detalles sobre lo que necesitas?"""
        
        else:
            return f"""🧠 Asistente: Excelente, veo que tienes una consulta universitaria.

🔍 Estoy procesando tu mensaje para entender exactamente qué necesitas...

💡 Basándome en tu consulta, puedo proporcionarte información detallada y personalizada. 

¿Te gustaría que profundice en algún aspecto específico?"""
    
    def _respuesta_contextual_avanzada(self, mensaje: str, id_usuario: str, historial: List[Dict]) -> str:
        """Respuesta que usa todo el contexto de la conversación"""
        # Analizar tendencias en la conversación
        temas_previos = self._extraer_temas_conversacion(historial)
        patron_consultas = self._identificar_patron_consultas(historial)
        
        # Respuesta personalizada
        if "anteriormente" in mensaje.lower() or "antes" in mensaje.lower():
            return self._respuesta_referencia_anterior(temas_previos, id_usuario)
        
        elif patron_consultas == "academico":
            return self._respuesta_especializada_academica(mensaje, temas_previos)
        
        elif patron_consultas == "tecnico":
            return self._respuesta_especializada_tecnica(mensaje, temas_previos)
        
        else:
            return self._respuesta_adaptativa_general(mensaje, temas_previos, id_usuario)
    
    def _extraer_temas_conversacion(self, historial: List[Dict]) -> List[str]:
        """Extrae temas principales de la conversación"""
        temas = []
        for entrada in historial:
            mensaje = entrada["mensaje"].lower()
            if any(palabra in mensaje for palabra in ["curso", "asignatura", "creditos"]):
                temas.append("academico")
            elif any(palabra in mensaje for palabra in ["wifi", "sistema", "password"]):
                temas.append("tecnico")
            elif any(palabra in mensaje for palabra in ["biblioteca", "reserva", "sala"]):
                temas.append("biblioteca")
        return list(set(temas))  # Eliminar duplicados
    
    def _identificar_patron_consultas(self, historial: List[Dict]) -> str:
        """Identifica el patrón principal de consultas del usuario"""
        temas = self._extraer_temas_conversacion(historial)
        
        if temas.count("academico") > len(temas) / 2:
            return "academico"
        elif temas.count("tecnico") > len(temas) / 2:
            return "tecnico"
        else:
            return "general"
    
    def _respuesta_referencia_anterior(self, temas_previos: List[str], id_usuario: str) -> str:
        """Respuesta que hace referencia a temas anteriores"""
        if temas_previos:
            return f"""🧠 Asistente: Recuerdo nuestra conversación anterior sobre {', '.join(temas_previos)}.

🔗 Conectando con lo que hablamos antes, puedo proporcionarte información más detallada o abordar aspectos relacionados.

📈 ¿Quieres que profundice en algún punto específico de lo que discutimos, o tienes una nueva consulta?"""
        else:
            return f"🧠 Asistente: Aunque mencionas algo anterior, esta es nuestra primera conversación. ¡Pero estoy listo para ayudarte con cualquier consulta!"
    
    def _respuesta_especializada_academica(self, mensaje: str, temas_previos: List[str]) -> str:
        """Respuesta especializada para temas académicos"""
        return f"""🧠 Asistente: Veo que tienes un enfoque académico en nuestras conversaciones.

📚 Basándome en tu historial de consultas, puedo proporcionarte:
• Información detallada sobre cursos y prerequisitos
• Planificación académica personalizada
• Seguimiento de tu progreso curricular
• Recomendaciones específicas para tu carrera

🎯 Tu consulta actual sobre: "{mensaje[:50]}..."

¿Te gustaría que analice esto en el contexto de tu perfil académico?"""
    
    def _respuesta_especializada_tecnica(self, mensaje: str, temas_previos: List[str]) -> str:
        """Respuesta especializada para temas técnicos"""
        return f"""🧠 Asistente: Noto que sueles tener consultas técnicas.

💻 Puedo ayudarte con:
• Resolución de problemas de sistemas
• Configuración de accesos y credenciales
• Optimización de tu experiencia digital universitaria
• Soporte técnico personalizado

🔧 Sobre tu consulta: "{mensaje[:50]}..."

¿Necesitas una solución paso a paso o información técnica específica?"""
    
    def _respuesta_adaptativa_general(self, mensaje: str, temas_previos: List[str], id_usuario: str) -> str:
        """Respuesta adaptativa general"""
        num_interacciones = len(self.contexto_sesion.get(id_usuario, {}).get("mensajes", []))
        
        return f"""🧠 Asistente: Entiendo tu consulta en el contexto de nuestras {num_interacciones} interacciones.

🧩 Considerando tu patrón de consultas y preferencias, te sugiero:

{self._generar_sugerencia_personalizada(mensaje, temas_previos)}

¿Esta aproximación te resulta útil, o prefieres que enfoque la respuesta de otra manera?"""
    
    def _generar_sugerencia_personalizada(self, mensaje: str, temas_previos: List[str]) -> str:
        """Genera sugerencia personalizada basada en historial"""
        if "academico" in temas_previos:
            return "• Enfoque académico con detalles de cursos y planificación"
        elif "tecnico" in temas_previos:
            return "• Solución técnica step-by-step con opciones avanzadas"
        else:
            return "• Información completa con múltiples opciones y contexto"
    
    def _aprender_de_interaccion(self, mensaje: str, respuesta: str, id_usuario: str):
        """Aprende y mejora basándose en la interacción"""
        # Actualizar preferencias del usuario
        if id_usuario not in self.preferencias_usuario:
            self.preferencias_usuario[id_usuario] = {
                "temas_interes": [],
                "estilo_comunicacion": "formal",
                "nivel_detalle": "medio"
            }
        
        # Detectar preferencias de estilo
        if any(palabra in mensaje.lower() for palabra in ["por favor", "gracias", "disculpe"]):
            self.preferencias_usuario[id_usuario]["estilo_comunicacion"] = "formal"
        elif any(palabra in mensaje.lower() for palabra in ["ok", "vale", "genial"]):
            self.preferencias_usuario[id_usuario]["estilo_comunicacion"] = "informal"
    
    def obtener_perfil_usuario(self, id_usuario: str) -> Dict[str, Any]:
        """Devuelve el perfil completo del usuario"""
        contexto = self.contexto_sesion.get(id_usuario, {})
        preferencias = self.preferencias_usuario.get(id_usuario, {})
        
        return {
            "total_interacciones": len(contexto.get("mensajes", [])),
            "temas_discutidos": self._extraer_temas_conversacion(contexto.get("mensajes", [])),
            "preferencias": preferencias,
            "primera_interaccion": contexto.get("inicio_sesion"),
            "patron_comportamiento": self._identificar_patron_consultas(contexto.get("mensajes", []))
        }

def demo_interactiva():
    """Demostración interactiva de los tres tipos de sistemas"""
    print("🎓 Demo Interactiva: Chatbot vs Agente vs Asistente Universitario")
    print("=" * 70)
    print("Vamos a probar los tres tipos de sistemas con las mismas consultas")
    print("para ver las diferencias en sus respuestas.\n")
    
    # Inicializar sistemas
    chatbot = ChatbotBasico()
    agente = AgenteUniversitario()
    asistente = AsistenteInteligente()
    
    # Consultas de ejemplo
    consultas_demo = [
        "Hola, necesito información sobre horarios de biblioteca",
        "¿Qué cursos están disponibles?",
        "Quiero reservar una sala de estudio",
        "¿Cuántos créditos suman INF101 y MAT101?",
        "Gracias por la ayuda"
    ]
    
    for i, consulta in enumerate(consultas_demo, 1):
        print(f"\n{'='*20} CONSULTA {i} {'='*20}")
        print(f"Usuario: {consulta}")
        print(f"\n{'-'*60}")
        
        # Respuesta del chatbot
        respuesta_chatbot = chatbot.procesar_mensaje(consulta)
        print(respuesta_chatbot)
        
        print(f"\n{'-'*60}")
        
        # Respuesta del agente
        respuesta_agente = agente.procesar_mensaje(consulta, "12345")
        print(respuesta_agente)
        
        print(f"\n{'-'*60}")
        
        # Respuesta del asistente
        respuesta_asistente = asistente.procesar_mensaje(consulta, "demo_user")
        print(respuesta_asistente)
        
        print(f"\n{'='*70}")
    
    # Mostrar estadísticas finales
    print("\n📊 ESTADÍSTICAS FINALES:")
    print("\n🤖 Chatbot:")
    print("   - Respuestas predefinidas")
    print("   - Sin memoria de conversación")
    print("   - Limitado a patrones específicos")
    
    print("\n🧠 Agente:")
    stats = agente.obtener_estadisticas()
    print(f"   - {stats['total_conversaciones']} interacciones registradas")
    print(f"   - {stats['herramientas_disponibles']} herramientas disponibles")
    print("   - Capacidad de realizar acciones")
    print("   - Memoria de conversación activa")
    
    print("\n✨ Asistente:")
    perfil = asistente.obtener_perfil_usuario("demo_user")
    print(f"   - {perfil['total_interacciones']} interacciones analizadas")
    print(f"   - Temas identificados: {perfil['temas_discutidos']}")
    print(f"   - Patrón de comportamiento: {perfil['patron_comportamiento']}")
    print("   - Aprendizaje y adaptación activos")

def main():
    """Función principal con opciones de ejecución"""
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_interactiva()
    elif len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        print("🎓 Modo Interactivo - Elige un sistema para probar:")
        print("1. Chatbot Básico")
        print("2. Agente Universitario") 
        print("3. Asistente Inteligente")
        
        while True:
            try:
                choice = input("\nElige opción (1-3, 'quit' para salir): ").strip()
                
                if choice.lower() in ['quit', 'exit', 'salir']:
                    break
                
                if choice == "1":
                    sistema = ChatbotBasico()
                    print("\n🤖 Chatbot activado. Escribe tus consultas:")
                elif choice == "2":
                    sistema = AgenteUniversitario()
                    print("\n🧠 Agente activado. Escribe tus consultas:")
                elif choice == "3":
                    sistema = AsistenteInteligente()
                    print("\n✨ Asistente activado. Escribe tus consultas:")
                else:
                    print("Opción no válida")
                    continue
                
                # Bucle de conversación
                while True:
                    user_input = input("\nTú: ").strip()
                    if user_input.lower() in ['salir', 'back', 'volver']:
                        break
                    
                    if hasattr(sistema, 'procesar_mensaje'):
                        if isinstance(sistema, (AgenteUniversitario, AsistenteInteligente)):
                            respuesta = sistema.procesar_mensaje(user_input, "usuario_demo")
                        else:
                            respuesta = sistema.procesar_mensaje(user_input)
                        print(respuesta)
                    
            except KeyboardInterrupt:
                break
    
    else:
        print("🎓 Conceptos Fundamentales - Ejemplos Interactivos")
        print("=" * 55)
        print("Este script demuestra las diferencias entre:")
        print("🤖 Chatbot: Respuestas predefinidas, sin memoria")
        print("🧠 Agente: Acciones, memoria, herramientas")
        print("✨ Asistente: Razonamiento, adaptación, aprendizaje")
        print("\nOpciones de ejecución:")
        print("  --demo        : Demostración automática comparativa")
        print("  --interactive : Modo interactivo para probar cada sistema")

if __name__ == "__main__":
    import sys
    main()
