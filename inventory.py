from object import Object
from typing import List, Optional


class Inventory:
    
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.items: List = []

    def get_items(self):
        return self.items.copy()

    def get_capacity(self):
        return self.capacity

    def is_full(self):
        return len(self.items) >= self.capacity
    
    def is_empty(self):
        return len(self.items) == 0

    def has_item(self, item_name: str):
        return any(item.get_name().lower() == item_name.lower() for item in self.items)
    
    def get_item_count(self):
        return len(self.items)
    
    def get_free_space(self):
        return self.capacity - len(self.items)

    def set_capacity(self, new_capacity: int):
        if new_capacity < len(self.items):
            raise ValueError("La nueva capacidad es menor que los objetos actuales")
        self.capacity = new_capacity

    def add_item(self, obj: Object):
        if self.is_full():
            return False
        
        if obj not in self.items:
            self.items.append(obj)
            return True
        return False

    def remove_item(self, item_name: str):
        for i, item in enumerate(self.items):
            if item.get_name().lower() == item_name.lower():
                return self.items.pop(i)
        return None
    
    def remove_object(self, obj: Object):
        if obj in self.items:
            self.items.remove(obj)
            return True
        return False
    
    def get_item_by_name(self, item_name: str):
        for item in self.items:
            if item.get_name().lower() == item_name.lower():
                return item
        return None

    def clear(self):
        self.items.clear()

    def show_inventory(self):
        if self.is_empty():
            return "Tu inventario está vacío."
        
        result = f"Inventario ({len(self.items)}/{self.capacity}):\n"
        for i, item in enumerate(self.items, 1):
            usable_text = " (usable)" if item.is_usable() else ""
            result += f"{i}. {item.get_name()}: {item.get_description()}{usable_text}\n"
        
        return result

    def list_item_names(self):
        return [item.get_name() for item in self.items]

    def __str__(self):
        return f"Inventory({len(self.items)}/{self.capacity} items)"
    
    def __len__(self):

        return len(self.items)
