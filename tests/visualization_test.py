from ladybug_vtk.visualization_set import VisualizationSet, LBVisualizationSet
import pathlib
import json


def test_vs(temp_folder, visualization_set):
    vs = VisualizationSet.from_visualization_set(visualization_set)
    path = vs.to_vtkjs(folder=temp_folder, name='vs-model')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'vs-model.vtkjs'


def test_vs_detailed(temp_folder, visualization_set_detailed):
    vs = VisualizationSet.from_visualization_set(visualization_set_detailed)
    path = vs.to_vtkjs(folder=temp_folder, name='vs-model-detailed')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'vs-model-detailed.vtkjs'


def test_extension(temp_folder, visualization_set):
    path = visualization_set.to_vtkjs(output_folder=temp_folder, file_name='vs-model-2')
    assert path.is_file()
    assert path.name == 'vs-model-2.vtkjs'


def test_vs_sunpath_2d(temp_folder):
    data = json.loads(pathlib.Path('./tests/assets/visualization_sunpath2d.json').read_text())
    vs = LBVisualizationSet.from_dict(data)
    vs = VisualizationSet.from_visualization_set(vs)
    path = vs.to_vtkjs(folder=temp_folder, name='vs-sunpath-2d')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'vs-sunpath-2d.vtkjs'


def test_vs_sunpath_3d(temp_folder):
    data = json.loads(pathlib.Path('./tests/assets/visualization_sunpath.json').read_text())
    vs = LBVisualizationSet.from_dict(data)
    vs = VisualizationSet.from_visualization_set(vs)
    path = vs.to_vtkjs(folder=temp_folder, name='vs-sunpath-3d')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'vs-sunpath-3d.vtkjs'


def test_daylight_factor_vs(temp_folder):
    data = json.loads(pathlib.Path('./tests/assets/daylight_factor.vsf').read_text())
    vs = LBVisualizationSet.from_dict(data)
    vs = VisualizationSet.from_visualization_set(vs)
    path = vs.to_vtkjs(folder=temp_folder, name='daylight_factor')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'daylight_factor.vtkjs'


def test_comfort_vsf(temp_folder):
    data = json.loads(pathlib.Path('./tests/assets/comfort.vsf').read_text())
    vs = LBVisualizationSet.from_dict(data)
    vs = VisualizationSet.from_visualization_set(vs)
    path = vs.to_vtkjs(folder=temp_folder, name='vs-comfort')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'vs-comfort.vtkjs'
