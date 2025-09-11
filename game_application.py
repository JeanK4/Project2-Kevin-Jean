from audio_manager import AudioManager
from game import Game
from menu import Menu


class GameApplication:
    """Clase principal que coordina toda la aplicación"""
    
    def __init__(self):
        self.audio_manager = AudioManager()
        self.game = Game(self.audio_manager)
        self.menu = Menu(self.game)
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            print("Bienvenido al juego!")
            self.menu.run()
        except Exception as e:
            print(f"Error en la aplicación: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpia los recursos antes de cerrar"""
        self.audio_manager.cleanup()