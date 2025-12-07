import os
from pathlib import Path

HOME = Path(__file__).parent
MODELS = os.listdir(Path(HOME, r"..\..\models"))
LLAMAEXE = Path(HOME, r"..\..\bin\llama-b7058-bin-win-cuda-12.4-x64\llama-server.exe")
