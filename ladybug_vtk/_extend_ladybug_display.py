"""Add capability to turn a Ladybug geometry object into a VTK polydata object."""

from ladybug_display.geometry2d import DisplayPoint2D, DisplayLineSegment2D, \
    DisplayPolyline2D, DisplayMesh2D
from ladybug_display.geometry3d import DisplayPoint3D, DisplayLineSegment3D, \
    DisplayPolyline3D, DisplayArc3D, DisplayMesh3D, DisplayFace3D, DisplayPolyface3D, \
    DisplayCone, DisplaySphere, DisplayCylinder, DisplayText3D

from .from_display_geometry import from_displayline2d, from_displaypoint2d, \
    from_displaypoint3d, from_displayline3d, from_displaypolyline3d, from_displayarc3d, \
    from_displaymesh3d, from_displaymesh2d, from_displayface3d, from_displaypolyface3d, \
    from_displaycone,from_displaysphere, from_displaycylinder, from_displaypolyline2d, \
    from_displaytext3d

# 2d goemetry
DisplayPoint2D.to_polydata = from_displaypoint2d
DisplayLineSegment2D.to_polydata = from_displayline2d
DisplayPolyline2D.to_polydata = from_displaypolyline2d

# 3d geometry
DisplayPoint3D.to_polydata = from_displaypoint3d
DisplayLineSegment3D.to_polydata = from_displayline3d
DisplayPolyline3D.to_polydata = from_displaypolyline3d
DisplayArc3D.to_polydata = from_displayarc3d
DisplayMesh3D.to_polydata = from_displaymesh3d
DisplayMesh2D.to_polydata = from_displaymesh2d
DisplayFace3D.to_polydata = from_displayface3d
DisplayPolyface3D.to_polydata = from_displaypolyface3d
DisplayCone.to_polydata = from_displaycone
DisplaySphere.to_polydata = from_displaysphere
DisplayCylinder.to_polydata = from_displaycylinder
DisplayText3D.to_polydata = from_displaytext3d
