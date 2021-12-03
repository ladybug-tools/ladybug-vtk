from ladybug_geometry.geometry3d import Point3D
from ladybug_vtk.to_vtk import to_circle, to_text


def test_to_vtk_circle():
    """Test to_vtk_circle function."""
    polydata = to_circle(Point3D(0, 0, 0), 5, 10)
    assert polydata.GetNumberOfPoints() == 10
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1


def test_to_text():
    """Test to_text function."""
    text_polydata = to_text('Hello World!', Point3D(5, 5, 5))
    assert round(text_polydata.GetBounds()[0], 2) == 5.54
    assert round(text_polydata.GetBounds()[2], 2) == 4.82
    assert round(text_polydata.GetBounds()[4], 2) == 5.0
