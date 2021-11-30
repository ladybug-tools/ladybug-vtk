"""Functions to create VTK objects from Ladybug Objects."""

from ladybug_geometry.geometry3d.face import Face3D
import vtk
from typing import List
from ladybug_geometry.geometry3d import Point3D, Polyline3D, Arc3D, Cone
from .polydata import PolyData


def to_vtk_point(point: Point3D) -> PolyData:
    """Create a VTK point from a ladybug Point.

    Args:
        point (Point3D): A Ladybug Point3D object.

    Returns:
        VTK Polydata containing one point.
    """
    vtk_point = vtk.vtkPoints()
    vtk_vertice = vtk.vtkCellArray()

    vtk_point.InsertNextPoint(tuple(point))
    vtk_vertice.InsertNextCell(1, [1])

    polydata = PolyData()
    polydata.SetPoints(vtk_point)
    polydata.SetVerts(vtk_vertice)
    polydata.Modified()

    return polydata


def to_vtk_points(points: List[Point3D]) -> PolyData:
    """Create VTK points from a list of Ladybug Point3D objects.

    Args:
        points: A list of Ladybug Point3D objects.

    Returns:
        VTK Polydata containing all points.
    """
    vtk_points = vtk.vtkPoints()
    vtk_vertices = vtk.vtkCellArray()

    for point in points:
        vtk_points.InsertNextPoint(tuple(point))

    vtk_vertices.InsertNextCell(len(points), list(range(len(points))))

    polydata = PolyData()
    polydata.SetPoints(vtk_points)
    polydata.SetVerts(vtk_vertices)
    polydata.Modified()

    return polydata


def to_vtk_polyline_from_points(points: List[Point3D]) -> PolyData:
    """Create a VTK polyline from a list of Ladybug Point3D objects.

    Args:
        points: A list of Ladybug Point3D objects.

    Returns:
        VTK Polydata containing a Polyline.
    """

    pts = vtk.vtkPoints()
    for pt in points:
        pts.InsertNextPoint(tuple(pt))

    polyline = vtk.vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(len(points))
    for i in range(len(points)):
        polyline.GetPointIds().SetId(i, i)

    cells = vtk.vtkCellArray()
    cells.InsertNextCell(polyline)

    polydata = PolyData()
    polydata.SetPoints(pts)
    polydata.SetLines(cells)

    return polydata


def to_vtk_arc(arc: Arc3D, divisions: int, interpolated: bool = True) -> PolyData:
    """Create a VTK polyline from a Ladybug Arc3D object.

    Args:
        arc: A Ladybug Arc3D object.
        divisions: The number of segments into which the arc will be divided.
        interpolated: Boolean to note whether the polyline should be interpolated 
            between the input vertices when it is translated to other interfaces. 
            This property has no effect on the geometric calculations performed by 
            this library and is only present in order to assist with 
            display/translation. Defaults to True.
    """
    return to_vtk_polyline(arc.to_polyline(divisions, interpolated))


def to_vtk_face(face: Face3D) -> PolyData:
    pass


def to_vtk_polyline(polyline: Polyline3D) -> PolyData:
    """Create a VTK polyline from a Ladybug Polyline3D object.

    Args:
        polyline: A Ladybug Polyline3D object.

    Returns:
        VTK Polydata containing a Polyline.
    """
    points = polyline.vertices
    return to_vtk_polyline_from_points(points)
