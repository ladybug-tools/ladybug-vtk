"""A Model object to collect all other DisplayPolyData objcts."""

from __future__ import annotations
import shutil
import tempfile
import os


from typing import List, Union
from ladybug_display.visualization import VisualizationSet as LBVisualizationSet

from .vtkjs.schema import IndexJSON
from .vtkjs.helper import convert_directory_to_zip_file
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
        """Write a vtkjs file.

        Write your honeybee-vtk model to a vtkjs file that you can open in
        Pollination Viewer.

        Args:
            folder: A valid text string representing the location of folder where
                you'd want to write the vtkjs file. Defaults to current working
                directory.
            name : Name for the vtkjs file. File name will be Model.vtkjs if not
                provided.

        Returns:
            A text string representing the file path to the vtkjs file.
        """

        # name of the vtkjs file
        file_name = name or 'visualization_set'
        # create a temp folder
        temp_folder = tempfile.mkdtemp()
        # The folder set by the user is the target folder
        target_folder = os.path.abspath(folder)
        # Set a file path to move the .zip file to the target folder
        target_vtkjs_file = os.path.join(target_folder, file_name + '.vtkjs')

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
