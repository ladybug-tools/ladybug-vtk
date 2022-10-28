"""Extend Ladybug Core functionalities."""

from pathlib import Path

from typing import List
from ladybug.color import Color
from ladybug_geometry.geometry3d import Point3D
from ladybug_geometry.geometry2d import Vector2D, Point2D
from ladybug.sunpath import Sunpath
from ladybug.compass import Compass
from ladybug.datacollection import HourlyContinuousCollection

from .from_geometry import from_points3d, to_circle, from_text, from_points2d
from .display_polydata import DisplayPolyData
from .visualization_set import VisualizationSet


def sunpath_to_vtkjs(
    self, output_folder: str = '.', file_name: str = 'sunpath', radius: int = 100,
    data: List[HourlyContinuousCollection] = None, sun_color: Color = Color(252, 177, 3),
        make_2d: bool = False) -> Path:
    """Export sunpath as a vtkjs file.

    Args:
        output_folder: Path to the target folder to write the vtkjs file. Defaults to
            current working directory.
        file_name: Output file name. Defaults to Sunpath.
        radius: Radius of the sunpath. Defaults to 100.
        data: A list of Ladybug continuous hourly collection objects. Defaults to None.
        sun_color: A Ladybug Color object to color the suns.
            Defaults to Color(235, 33, 38).
        make_2d: Boolean to indicate whether to make the sunpath 2D. Defaults to False.

    Returns:
        A pathlib Path object to the vtkjs file.
    """
    datasets = []

    # daily analemmas
    data = data or []
    origin = Point3D()

    if not make_2d:
        polylines = self.hourly_analemma_polyline3d(radius=radius)
        sp_polydata = [pl.to_polydata() for pl in polylines]
    else:
        polylines = self.hourly_analemma_polyline2d(radius=radius)
        sp_polydata = [pl.to_polydata() for pl in polylines]
    sp_dataset = DisplayPolyData(
        name='Sun path::Hourly Analemmas', identifier='hourly_analemmas',
        polydata=sp_polydata, color=Color()
    )
    datasets.append(sp_dataset)

    # monthly arcs
    if not make_2d:
        arcs = self.monthly_day_arc3d(radius=radius)
        monthly_polydata = [arc.to_polydata(resolution=100) for arc in arcs]
    else:
        polylines = self.monthly_day_polyline2d(radius=radius)
        monthly_polydata = [polyline.to_polydata() for polyline in polylines]
    arc_dataset = DisplayPolyData(
        name='Sun path::Monthly Arcs', identifier='monthly_arcs',
        polydata=monthly_polydata, color=Color()
    )
    datasets.append(arc_dataset)

    # compass circles
    offset_1 = (radius * 1.5) / 100
    offset_2 = (radius * 4.5) / 100
    rads = [radius, radius+offset_1, radius+offset_2]
    base_polydata = [to_circle(origin, radius) for radius in rads]

    # compass ticks
    compass = Compass(radius=radius, north_angle=self.north_angle)
    ticks_major = compass.ticks_from_angles(
        angles=compass.MAJOR_AZIMUTHS, factor=0.55)
    ticks_minor = compass.ticks_from_angles(angles=compass.MINOR_AZIMUTHS)
    ticks_polydata = [tick.to_polydata() for tick in ticks_major+ticks_minor]
    base_polydata.extend(ticks_polydata)
    base_dataset = DisplayPolyData(
        name='Sun path::Compass', identifier='base_circle',
        polydata=base_polydata, color=Color()
    )
    datasets.append(base_dataset)

    # Since vtkVectorText starts from left bottom we need to move the labels to the left
    # and down by a certain amount.
    moving_factor = (radius*3) / 100
    left_vector = Vector2D(-1, 0) * moving_factor
    down_vector = Vector2D(0, -1) * moving_factor

    # compass minor labels
    minor_scale = (radius * 2) / 100
    minor_text_polydata = [from_text(text, plane=compass.minor_azimuth_points[count].
                                   move(left_vector).move(down_vector), height=minor_scale)
                           for count, text in enumerate(compass.MINOR_TEXT)]
    minor_label_dataset = DisplayPolyData(
        name='Sun path::Minor Labels', identifier='minor_labels',
        polydata=minor_text_polydata, color=Color()
    )
    datasets.append(minor_label_dataset)

    # compass major labels
    major_scale = (radius * 5) / 100
    major_text_polydata = [from_text(text, plane=compass.major_azimuth_points[count].
                                   move(left_vector).move(down_vector), height=major_scale) for
                           count, text in enumerate(compass.MAJOR_TEXT)]
    major_label_dataset = DisplayPolyData(
        name='Sun path::Major Labels', identifier='major_labels',
        polydata=major_text_polydata, color=Color()
    )
    datasets.append(major_label_dataset)

    # add suns
    day = self.hourly_analemma_suns(daytime_only=True)

    # calculate sun positions from sun vector
    pts = []
    hours = []
    for suns in day:
        for sun in suns:
            if not make_2d:
                pts.append(origin.move(sun.sun_vector.reverse() * radius))
            else:
                pts.append(origin.move(sun.sun_vector.reverse() * radius))
            hours.append(sun.hoy)

    if not make_2d:
        sun_positions = from_points3d(pts)
    else:
        sun_positions = from_points2d(pts)
    sun_dataset = DisplayPolyData(
        name='data', identifier='data', polydata=[sun_positions]
    )

    # Load data if provided
    if data:
        for dt in data:
            assert isinstance(dt, HourlyContinuousCollection), 'Data needs to be a'\
                f' Ladybug HourlyContinuousCollection object. Instead got {type(dt)}'
            filtered_data = dt.filter_by_hoys(hours)
            name = filtered_data.header.data_type.name
            for data in sun_dataset.polydata:
                data.add_data(
                    filtered_data.values, name=name, per_face=False,
                    data_type=filtered_data.header.data_type,
                    unit=filtered_data.header.unit
                )
            sun_dataset.color_by = name
        datasets.append(sun_dataset)
    else:
        sun_dataset = DisplayPolyData(
            name='Suns', identifier='suns',
            polydata=[sun_positions], color=sun_color)
        datasets.append(sun_dataset)

    # join polylines into a single polydata
    sunpath = VisualizationSet(datasets=datasets)
    return Path(sunpath.to_vtkjs(output_folder, file_name))


Sunpath.to_vtkjs = sunpath_to_vtkjs
