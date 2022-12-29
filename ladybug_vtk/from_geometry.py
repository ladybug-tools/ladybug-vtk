"""Functions to translate ladybug geometry objects into VTK polydata objects."""


import vtk
import math
from typing import List, Union
from ladybug_geometry.geometry2d import Point2D, LineSegment2D, Polyline2D, \
    Polygon2D, Mesh2D
from ladybug_geometry.geometry3d import Point3D, Polyline3D, Arc3D, LineSegment3D,\
    Mesh3D, Polyface3D, Cone, Cylinder, Sphere, Face3D, Plane, Vector3D
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
    """Create Polydata from a Ladybug LineSegment2D object.

    Args:
        line: A Ladybug LineSegment2D object.

    Returns:
        Polydata containing a line.
    """
    return from_points2d(line.vertices, join=True)


def from_polyline2d(polyline: Polyline2D) -> PolyData:
    """Create Polydata from a Ladybug Polyline2D object.

    Args:
        polyline: A Ladybug Polyline2D object.

    Returns:
        Polydata containing a polyline.
    """
    return from_points2d(polyline.vertices, join=True)


def from_polygon2d(polygon: Polygon2D) -> PolyData:
    """Create Polydata from a Ladybug Polygon2D object.

    Args:
        polygon: A Ladybug Polygon2D object.

    Returns:
        Polydata containing a polygon.
    """
    verts = polygon.vertices + (polygon[0],)
    return from_points2d(verts, join=True)


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


def from_arc3d(arc3d: Arc3D, resolution: int = 3) -> PolyData:
    """Create Polydata from a Ladybug Arc3D object.

    Args:
        arc3d: A Ladybug Arc3D object.
        resolution: The number of degrees per subdivision. The default is 3 that creates
            120 segments for an full circle.

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
    vtk_resolution = max(int(math.degrees(arc3d.angle) / resolution), 2)
    arc.SetResolution(vtk_resolution)
    arc.Update()

    polydata = PolyData()
    polydata.ShallowCopy(arc.GetOutput())

    # delete the array named 'Texture Coordinates'
    # that's generated automatically for some reason
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


def from_mesh2d(mesh: Mesh2D) -> PolyData:
    """Create Polydata from a Ladybug mesh 2D.

    Args:
        mesh: A Ladybug Mesh2D object.

    Returns:
        Polydata containing face and points of a mesh.
    """
    points = vtk.vtkPoints()
    polygon = vtk.vtkPolygon()
    cells = vtk.vtkCellArray()

    for ver in mesh.vertices:
        points.InsertNextPoint(ver[0], ver[1], 0)

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


def from_polyface3d(polyface: Polyface3D) -> PolyData:
    """Create Polydata from a Ladybug Polyface.

    Args:
        polyface: A Ladybug Polyface3D object.

    Returns:
        A Polydata representing the PolyFace3D.

    """
    points = vtk.vtkPoints()
    polygon = vtk.vtkPolygon()
    cells = vtk.vtkCellArray()

    for ver in polyface.vertices:
        points.InsertNextPoint(*ver)

    # starting number to count for the new vertices that are being added for
    # triangulated meshes
    addition = len(polyface.vertices)
    for face, face_geo in zip(polyface.face_indices, polyface.faces):
        if face_geo.has_holes or not face_geo.is_convex:
            meshed_face = face_geo.triangulated_mesh3d
            for ver in meshed_face.vertices:
                points.InsertNextPoint(*ver)
            for face in meshed_face.faces:
                polygon.GetPointIds().SetNumberOfIds(len(face))
                for count, i in enumerate(face):
                    polygon.GetPointIds().SetId(count, i + addition)
                cells.InsertNextCell(polygon)
            addition += len(meshed_face.vertices)
        else:
            face = face[0]
            polygon.GetPointIds().SetNumberOfIds(len(face))
            for count, i in enumerate(face):
                polygon.GetPointIds().SetId(count, i)
            cells.InsertNextCell(polygon)

    polydata = PolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(cells)

    return polydata


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


def from_sphere(sphere: Sphere, resolution: int = 50) -> PolyData:
    """Create Polydata from a Ladybug Sphere.

    Args:
        sphere: A Ladybug Sphere object.
        resolution: The number of segments into which the sphere will be divided.
            Defaults to 50.

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


