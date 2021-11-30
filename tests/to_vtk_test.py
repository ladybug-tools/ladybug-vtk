from ladybug_geometry.geometry3d import Point3D
from ladybug_vtk.to_vtk import to_circle


def test_to_vtk_circle():
    """Test to_vtk_circle function."""
    polydata = to_circle(Point3D(0, 0, 0), 5, 10)
    assert polydata.GetNumberOfPoints() == 10
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
