from room import Room
from object import Object
from typing import Dict, List, Optional


class GameMap:
    """Representa el mapa del juego como un grafo de habitaciones conectadas"""
    
    def __init__(self):
        self.rooms = {}
        self.connections = {}
        self.initialize_map()
    
    def initialize_map(self):
        """Inicializa todas las habitaciones y sus conexiones"""
        # Crear habitaciones
        room_data = {
            "oficina": "Tu oficina personal. Huele a café y papeles.",
            "pasillo 1": "Un pasillo largo con luces parpadeantes.",
            "pasillo 2": "Un pasillo estrecho con tuberías visibles.",
            "pasillo 3": "Un pasillo que lleva a las áreas críticas.",
            "sala de seguridad": "Centro de seguridad con monitores rotos.",
            "banos 1": "Área de baños principal.",
            "banos Hombre": "Baño de hombres. Algo huele mal aquí.",
            "banos Mujeres": "Baño de mujeres. Relativamente limpio.",
            "escaleras": "Escaleras que llevan a otros pisos.",
            "sala de operaciones": "Centro de operaciones principal.",
            "zona de descanso": "Área de descanso para empleados.",
            "salida 1": "Una de las salidas de emergencia.",
            "salida 2": "Una de las salidas de emergencia.",
            "sala de mantenimiento": "Cuarto lleno de herramientas y equipos.",
            "sala de control": "Centro de control principal del edificio.",
            "Generador eléctrico": "El generador principal. Hace mucho ruido.",
            "Sala de control de respaldo": "Sistema de respaldo del edificio.",
            "enfermeria": "Enfermería con suministros médicos.",
            "Laboratorios": "Laboratorios de investigación.",
            "reactor": "El reactor principal. ¡PELIGROSO!"
        }
        
        room_objects = {
            "oficina": [Object("botiquin", "Un botiquín de primeros auxilios", True), 
                       Object("piedra", "Una piedra pequeña pero pesada", False)],
            "pasillo 3": [Object("Lata vacia", "Una lata de comida vacía", False)],
            "sala de seguridad": [Object("Pistola", "Una pistola de seguridad", True)],
            "banos Hombre": [Object("Llave 1", "Una llave dorada", True)],
            "banos Mujeres": [Object("Tampones", "Productos de higiene femenina", False)],
            "sala de operaciones": [Object("Manual basico de control de operaciones", "Manual técnico", True)],
            "zona de descanso": [Object("Cobija", "Una cobija suave y cálida", True)],
            "sala de mantenimiento": [Object("Llave 2", "Una llave plateada", True)],
            "Generador eléctrico": [Object("Llave 3", "Una llave de bronce", True)],
            "Sala de control de respaldo": [Object("botiquin", "Botiquín de emergencia", True)],
            "enfermeria": [Object("Agua", "Una botella de agua", True)],
        }
        
        for room_name, description in room_data.items():
            room = Room(room_name, description)
            if room_name in room_objects:
                for obj in room_objects[room_name]:
                    room.add_object(obj)
            self.rooms[room_name] = room
        

        self.connections = {
            "oficina": ["pasillo 1", "pasillo 2", "pasillo 3"],
            "pasillo 1": ["oficina", "sala de seguridad", "escaleras", "sala de operaciones"],
            "pasillo 2": ["oficina", "pasillo 3", "sala de mantenimiento", "sala de control"],
            "pasillo 3": ["oficina", "pasillo 2", "enfermeria", "reactor"],
            "sala de seguridad": ["pasillo 1", "banos 1"],
            "banos 1": ["sala de operaciones", "sala de seguridad", "banos Hombre", "banos Mujeres"],
            "banos Hombre": ["banos 1"],
            "banos Mujeres": ["banos 1"],
            "escaleras": ["pasillo 1"],
            "sala de operaciones": ["pasillo 1", "banos 1", "zona de descanso", "salida 1"],
            "zona de descanso": ["sala de operaciones"],
            "salida 1": ["sala de operaciones"],
            "sala de mantenimiento": ["pasillo 2"],
            "sala de control": ["pasillo 2", "Generador eléctrico", "Sala de control de respaldo"],
            "Generador eléctrico": ["sala de control"],
            "Sala de control de respaldo": ["sala de control", "salida 2"],
            "salida 2": ["Sala de control de respaldo"],
            "enfermeria": ["pasillo 3", "Laboratorios", "reactor"],
            "Laboratorios": ["enfermeria"],
            "reactor": ["pasillo 3", "enfermeria"]
        }
        
        self.rooms["sala de seguridad"].set_locked(True, "Llave 1")
        self.rooms["sala de control"].set_locked(True, "Llave 2")
        self.rooms["reactor"].set_locked(True, "Llave 3")
        
    # === GETTERS ===
    def get_room(self, room_name: str) -> Optional[Room]:
        """Obtiene una habitación por nombre"""
        return self.rooms.get(room_name)
    
    def get_connected_rooms(self, room_name: str) -> List[str]:
        """Obtiene las habitaciones conectadas a una habitación"""
        return self.connections.get(room_name, [])
    
    def get_all_room_names(self) -> List[str]:
        """Obtiene todos los nombres de habitaciones"""
        return list(self.rooms.keys())
    
    # === NAVIGATION ===
    def can_move_to(self, from_room: str, to_room: str, player_inventory) -> tuple[bool, str]:
        """Verifica si se puede mover de una habitación a otra"""
        if to_room not in self.get_connected_rooms(from_room):
            return False, f"No puedes ir a {to_room} desde {from_room}."
        
        target_room = self.get_room(to_room)
        if target_room:
            return target_room.can_enter(player_inventory)
        
        return False, "Habitación no encontrada."
    
    def get_room_description(self, room_name: str, explored: bool = False) -> str:
        """Obtiene la descripción de una habitación"""
        room = self.get_room(room_name)
        if not room:
            return "Habitación desconocida."
        
        if explored:
            return room.explore()
        else:
            return room.get_description()
        
    def remove_room(self, from_room: str, to_room: str):
        if from_room in self.connections and to_room in self.connections[from_room]:
            self.connections[from_room].remove(to_room)
        if to_room in self.connections and from_room in self.connections[to_room]:
            self.connections[to_room].remove(from_room)
    
    def __str__(self):
        return f"GameMap with {len(self.rooms)} rooms"