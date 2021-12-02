"""Functions to create VTK objects from Ladybug Objects."""


import vtk
from ladybug_geometry.geometry3d import Point3D
from .polydata import PolyData


def to_circle(center: Point3D, radius: int = 100, sides: int = 100) -> PolyData:
    """Create a VTK circle from a ladybug Point3D and radius.

    Args:
        center: A ladybug Point3D object.
        radius: The radius of the circle. Defaults to 100 meters.
        sides: The number of sides of the circle. Defaults to 100.

    Returns:
        A Polydata object containing a circle.
    """
    polygonSource = vtk.vtkRegularPolygonSource()
    polygonSource.GeneratePolygonOff()
    polygonSource.SetNumberOfSides(sides)
    polygonSource.SetRadius(radius)
    polygonSource.SetCenter(center.x, center.y, center.z)
    polygonSource.Update()

    polydata = PolyData()
    polydata.ShallowCopy(polygonSource.GetOutput())
    return polydata


def to_text(text: str, point: Point3D) -> PolyData:
    """Create a VTK text object from a text string and a ladybug Point3D.

    Args:
        text: A text string.
        point: A ladybug Point3D object. This is the location in 3D space of the text.

    Returns:
        A Polydata object containing the text.
    """
    source = vtk.vtkVectorText()
    source.SetText(text)

    translation = vtk.vtkTransform()
    translation.Translate(point.x, point.y, point.z)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(source.GetOutputPort())
    transformFilter.SetTransform(translation)
    transformFilter.Update()

    polydata = PolyData()
    polydata.ShallowCopy(transformFilter.GetOutput())
    return polydata
