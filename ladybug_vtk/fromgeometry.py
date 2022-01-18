"""Functions to translate ladybug geometry objects into VTK polydata objects."""


import vtk
import math
from typing import List, Union
from ladybug_geometry.geometry2d import Point2D, LineSegment2D, Polyline2D
from ladybug_geometry.geometry3d import Point3D, Polyline3D, Arc3D, LineSegment3D,\
    Mesh3D, Polyface3D, Cone, Cylinder, Sphere, Face3D
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


def from_polyline2d(polyline: Polyline2D) -> PolyData:
    """Create Polydata from a Ladybug Polyline3D object.

    Args:
        polyline: A Ladybug Polyline3D object.

    Returns:
        Polydata containing a polyline.
    """
    return from_points2d(polyline.vertices, join=True)


def from_point3d(point: Point3D) -> PolyData:
    """Create Polydata from a Ladybug Point3D object.

    Args:
        point: A ladybug Point object.

    Returns:
        Polydata containing a single point.
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


def _polyline_from_points3d(points: List[Point3D]) -> PolyData:
    """Create Polydata from a list of Ladybug Point3D objects.

    Args:
        points: A list of Ladybug Point3D objects.

    Returns:
        Polydata containing a polyline created by joining the points.
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


def from_points3d(points: List[Point3D], join: bool = False) -> PolyData:
    """Create Polydata from a list of Ladybug Point3D objects.

    Args:
        points: A list of Ladybug Point3D objects.
        join: Boolean to indicate whether the points should be joined into a polyline.

    Returns:
        Polydata containing all points or a polyline.
    """
    if join:
        return _polyline_from_points3d(points)

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


def from_line3d(line: LineSegment3D) -> PolyData:
    """Create Polydata from a Ladybug LineSegment3D object.

    Args:
        line: A Ladybug LineSegment3D object.

    Returns:
        Polydata containing a line.
    """
    return from_points3d(line.vertices, join=True)


def from_polyline3d(polyline: Polyline3D) -> PolyData:
    """Create Polydata from a Ladybug Polyline3D object.

    Args:
        polyline: A Ladybug Polyline3D object.

    Returns:
        Polydata containing a polyline.
    """
    return from_points3d(polyline.vertices, join=True)


def from_arc3d(arc3d: Arc3D, resolution: int = 25) -> PolyData:
    """Create Polydata from a Ladybug Arc3D object.

    Args:
        arc3d: A Ladybug Arc3D object.
        resolution: The number of segments into which the arc will be divided.
            Defaults to 25.

    Returns:
        Polydata containing an arc.
    """
    arc = vtk.vtkArcSource()
    arc.UseNormalAndAngleOn()
    arc.SetCenter(arc3d.c.x, arc3d.c.y, arc3d.c.z)
    polar_vector = LineSegment3D.from_end_points(arc3d.c, arc3d.p1).v
    arc.SetPolarVector(round(polar_vector.x, 2), round(
        polar_vector.y, 2), round(polar_vector.z, 2))
    normal = arc3d.plane.n
    arc.SetNormal(round(normal.x, 2), round(normal.y, 2), round(normal.z, 2))
    arc.SetAngle(math.degrees(arc3d.angle))
    arc.SetResolution(resolution)
    arc.Update()

    polydata = PolyData()
    polydata.ShallowCopy(arc.GetOutput())

    # delete the array named 'Texture Coordinates' that's generated automatically for some reason
    polydata.GetPointData().RemoveArray('Texture Coordinates')
    return polydata


def from_mesh3d(mesh: Mesh3D) -> PolyData:
    """Create Polydata from a Ladybug mesh.

    Args:
        mesh: A Ladybug Mesh3D object.

    Returns:
        Polydata containing face and points of a mesh.
    """
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


def from_face3d(face: Face3D) -> PolyData:
    """Create Polydata from a Ladybug face.

    Args:
        face: A Ladybug Face3D object.

    Returns:
        Polydata containing face and points of a face.
    """

    if face.has_holes or not face.is_convex:
        return from_mesh3d(face.triangulated_mesh3d)

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


def from_polyface3d(polyface: Polyface3D) -> List[PolyData]:
    """Create Polydata from a Ladybug Polyface.

    Args:
        polyface: A Ladybug Polyface3D object.

    Returns:
        A list of Polydata. Each polydata contains a face and points of a face of Polyface.
    """
    return [from_face3d(face) for face in polyface.faces]


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
    """Create Polydata from a Ladybug Sphere.

    Args:
        sphere: A Ladybug Sphere object.
        resolution: The number of segments into which the sphere will be divided.
            Defaults to 25.

    Returns:
        Polydata containing a sphere.
    """

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
    """Create Polydata from a Ladybug Cylinder.

    Args:
        cylinder: A Ladybug Cylinder object.
        resolution: The number of segments into which the cylinder will be divided.
            Defaults to 25.
        cap: Boolean to indicate whether the cylinder should capped or not.
            Default to True.

    Returns:
        Polydata containing a cylinder.
    """

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


def to_text(text: str, point: Union[Point3D, Point2D], scale: float = 2) -> PolyData:
    """Create a VTK text object from a text string and a ladybug Point3D.

    Args:
        text: A text string.
        point: A ladybug Point3D or Point2D object. This is the location in 3D 
            space of the text.
        scale: The scale of the text. Defaults to 2.

    Returns:
        A Polydata object containing the text.
    """
    source = vtk.vtkVectorText()
    source.SetText(text)

    translation = vtk.vtkTransform()
    if isinstance(point, Point3D):
        translation.Translate(point.x, point.y, point.z)
    else:
        translation.Translate(point.x, point.y, 0)
    translation.Scale(scale, scale, scale)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(source.GetOutputPort())
    transformFilter.SetTransform(translation)
    transformFilter.Update()

    polydata = PolyData()
    polydata.ShallowCopy(transformFilter.GetOutput())
    return polydata
