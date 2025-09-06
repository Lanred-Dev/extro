# python build.py

from Cython.Compiler.Main import compile as cython_compile
from pathlib import Path
import os


for pyx_file in Path("src").rglob("*.pyx"):
    pyx_path = str(pyx_file)
    cython_compile(str(pyx_file), ["--embed-signature", "--cplus"])

# Remove .c files
for filename in list(Path("src").rglob("*.c")):
    os.remove(filename)
