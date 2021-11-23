import math
import pytest
from pathlib import Path
from ladybug.epw import EPW
from ladybug.location import Location
from ladybug.sunpath import Sunpath, Point3D, Vector3D
from ladybug_vtk.to_vtk import create_polyline, create_points
from ladybug_vtk.model_dataset import ModelDataSet
from ladybug_vtk.model import Model


def test_sunpath(temp_folder):

    # Get location from epw file
    epw = EPW('./tests/assets/weather/boston.epw')
    location = epw.location

    # Initiate sunpath
    sp = Sunpath.from_location(location)

    radius = 100
    origin = Point3D(0, 0, 0)

    # daily analemmas
    polylines = sp.hourly_analemma_polyline3d(
        origin=origin, daytime_only=True, radius=radius)
    sp_polydata = [create_polyline(pl) for pl in polylines]
    sp_dataset = ModelDataSet(name='Polylines', data=sp_polydata)

    # monthly arcs
    arcs = sp.monthly_day_arc3d()
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
    day = sp.hourly_analemma_suns(daytime_only=True)
    # calculate sun positions from sun vector
    pts = []
    hours = []
    for suns in day:
        for sun in suns:
            pts.append(origin.move(sun.sun_vector.reverse() * radius))
            hours.append(sun.hoy)

    radiation_data = epw.global_horizontal_radiation
    filtered_radiation_data = radiation_data.filter_by_hoys(hours)

    sun_positions = create_points(pts)
    sun_positions.add_data(
        filtered_radiation_data.values, name='Global Horizontal Radiation', cell=False
    )
    sun_positions.color_by('Global Horizontal Radiation', cell=False)
    sun_dataset = ModelDataSet(name='Suns', data=[sun_positions])

    # join polylines into a single polydata
    sunpath = Model(datasets=[sp_dataset, arc_dataset, plot_dataset, sun_dataset])
    path = Path(sunpath.to_vtkjs(temp_folder, 'sunpath'))
    assert path.name == 'sunpath.vtkjs'