def from_cylinder(
    cylinder: Cylinder, resolution: int = 50, cap: bool = True
) -> PolyData:
    """Create Polydata from a Ladybug Cylinder.

    Args:
        cylinder: A Ladybug Cylinder object.
        resolution: The number of segments into which the cylinder will be divided.
            Defaults to 50.
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


def from_text(
    text: str, *, plane: Union[Point3D, Point2D, Plane], height: float = 2,
    horizontal_alignment: int = 0, vertical_alignment: int = 2
) -> PolyData:
    """Create a VTK text object from a text string and a ladybug Point3D.

    Args:
        text: A text string.
        plane: A ladybug Plane, Point3D or Point2D object to locate and orient the text
            in the VTK scene.
        height: A number for the height of the text in the scene. Defaults is set to 2.
        horizontal_alignment: An optional integer to specify the horizontal alignment
            of the text. Choose from: (0 = Left, 1 = Center, 2 = Right).
        vertical_alignment: An optional integer to specify the vertical alignment of
            the text. Choose from: (0 = Top, 1 = Middle, 2 = Bottom)

    Returns:
        A Polydata object containing the text.
    """

    def _apply_transformation(
        source: vtk.vtkVectorText,
        plane: Plane,
        height: float,
        offset_multiline: bool = False
    ) -> vtk.vtkTransformPolyDataFilter:
        transform = vtk.vtkTransform()
        transform.PostMultiply()

        # VTK generates the texts initially on a plane at the origin
        original_plane = Plane(
            n=Vector3D(0, 0, 1), o=Point3D(0, 0, 0), x=Vector3D(1, 0, 0)
        )
        rotated_plane = original_plane
        if plane.n != original_plane.n:
            # match the normal of the two plane
            angle_rad = original_plane.n.angle(plane.n)
            angle = math.degrees(angle_rad)
            if angle > 0.1:
                vector = original_plane.n.cross(plane.n)
                if vector == Vector3D(0, 0, 0):
                    vector = Vector3D(1, 0, 0)

                transform.RotateWXYZ(angle, vector.x, vector.y, vector.z)
                rotated_plane = original_plane.rotate(vector, angle_rad, original_plane.o)

        # now match the x axis
        angle_rad = rotated_plane.x.angle(plane.x)
        angle = math.degrees(angle_rad)
        if angle > 0.1:
            vector = rotated_plane.n
            # this is an edge case that I couldn't really figure out why is happening
            # we should try to find a more generic solution. Use the simple_box.vsf
            # sample file for testing
            if rotated_plane.x.angle(Vector3D(0, 0, 1)) < 0.01 and \
                    plane.x.angle(Vector3D(0, -1, 0)) < 0.01 and \
                    vector.angle(Vector3D(-1, 0, 0)) < 0.01:
                vector = Vector3D(1, 0, 0)
            transform.RotateWXYZ(angle, vector.x, vector.y, vector.z)
            rotated_plane = rotated_plane.rotate(vector, angle_rad, original_plane.o)

        transform.Scale(height, height, height)

        # add a transformation to move the text to the new plane origin
        almost_horizontal = math.degrees(rotated_plane.x.angle(Vector3D(1, 0, 0))) < 5
        if offset_multiline:
            if almost_horizontal and vertical_alignment == 0:
                # horizontal text with top adjustment. No need to move
                line_count = 0
            else:
                line_count = len(text.split('\n')) - 1

            move_vector = rotated_plane.y * (line_count * 1.5 * height)
            move_vector = move_vector.reverse()
            moved_point = plane.o.move(move_vector)
            transform.Translate(*moved_point)
        else:
            transform.Translate(*plane.o)

        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetInputConnection(source.GetOutputPort())
        transformFilter.SetTransform(transform)
        transformFilter.Update()
        tf = transformFilter.GetOutput()
        return tf

    if isinstance(plane, Point3D):
        plane = Plane(o=plane)
    elif isinstance(plane, Point2D):
        plane = Plane(o=Point3D(plane.x, plane.y, 0))

    assert isinstance(plane, Plane), 'The plane for text must be from a Ladybug Plane.'
    source = vtk.vtkVectorText()
    source.SetText(text)
    # initial transform to project the text from origin to the target plane
    transform_filter = _apply_transformation(source, plane, height)

    # this vector is the initial difference between the left lower corner og the
    # generated text and the desired text insertion point. In theory, it should be 0
    # but VTK doesn't generate the text at the exact 0, 0, 0 - the difference is usually
    # very small
    bounds = list(transform_filter.GetBounds())
    left_lower_corner = Point3D(bounds[0], bounds[2], bounds[4])
    offset_vector = plane.o - left_lower_corner

    # make adjustments for text justification
    if not (horizontal_alignment == 0 and vertical_alignment == 2):
        # find the size of the text
        bounds = list(transform_filter.GetBounds())
        bottom_left = Point3D(bounds[0], bounds[2], bounds[4])
        top_right = Point3D(bounds[1], bounds[3], bounds[5])
        bottom_left_2d = plane.xyz_to_xy(bottom_left)
        top_right_2d = plane.xyz_to_xy(top_right)

        x_dist = top_right_2d.x - bottom_left_2d.x
        y_dist = top_right_2d.y - bottom_left_2d.y

        if horizontal_alignment == 0:  # left alignment
            x_dist = 0
        elif horizontal_alignment == 1:  # center alignment
            x_dist = x_dist / 2

        if vertical_alignment == 2:  # bottom alignment
            y_dist = 0
        elif vertical_alignment == 1:  # center alignment
            y_dist = y_dist / 2

        x_vector = plane.x * -1 * x_dist
        y_vector = plane.y * -1 * y_dist
        move_vector = x_vector + y_vector

        plane = plane.move(moving_vec=move_vector)

    plane = plane.move(offset_vector)

    transform_filter = _apply_transformation(
        source, plane, height, offset_multiline=True
    )

    polydata = PolyData()
    polydata.ShallowCopy(transform_filter)
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
