from object import Object
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from enemy import Enemy


class Room:
    """Representa un cuarto del juego con objetos y posibles enemigos"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description or f"Estás en {name}"
        self.objects = []  # Lista de objetos Object
        self.enemies = []  # Lista de enemigos
        self.explored = False  # Si ya fue explorado
        self.locked = False  # Si está bloqueado
        self.key_required = None  # Llave necesaria para entrar
        self.visited = False  # Si el jugador ha entrado alguna vez
    
    # === GETTERS ===
    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return self.description
    
    def get_objects(self) -> List[Object]:
        return self.objects.copy()
    
    def get_enemies(self) -> List['Enemy']:
        return self.enemies.copy()
    
    def is_visited(self) -> bool:
        return self.visited

    def is_explored(self) -> bool:
        return self.explored
    
    def is_locked(self) -> bool:
        return self.locked
    
    # === SETTERS ===
    def set_description(self, description: str):
        self.description = description
    
    def set_locked(self, locked: bool, key_name: str = None):
        self.locked = locked
        self.key_required = key_name
    
    # === OBJECT MANAGEMENT ===
    def add_object(self, obj: Object):
        """Agrega un objeto al cuarto"""
        if obj not in self.objects:
            self.objects.append(obj)
    
    def remove_object(self, object_name: str) -> Optional[Object]:
        """Remueve un objeto por nombre y lo devuelve"""
        for i, obj in enumerate(self.objects):
            if obj.get_name().lower() == object_name.lower():
                return self.objects.pop(i)
        return None
    
    def has_object(self, object_name: str) -> bool:
        """Verifica si el cuarto tiene un objeto específico"""
        return any(obj.get_name().lower() == object_name.lower() for obj in self.objects)
    
    # === ENEMY MANAGEMENT ===
    def add_enemy(self, enemy: 'Enemy'):
        """Agrega un enemigo al cuarto"""
        if enemy not in self.enemies:
            self.enemies.append(enemy)
    
    def remove_enemy(self, enemy: 'Enemy'):
        """Remueve un enemigo del cuarto"""
        if enemy in self.enemies:
            self.enemies.remove(enemy)
    
    def has_living_enemies(self) -> bool:
        """Verifica si hay enemigos vivos en el cuarto"""
        return any(enemy.is_alive_check() for enemy in self.enemies)
    
    # === EXPLORATION ===
    def explore(self) -> str:
        """Explora el cuarto y devuelve la descripción detallada"""
        self.explored = True
        result = f"{self.description}\n"
        
        if self.objects:
            result += "Objetos visibles:\n"
            for obj in self.objects:
                result += f"- {obj.get_name()}: {obj.get_description()}\n"
        else:
            result += "No hay objetos visibles.\n"
        
        if self.enemies:
            living_enemies = [e for e in self.enemies if e.is_alive_check()]
            if living_enemies:
                result += "¡Enemigos presentes!\n"
                for enemy in living_enemies:
                    result += f"- {enemy.get_name()} (Vida: {enemy.get_health()})\n"
        
        return result

    def set_visited(self):
        self.visited = True
    
    def can_enter(self, player_inventory) -> tuple[bool, str]:
        """Verifica si el jugador puede entrar al cuarto"""
        if not self.locked:
            return True, ""
        
        if self.key_required and player_inventory.has_item(self.key_required):
            return True, f"Usaste {self.key_required} para abrir la puerta."
        
        return False, f"La puerta está cerrada. Necesitas {self.key_required}."
    
    def __str__(self):
        return f"Room({self.name}, explored={self.explored}, objects={len(self.objects)}, enemies={len(self.enemies)})"
        return False