"""Extend Ladybug Core functionalities."""

import math
from pathlib import Path

from typing import List, Union, Tuple, Optional
from ladybug_geometry.geometry3d import Plane, Arc3D
from ladybug.sunpath import Sunpath, Point3D, Vector3D
from ladybug.datacollection import HourlyContinuousCollection

from .from_ladybug import from_points, from_polyline, from_arc
from .to_vtk import to_circle
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
    # daily analemmas
    data = data or []
    origin = Point3D()

    polylines = self.hourly_analemma_polyline3d(
        origin=origin, daytime_only=True, radius=radius)
    sp_polydata = [from_polyline(pl) for pl in polylines]
    sp_dataset = ModelDataSet(name='Hourly_Analemmas', data=sp_polydata)

    # monthly arcs
    arcs = self.monthly_day_arc3d()
    arc_polydata = [from_arc(arc, 100) for arc in arcs]
    arc_dataset = ModelDataSet(name='Monthly_Arcs', data=arc_polydata)

    # base circle
    base_polydata = to_circle(origin, radius)
    base_dataset = ModelDataSet(name='Base_Circle', data=[base_polydata])

    # add suns
    day = self.hourly_analemma_suns(daytime_only=True)
    # calculate sun positions from sun vector
    pts = []
    hours = []
    for suns in day:
        for sun in suns:
            pts.append(origin.move(sun.sun_vector.reverse() * radius))
            hours.append(sun.hoy)

    sun_positions = from_points(pts)

    datasets = [sp_dataset, arc_dataset, base_dataset]
    if data:
        for dt in data:
            assert isinstance(dt, HourlyContinuousCollection), 'Data needs to be a'\
                f' Ladybug HourlyContinuousCollection object. Instead got {type(dt)}'
            filtered_data = dt.filter_by_hoys(hours)
            name = filtered_data.header.data_type.name
            sun_positions.add_data(filtered_data.values, name=name, cell=False)

        # use the last data set for color by
        sun_positions.color_by(name, cell=False)
        sun_dataset = ModelDataSet(name='Suns', data=[sun_positions])
        datasets.append(sun_dataset)

    # join polylines into a single polydata
    sunpath = Model(datasets=datasets)
    return Path(sunpath.to_vtkjs(output_folder, 'sunpath'))


Sunpath.to_vtkjs = sunpath_to_vtkjs
