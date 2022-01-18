"""Extend Ladybug Core functionalities."""

from pathlib import Path

from typing import List
from ladybug.color import Color
from ladybug_geometry.geometry3d import Point3D
from ladybug_geometry.geometry2d import Vector2D, Point2D
from ladybug.sunpath import Sunpath
from ladybug.compass import Compass
from ladybug.datacollection import HourlyContinuousCollection

from .fromgeometry import from_points3d, to_circle, to_text, from_points2d
from .model_dataset import ModelDataSet
from .model import Model


def sunpath_to_vtkjs(self, output_folder: str = '.', file_name: str = 'sunpath', radius: int = 100,
                     data: List[HourlyContinuousCollection] = None,
                     sun_color: Color = Color(252, 177, 3), make_2d: bool = False) -> Path:
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
    sp_dataset = ModelDataSet(name='hourly_analemmas', data=sp_polydata, color=Color())
    datasets.append(sp_dataset)

    # monthly arcs
    if not make_2d:
        arcs = self.monthly_day_arc3d(radius=radius)
        monthly_polydata = [arc.to_polydata(resolution=100) for arc in arcs]
    else:
        polylines = self.monthly_day_polyline2d(radius=radius)
        monthly_polydata = [polyline.to_polydata() for polyline in polylines]
    arc_dataset = ModelDataSet(name='monthly_arcs', data=monthly_polydata, color=Color())
    datasets.append(arc_dataset)

    # compass circles
    offset_1 = (radius*1.5)/100
    offset_2 = (radius*4.5)/100
    rads = [radius, radius+offset_1, radius+offset_2]
    base_polydata = [to_circle(origin, radius) for radius in rads]

    # compass ticks
    compass = Compass(radius=radius, north_angle=self.north_angle)
    ticks_major = compass.ticks_from_angles(angles=compass.MAJOR_AZIMUTHS, factor=0.55)
    ticks_minor = compass.ticks_from_angles(angles=compass.MINOR_AZIMUTHS)
    ticks_polydata = [tick.to_polydata() for tick in ticks_major+ticks_minor]
    base_polydata.extend(ticks_polydata)
    base_dataset = ModelDataSet(name='base_circle', data=base_polydata, color=Color())
    datasets.append(base_dataset)

    # Since vtkVectorText starts from left bottom we need to move the labels to the left
    # and down by a certain amount.
    moving_factor = (radius*3)/100
    left_vector = Vector2D(-1, 0)*moving_factor
    down_vector = Vector2D(0, -1)*moving_factor

    # compass minor labels
    minor_scale = (radius*2)/100
    minor_text_polydata = [to_text(text, compass.minor_azimuth_points[count].
                                   move(left_vector).move(down_vector), minor_scale)
                           for count, text in enumerate(compass.MINOR_TEXT)]
    minor_label_dataset = ModelDataSet(
        name='minor_labels', data=minor_text_polydata, color=Color())
    datasets.append(minor_label_dataset)

    # compass major labels
    major_scale = (radius*5)/100
    major_text_polydata = [to_text(text, compass.major_azimuth_points[count].
                                   move(left_vector).move(down_vector), scale=major_scale) for
                           count, text in enumerate(compass.MAJOR_TEXT)]
    major_label_dataset = ModelDataSet(
        name='major_labels', data=major_text_polydata, color=Color())
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
    sun_dataset = ModelDataSet(name='suns', data=[sun_positions])

    # Load data if provided
    if data:
        for dt in data:
            assert isinstance(dt, HourlyContinuousCollection), 'Data needs to be a'\
                f' Ladybug HourlyContinuousCollection object. Instead got {type(dt)}'
            filtered_data = dt.filter_by_hoys(hours)
            name = filtered_data.header.data_type.name
            sun_dataset.add_data_fields([filtered_data], name, per_face=False)
            sun_dataset.color_by = name
        datasets.append(sun_dataset)
    else:
        sun_dataset = ModelDataSet(
            name='suns', data=[sun_positions], color=sun_color)
        datasets.append(sun_dataset)

    # join polylines into a single polydata
    sunpath = Model(datasets=datasets)
    return Path(sunpath.to_vtkjs(output_folder, file_name))


Sunpath.to_vtkjs = sunpath_to_vtkjs
