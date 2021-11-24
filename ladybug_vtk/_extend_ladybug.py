import math
from pathlib import Path

from ladybug.sunpath import Sunpath, Point3D, Vector3D

from .to_vtk import create_points, create_polyline
from .model_dataset import ModelDataSet
from .model import Model


def sunpath_to_vtkjs(self, output_folder, name='sunpath', radius=100, data=None):
    """Export sunpath as a vtkjs file.

    Args:
        output_folder:
        name: Output file name (default: sunpath).
        radius:
        data: A list of Ladybug continuous hourly data.

    Returns:
        path to vtkjs file.
    """
    # daily analemmas
    data = data or []
    origin = Point3D()

    polylines = self.hourly_analemma_polyline3d(
        origin=origin, daytime_only=True, radius=radius)
    sp_polydata = [create_polyline(pl) for pl in polylines]
    sp_dataset = ModelDataSet(name='Polylines', data=sp_polydata)

    # monthly arcs
    arcs = self.monthly_day_arc3d()
    arc_polylines = [arc.to_polyline(divisions=10)for arc in arcs]
    arc_polydata = [create_polyline(arc) for arc in arc_polylines]
    arc_dataset = ModelDataSet(name='Arcs', data=arc_polydata)

    # add a circle
    north = origin.move(Vector3D(0, radius, 0))
    plot_points = [
        north.rotate_xy(math.radians(angle), origin)
        for angle in range(0, 365, 5)
    ]
    plot = create_points(plot_points)
    plot_dataset = ModelDataSet(name='Plot', data=[plot])

    # add suns
    day = self.hourly_analemma_suns(daytime_only=True)
    # calculate sun positions from sun vector
    pts = []
    hours = []
    for suns in day:
        for sun in suns:
            pts.append(origin.move(sun.sun_vector.reverse() * radius))
            hours.append(sun.hoy)

    sun_positions = create_points(pts)

    # TODO: Only add checks for data type
    datasets=[sp_dataset, arc_dataset, plot_dataset]
    if data:
        for dt in data:
            filtered_data = dt.filter_by_hoys(hours)
            name = filtered_data.header.data_type.name
            sun_positions.add_data(filtered_data.values, name=name, cell=False)

        # use the last data set for color by
        sun_positions.color_by(name, cell=False)
        sun_dataset = ModelDataSet(name='Suns', data=[sun_positions])
        datasets.append(sun_dataset)

    # join polylines into a single polydata
    sunpath = Model(datasets=datasets)
    path = Path(sunpath.to_vtkjs(output_folder, 'sunpath'))
    return path

Sunpath.to_vtkjs = sunpath_to_vtkjs

