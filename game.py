import os
import time
from player import Player
from map import GameMap
from enemy import Enemy
from object import Object

global_stairs = True

class Game:
    
    def __init__(self, audio_manager):
        self.audio_manager = audio_manager
        self.is_running = False
        self.player = None
        self.game_map = None
        self.turn_counter = 0
        self.game_won = False
    
    def start_game(self):
        self.is_running = True
        self.turn_counter = 0
        self.game_won = False
        self.player = Player("Superviviente")
        self.game_map = GameMap()
        self._play_intro_sequence()
        self._add_enemies_to_map()
        self.game_loop()
    
    def _add_enemies_to_map(self):
        enemy1 = Enemy("Guardia Infectado", 30, 8, 2, Object("Pistola", "Pistola del guardia", True))
        enemy2 = Enemy("Criatura Mutante", 50, 12, 3, Object("Llave especial", "Llave extraña", True))
        self.game_map.get_room("sala de seguridad").add_enemy(enemy1)
        self.game_map.get_room("reactor").add_enemy(enemy2)
    
    def _play_intro_sequence(self):
        os.system("cls")
        print("Hoy iba a ser como cualquier día en el trabajo, pero Rusia ha atacado nuevamente el país.")
        time.sleep(2)
        print("\n")
        self.audio_manager.play_audio_for_duration("alarma.wav", 6,  loop=False, volume= 0.1)
        print("La primera bomba cayó muy cerca de tu lugar de trabajo: el reactor nuclear.")
        time.sleep(2)
        print("\n")
        print("Entre los escombros, apenas logras mantenerte en pie y sabes que tu vida acaba de cambiar para siempre.")
        self.audio_manager.play_audio_for_duration("explosion.wav", 6, loop=False, volume= 0.1)
        self.audio_manager.wait_for_audio_finish()
        self.audio_manager.wait_for_audio_finish()
        input("\nPresiona Enter para continuar...")
        os.system("cls")
        print("Debes actuar rápido para sobrevivir.")
        print("Te encuentras herido y has empezado a desangrarte por una herida grave. Para escapar, deberás encontrar las llaves que abren las puertas bloqueadas del complejo.\nSin embargo, la radiación ha infectado a tus compañeros y animales del lugar. Ten cuidado, entre los escombros no solo hay silencio… también hay amenazas ocultas.")
        print("\nTu objetivo: Encuentra una forma de detener el sangrado y escapar del edificio.")
        input("\nPresiona Enter para continuar...")
    
    def game_loop(self):
        while self.is_running and self.player.is_alive_check():
            self.turn_counter += 1
            self._show_current_status()
            action = self._get_player_action()
            self._process_action(action)
            if action != '6':
                self._process_turn_effects()
            if self._check_game_end():
                break
        self._show_game_end()
    
    def _show_current_status(self):
        os.system("cls")
        print(self.player.get_quick_status())
        print()
        current_room = self.game_map.get_room(self.player.get_current_room())
        if current_room:
            if "oficina" in current_room.get_name().lower():
                if not current_room.is_visited():
                    print("La radiación ha infectado a tus compañeros y animales del lugar.\nTen cuidado: entre los escombros no solo hay silencio… también hay amenazas ocultas.\n")
            elif "pasillo 1" in current_room.get_name().lower():
                print("Escuchas como la electricidad fallo y por unas tuberias rotas se filtra un poco de agua.\n")
                self.audio_manager.play_audio("pasillo1.wav", loop = True, volume = 0.1)
            elif "pasillo 2" in current_room.get_name().lower():
                print("A tu izquierda notas que la energía eléctrica ha fallado y a tu derecha escuchas agua gotear.\n")
                self.audio_manager.play_audio("pasillo2.wav", loop = True, volume = 0.5)
            elif "pasillo 3" in current_room.get_name().lower():
                print("Escuchas agua goteando y circulando por todo el pasillo.\n")
                self.audio_manager.play_audio("pasillo3.wav", loop = True, volume = 0.1)
            elif "salida 1" in current_room.get_name().lower():
                self.audio_manager.play_audio("salida1.wav", loop = True, volume = 0.3)
            elif "salida 2" in current_room.get_name().lower():
                self.audio_manager.play_audio("salida1.wav", loop = True, volume = 0.3)
            elif "reactor" in current_room.get_name().lower():
                self.audio_manager.play_audio("reactor.wav", loop = True, volume = 0.3)
            elif "sala de operaciones" in current_room.get_name().lower():
                self.audio_manager.play_audio("operaciones.wav", loop = True, volume = 0.2)
            elif "zona de descanso" in current_room.get_name().lower():
                print("Escuchas a tu amigo de fondo gritando pero no podras hacer nada para ayudarlo")
            elif "sala de mantenimiento" in current_room.get_name().lower():
                print("Los pasillos resuenan con un rugido inhumano: la bestia.\nNo sabes dónde está, pero la sensación de que acecha más cerca de lo que crees acelera tu respiración.\n\nCada paso podría ser el último.")
            print(current_room.get_description())
            if current_room.is_explored():
                print("Ya has explorado este lugar.")
        print()
    
    def _get_player_action(self):
        print("¿Qué quieres hacer?")
        print("1. Explorar habitación actual")
        print("2. Moverse a otra habitación")
        print("3. Ver inventario")
        print("4. Ver estado detallado")
        print("5. Descansar")
        print("6. Salir del juego")
        while True:
            try:
                choice = input("\nSelecciona una opción (1-6): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6']:
                    self.audio_manager.stop_audio()
                    return choice
                else:
                    print("Opción inválida. Selecciona 1-6.")
            except KeyboardInterrupt:
                return '6'
    
    def _process_action(self, action: str):
        if action == '1':
            self._explore_current_room()
        elif action == '2':
            self._move_to_room()
        elif action == '3':
            self._show_inventory()
        elif action == '4':
            self._show_detailed_status()
        elif action == '5':
            self._rest_action()
        elif action == '6':
            self.is_running = False
    
    def _explore_current_room(self):
        current_room = self.game_map.get_room(self.player.get_current_room())
        if not current_room:
            print("Error: Habitación no encontrada.")
            return
        os.system("cls")
        print("Explorando la habitación...")
        self.audio_manager.play_audio("explorar.wav")
        self.audio_manager.wait_for_audio_finish()
        os.system("cls")
        print(current_room.explore())
        if current_room.get_objects():
            
            self._handle_room_objects(current_room)
        
        if current_room.has_living_enemies():
            os.system("cls")
            self._handle_combat(current_room)
        
        input("\nPresiona Enter para continuar...")
    
    def _handle_room_objects(self, room):
        objects = room.get_objects()
        if not objects:
            return
        
        print("\n¿Quieres recoger algún objeto?")
        for i, obj in enumerate(objects, 1):
            print(f"{i}. {obj.get_name()}: {obj.get_description()}")
        print(f"{len(objects) + 1}. No recoger nada")
        
        try:
            choice = int(input("Selecciona: ")) - 1
            if 0 <= choice < len(objects):
                obj_to_pick = objects[choice]
                picked_obj = room.remove_object(obj_to_pick.get_name())
                if picked_obj and self.player.pick_up_object(picked_obj):
                    if "llave" in picked_obj.name.lower(): 
                        self.audio_manager.play_audio("llaves.wav")
                        self.audio_manager.wait_for_audio_finish()
                    elif "pistola" in picked_obj.name.lower():
                        self.audio_manager.play_audio("pistola.wav")
                        self.audio_manager.wait_for_audio_finish()
                    elif "lata" in picked_obj.name.lower():
                        self.audio_manager.play_audio("lata.wav")
                        self.audio_manager.wait_for_audio_finish()
                    elif "cobija" in picked_obj.name.lower():
                        self.audio_manager.play_audio("cobija.wav", volume = 0.1)
                        self.audio_manager.wait_for_audio_finish()
                    print(f"Recogiste: {picked_obj.get_name()}")
                    self.audio_manager.play_audio("inventario.wav", volume = 0.3)
                    self.audio_manager.wait_for_audio_finish()                   
                else:
                    print("No pudiste recoger el objeto (inventario lleno).")
                    room.add_object(picked_obj)
        except (ValueError, IndexError):
            print("Selección inválida.")
    
    def _handle_combat(self, room):
        living_enemies = [e for e in room.get_enemies() if e.is_alive_check()]
        if not living_enemies:
            return
        
        print("\n¡HAY ENEMIGOS EN ESTA HABITACIÓN!")
        
        while living_enemies and self.player.is_alive_check():
            print("\nEnemigos presentes:")
            for i, enemy in enumerate(living_enemies, 1):
                print(f"{i}. {enemy.get_combat_status()}")
            print("\n¿Qué quieres hacer?")
            print("1. Atacar")
            print("2. Usar objeto")
            print("3. Huir")
            try:
                combat_choice = input("Selecciona (1-3): ").strip()     
                if combat_choice == '1':
                    self._player_attack(living_enemies)
                elif combat_choice == '2':
                    self._use_object()
                elif combat_choice == '3':
                    if self._attempt_flee():
                        return
                self._enemies_turn(living_enemies)
                living_enemies = [e for e in living_enemies if e.is_alive_check()]
                for enemy in room.get_enemies():
                    if not enemy.is_alive_check():
                        reward = enemy.drop_reward()
                        if reward:
                            room.add_object(reward)
                            print(f"{enemy.get_name()} dejó caer: {reward.get_name()}")
                
            except (ValueError, KeyboardInterrupt):
                print("Acción inválida.")
        
        if not living_enemies:
            print("\n¡Has derrotado a todos los enemigos!")
    
    def _player_attack(self, enemies):
        if len(enemies) == 1:
            target = enemies[0]
        else:
            print("¿A quién quieres atacar?")
            for i, enemy in enumerate(enemies, 1):
                print(f"{i}. {enemy.get_name()}")
            
            try:
                choice = int(input("Selecciona: ")) - 1
                if 0 <= choice < len(enemies):
                    target = enemies[choice]
                else:
                    print("Selección inválida.")
                    return
            except ValueError:
                print("Selección inválida.")
                return
        
        success, damage = self.player.attack_target(target)
        if success:
            self.audio_manager.play_audio("golpejugador.wav", volume=0.5)
            self.audio_manager.wait_for_audio_finish()
            print(f"Atacaste a {target.get_name()} causando {damage} de daño!")
            if not target.is_alive_check():
                print(f"¡{target.get_name()} ha sido derrotado!")
        else:
            print("Tu ataque falló.")
    
    def _enemies_turn(self, enemies):
        for enemy in enemies:
            if enemy.is_alive_check():
                action_result = enemy.act_turn(self.player)
                self.audio_manager.play_audio("golpemonstruo.wav", volume=0.1)
                self.audio_manager.wait_for_audio_finish()
                print(action_result)
                time.sleep(1)
    
    def _attempt_flee(self) -> bool:
        print("Intentas huir...")
        import random
        if random.random() < 0.7:
            self.audio_manager.play_audio("escape.wav", volume=0.7)
            self.audio_manager.wait_for_audio_finish()
            print("¡Lograste escapar!")
            return True
        else:
            print("No pudiste escapar.")
            return False
    
    def _move_to_room(self):
        current_room_name = self.player.get_current_room()
        connected_rooms = self.game_map.get_connected_rooms(current_room_name)
        
        if not connected_rooms:
            print("No hay salidas disponibles.")
            return
        os.system("cls")
        print("¿A dónde quieres ir?")
        for i, room_name in enumerate(connected_rooms, 1):
            print(f"{i}. {room_name}")
        print(f"{len(connected_rooms) + 1}. Cancelar")
        
        try:
            choice = int(input("Selecciona: ")) - 1
            if 0 <= choice < len(connected_rooms):
                target_room = connected_rooms[choice]
                can_move, message = self.game_map.can_move_to(current_room_name, target_room, self.player.get_inventory())
                new_room = self.game_map.get_room(target_room)
                if can_move:
                    self.player.move_to_room(target_room)
                    print(f"Te moviste a: {target_room}")
                    os.system("cls")
                    if message:
                        print(message)
                    print("Cambiando de lugar...")
                    if target_room == "escaleras":
                        self.audio_manager.play_audio("pasos.wav")
                        self.audio_manager.wait_for_audio_finish()
                        self.audio_manager.play_audio("escaleras.wav", volume = 0.2)
                        self.audio_manager.wait_for_audio_finish()
                        print("Camino bloqueado")
                        self.player.move_to_room("pasillo 1")
                        self.game_map.remove_room("pasillo 1", "escaleras")
                        input("\nPresiona Enter para continuar...")
                    elif target_room == "sala de mantenimiento":
                        self.audio_manager.play_audio("puerta.wav")
                        self.audio_manager.wait_for_audio_finish()
                        self.audio_manager.play_audio("pasos.wav")
                        if not new_room.is_visited():
                            print("Los pasillos resuenan con un rugido inhumano: la bestia.\nNo sabes dónde está, pero la sensación de que acecha más cerca de lo que crees acelera tu respiración. Cada paso podría ser el último.")
                            self.audio_manager.play_audio("monsterfaraway.wav", volume=0.2)
                            self.audio_manager.wait_for_audio_finish()
                        time.sleep(0.5)
                    elif target_room == "zona de descanso":
                        self.audio_manager.play_audio("puerta.wav")
                        self.audio_manager.wait_for_audio_finish()
                        self.audio_manager.play_audio("pasos.wav")
                        if not new_room.is_visited():
                            print("Escuchas a tu amigo de fondo gritando pero no podras hacer nada para ayudarlo")
                            self.audio_manager.play_audio("grito.wav", volume=0.1)
                            self.audio_manager.wait_for_audio_finish()
                        time.sleep(0.5)
                    elif target_room == "enfermeria":
                        self.audio_manager.play_audio("puerta.wav")
                        self.audio_manager.wait_for_audio_finish()
                        self.audio_manager.play_audio("pasos.wav")
                        self.audio_manager.wait_for_audio_finish()
                        if not new_room.is_visited():
                            self.audio_manager.play_audio("llamada.wav", volume=0.1)
                            self.audio_manager.wait_for_audio_finish()
                            print("Tu familia intenta llamarte una y otra vez, pero la señal es débil y se corta.\nEscuchas sus voces entrecortadas mientras te abres paso entre los restos del edificio. Sabes que te esperan afuera, pero el camino está bloqueado y necesitas encontrar una salida.")
                            input("\nPresiona Enter para continuar...")
                        time.sleep(0.5)
                    elif (target_room == "sala de seguridad" and self.player.has_object("Llave 1")) or (target_room == "sala de control" and self.player.has_object("Llave 2")) or (target_room == "reactor" and self.player.has_object("Llave 3l")):
                        self.audio_manager.play_audio("puerta.wav")
                        self.audio_manager.wait_for_audio_finish()
                        self.audio_manager.play_audio("pasos.wav")
                        self.audio_manager.wait_for_audio_finish()
                        self.audio_manager.play_audio("llavepuerta.wav", volume = 0.4)
                        self.audio_manager.wait_for_audio_finish()
                        time.sleep(0.5)
                    elif self.game_map.get_room(target_room).is_locked():
                        print("La puerta está cerrada.")
                        input("\nPresiona Enter para continuar...")
                    else:
                        self.audio_manager.play_audio("puerta.wav")
                        self.audio_manager.wait_for_audio_finish()
                        self.audio_manager.play_audio("pasos.wav")
                        self.audio_manager.wait_for_audio_finish()
                        time.sleep(0.5)
                    new_room.set_visited()
                else:
                    print(message)
                    input("\nPresiona Enter para continuar...")
            
        except (ValueError, IndexError):
            print("Selección inválida.")
    
    def _show_inventory(self):
        os.system("cls")
        print("Abriendo inventario...")
        self.audio_manager.play_audio("inventario.wav", volume=0.3)
        self.audio_manager.wait_for_audio_finish()
        
        inv = self.player.get_inventory()
        print(inv.show_inventory())
        
        print("\n¿Qué quieres hacer?")
        print("1. Usar objeto")
        print("2. Soltar objeto")
        print("3. Cerrar inventario")
        
        choice = input("Selecciona (1-3): ").strip()
        if choice == "1":
            self._use_object()
        elif choice == "2":
            self._drop_object()

    def _drop_object(self):
        items = self.player.get_inventory().get_items()
        if not items:
            print("Tu inventario está vacío.")
            return
        
        print("¿Qué objeto quieres soltar?")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item.get_name()}")
        print(f"{len(items) + 1}. Cancelar")
        
        try:
            choice = int(input("Selecciona: ")) - 1
            if 0 <= choice < len(items):
                item = items[choice]
                dropped = self.player.get_inventory().remove_item(item.get_name())
                if dropped:
                    current_room = self.game_map.get_room(self.player.get_current_room())
                    current_room.add_object(dropped)
                    print(f"Has soltado {item.get_name()} en {current_room.get_name()}.")
        except (ValueError, IndexError):
            print("Selección inválida.")

    def _use_object(self):
        if self.player.get_inventory().is_empty():
            print("Tu inventario está vacío.")
            input("\nPresiona Enter para continuar...")
            return
        
        print("¿Qué objeto quieres usar?")
        items = self.player.get_inventory().get_items()
        for i, item in enumerate(items, 1):
            usable_text = " (usable)" if item.is_usable() else " (no usable)"
            print(f"{i}. {item.get_name()}{usable_text}")
        print(f"{len(items) + 1}. Cancelar")
        
        try:
            choice = int(input("Selecciona: ")) - 1
            if 0 <= choice < len(items):
                item = items[choice]
                if "botiquin" in item.get_name().lower():
                    self.audio_manager.play_audio("botiquin.wav", volume = 0.5)
                    self.audio_manager.wait_for_audio_finish()
                    self.player.stop_bleeding()
                    print("¡Tu sangrado se ha detenido!")
                    self.player.get_inventory().remove_object(item)
                elif "agua" in item.get_name().lower():
                    self.audio_manager.play_audio("tomaragua.wav", volume=0.4)
                    self.audio_manager.wait_for_audio_finish()
                    self.player.get_inventory().remove_object(item)
                elif "pistola" in item.get_name().lower():
                    self.audio_manager.play_audio("pistola.wav", volume=0.5)
                    self.audio_manager.wait_for_audio_finish()
                    print("Sientes el peso de la pistola en tus manos. Puede ayudarte en combate.")
                    self.player.buff_attack(5)
                elif "cobija" in item.get_name().lower():
                    self.audio_manager.play_audio("cobija.wav", volume=0.1)
                    self.audio_manager.wait_for_audio_finish()
                    self.player.buff_defense(2)
                    if not getattr(self.player, "has_blanket", False):
                        self.player.has_blanket = True
                        print("Te envuelves en la cobija. Te sientes más protegido.")
                    else:
                        print("Ya llevas la cobija puesta.")
                elif "llave" in item.get_name().lower():
                    self.audio_manager.play_audio("llaves.wav")
                    self.audio_manager.wait_for_audio_finish()
                    print(f"Guardas {item.get_name()} con cuidado. Te servirá para abrir una puerta.")
                elif "manual" in item.get_name().lower():
                    print("Lees el manual… obtienes algo de conocimiento técnico, pero no tiene un efecto inmediato.")
                else:
                    print(f"Intentaste usar {item.get_name()}, pero no pasó nada.")
            else:
                print("Acción cancelada.")
        except (ValueError, IndexError):
            print("Selección inválida.")   
        
        input("\nPresiona Enter para continuar...")

    
    def _show_detailed_status(self):
        print(self.player.get_detailed_status())
        input("\nPresiona Enter para continuar...")
    
    def _rest_action(self):
        success, message = self.player.rest()
        print(message)
        input("\nPresiona Enter para continuar...")
    
    def _process_turn_effects(self):
        if self.player.is_bleeding():
            bleeding_damage = self.player.apply_bleeding_damage()
            if bleeding_damage > 0:
                print(f"\nPerdiste {bleeding_damage} puntos de salud por sangrado.")
                time.sleep(1)
    
    def _check_game_end(self):
        if not self.player.is_alive_check():
            return True
        if self.player.get_current_room() == "reactor":
            reactor_room = self.game_map.get_room("reactor")
            if reactor_room and not reactor_room.has_living_enemies():
                self.game_won = True
                return True
        if (self.player.get_current_room() == "salida 1" and 
            self.player.has_object("Llave especial")) or (self.player.get_current_room() == "salida 2"):
            self.game_won = True
            return True
        return False
    
    def _show_game_end(self):
        os.system("cls")
        if self.game_won:
            print("¡FELICITACIONES!")
            print("Has logrado sobrevivir y escapar del edificio.\n Toda tu familia y amigos te esperan afuera.")
        elif not self.player.is_alive_check():
            print("GAME OVER")
            print("Has sucumbido a tus heridas.")
        else:
            print("Juego terminado.")
        self.is_running = False
        input("\nPresiona Enter para volver al menú...")
    
    def end_game(self):

        self.is_running = False
