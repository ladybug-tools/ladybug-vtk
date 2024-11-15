"""Test cli."""
import os
from click.testing import CliRunner

from ladybug_vtk.cli import vis_set_to_vtk_cli


def test_vis_set_to_vtk_cli():
    """Test the vis_set_to_vtk_cli command."""
    runner = CliRunner()
    input_vsf = './tests/assets/daylight_factor.vsf'
    output_vtkjs = './tests/assets/daylight_factor.vtkjs'
    output_html = './tests/assets/daylight_factor.html'

    in_args = [input_vsf, '--output-format', 'vtkjs', '--output-file', output_vtkjs]
    result = runner.invoke(vis_set_to_vtk_cli, in_args)
    assert result.exit_code == 0
    assert os.path.isfile(output_vtkjs)
    os.remove(output_vtkjs)

    in_args = [input_vsf, '--output-format', 'html', '--output-file', output_html]
    result = runner.invoke(vis_set_to_vtk_cli, in_args)
    assert result.exit_code == 0
    assert os.path.isfile(output_html)
    os.remove(output_html)
