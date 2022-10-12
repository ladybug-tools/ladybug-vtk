from ladybug_display.visualization import VisualizationSet
from ladybug_vtk.visualization_set import VTKVisualizationSet
import pathlib
import json


def test_vs(temp_folder, visualization_set):
    data = json.loads(pathlib.Path(visualization_set).read_text())
    vs = VisualizationSet.from_dict(data)
    model = VTKVisualizationSet.from_visualization_set(vs)
    path = model.to_vtkjs(folder=temp_folder, name='vs-model')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'vs-model.vtkjs'
