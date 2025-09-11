from pathlib import Path
import time
from openal import oalOpen, oalQuit, AL_PLAYING
import threading


class AudioManager:
    """Clase para manejar todo lo relacionado con audio"""
    
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent / "audios"
        self.current_source = None
        self.audio_timer = None
    
    def play_audio(self, filename, loop=False, volume: float = 1.0):
        """Reproduce un archivo de audio con volumen (0.0 - 1.0)"""
        wav_path = self.base_path / filename
        if not wav_path.exists():
            print(f"Error: No se encontró el archivo {filename}")
            return False
        
        try:
            self.current_source = oalOpen(str(wav_path))
            self.current_source.set_looping(loop)
            
            # Configurar volumen inicial
            volume = max(0.0, min(volume, 1.0))
            self.current_source.set_gain(volume)
            
            self.current_source.play()
            return True
        except Exception as e:
            print(f"Error al reproducir audio: {e}")
            return False
    
    def play_audio_for_duration(self, filename, duration_seconds, loop=False, volume: float = 1.0):
        """Reproduce un archivo de audio por una duración específica en segundos"""
        if self.play_audio(filename, loop, volume):
            # Programa parar el audio después de la duración especificada
            self.audio_timer = threading.Timer(duration_seconds, self.stop_audio)
            self.audio_timer.start()
            return True
        return False
    
    def wait_for_audio_finish(self):
        """Espera a que termine de reproducirse el audio actual"""
        if self.current_source:
            while self.current_source.get_state() == AL_PLAYING:
                time.sleep(0.05)
    
    def wait_for_duration(self, duration_seconds):
        """Espera por una duración específica mientras el audio se reproduce"""
        if self.current_source:
            start_time = time.time()
            while (time.time() - start_time) < duration_seconds and self.current_source.get_state() == AL_PLAYING:
                time.sleep(0.05)
            # Detener el audio si aún se está reproduciendo
            if self.current_source.get_state() == AL_PLAYING:
                self.stop_audio()
    
    def get_audio_duration(self):
        """Obtiene la duración total del audio actual (en segundos)"""
        if self.current_source:
            try:
                return self.current_source.get_sec_offset()
            except:
                return None
        return None
    
    def set_volume(self, volume: float):
        """Cambia el volumen del audio actual (0.0 = silencio, 1.0 = normal)"""
        if self.current_source:
            volume = max(0.0, min(volume, 1.0))
            self.current_source.set_gain(volume)
    
    def get_volume(self) -> float:
        """Obtiene el volumen actual"""
        if self.current_source:
            return self.current_source.get_gain()
        return 0.0
    
    def stop_audio(self):
        """Detiene el audio actual"""
        if self.current_source:
            self.current_source.stop()
        if self.audio_timer:
            self.audio_timer.cancel()
            self.audio_timer = None
    
    def cleanup(self):
        """Limpia los recursos de audio"""
        if self.audio_timer:
            self.audio_timer.cancel()
        if self.current_source:
            self.current_source.destroy()
        oalQuit()
