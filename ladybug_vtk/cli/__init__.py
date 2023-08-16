"""ladybug-vtk commands."""
import click
import sys
import os
import logging

from ladybug_display.visualization import VisualizationSet
from ladybug.cli import main

_logger = logging.getLogger(__name__)


# command group for all vtk extension commands.
@click.group(help='ladybug VTK commands.')
@click.version_option()
def vtk():
    pass


@vtk.command('vis-to-vtk')
@click.argument('vis-file', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option(
    '--output-format', '-of', help='Text for the output format of the resulting '
    'file. Choose from: vtkjs, html. Note that the html format refers to a web page '
    'with the vtkjs file embedded within it. ',
    type=str, default='vtkjs', show_default=True)
@click.option(
    '--output-file', help='File to output the result. Default: vis_set',
    type=click.File('w'), default='vis_set', show_default=True)
def vis_set_to_vtk(vis_file, output_format, output_file):
    """Translate a VisualizationSet file (.vsf) to VTK formats.

    \b
    Args:
        vis_file: Full path to a Ladybug Display Visualization Set (VSF) file.
    """
    try:
        vis_set = VisualizationSet.from_file(vis_file)
        output_format = output_format.lower()
        out_folder, out_file = os.path.split(output_file.name)
        if out_file.endswith('.vtkjs'):
            out_file = out_file[:-6]
        elif out_file.endswith('.html'):
            out_file = out_file[:-5]
        if output_format == 'vtkjs':
            vis_set.to_vtkjs(output_folder=out_folder, file_name=out_file)
        if output_format == 'html':
            vis_set.to_html(output_folder=out_folder, file_name=out_file)
    except Exception as e:
        _logger.exception('Failed to translate VisualizationSet to VTK.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


# add vtk sub-group to ladybug CLI
main.add_command(vtk)
