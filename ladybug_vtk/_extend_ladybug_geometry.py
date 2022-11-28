"""Add capability to turn a Ladybug geometry object into a VTK polydata object."""

from ladybug_geometry.geometry2d import Point2D, LineSegment2D, Polyline2D, \
    Polygon2D, Mesh2D
from ladybug_geometry.geometry3d import Point3D, LineSegment3D, Polyline3D, Arc3D, \
    Mesh3D, Face3D, Polyface3D, Cone, Sphere, Cylinder
from .from_geometry import from_line2d, from_point2d, from_point3d, from_line3d, \
    from_polyline3d, from_arc3d, from_mesh3d, from_mesh2d, from_face3d, \
    from_polyface3d, from_cone, from_sphere, from_cylinder, from_polyline2d, \
    from_polygon2d

# 2d goemetry
Point2D.to_polydata = from_point2d
LineSegment2D.to_polydata = from_line2d
Polyline2D.to_polydata = from_polyline2d
Polygon2D.to_polydata = from_polygon2d

# 3d geometry
Point3D.to_polydata = from_point3d
LineSegment3D.to_polydata = from_line3d
Polyline3D.to_polydata = from_polyline3d
Arc3D.to_polydata = from_arc3d
Mesh3D.to_polydata = from_mesh3d
Mesh2D.to_polydata = from_mesh2d
Face3D.to_polydata = from_face3d
Polyface3D.to_polydata = from_polyface3d
Cone.to_polydata = from_cone
Sphere.to_polydata = from_sphere
Cylinder.to_polydata = from_cylinder
