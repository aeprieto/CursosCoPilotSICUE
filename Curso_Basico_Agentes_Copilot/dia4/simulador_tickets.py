
import uuid
import datetime

class Ticket:
    """
    Representa un ticket de soporte técnico.
    """
    def __init__(self, usuario, problema):
        self.id = uuid.uuid4()
        self.usuario = usuario
        self.problema = problema
        self.estado = "Abierto"
        self.creado_en = datetime.datetime.now()
        self.actualizado_en = datetime.datetime.now()
        self.historial = [f"{self.creado_en}: Ticket creado por {self.usuario}."]

    def __str__(self):
        return f"Ticket[{self.id}] - {self.problema} ({self.estado}) by {self.usuario}"

    def actualizar_estado(self, nuevo_estado, autor="Sistema"):
        """Actualiza el estado del ticket y registra el cambio en el historial."""
        self.estado = nuevo_estado
        self.actualizado_en = datetime.datetime.now()
        log = f"{self.actualizado_en}: Estado cambiado a '{nuevo_estado}' por {autor}."
        self.historial.append(log)
        print(f"INFO: {log}")

    def agregar_comentario(self, comentario, autor):
        """Agrega un comentario al historial del ticket."""
        self.actualizado_en = datetime.datetime.now()
        log = f"{self.actualizado_en}: Comentario de {autor}: {comentario}"
        self.historial.append(log)
        print(f"INFO: {log}")

class SistemaTickets:
    """
    Gestiona una colección de tickets de soporte.
    """
    def __init__(self):
        self.tickets = {}

    def crear_ticket(self, usuario, problema):
        """Crea un nuevo ticket y lo añade al sistema."""
        ticket = Ticket(usuario, problema)
        self.tickets[ticket.id] = ticket
        print(f"ÉXITO: Se ha creado el ticket con ID: {ticket.id}")
        return ticket

    def buscar_ticket(self, ticket_id):
        """Busca un ticket por su ID."""
        try:
            uid = uuid.UUID(ticket_id)
            return self.tickets.get(uid)
        except ValueError:
            print("ERROR: El ID del ticket no es válido.")
            return None

    def mostrar_tickets(self, estado=None):
        """Muestra todos los tickets o los filtra por estado."""
        print("\n--- LISTA DE TICKETS ---")
        if not self.tickets:
            print("No hay tickets en el sistema.")
            return

        filtrados = [t for t in self.tickets.values() if not estado or t.estado == estado]

        if not filtrados:
            print(f"No se encontraron tickets con el estado '{estado}'.")
            return

        for ticket in filtrados:
            print(f"- ID: {ticket.id} | Usuario: {ticket.usuario} | Problema: {ticket.problema} | Estado: {ticket.estado}")
        print("------------------------\n")

def main():
    """
    Función principal para ejecutar la interfaz de línea de comandos del sistema de tickets.
    """
    sistema = SistemaTickets()
    print("Bienvenido al Simulador de Sistema de Tickets para el Servicio de Informática.")
    print("Este script es un ejemplo práctico para el Día 4 del curso de agentes.")

    # Precargar algunos datos para la demo
    sistema.crear_ticket("profesor.x", "No puedo acceder al proyector del aula 101.")
    sistema.crear_ticket("alumno.y", "La red WiFi es muy lenta en la biblioteca.")

    while True:
        print("\n¿Qué te gustaría hacer?")
        print("1. Crear un nuevo ticket")
        print("2. Ver todos los tickets")
        print("3. Buscar y actualizar un ticket")
        print("4. Salir")
        opcion = input("Elige una opción (1-4): ")

        if opcion == '1':
            usuario = input("Tu nombre de usuario: ")
            problema = input("Describe tu problema: ")
            sistema.crear_ticket(usuario, problema)

        elif opcion == '2':
            sistema.mostrar_tickets()

        elif opcion == '3':
            ticket_id = input("Introduce el ID del ticket a buscar: ")
            ticket = sistema.buscar_ticket(ticket_id)
            if ticket:
                print("\n--- DETALLES DEL TICKET ---")
                print(ticket)
                for entrada in ticket.historial:
                    print(f"  - {entrada}")
                print("---------------------------\n")

                print("¿Qué quieres hacer con este ticket?")
                print("  a. Cambiar estado")
                print("  b. Agregar comentario")
                print("  c. Volver al menú principal")
                accion = input("Elige una opción (a-c): ").lower()

                if accion == 'a':
                    nuevo_estado = input("Introduce el nuevo estado (e.g., En Proceso, Resuelto, Cerrado): ")
                    ticket.actualizar_estado(nuevo_estado, "Agente de Soporte")
                elif accion == 'b':
                    comentario = input("Escribe tu comentario: ")
                    autor = input("Tu nombre (como autor del comentario): ")
                    ticket.agregar_comentario(comentario, autor)

        elif opcion == '4':
            print("Gracias por usar el simulador. ¡Hasta pronto!")
            break

        else:
            print("Opción no válida. Por favor, elige de nuevo.")

if __name__ == "__main__":
    main()
