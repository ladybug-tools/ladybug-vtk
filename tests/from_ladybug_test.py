"""Testing to_vtk functions."""

from ladybug_geometry.geometry3d import Point3D, Polyline3D, Arc3D, Vector3D, Mesh3D,\
    Face3D, Plane, LineSegment3D, Polyface3D, Cone, Sphere, Cylinder
from ladybug_vtk.from_ladybug import from_point, from_points, from_line, from_polyline,\
    from_arc, from_mesh, from_face, from_polyface, from_cone, from_sphere, from_cylinder


def test_from_point():
    """Test point to Polydata conversion."""
    point = Point3D(5, 6, 7)
    polydata = from_point(point)
    assert polydata.GetNumberOfPoints() == 1
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetBounds() == (5.0, 5.0, 6.0, 6.0, 7.0, 7.0)


def test_from_points():
    """Test a list of points to Polydata conversion."""
    points = [Point3D(5, 6, 7), Point3D(8, 9, 10)]
    polydata = from_points(points)
    assert polydata.GetNumberOfPoints() == 2
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetBounds() == (5.0, 8.0, 6.0, 9.0, 7.0, 10.0)


def test_polyline_from_points():
    """Test a list of points to Polydata conversion as a joined polyline."""
    points = [Point3D(5, 6, 7), Point3D(8, 9, 10), Point3D(11, 12, 13)]
    polydata = from_points(points, join=True)
    assert polydata.GetNumberOfPoints() == 3
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
    assert polydata.GetBounds() == (5.0, 11.0, 6.0, 12.0, 7.0, 13.0)


def test_from_line():
    """Test line to Polydata conversion."""
    line = LineSegment3D.from_end_points(Point3D(0, 0, 2), Point3D(2, 0, 2))
    polydata = from_line(line)
    assert polydata.GetNumberOfPoints() == 2
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
    assert polydata.GetBounds() == (0.0, 2.0, 0.0, 0.0, 2.0, 2.0)


def test_from_polyline():
    """Test polyline to Polydata conversion."""
    polyline = Polyline3D([Point3D(5, 6, 7), Point3D(8, 9, 10), Point3D(11, 12, 13)])
    polydata = from_polyline(polyline)
    assert polydata.GetNumberOfPoints() == 3
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1
    assert polydata.GetBounds() == (5.0, 11.0, 6.0, 12.0, 7.0, 13.0)


def test_from_arc():
    """Test arc to Polydata conversion."""
    arc = Arc3D.from_start_mid_end(
        Point3D(0, 0, 0), Point3D(5, 0, 20), Point3D(10, 0, 0))
    polydata = from_arc(arc, 10)
    assert polydata.GetNumberOfPoints() == 11
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfLines() == 1


def test_from_mesh():
    """Test mesh to Polydata conversion."""
    pts = (Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2))
    mesh = Mesh3D(pts, [(0, 1, 2, 3)])
    polydata = from_mesh(mesh)
    assert polydata.GetNumberOfPoints() == 4
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfPolys() == 1
    assert polydata.GetBounds() == (0.0, 2.0, 0.0, 2.0, 2.0, 2.0)


def test_from_face():
    """Test face to Polydata conversion."""
    pts = (Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2))
    plane = Plane(Vector3D(0, 0, 1), Point3D(0, 0, 2))
    face = Face3D(pts, plane)
    polydata = from_face(face)
    assert polydata.GetNumberOfPoints() == 4
    assert polydata.GetNumberOfCells() == 1
    assert polydata.GetNumberOfPolys() == 1
    assert polydata.GetBounds() == (0.0, 2.0, 0.0, 2.0, 2.0, 2.0)


def test_from_polyface():
    """Test polyface to Polydata conversion."""
    pts = [Point3D(0, 0, 0), Point3D(0, 2, 0), Point3D(2, 2, 0), Point3D(2, 0, 0),
           Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2)]
    face_indices = [[(0, 1, 2, 3)], [(0, 4, 5, 1)], [(0, 3, 7, 4)],
                    [(2, 1, 5, 6)], [(2, 3, 7, 6)], [(4, 5, 6, 7)]]
    polyface = Polyface3D(pts, face_indices)
    polydata = from_polyface(polyface)
    assert polydata[0].GetNumberOfPoints() == 4
    assert polydata[0].GetNumberOfCells() == 1
    assert polydata[0].GetNumberOfPolys() == 1
    assert polydata[0].GetBounds() == (0.0, 2.0, 0.0, 2.0, 0.0, 0.0)


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
    polydata = from_sphere(sphere)
    assert polydata.GetNumberOfPoints() == 577
    assert polydata.GetNumberOfCells() == 1150
    assert polydata.GetNumberOfPolys() == 1150


def test_from_cylinder():
    """Test cylinder to Polydata conversion."""
    center = Point3D(2, 0, 2)
    axis = Vector3D(0, 2, 2)
    radius = 0.7
    cylinder = Cylinder(center, axis, radius)
    polydata = from_cylinder(cylinder)
    assert polydata.GetNumberOfPoints() == 100
    assert polydata.GetNumberOfCells() == 27
    assert polydata.GetNumberOfPolys() == 27
    polydata = from_cylinder(cylinder, cap=False)
    assert polydata.GetNumberOfPolys() == 25
