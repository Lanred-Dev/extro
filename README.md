# Extro

**Extro** is an in-development **2D game engine** written in Python, using **Raylib** as the rendering backend. It is lightweight, flexible, and designed specifically for **Windows**.

---

### Setup

1. Create a Python virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -e .
```

---

### Building native extensions

Build the `nanobind` extensions by running the provided script:

```bash
./build_release.sh
```

### Examples

Examples can be found [here](https://github.com/Lanred-Dev/extro/tree/main/examples)
