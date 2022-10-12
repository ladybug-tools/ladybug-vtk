from ladybug_vtk.visualization_set import VisualizationSet
import pathlib


def test_vs(temp_folder, visualization_set):
    vs = VisualizationSet.from_visualization_set(visualization_set)
    path = vs.to_vtkjs(folder=temp_folder, name='vs-model')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'vs-model.vtkjs'


def test_extension(temp_folder, visualization_set):
    path = visualization_set.to_vtkjs(output_folder=temp_folder, file_name='vs-model-2')
    assert path.is_file()
    assert path.name == 'vs-model-2.vtkjs'
