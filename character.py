from inventory import Inventory
from object import Object


class Character:
    
    def __init__(self, name: str, health: int = 100, attack: int = 10, defense: int = 0):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.inventory = Inventory(capacity=10)
        self.is_alive = True

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health
    
    def get_max_health(self):
        return self.max_health

    def get_inventory(self):
        return self.inventory
    
    def get_attack(self):
        return self.attack
    
    def get_defense(self):
        return self.defense

    def set_name(self, new_name: str):
        self.name = new_name

    def set_health(self, new_health: int):
        self.health = max(0, min(new_health, self.max_health))
        self.is_alive = self.health > 0

    def set_attack(self, new_attack: int):
        self.attack = max(0, new_attack)
    
    def set_defense(self, new_defense: int):
        self.defense = max(0, new_defense)

    def heal(self, amount: int):
        if not self.is_alive:
            return False
        
        old_health = self.health
        self.set_health(self.health + amount)
        actual_heal = self.health - old_health
        
        if actual_heal > 0:
            return True
        return False

    def take_damage(self, damage: int):
        if not self.is_alive:
            return 0
        
        actual_damage = max(1, damage - self.defense)
        old_health = self.health
        self.set_health(self.health - actual_damage)
        
        return old_health - self.health

    def is_alive_check(self):
        return self.is_alive and self.health > 0

    def attack_target(self, target: "Character"):
        if not self.is_alive_check():
            return False, 0
        
        if not target.is_alive_check():
            return False, 0
        
        damage_dealt = target.take_damage(self.attack)
        return True, damage_dealt

    def pick_up_object(self, obj: Object):
        if self.inventory.add_item(obj):
            return True
        return False

    def use_object(self, object_name: str):
        obj = self.inventory.remove_item(object_name)
        if obj and obj.is_usable():
            return self._apply_object_effect(obj)
        return False

    def _apply_object_effect(self, obj: Object):
        object_name = obj.get_name().lower()

        if "botiquin" in object_name or "agua" in object_name:
            return self.heal(20)
        elif "pistola" in object_name:
            self.set_attack(self.attack + 5)
            return True
        elif "cobija" in object_name:
            self.set_defense(self.defense + 2)
            return True
        
        return False

    def has_object(self, object_name: str):
        return self.inventory.has_item(object_name)

    def get_status(self):
        status = f"{self.name}\n"
        status += f"Salud: {self.health}/{self.max_health}\n"
        status += f"Ataque: {self.attack}\n"
        status += f"Defensa: {self.defense}\n"
        status += f"Estado: {'Vivo' if self.is_alive_check() else 'Muerto'}"
        return status

    def __str__(self):
        return f"Character({self.name}, HP: {self.health}/{self.max_health})"
