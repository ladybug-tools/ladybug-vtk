from ladybug.sunpath import Sunpath


def test_sunpath(temp_folder, epw):
    location = epw.location
    sp = Sunpath.from_location(location)
    path = sp.to_vtkjs(temp_folder,
                       data=[epw.global_horizontal_radiation,
                             epw.dry_bulb_temperature]
                       )
    assert path.name == 'sunpath.vtkjs'
