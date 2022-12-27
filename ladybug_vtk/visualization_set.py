"""A Model object to collect all other DisplayPolyData objcts."""

from __future__ import annotations
import shutil
import tempfile
import pathlib
import webbrowser

from typing import List, Union
from ladybug_display.visualization import VisualizationSet as LBVisualizationSet

from .vtkjs.schema import IndexJSON
from .vtkjs.helper import convert_directory_to_zip_file, add_data_to_viewer
from .display_polydata import DisplayPolyData


class VisualizationSet:

    def __init__(self, datasets: Union[DisplayPolyData, List[DisplayPolyData]] = None) -> None:
        self.datasets = self._validate_datasets(datasets)

    @classmethod
    def from_visualization_set(
            cls, visualization_set: LBVisualizationSet) -> VisualizationSet:
        """Create a VisualizationSet from a Ladybug Display VisualizationSet."""
        # translate analysis geometry
        data_sets = [
            DisplayPolyData.from_visualization_geometry(geometry)
            for geometry in visualization_set.geometry
        ]

        return cls(data_sets)

    @staticmethod
    def _validate_datasets(datasets: Union[DisplayPolyData, List[DisplayPolyData]]):
        if isinstance(datasets, DisplayPolyData):
            return [datasets]
        elif isinstance(datasets, list):
            return datasets
        else:
            raise TypeError(
                'datasets should be a DisplayPolyData or a list of DisplayPolyData.'
                f' Instead got {type(datasets)}.')

    def add_datasets(self, datasets: Union[DisplayPolyData, List[DisplayPolyData]]) -> None:
        datasets = self._validate_datasets(datasets)
        self.datasets.extend(datasets)

    def to_vtkjs(self, folder: str = '.', name: str = None) -> str:
        """Translate the visualization set a vtkjs file.

        Write the visualization set to a vtkjs file that you can open in
        Pollination Viewer.

        Args:
            folder: A valid text string representing the location of folder where
                you'd want to write the vtkjs file. Defaults to current working
                directory.
            name: Name for the vtkjs file. File name will be visualization_set.vtkjs if
                not provided.

        Returns:
            A text string representing the file path to the vtkjs file.
        """

        # name of the vtkjs file
        file_name = name or 'visualization_set'
        # create a temp folder
        temp_folder = tempfile.mkdtemp()
        # The folder set by the user is the target folder
        target_folder = pathlib.Path(folder).absolute()
        # Set a file path to move the .zip file to the target folder
        target_vtkjs_file = target_folder.joinpath(f'{file_name}.vtkjs').as_posix()

        # write every dataset
        scene = []

        for data in self.datasets:
            path = data.to_folder(temp_folder)
            if not path:
                # empty dataset
                continue
            scene.append(data.to_vtk_dataset())

        # write index.json
        index_json = IndexJSON()
        index_json.scene = scene
        index_json.to_json(temp_folder)

        # zip as vtkjs
        temp_vtkjs_file = convert_directory_to_zip_file(
            temp_folder, extension='vtkjs', move=False
        )

        # Move the generated vtkjs to target folder
        shutil.move(temp_vtkjs_file, target_vtkjs_file)

        try:
            shutil.rmtree(temp_folder)
        except Exception:
            pass

        return target_vtkjs_file

    def to_html(self, folder: str = '.', name: str = None, open: bool = False) -> str:
        """Translate the visualization set to an HTML file.

        This HTML file is self .

        Args:
            folder: A valid text string representing the location of folder where
                you'd want to write the HTML file. Defaults to current working
                directory.
            name: Name for the HTML file. File name will be visualization_set.html if
                not provided.
            open: A boolean to open the HTML file once created. Default is set to False.

        Returns:
            A text string representing the file path to the vtkjs file.
        """
        file_name = name or 'visualization_set'
        target_folder = pathlib.Path(folder)
        target_folder.mkdir(parents=True, exist_ok=True)

        html_file = target_folder.joinpath(f'{file_name}.html').as_posix()

        temp_folder = tempfile.mkdtemp()
        vtkjs_file = self.to_vtkjs(folder=temp_folder, name=name)
        temp_html_file = add_data_to_viewer(vtkjs_file)
        shutil.copy(temp_html_file, html_file)

        try:
            shutil.rmtree(temp_folder)
        except Exception:
            pass

        if open:
            webbrowser.open(html_file)

        return html_file
