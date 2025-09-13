from character import Character
from object import Object
from typing import Optional


class Player(Character):
    
    def __init__(self, name: str = "Jugador"):
        super().__init__(name, health=100, attack=10, defense=2)
        self.current_room = "oficina"
        self.experience_points = 0
        self.level = 1
        self.bleeding = True
        self.bleeding_damage = 2
    
    def get_current_room(self):
        return self.current_room
    
    def get_experience(self):
        return self.experience_points
    
    def get_level(self) -> int:
        return self.level
    
    def is_bleeding(self) -> bool:
        return self.bleeding

    def set_current_room(self, room_name: str):
        self.current_room = room_name
    
    def set_bleeding(self, bleeding: bool):
        self.bleeding = bleeding
    
    def move_to_room(self, room_name: str):
        self.current_room = room_name
        return True
    
    def apply_bleeding_damage(self):
        if self.bleeding and self.is_alive_check():
            damage_taken = self.take_damage(self.bleeding_damage)
            return damage_taken
        return 0
    
    def stop_bleeding(self):
        self.bleeding = False

    def gain_experience(self, amount: int):
        self.experience_points += amount
        self._check_level_up()
    
    def _check_level_up(self):
        required_exp = self.level * 100
        if self.experience_points >= required_exp:
            self.level_up()
    
    def buff_defense(self, amount: int):
        self.defense += amount

    def buff_attack(self, amount: int):
        self.attack += amount

    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health += 20
        self.attack += 3
        self.defense += 1

    def rest(self):
        if self.health >= self.max_health:
            return False, "Ya estás completamente curado."
        
        heal_amount = min(10, self.max_health - self.health)
        self.heal(heal_amount)
        return True, f"Descansas y recuperas {heal_amount} puntos de salud."
    
    def examine_inventory(self):
        return self.inventory.show_inventory()
    
    def use_healing_item(self):
        healing_items = ["botiquin", "agua", "pocion"]
        
        for item_name in healing_items:
            if self.has_object(item_name):
                success = self.use_object(item_name)
                if success:
                    if "botiquin" in item_name.lower():
                        self.stop_bleeding()
                    return True, f"Usaste {item_name} y te sientes mejor."
        
        return False, "No tienes objetos de curación."

    def attack_target(self, target):
        success, damage = super().attack_target(target)
        
        if success and not target.is_alive_check():
            exp_gained = target.get_level() * 25 if hasattr(target, 'get_level') else 25
            self.gain_experience(exp_gained)
        
        return success, damage

    def get_detailed_status(self):
        status = f"=== {self.name} ===\n"
        status += f"Salud: {self.health}/{self.max_health}\n"
        status += f"Ataque: {self.attack}\n"
        status += f"Defensa: {self.defense}\n"
        status += f"Ubicación: {self.current_room}\n"
        
        if self.bleeding:
            status += f"¡SANGRANDO! Busca la manera de curarte\n"
        
        status += f"Estado: {'Vivo' if self.is_alive_check() else 'Muerto'}\n"
        
        return status
    
    def get_quick_status(self):
        bleeding_indicator = " [SANGRANDO]" if self.bleeding else ""
        return f"{self.name} | HP: {self.health}/{self.max_health}{bleeding_indicator} | Ubicación: {self.current_room}"
    
    def __str__(self):
        return f"Player({self.name}, Level {self.level}, HP: {self.health}/{self.max_health}, Room: {self.current_room})"

