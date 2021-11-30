"""Functions to create VTK Polydata from Ladybug Objects."""
import vtk
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.polyface import Polyface3D
from typing import List
from ladybug_geometry.geometry3d import Point3D, Polyline3D, Arc3D, LineSegment3D,\
    Mesh3D, Polyface3D, Cone, Cylinder, Sphere
from .polydata import PolyData


def from_point(point: Point3D) -> PolyData:
    """Create Polydata from a ladybug Point."""
    vtk_point = vtk.vtkPoints()
    vtk_vertice = vtk.vtkCellArray()

    vtk_point.InsertNextPoint(tuple(point))
    vtk_vertice.InsertNextCell(1, [1])

    polydata = PolyData()
    polydata.SetPoints(vtk_point)
    polydata.SetVerts(vtk_vertice)
    polydata.Modified()

    return polydata


def _polyline_from_points(points: List[Point3D]) -> PolyData:
    """Create Polydata from a list of Ladybug Point3D objects."""

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


def from_points(points: List[Point3D], join: bool = False) -> PolyData:
    """Create Polydata from a list of Ladybug Point3D objects.

    Args:
        points: A list of Ladybug Point3D objects.
        join: Boolean to indicate whether the points should be joined into a polyline.

    Returns:
        Polydata containing all points or a polyline.
    """
    if join:
        return _polyline_from_points(points)

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


def from_line(line: LineSegment3D) -> PolyData:
    """Create Polydata from a Ladybug LineSegment3D object."""
    return from_points(line.vertices, join=True)


def from_polyline(polyline: Polyline3D) -> PolyData:
    """Create Polydata from a Ladybug Polyline3D object."""
    return from_points(polyline.vertices, join=True)


def from_arc(arc: Arc3D, divisions: int = 50,
             interpolated: bool = True) -> PolyData:
    """Create Polydata from a Ladybug Arc3D object.

    Args:
        arc: A Ladybug Arc3D object.
        divisions: The number of segments into which the arc will be divided.
            Defaults to 50.
        interpolated: Boolean to note whether the polyline should be interpolated
            between the input vertices when it is translated to other interfaces.
            This property has no effect on the geometric calculations performed by
            this library and is only present in order to assist with
            display/translation. Defaults to True.

    Returns:
        Polydata containing a Polyline representation of an arc.
    """
    return from_polyline(arc.to_polyline(divisions, interpolated))


def from_mesh(mesh: Mesh3D) -> PolyData:
    """Create Polydata from a Ladybug mesh."""
    points = vtk.vtkPoints()
    polygon = vtk.vtkPolygon()
    cells = vtk.vtkCellArray()

    for ver in mesh.vertices:
        points.InsertNextPoint(*ver)

    for face in mesh.faces:
        polygon.GetPointIds().SetNumberOfIds(len(face))
        for count, i in enumerate(face):
            polygon.GetPointIds().SetId(count, i)
        cells.InsertNextCell(polygon)

    polydata = PolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(cells)

    return polydata


def from_face(face: Face3D) -> PolyData:
    """Create Polydata from a Ladybug face."""

    if face.has_holes or not face.is_convex:
        return from_mesh(face.triangulated_mesh3d)

    points = vtk.vtkPoints()
    polygon = vtk.vtkPolygon()
    cells = vtk.vtkCellArray()

    vertices_count = len(face.vertices)
    polygon.GetPointIds().SetNumberOfIds(vertices_count)
    for ver in face.vertices:
        points.InsertNextPoint(*ver)
    for count in range(vertices_count):
        polygon.GetPointIds().SetId(count, count)
    cells.InsertNextCell(polygon)

    polydata = PolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(cells)

    return polydata


def from_polyface(polyface: Polyface3D) -> List[PolyData]:
    """Create Polydata from a Ladybug Polyface."""
    return [from_face(face) for face in polyface.faces]


def from_cone(cone: Cone, resolution: int = 2, cap: bool = True) -> PolyData:
    """Create Polydata from a Ladybug Cone.

    Args:
        cone: A Ladybug Cone object.
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

    cone_source = vtk.vtkConeSource()
    cone_source.SetResolution(resolution)
    cone_source.SetRadius(cone.radius)
    cone_source.SetHeight(cone.height)
    cone_source.SetDirection(tuple(cone.axis))
    center = cone.vertex.move(cone.axis.reverse())
    cone_source.SetCenter(tuple(center))
    if not cap:
        cone_source.CappingOff()
    cone_source.Update()

    polydata = PolyData()
    polydata.ShallowCopy(cone_source.GetOutput())

    return polydata


def from_sphere(sphere: Sphere, resolution: int = 25) -> PolyData:
    """Create Polydata from a Ladybug Sphere."""

    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetCenter(tuple(sphere.center))
    sphere_source.SetRadius(sphere.radius)
    sphere_source.SetPhiResolution(resolution)
    sphere_source.SetThetaResolution(resolution)
    sphere_source.Update()

    polydata = PolyData()
    polydata.ShallowCopy(sphere_source.GetOutput())

    return polydata


def from_cylinder(cylinder: Cylinder, resolution: int = 25, cap: bool = True) -> PolyData:
    """Create Polydata from a Ladybug Cylinder."""

    cylinder_source = vtk.vtkCylinderSource()
    cylinder_source.SetCenter(tuple(cylinder.center))
    cylinder_source.SetRadius(cylinder.radius)
    cylinder_source.SetHeight(cylinder.height)
    cylinder_source.SetResolution(resolution)
    if not cap:
        cylinder_source.CappingOff()
    cylinder_source.Update()

    polydata = PolyData()
    polydata.ShallowCopy(cylinder_source.GetOutput())

    return polydata
