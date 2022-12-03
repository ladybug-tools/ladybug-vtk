"""testing functions in from_geometry module."""

from ladybug_geometry.geometry2d import Point2D, LineSegment2D
from ladybug_geometry.geometry3d import Point3D, Polyline3D, Arc3D, Vector3D, Mesh3D,\
    Face3D, Plane, LineSegment3D, Polyface3D, Cone, Sphere, Cylinder
from ladybug_vtk.from_geometry import from_point2d, from_points2d, from_line2d, \
    from_point3d, from_points3d, from_line3d, from_polyline3d, from_arc3d, from_mesh3d,\
    from_face3d, from_polyface3d, from_cone, from_sphere, from_cylinder, to_circle,\
    from_text


def test_from_point2d():
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


def test_from_point3d():
    """Test point to Polydata conversion."""
    point = Point3D(5, 6, 7)
    polydata = from_point3d(point)
    assert polydata.GetNumberOfPoints() == 1
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetBounds() == (5.0, 5.0, 6.0, 6.0, 7.0, 7.0)


def test_from_points3d():
    """Test a list of points to Polydata conversion."""
    points = [Point3D(5, 6, 7), Point3D(8, 9, 10)]
    polydata = from_points3d(points)
    assert polydata.GetNumberOfPoints() == 2
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetBounds() == (5.0, 8.0, 6.0, 9.0, 7.0, 10.0)


def test_polyline_from_points3d():
    """Test a list of points to Polydata conversion as a joined polyline."""
    points = [Point3D(5, 6, 7), Point3D(8, 9, 10), Point3D(11, 12, 13)]
    polydata = from_points3d(points, join=True)
    assert polydata.GetNumberOfPoints() == 3
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
    assert polydata.GetBounds() == (5.0, 11.0, 6.0, 12.0, 7.0, 13.0)


def test_from_line3d():
    """Test line to Polydata conversion."""
    line = LineSegment3D.from_end_points(Point3D(0, 0, 2), Point3D(2, 0, 2))
    polydata = from_line3d(line)
    assert polydata.GetNumberOfPoints() == 2
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
    assert polydata.GetBounds() == (0.0, 2.0, 0.0, 0.0, 2.0, 2.0)


def test_from_polyline3d():
    """Test polyline to Polydata conversion."""
    polyline = Polyline3D([Point3D(5, 6, 7), Point3D(8, 9, 10), Point3D(11, 12, 13)])
    polydata = from_polyline3d(polyline)
    assert polydata.GetNumberOfPoints() == 3
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
    assert polydata.GetBounds() == (5.0, 11.0, 6.0, 12.0, 7.0, 13.0)


def test_from_arc3d():
    """Test arc to Polydata conversion."""
    arc = Arc3D.from_start_mid_end(
        Point3D(0, 0, 0), Point3D(5, 0, 20), Point3D(10, 0, 0))
    polydata = from_arc3d(arc, 10)
    assert polydata.GetNumberOfPoints() == 31
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1


def test_from_mesh3d():
    """Test mesh to Polydata conversion."""
    pts = (Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2))
    mesh = Mesh3D(pts, [(0, 1, 2, 3)])
    polydata = from_mesh3d(mesh)
    assert polydata.GetNumberOfPoints() == 4
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfPolys() == 1
    assert polydata.GetBounds() == (0.0, 2.0, 0.0, 2.0, 2.0, 2.0)


def test_from_face3d():
    """Test face to Polydata conversion."""
    pts = (Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2))
    plane = Plane(Vector3D(0, 0, 1), Point3D(0, 0, 2))
    face = Face3D(pts, plane)
    polydata = from_face3d(face)
    assert polydata.GetNumberOfPoints() == 4
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfPolys() == 1
    assert polydata.GetBounds() == (0.0, 2.0, 0.0, 2.0, 2.0, 2.0)


def test_from_polyface3d():
    """Test polyface to Polydata conversion."""
    pts = [Point3D(0, 0, 0), Point3D(0, 2, 0), Point3D(2, 2, 0), Point3D(2, 0, 0),
           Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2)]
    face_indices = [[(0, 1, 2, 3)], [(0, 4, 5, 1)], [(0, 3, 7, 4)],
                    [(2, 1, 5, 6)], [(2, 3, 7, 6)], [(4, 5, 6, 7)]]
    polyface = Polyface3D(pts, face_indices)
    polydata = from_polyface3d(polyface)
    assert polydata.GetNumberOfPoints() == 8
    assert polydata.GetNumberOfCells() == 6
    assert polydata.GetNumberOfPolys() == 6
    assert polydata.GetBounds() == (0.0, 2.0, 0.0, 2.0, 0.0, 2.0)


def test_from_cone():
    """Test cone to Polydata conversion."""
    vertex = Point3D(2, 0, 2)
    axis = Vector3D(0, 2, 2)
    angle = 0.7
    cone = Cone(vertex, axis, angle)
    polydata = from_cone(cone, resolution=3)
    assert polydata.GetNumberOfPoints() == 4
    assert polydata.GetNumberOfCells() == 4
    assert polydata.GetNumberOfPolys() == 4
    polydata = from_cone(cone, resolution=3, cap=False)
    assert polydata.GetNumberOfPolys() == 3


def test_from_sphere():
    """Test sphere to Polydata conversion."""
    point = Point3D(2, 0, 2)
    radius = 3
    sphere = Sphere(point, radius)
    polydata = from_sphere(sphere, resolution=25)
    assert polydata.GetNumberOfPoints() == 577
    assert polydata.GetNumberOfCells() == 1150
    assert polydata.GetNumberOfPolys() == 1150


def test_from_cylinder():
    """Test cylinder to Polydata conversion."""
    center = Point3D(2, 0, 2)
    axis = Vector3D(0, 2, 2)
    radius = 0.7
    cylinder = Cylinder(center, axis, radius)
    polydata = from_cylinder(cylinder, resolution=25)
    assert polydata.GetNumberOfPoints() == 100
    assert polydata.GetNumberOfCells() == 27
    assert polydata.GetNumberOfPolys() == 27
    polydata = from_cylinder(cylinder, cap=False)
    assert polydata.GetNumberOfPolys() == 50


def test_to_vtk_circle():
    """Test to_vtk_circle function."""
    polydata = to_circle(Point3D(0, 0, 0), 5, 10)
    assert polydata.GetNumberOfPoints() == 10
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1


def test_to_text():
    """Test from_text function."""
    text_polydata = from_text('Hello World!', plane=Point3D(5, 5, 5))
    assert round(text_polydata.GetBounds()[0], 2) == 5.0
    assert round(text_polydata.GetBounds()[2], 2) == 5.0
    assert round(text_polydata.GetBounds()[4], 2) == 5.0
