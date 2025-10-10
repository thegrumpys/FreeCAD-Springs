# 🌀 Springs Workbench for FreeCAD

Design and analyze **compression**, **extension**, and **torsion** springs directly inside FreeCAD.

![Springs Workbench Toolbar](Resources/icons/Springs.svg)

---

## ✨ Features

- ✅ Accurate solid-model geometry for compression, extension, and torsion springs  
- 🧩 Configurable end types (Open, Closed, Ground, Closed & Ground)  
- 🧮 Solver integration (Hooke & Jeeves pattern search)  
- 📈 Catalog search and comparison using objective values  
- 🎨 Multiple display modes (Detailed, Simplified, Envelope)  
- 🧷 Attachment support for PartDesign & Assembly workflows  
- 🧾 Material integration via `.FCMat` files  
- 🌍 Full internationalization support (Qt `.ts` / `.qm` translations)

---

## 🧰 Installation

### Option 1 – Addon Manager (recommended)
1. Open **Tools → Addon Manager** in FreeCAD.  
2. Search for **“Springs”**.  
3. Click **Install**.  
4. Restart FreeCAD.

### Option 2 – Manual Install
1. Clone or download this repository.  
2. Copy the `FreeCAD-Springs` folder into your FreeCAD `Mod/` directory.  
3. Restart FreeCAD.

---

## 🚀 Usage

1. Switch to the **Springs Workbench**.
2. Use the toolbar or menu to create:
   - **Compression Spring**
   - **Extension Spring**
   - **Torsion Spring**
3. Edit geometry, material, loads, and placement in the Property Editor.  
4. Optionally run the **solver** to optimize parameters.  
5. Open **Find Catalog Matches** to locate real-world equivalents.

---

## ⚙️ Preferences in code

The preference page (``Edit → Preferences → Springs``) stores solver options,
weights, and UI toggles inside FreeCAD's parameter system. Modules can query
these values through helpers in ``Features.Utils``:

```python
from Springs.Features import Utils

max_iterations = Utils.preference_int("maxit", 600)
objective_minimum = Utils.preference_float("objmin", 1.0e-5)
show_units = Utils.preference_bool("show_units", True)
```

Each helper reads from ``BaseApp/Preferences/Mod/Springs`` and falls back to
the supplied default if a setting has not been stored yet.

---

## 📁 Repository Structure (via `tree -I '__pycache__'`)

    FreeCAD-Springs/
    ├── __init__.py
    ├── Commands
    │   ├── __init__.py
    │   ├── CmdCompressionSpring.py
    │   ├── CmdExtensionSpring.py
    │   ├── CmdSpringInfo.py
    │   └── CmdTorsionSpring.py
    ├── Dialogs
    │   ├── __init__.py
    │   └── SpringInfoDialog.py
    ├── Features
    │   ├── __init__.py
    │   ├── Compression
    │   │   ├── __init__.py
    │   │   └── Spring.py
    │   ├── Extension
    │   │   ├── __init__.py
    │   │   └── Spring.py
    │   ├── Torsion
    │   │   ├── __init__.py
    │   │   └── Spring.py
    │   ├── Utils.py
    │   └── ViewProviderSpring.py
    ├── Init.py
    ├── InitGui.py
    ├── LICENSE
    ├── Preferences
    │   ├── __init__.py
    │   └── SpringsPreferencePage.py
    ├── README.md
    ├── Resources
    │   └── icons
    │       ├── compression.svg
    │       ├── extension.svg
    │       ├── preferences-springs.svg
    │       ├── SpringInfo.svg
    │       ├── torsion.svg
    │       └── workbench.svg
    └── Tests
        └── test_Springs.py

---

## ✅ Testing

Run the regression suite from FreeCAD's command-line executable so the
application modules are available to the interpreter:

```bash
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd \
  ~/Library/Application\ Support/FreeCAD/Mod/Springs/Tests/test_Springs.py
```

---

## 🧑‍💻 Maintainer

**thegrumpys**  
📧 <<< Info@SpringDesignSoftware.org >>>  
🌐 [https://github.com/thegrumpys](https://github.com/thegrumpys)

---

## 📜 License

[MIT License](LICENSE)

---

*Compatible with FreeCAD 0.21 and newer.*
