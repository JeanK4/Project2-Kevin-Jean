import os

class Menu:
    
    def __init__(self, game):
        self.game = game
        self.running = True
    
    def show_menu(self):
        print("\n" + "="*25)
        print("      MENÚ PRINCIPAL")
        print("="*25)
        print("1. Nuevo Juego")
        print("2. Salir")
        print("="*25)
    
    def get_user_choice(self):
        while True:
            try:
                choice = input("Seleccione una opción: ").strip()
                if choice in ["1", "2"]:
                    return choice
                else:
                    print("Opción inválida. Por favor, seleccione 1 o 2.")
            except KeyboardInterrupt:
                print("\nSaliendo del juego...")
                return "2"
    
    def run(self):
        while self.running:
            self.show_menu()
            choice = self.get_user_choice()
            
            if choice == "1":
                self.game.start_game()
            elif choice == "2":
                os.system("cls")
                print("¡Gracias por jugar!")
                self.running = False

