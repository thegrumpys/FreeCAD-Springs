import FreeCAD, Part
import math

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
