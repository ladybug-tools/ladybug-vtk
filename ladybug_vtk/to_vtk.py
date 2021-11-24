"""Functions to create VTK objects from Ladybug Objects."""

import vtk
from typing import List, Union
from ladybug_geometry.geometry3d import Point3D, Polyline3D
from .polydata import PolyData


def to_vtk_points(points: List[Point3D]) -> PolyData:
    """Create Polydata from a list of Points."""
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
    """Create Polydata with a Polyline from a list of points."""
    # Create a vtkPoints container and store the points for all the lines
    pts = vtk.vtkPoints()
    for pt in points:
        pts.InsertNextPoint(tuple(pt))

    # add all the points to lines dataset
    polyline = vtk.vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(len(points))
    for i in range(len(points)):
        polyline.GetPointIds().SetId(i, i)

    # Create a cell array to store the lines in and add the lines to it
    cells = vtk.vtkCellArray()
    cells.InsertNextCell(polyline)

    # Create a polydata to store everything in
    polydata = PolyData()

    # Add the points to the dataset
    polydata.SetPoints(pts)

    # Add the lines to the dataset
    polydata.SetLines(cells)

    return polydata


def to_vtk_polyline(polyline: Polyline3D) -> PolyData:
    """Create Polydata from a Polyline."""
    points = polyline.vertices
    return to_vtk_polyline_from_points(points)
