"""Testing to_vtk functions."""

from ladybug_geometry.geometry2d import Point2D, Polyline2D, LineSegment2D
from ladybug_vtk.from_ladybug2d import from_point2d, from_points2d, from_line2d


def test_from_point3d():
    """Test point to Polydata conversion."""
    point = Point2D(5, 6)
    polydata = from_point2d(point)
    assert polydata.GetNumberOfPoints() == 1
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetBounds() == (5.0, 5.0, 6.0, 6.0, 0.0, 0.0)


def test_from_points2d():
    """Test a list of points to Polydata conversion."""
    points = [Point2D(5, 6), Point2D(8, 9)]
    polydata = from_points2d(points)
    assert polydata.GetNumberOfPoints() == 2
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetBounds() == (5.0, 8.0, 6.0, 9.0, 0.0, 0.0)


def test_polyline_from_points2d():
    """Test a list of points to Polydata conversion as a joined polyline."""
    points = [Point2D(5, 6), Point2D(8, 9), Point2D(11, 12)]
    polydata = from_points2d(points, join=True)
    assert polydata.GetNumberOfPoints() == 3
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
    assert polydata.GetBounds() == (5.0, 11.0, 6.0, 12.0, 0.0, 0.0)


def test_from_line2d():
    """Test line to Polydata conversion."""
    line = LineSegment2D.from_end_points(Point2D(0, 0), Point2D(2, 0))
    polydata = from_line2d(line)
    assert polydata.GetNumberOfPoints() == 2
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
    assert polydata.GetBounds() == (0.0, 2.0, 0.0, 0.0, 0.0, 0.0)
