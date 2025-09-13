from character import Character
from object import Object
from typing import Optional


class Enemy(Character):
    
    def __init__(self, name: str, health: int = 50, attack: int = 8, defense: int = 2, 
                 reward: Optional[Object] = None, aggressive: bool = True):
        super().__init__(name, health, attack, defense)
        self.reward = reward
        self.aggressive = aggressive 
        self.has_acted_this_turn = False

    def get_reward(self):
        return self.reward
    
    def is_aggressive(self):
        return self.aggressive
    
    def has_acted(self) -> bool:
        return self.has_acted_this_turn

    def set_reward(self, reward: Optional[Object]):
        self.reward = reward
    
    def set_aggressive(self, aggressive: bool):
        self.aggressive = aggressive

    def act_turn(self, target: Character):
        self.has_acted_this_turn = True
        
        if not self.is_alive_check():
            return f"{self.name} está muerto y no puede actuar."
        
        if not target.is_alive_check():
            return f"{self.name} no tiene objetivo válido."
        
        if self.aggressive:
            success, damage = self.attack_target(target)
            if success:
                return f"{self.name} ataca a {target.get_name()} y causa {damage} de daño!"
            else:
                return f"{self.name} falla su ataque contra {target.get_name()}."
        else:
            return f"{self.name} observa cautelosamente..."

    def drop_reward(self):
        if not self.is_alive_check() and self.reward:
            dropped_reward = self.reward
            self.reward = None 
            return dropped_reward
        return None

    def reset_turn(self):
        self.has_acted_this_turn = False

    def special_attack(self, target: Character):
        if not self.is_alive_check():
            return False, f"{self.name} no puede usar ataques especiales."
        
        special_damage = int(self.attack * 1.5)
        actual_damage = target.take_damage(special_damage)
        
        if actual_damage > 0:
            return True, f"{self.name} usa un ataque especial contra {target.get_name()} causando {actual_damage} de daño!"
        else:
            return False, f"El ataque especial de {self.name} falló."

    def intimidate(self, target: Character):
        if self.is_alive_check():
            return f"{self.name} gruñe amenazadoramente hacia {target.get_name()}!"
        return f"{self.name} no puede intimidar desde la muerte."

    def should_flee(self) -> bool:
        health_percentage = (self.health / self.max_health) * 100
        return health_percentage < 20  

    def get_behavior_description(self):
        if not self.is_alive_check():
            return f"{self.name} yace inmóvil."
        
        health_percentage = (self.health / self.max_health) * 100
        
        if health_percentage > 75:
            return f"{self.name} se ve fuerte y amenazante."
        elif health_percentage > 50:
            return f"{self.name} muestra algunas heridas pero sigue siendo peligroso."
        elif health_percentage > 25:
            return f"{self.name} está gravemente herido pero sigue luchando."
        else:
            return f"{self.name} está al borde de la muerte, desesperado."

    def get_combat_status(self):
        status = f"{self.name} - {self.get_behavior_description()}\n"
        status += f"Salud: {self.health}/{self.max_health}\n"
        status += f"Ataque: {self.attack} | Defensa: {self.defense}\n"
        if self.reward:
            status += f"Posible recompensa: {self.reward.get_name()}"
        return status

    def __str__(self):
        alive_status = "Vivo" if self.is_alive_check() else "Muerto"

        return f"Enemy({self.name}, {alive_status}, HP: {self.health}/{self.max_health})"
