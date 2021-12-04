from ladybug.hourlyplot import HourlyPlot


def test_hourly_plot(temp_folder, epw):
    hp = HourlyPlot(epw.wind_speed, z_dim=100)
    path = hp.to_vtkjs(temp_folder)
    assert path.name == 'hourly plot.vtkjs'
