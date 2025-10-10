import FreeCAD, Part
import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

def add_property(obj, name, default, typ="App::PropertyFloat", group="Spring"):
    """Safely add a FreeCAD property if it doesn't already exist."""
    if not hasattr(obj, name):
        obj.addProperty(typ, name, group, "")
        setattr(obj, name, default)


def helix_solid(radius, pitch, height, wire_radius):
    """Create a helical solid (coil) from geometric parameters."""
    helix = Part.makeHelix(pitch, height, radius)
    helix_wire = helix if isinstance(helix, Part.Wire) else Part.Wire([helix])
    helix_edge = helix_wire.Edges[0]

    u0 = helix_edge.FirstParameter
    start_pt = helix_edge.valueAt(u0)
    tangent = helix_edge.tangentAt(u0)
    if isinstance(tangent, tuple):
        tangent = tangent[0]
    tangent.normalize()

    circle = Part.makeCircle(wire_radius, start_pt, tangent)
    circle_wire = Part.Wire(circle)

    try:
        sweep = helix_wire.makePipeShell([circle_wire], True, True)
        if sweep.ShapeType == "Shell":
            sweep = Part.makeSolid(sweep)
    except Exception:
        sweep = Part.makeCylinder(wire_radius, height)

    return sweep

def spring_coils(height, pitch):
    """Number of coils based on total height and pitch."""
    return height / pitch

def spring_wire_length(mean_diameter, pitch, coils):
    """Length of wire forming the helix."""
    return math.sqrt((math.pi * mean_diameter)**2 + pitch**2) * coils

def spring_rate(G, wire_diameter, mean_diameter, coils):
    """Return spring rate (N/mm) using the classic formula."""
    d = wire_diameter
    D = mean_diameter
    n = coils
    k = (G * d**4) / (8 * n * (D**3))
    return k / 1000.0  # Convert from N/m to N/mm for convenience

def spring_solid_length(wire_diameter, coils):
    """Total length when fully compressed."""
    return wire_diameter * (coils + 1)

# -----------------------------------------------------------------------------
# End type helpers
# -----------------------------------------------------------------------------


@dataclass(frozen=True)
class EndTypeProperty:
    """Metadata describing a property managed by an end-type table."""

    key: str
    name: str
    group: str


@dataclass
class EndTypeTable:
    """Structured representation of an end-type configuration file."""

    name: str
    options: List[str]
    properties: List[EndTypeProperty]
    values: Dict[str, Dict[str, Any]]

    @property
    def default(self) -> Optional[str]:
        return self.options[0] if self.options else None


def _parse_property_key(raw: str) -> EndTypeProperty:
    """Translate a header entry into a property descriptor."""

    if "@" in raw:
        name, group = raw.split("@", 1)
    else:
        name, group = raw, "Spring"
    return EndTypeProperty(key=raw, name=name, group=group)


def _coerce_property_value(value: Any) -> Any:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return None
    return str(value)


def _property_type_for(value: Any) -> str:
    if isinstance(value, bool):
        return "App::PropertyBool"
    if isinstance(value, (int, float)):
        return "App::PropertyFloat"
    return "App::PropertyString"


@lru_cache(maxsize=None)
def load_end_type_table(path: Union[str, Path]) -> Optional[EndTypeTable]:
    """Load an end-type definition JSON file.

    Parameters
    ----------
    path: Union[str, Path]
        Location of the JSON configuration file describing available end types.
    """

    resolved = Path(path)
    if not resolved.exists():
        return None

    try:
        data = json.loads(resolved.read_text())
    except Exception:
        return None

    if not data:
        return None

    header, *rows = data
    if not header or header[0] != "End_Type":
        return None

    props = [_parse_property_key(h) for h in header[1:]]
    options: List[str] = []
    values: Dict[str, Dict[str, Any]] = {}

    for row in rows:
        if not row:
            continue
        option = str(row[0])
        options.append(option)
        mapping = {
            prop.key: row[i + 1] if i + 1 < len(row) else None
            for i, prop in enumerate(props)
        }
        values[option] = mapping

    return EndTypeTable(name="End_Type", options=options, properties=props, values=values)


def ensure_end_type_properties(obj, table: Optional[EndTypeTable]) -> Optional[str]:
    """Create properties defined by an end-type table and return the selection."""

    if table is None or not table.options:
        return None

    if not hasattr(obj, "EndType"):
        obj.addProperty("App::PropertyEnumeration", "EndType", "Spring", "")

    # Assign available options and choose a valid current value
    obj.EndType = table.options
    current = obj.EndType
    if isinstance(current, (list, tuple)):
        current = current[0] if current else table.default

    if current not in table.values:
        current = table.default
    if current is None:
        return None

    obj.EndType = current

    defaults = table.values.get(current, {})
    for prop in table.properties:
        default_value = defaults.get(prop.key)
        typ = _property_type_for(default_value)
        coerced = _coerce_property_value(default_value)
        add_property(obj, prop.name, coerced, typ=typ, group=prop.group)

    return current


def apply_end_type_properties(obj, table: Optional[EndTypeTable], selected: Optional[str]) -> None:
    """Update dependent properties when the end type changes."""

    if table is None or not selected:
        return

    values = table.values.get(selected)
    if not values:
        return

    for prop in table.properties:
        if not hasattr(obj, prop.name):
            continue
        value = _coerce_property_value(values.get(prop.key))
        if value is None:
            continue
        setattr(obj, prop.name, value)
