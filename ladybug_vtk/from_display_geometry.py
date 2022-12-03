"""Functions to translate ladybug display geometry objects into VTK polydata objects.

This module currently ignores all the display attributes and only translates the geometry.
"""

from typing import List

from ladybug_display.geometry2d import DisplayPoint2D, DisplayLineSegment2D, \
    DisplayPolyline2D, DisplayMesh2D
from ladybug_display.geometry3d import DisplayPoint3D, DisplayPolyline3D, DisplayArc3D, \
    DisplayLineSegment3D, DisplayMesh3D, DisplayPolyface3D, DisplayCone, \
    DisplayCylinder, DisplaySphere, DisplayFace3D, DisplayText3D

from .from_geometry import from_arc3d, from_cone, from_cylinder, from_face3d, \
    from_line2d, from_line3d, from_mesh2d, from_mesh3d, from_point2d, from_point3d, \
    from_points2d, from_points3d, from_polyface3d, from_polyline2d, from_polyline3d, \
    from_sphere, from_text


from .polydata import PolyData


def from_displaypoint2d(point: DisplayPoint2D) -> PolyData:
    """Create Polydata from a Ladybug DisplayPoint2D object.

    Args:
        point: A ladybug DisplayPoint object.

    Returns:
        Polydata containing a single point.
    """
    return from_point2d(point=point.geometry)


def from_displaypoints2d(points: List[DisplayPoint2D], join: bool = False) -> PolyData:
    """Create Polydata from a list of Ladybug Point2D objects.

    Args:
        points: A list of Ladybug DisplayPoint2D objects.
        join: Boolean to indicate whether the points should be joined into a polyline.

    Returns:
        Polydata containing all points or a polyline.
    """
    return from_points2d(points=[pt.geometry for pt in points], join=join)


def from_displayline2d(line: DisplayLineSegment2D) -> PolyData:
    """Create Polydata from a Ladybug DisplayLineSegment3D object.

    Args:
        line: A Ladybug DisplayLineSegment3D object.

    Returns:
        Polydata containing a line.
    """
    return from_line2d(line=line.geometry)


def from_displaypolyline2d(polyline: DisplayPolyline2D) -> PolyData:
    """Create Polydata from a Ladybug Polyline3D object.

    Args:
        polyline: A Ladybug DisplayPolyline3D object.

    Returns:
        Polydata containing a polyline.
    """
    return from_polyline2d(polyline=polyline.geometry)


def from_displaypoint3d(point: DisplayPoint3D) -> PolyData:
    """Create Polydata from a Ladybug DisplayPoint3D object.

    Args:
        point: A ladybug DisplayPoint3D object.

    Returns:
        Polydata containing a single point.
    """
    from_point3d(point=point.geometry)


def from_displaypoints3d(points: List[DisplayPoint3D], join: bool = False) -> PolyData:
    """Create Polydata from a list of Ladybug DisplayPoint3D objects.

    Args:
        points: A list of Ladybug DisplayPoint3D objects.
        join: Boolean to indicate whether the points should be joined into a polyline.

    Returns:
        Polydata containing all points or a polyline.
    """
    return from_points3d(points=[pt.geometry for pt in points], join=join)


def from_displayline3d(line: DisplayLineSegment3D) -> PolyData:
    """Create Polydata from a Ladybug DisplayLineSegment3D object.

    Args:
        line: A Ladybug DisplayLineSegment3D object.

    Returns:
        Polydata containing a line.
    """
    return from_line3d(line.geometry)


def from_displaypolyline3d(polyline: DisplayPolyline3D) -> PolyData:
    """Create Polydata from a Ladybug DisplayPolyline3D object.

    Args:
        polyline: A Ladybug DisplayPolyline3D object.

    Returns:
        Polydata containing a polyline.
    """
    return from_polyline3d(polyline=polyline.geometry)


