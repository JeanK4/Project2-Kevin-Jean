class Object:
    """Representa un objeto del juego que puede ser recogido y usado"""
    
    def __init__(self, name: str, description: str = "", usable: bool = False, value: int = 0):
        self.name = name
        self.description = description or name
        self.usable = usable
        self.value = value  # Valor del objeto (para posible sistema de comercio)

    # === GETTERS ===
    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
    
    def get_value(self) -> int:
        return self.value

    def is_usable(self) -> bool:
        return self.usable

    # === SETTERS ===
    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_usable(self, usable: bool):
        self.usable = usable
    
    def set_value(self, value: int):
        self.value = max(0, value)

    # === UTILITY ===
    def get_object_type(self) -> str:
        """Determina el tipo de objeto basado en su nombre"""
        name_lower = self.name.lower()
        
        if any(healing in name_lower for healing in ["botiquin", "agua", "pocion"]):
            return "healing"
        elif any(weapon in name_lower for weapon in ["pistola", "cuchillo", "espada"]):
            return "weapon"
        elif any(key in name_lower for key in ["llave", "key"]):
            return "key"
        elif any(armor in name_lower for armor in ["cobija", "escudo", "armadura"]):
            return "armor"
        elif any(tool in name_lower for tool in ["manual", "libro"]):
            return "tool"
        else:
            return "misc"

    def can_stack_with(self, other: "Object") -> bool:
        """Verifica si este objeto puede apilarse con otro (mismo nombre y tipo)"""
        return (self.name == other.name and 
                self.get_object_type() == other.get_object_type())

    # === DISPLAY ===
    def get_full_description(self) -> str:
        """Obtiene una descripción completa del objeto"""
        desc = f"{self.name}: {self.description}"
        if self.usable:
            desc += " (Usable)"
        if self.value > 0:
            desc += f" (Valor: {self.value})"
        return desc

    def __str__(self):
        return f"Object({self.name}, usable={self.usable})"
    
    def __repr__(self):
        return f"Object(name='{self.name}', description='{self.description}', usable={self.usable}, value={self.value})"
    
    def __eq__(self, other):
        if isinstance(other, Object):
            return (self.name == other.name and 
                   self.description == other.description and 
                   self.usable == other.usable)
        return False
    
    def __hash__(self):
        return hash((self.name, self.description, self.usable))