from character import Character
from object import Object
from typing import Optional


class Player(Character):
    """Clase específica para el jugador"""
    
    def __init__(self, name: str = "Jugador"):
        super().__init__(name, health=100, attack=10, defense=2)
        self.current_room = "oficina"  # Ubicación inicial
        self.experience_points = 0
        self.level = 1
        self.bleeding = True  # El jugador empieza herido
        self.bleeding_damage = 2  # Daño por turno por sangrado
    
    # === GETTERS ===
    def get_current_room(self) -> str:
        return self.current_room
    
    def get_experience(self) -> int:
        return self.experience_points
    
    def get_level(self) -> int:
        return self.level
    
    def is_bleeding(self) -> bool:
        return self.bleeding
    
    # === SETTERS ===
    def set_current_room(self, room_name: str):
        self.current_room = room_name
    
    def set_bleeding(self, bleeding: bool):
        self.bleeding = bleeding
    
    # === MOVEMENT ===
    def move_to_room(self, room_name: str) -> bool:
        """Mueve al jugador a una nueva habitación"""
        self.current_room = room_name
        return True
    
    # === BLEEDING SYSTEM ===
    def apply_bleeding_damage(self) -> int:
        """Aplica daño por sangrado cada turno"""
        if self.bleeding and self.is_alive_check():
            damage_taken = self.take_damage(self.bleeding_damage)
            return damage_taken
        return 0
    
    def stop_bleeding(self):
        """Detiene el sangrado (usando botiquín u objeto médico)"""
        self.bleeding = False
    
    # === EXPERIENCE SYSTEM ===
    def gain_experience(self, amount: int):
        """Gana puntos de experiencia"""
        self.experience_points += amount
        self._check_level_up()
    
    def _check_level_up(self):
        """Verifica si debe subir de nivel"""
        required_exp = self.level * 100  # 100 exp por nivel
        if self.experience_points >= required_exp:
            self.level_up()
    
    def buff_defense(self, amount: int):
        self.defense += amount

    def buff_attack(self, amount: int):
        self.attack += amount

    def level_up(self):
        """Sube de nivel y mejora estadísticas"""
        self.level += 1
        # Mejoras por nivel
        self.max_health += 20
        self.health += 20  # También cura al subir de nivel
        self.attack += 3
        self.defense += 1
    
    # === SPECIAL ACTIONS ===
    def rest(self) -> tuple[bool, str]:
        """Descansa para recuperar algo de salud"""
        if self.health >= self.max_health:
            return False, "Ya estás completamente curado."
        
        heal_amount = min(10, self.max_health - self.health)
        self.heal(heal_amount)
        return True, f"Descansas y recuperas {heal_amount} puntos de salud."
    
    def examine_inventory(self) -> str:
        """Examina el inventario del jugador"""
        return self.inventory.show_inventory()
    
    def use_healing_item(self) -> tuple[bool, str]:
        """Busca y usa automáticamente un objeto de curación"""
        healing_items = ["botiquin", "agua", "pocion"]
        
        for item_name in healing_items:
            if self.has_object(item_name):
                success = self.use_object(item_name)
                if success:
                    # Si es botiquín, también detiene el sangrado
                    if "botiquin" in item_name.lower():
                        self.stop_bleeding()
                    return True, f"Usaste {item_name} y te sientes mejor."
        
        return False, "No tienes objetos de curación."
    
    # === COMBAT OVERRIDES ===
    def attack_target(self, target) -> tuple[bool, int]:
        """Ataque del jugador con posibilidad de experiencia"""
        success, damage = super().attack_target(target)
        
        if success and not target.is_alive_check():
            # Gana experiencia por derrotar enemigos
            exp_gained = target.get_level() * 25 if hasattr(target, 'get_level') else 25
            self.gain_experience(exp_gained)
        
        return success, damage
    
    # === STATUS AND DISPLAY ===
    def get_detailed_status(self) -> str:
        """Obtiene un estado detallado del jugador"""
        status = f"=== {self.name} ===\n"
        status += f"Salud: {self.health}/{self.max_health}\n"
        status += f"Ataque: {self.attack}\n"
        status += f"Defensa: {self.defense}\n"
        status += f"Ubicación: {self.current_room}\n"
        
        if self.bleeding:
            status += f"¡SANGRANDO! Busca la manera de curarte\n"
        
        status += f"Estado: {'Vivo' if self.is_alive_check() else 'Muerto'}\n"
        
        return status
    
    def get_quick_status(self) -> str:
        """Estado rápido para mostrar durante el juego"""
        bleeding_indicator = " [SANGRANDO]" if self.bleeding else ""
        return f"{self.name} | HP: {self.health}/{self.max_health}{bleeding_indicator} | Ubicación: {self.current_room}"
    
    def __str__(self):
        return f"Player({self.name}, Level {self.level}, HP: {self.health}/{self.max_health}, Room: {self.current_room})"
