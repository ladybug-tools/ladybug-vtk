"""Functions to translate Ladybug2D Objects to Polydata."""

import vtk
import math
from typing import List
from ladybug_geometry.geometry2d import Point2D, LineSegment2D
from .polydata import PolyData


def from_point2d(point: Point2D) -> PolyData:
    """Create Polydata from a Ladybug Point2D object.

    Args:
        point: A ladybug Point object.

    Returns:
        Polydata containing a single point.
    """
    vtk_point = vtk.vtkPoints()
    vtk_vertice = vtk.vtkCellArray()

    vtk_point.InsertNextPoint(point.x, point.y, 0)
    vtk_vertice.InsertNextCell(1, [1])

    polydata = PolyData()
    polydata.SetPoints(vtk_point)
    polydata.SetVerts(vtk_vertice)
    polydata.Modified()

    return polydata


def _polyline_from_points(points: List[Point2D]) -> PolyData:
    """Create Polydata from a list of Ladybug Point2D objects.

    Args:
        points: A list of Ladybug Point2D objects.

    Returns:
        Polydata containing a polyline created by joining the points.
    """
    pts = vtk.vtkPoints()
    for point in points:
        pts.InsertNextPoint(point.x, point.y, 0)

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


def from_points2d(points: List[Point2D], join: bool = False) -> PolyData:
    """Create Polydata from a list of Ladybug Point2D objects.

    Args:
        points: A list of Ladybug Point2D objects.
        join: Boolean to indicate whether the points should be joined into a polyline.

    Returns:
        Polydata containing all points or a polyline.
    """
    if join:
        return _polyline_from_points(points)

    vtk_points = vtk.vtkPoints()
    vtk_vertices = vtk.vtkCellArray()

    for point in points:
        vtk_points.InsertNextPoint(point.x, point.y, 0)

    vtk_vertices.InsertNextCell(len(points), list(range(len(points))))

    polydata = PolyData()
    polydata.SetPoints(vtk_points)
    polydata.SetVerts(vtk_vertices)
    polydata.Modified()

    return polydata


def from_line2d(line: LineSegment2D) -> PolyData:
    """Create Polydata from a Ladybug LineSegment3D object.

    Args:
        line: A Ladybug LineSegment3D object.

    Returns:
        Polydata containing a line.
    """
    return from_points2d(line.vertices, join=True)
