import camera
import camerasettings

class CameraInterface:
    def __init__(self, camera):
        self.camera = camera
        self.settings = CameraSettings()
        
