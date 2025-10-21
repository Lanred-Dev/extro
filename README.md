# extro

**extro** is an in-development **2D game engine** written in Python, using **Raylib** as the rendering backend.

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

---

### Building the wheel

To create a distributable `.whl` file that includes the compiled `.pyd` extensions:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install scikit-build nanobind
python -m build
```

---

### Examples

Examples can be found [here](https://github.com/Lanred-Dev/extro/tree/main/examples)
