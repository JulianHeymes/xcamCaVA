# xcamCaVA
Software for operating the xcam CaVa camera system.
## Usage
The module contains 3 classes current. CameraSettings provides some helper functions and stores the operating voltages and various parameters of the camera system. Modifications to camera parameters should be applied to this class and then fed into the CameraInterface() class via the apply_settings() method, which takes an instance of the CameraSettings class.

The Camera class provides access to the xcam dll, and be used without the other helper classes.

