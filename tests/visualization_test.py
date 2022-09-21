from ladybug_display_schema.visualization import VisualizationSet
from ladybug_vtk.vis_set import from_visualization_set
import pathlib

def test_vs(temp_folder, visualization_set):
    vs = VisualizationSet.parse_file(visualization_set)
    model = from_visualization_set(vs)
    path = model.to_vtkjs(folder=temp_folder, name='vs-model')
    path = pathlib.Path(path)
    assert path.is_file()
    assert path.name == 'vs-model.vtkjs'
