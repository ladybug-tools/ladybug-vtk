"""Extend visualization set object in ladybug display to have a to_vtkjs method.

This extension makes it easier for developers to get started with using this feature
for developing apps.
"""

from pathlib import Path
from ladybug_display.visualization import VisualizationSet as LBVisualizationSet
from .visualization_set import VisualizationSet as VTKVisualizationSet, DisplayPolyData


def vs_to_vtkjs(
    self: LBVisualizationSet, output_folder: str,
    file_name: str = 'visualization_set'
):
    """
    Export Visualization set to a vtkjs file.

    Args:
        output_folder: Path to the target folder to write the vtkjs file.
        file_name: Output file name. Defaults to visualization_set.

    Returns:
        A pathlib Path object to the vtkjs file.
    """
    data_sets = [
        DisplayPolyData.from_visualization_geometry(geometry)
        for geometry in self.geometry
    ]
    vs = VTKVisualizationSet(datasets=data_sets)
    path = vs.to_vtkjs(folder=output_folder, name=file_name)
    return Path(path)


def vs_to_html(
    self: LBVisualizationSet, output_folder: str,
    file_name: str = 'visualization_set',
    open: bool = False
):
    """
    Export Visualization set to a HTML file.

    Args:
        output_folder: Path to the target folder to write the HTML file.
        file_name: Output file name. Defaults to visualization_set.
        open: A boolean to open the HTML file once created. Default is set to False.

    Returns:
        A pathlib Path object to the HTML file.
    """
    data_sets = [
        DisplayPolyData.from_visualization_geometry(geometry)
        for geometry in self.geometry
    ]
    vs = VTKVisualizationSet(datasets=data_sets)
    path = vs.to_html(folder=output_folder, name=file_name, open=open)
    return Path(path)


LBVisualizationSet.to_vtkjs = vs_to_vtkjs
LBVisualizationSet.to_html = vs_to_html
