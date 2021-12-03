"""Extend Ladybug Core functionalities."""

import math
from pathlib import Path

from typing import List
from ladybug.color import Color
from ladybug_geometry.geometry3d import Point3D
from ladybug_geometry.geometry2d import Vector2D
from ladybug.sunpath import Sunpath, Point3D
from ladybug.compass import Compass
from ladybug.datacollection import HourlyContinuousCollection

from .from_ladybug3d import from_points3d, from_polyline3d, from_arc3d
from .from_ladybug2d import from_line2d
from .to_vtk import to_circle, to_text
from .model_dataset import ModelDataSet
from .model import Model


def sunpath_to_vtkjs(self, output_folder: str, name: str = 'sunpath', radius: int = 100,
                     data: List[HourlyContinuousCollection] = None):
    """Export sunpath as a vtkjs file.

    Args:
        output_folder:
        name: Output file name. Defaults to Sunpath.
        radius: Radius of the sunpath. Defaults to 100.
        data: A list of Ladybug continuous hourly collection objects. Defaults to None.

    Returns:
        A pathlib Path object to the vtkjs file.
    """
    datasets = []

    # daily analemmas
    data = data or []
    origin = Point3D()

    polylines = self.hourly_analemma_polyline3d(
        origin=origin, daytime_only=True, radius=radius)
    sp_polydata = [from_polyline3d(pl) for pl in polylines]
    sp_dataset = ModelDataSet(name='Hourly_Analemmas', data=sp_polydata, color=Color())
    datasets.append(sp_dataset)

    # monthly arcs
    arcs = self.monthly_day_arc3d()
    arc_polydata = [from_arc3d(arc, 100) for arc in arcs]
    arc_dataset = ModelDataSet(name='Monthly_Arcs', data=arc_polydata, color=Color())
    datasets.append(arc_dataset)

    # compass circles
    rads = [radius, radius + 1.5, radius + 4.5]
    base_polydata = [to_circle(origin, radius) for radius in rads]

    # compass ticks
    compass = Compass(radius=radius, north_angle=self.north_angle)
    ticks_major = compass.ticks_from_angles(angles=compass.MAJOR_AZIMUTHS, factor=0.55)
    ticks_minor = compass.ticks_from_angles(angles=compass.MINOR_AZIMUTHS)
    ticks_polydata = [from_line2d(tick) for tick in ticks_major+ticks_minor]
    base_polydata.extend(ticks_polydata)
    base_dataset = ModelDataSet(name='Base_Circle', data=base_polydata, color=Color())
    datasets.append(base_dataset)

    # Since vtkVectorText starts from left bottom we need to move the labels to the left
    # and down by a certain amount.
    left_vector = Vector2D(-1, 0)*3
    down_vector = Vector2D(0, -1)*3

    # compass minor labels
    minor_text_polydata = [to_text(text, compass.minor_azimuth_points[count].
                                   move(left_vector).move(down_vector))
                           for count, text in enumerate(compass.MINOR_TEXT)]
    minor_label_dataset = ModelDataSet(
        name='Minor_Labels', data=minor_text_polydata, color=Color())
    datasets.append(minor_label_dataset)

    # compass major labels
    major_text_polydata = [to_text(text, compass.major_azimuth_points[count].
                                   move(left_vector).move(down_vector), scale=5) for
                           count, text in enumerate(compass.MAJOR_TEXT)]
    major_label_dataset = ModelDataSet(
        name='Major_Labels', data=major_text_polydata, color=Color())
    datasets.append(major_label_dataset)

    # add suns
    day = self.hourly_analemma_suns(daytime_only=True)
    # calculate sun positions from sun vector
    pts = []
    hours = []
    for suns in day:
        for sun in suns:
            pts.append(origin.move(sun.sun_vector.reverse() * radius))
            hours.append(sun.hoy)

    sun_positions = from_points3d(pts)
    sun_dataset = ModelDataSet(name='Suns', data=[sun_positions])

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
            name='Suns', data=[sun_positions], color=Color(255, 255, 0))
        datasets.append(sun_dataset)

    # join polylines into a single polydata
    sunpath = Model(datasets=datasets)
    return Path(sunpath.to_vtkjs(output_folder, 'sunpath'))


Sunpath.to_vtkjs = sunpath_to_vtkjs
