import pytest
from tempfile import TemporaryDirectory
from pathlib import Path
from ladybug.epw import EPW


@pytest.fixture(scope='session')
def temp_folder():
    d = TemporaryDirectory()
    yield Path(d.name)
    d.cleanup()


@pytest.fixture()
def epw():
    return EPW('./tests/assets/weather/boston.epw')
