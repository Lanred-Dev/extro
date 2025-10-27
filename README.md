# extro

A 2D game engine written in Python that uses Pyray (Raylib) as its backend.

---

### Features

- Instance and scene management
- Built-in developer console
- Built-in profiler and performance metrics
- 2D physics and collision detection
- UI framework
- Instance hierarchy and object parenting
- Animation system supporting sprites and tweened instances
- Utility classes (timeouts, janitor, signals, etc.)
- Built-in 2D camera support

---

### Examples

Examples can be found [here](https://github.com/Lanred-Dev/extro/tree/main/examples)

---

### Requirements

- Python 3.13.2 (or newer)
- CMake 3.15 (or newer) \*
- C++23 (or newer) compiler \*

\* Required only if building from source

> **Note:** extro has only been tested on **Windows 11**. Other platforms may work but are currently unverified.

---

### Setup

1. Clone this repository

```bash
git clone https://github.com/Lanred-Dev/extro.git
cd extro
```

2. Create a Python virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

```bash
.venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install raylib
```

---

### Building native extensions

extro includes some C++ extensions using `nanobind`.
You must build them before use:

```bash
cmake -S . -B build
cmake --build build --config Release
```

---

### Building the wheel

To create a distributable `.whl` file:

```bash
pip install --upgrade pip setuptools wheel build nanobind scikit-build
python -m build
```
