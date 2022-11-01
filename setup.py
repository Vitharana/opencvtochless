import sys
from cx_Freeze import setup, Executable




setup(name="Boccia Touchless Interface",
      version="0.5",
      description="This software used to control boccia ramp",
      executables=[Executable("Boccia_Tochless_Interface_v1.py")]
      )

