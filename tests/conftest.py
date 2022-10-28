import pytest
import json

from tempfile import TemporaryDirectory
from pathlib import Path

from ladybug.epw import EPW
from ladybug_display.visualization import VisualizationSet


@pytest.fixture(scope='session')
def temp_folder():
    d = TemporaryDirectory()
    yield Path(d.name)
    d.cleanup()


@pytest.fixture()
def epw():
    return EPW('./tests/assets/weather/boston.epw')


@pytest.fixture()
def visualization_set():
    data = json.loads(Path('./tests/assets/visualization.json').read_text())
    vs = VisualizationSet.from_dict(data)
    return vs


@pytest.fixture()
def visualization_set_detailed():
    data = json.loads(Path('./tests/assets/visualization_detailed.json').read_text())
    vs = VisualizationSet.from_dict(data)
    return vs
