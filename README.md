# extro

A 2D game engine written in Python that uses Pyray (Raylib) as its backend.

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

### Examples

Code examples can be found [here](https://github.com/Lanred-Dev/extro/tree/main/examples)

<div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <video src="media/animated_sprite.mp4" height="200" controls></video>
    <video src="media/button_and_sound.mp4" height="200" controls></video>
    <video src="media/sin.mp4" height="200" controls></video>
    <video src="media/tween.mp4" height="200" controls></video>
</div>

### Requirements

- Python 3.13.2 (or newer)
- CMake 3.15 (or newer) \*
- C++23 (or newer) compiler \*

\* Required only if building from source

> **Note:** extro has only been tested on **Windows 11**. Other platforms may work but are currently unverified.

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

### Building the wheel

To create a distributable `.whl` file:

```bash
pip install --upgrade build
python -m build
```

### Building C++ extensions separately from the wheel

If you want to build the C++ extensions separately from the `.whl`, you can do so using CMake and nanobind.

1. Install nanobind:

```bash
pip install nanobind
```

2. Then build using CMake:

```bash
cmake -S . -B build
cmake --build build --config Release
```
