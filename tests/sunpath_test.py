import pathlib

from ladybug.epw import EPW
from ladybug.sunpath import Sunpath


def test_sunpath():
    epw = EPW('./tests/assets/weather/boston.epw')
    location = epw.location

    temp_folder = pathlib.Path('./tests/temp')
    temp_folder.mkdir(parents=True, exist_ok=True)
    # Initiate sunpath
    sp = Sunpath.from_location(location)
    path = sp.to_vtkjs(
        temp_folder,
        data = [epw.global_horizontal_radiation, epw.dry_bulb_temperature]
    )
    assert path.name == 'sunpath.vtkjs'