def from_displayarc3d(arc3d: DisplayArc3D, resolution: int = 3) -> PolyData:
    """Create Polydata from a Ladybug DisplayArc3D object.

    Args:
        arc3d: A Ladybug DisplayArc3D object.
        resolution: The number of degrees per subdivision. The default is 3 that creates
            120 segments for an full circle.

    Returns:
        Polydata containing an arc.
    """
    return from_arc3d(arc3d=arc3d.geometry, resolution=resolution)


def from_displaymesh3d(mesh: DisplayMesh3D) -> PolyData:
    """Create Polydata from a Ladybug DisplayMesh3D.

    Args:
        mesh: A Ladybug DisplayMesh3D object.

    Returns:
        Polydata containing face and points of a mesh.
    """
    return from_mesh3d(mesh=mesh.geometry)


def from_displaymesh2d(mesh: DisplayMesh2D) -> PolyData:
    """Create Polydata from a Ladybug DisplayMesh2D.

    Args:
        mesh: A Ladybug DisplayMesh2D object.

    Returns:
        Polydata containing face and points of a mesh.
    """
    return from_mesh2d(mesh.geometry)


def from_displayface3d(face: DisplayFace3D) -> PolyData:
    """Create Polydata from a Ladybug DisplayFace3D.

    Args:
        face: A Ladybug DisplayFace3D object.

    Returns:
        Polydata containing face and points of a face.
    """
    return from_face3d(face=face.geometry)


def from_displaypolyface3d(polyface: DisplayPolyface3D) -> PolyData:
    """Create Polydata from a Ladybug DisplayPolyface3D.

    Args:
        polyface: A Ladybug DisplayPolyface3D object.

    Returns:
        A list of Polydata. Each polydata contains a face and points of a face of Polyface.
    """
    return from_polyface3d(polyface=polyface.geometry)


def from_displaytext3d(text: DisplayText3D) -> PolyData:
    
    HORIZONTAL_ALIGN = ['Left', 'Center', 'Right']
    VERTICAL_ALIGN = ['Top', 'Middle', 'Bottom']

    return from_text(
        text.text, plane=text.plane, height=text.height,
        horizontal_alignment=HORIZONTAL_ALIGN.index(text.horizontal_alignment),
        vertical_alignment=VERTICAL_ALIGN.index(text.vertical_alignment)
    )


def from_displaycone(cone: DisplayCone, resolution: int = 2, cap: bool = True) -> PolyData:
    """Create Polydata from a Ladybug DisplayCone.

    Args:
        cone: A Ladybug DisplayCone object.
        resolution: The number of segments into which the cone will be divided.
            If set to 0, a line will be created.
            If set to 1, a single triangle will be created.
            If set to 2, two crossed triangles will be created.
            If set to greater than 2, a 3D cone with the number of sides equal to
            the resolution will be created. Defaults to 2.
        cap: Boolean to indicate whether the cone should capped or not. Default to True.

    Returns:
        Polydata containing a cone.
    """
    return from_cone(cone=cone.geometry, resolution=resolution, cap=cap)


def from_displaysphere(sphere: DisplaySphere, resolution: int = 50) -> PolyData:
    """Create Polydata from a Ladybug DisplaySphere.

    Args:
        sphere: A Ladybug DisplaySphere object.
        resolution: The number of segments into which the sphere will be divided.
            Defaults to 25.

    Returns:
        Polydata containing a sphere.
    """
    return from_sphere(sphere=sphere.geometry, resolution=resolution)


def from_displaycylinder(cylinder: DisplayCylinder, resolution: int = 50, cap: bool = True) -> PolyData:
    """Create Polydata from a Ladybug DisplayCylinder.

    Args:
        cylinder: A Ladybug DisplayCylinder object.
        resolution: The number of segments into which the cylinder will be divided.
            Defaults to 25.
        cap: Boolean to indicate whether the cylinder should capped or not.
            Default to True.

    Returns:
        Polydata containing a cylinder.
    """
    return from_cylinder(cylinder=cylinder.geometry, resolution=resolution, cap=cap)

