"""A Model object to collect all other ModelDataSet objcts."""

from __future__ import annotations
import shutil
import tempfile
import os


from typing import List, Union
from .vtkjs.schema import IndexJSON
from .vtkjs.helper import convert_directory_to_zip_file
from .model_dataset import ModelDataSet


class Model:

    def __init__(self, datasets: Union[ModelDataSet, List[ModelDataSet]] = None) -> None:
        self.datasets = self._assign_datasets(datasets)

    @staticmethod
    def _assign_datasets(datasets: Union[ModelDataSet, List[ModelDataSet]]):
        if isinstance(datasets, ModelDataSet):
            return [datasets]
        elif isinstance(datasets, list):
            return datasets
        else:
            raise TypeError(
                'datasets should be a ModelDataSet or a list of ModelDataSet.'
                f' Instead got {type(datasets)}.')

    def add(self, datasets: Union[ModelDataSet, List[ModelDataSet]]) -> None:
        datasets = self._assign_datasets(datasets)
        self.datasets.extend(datasets)

    def to_vtkjs(self, folder: str = '.', name: str = None) -> str:
        """Write a vtkjs file.

        Write your honeybee-vtk model to a vtkjs file that you can open in
        Paraview-Glance.

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
        file_name = name or 'model'
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
            scene.append(data.as_data_set())

        # write index.json
        index_json = IndexJSON()
        index_json.scene = scene
        index_json.to_json(temp_folder)

        # zip as vtkjs
        temp_vtkjs_file = convert_directory_to_zip_file(temp_folder, extension='vtkjs',
                                                        move=False)

        # Move the generated vtkjs to target folder
        shutil.move(temp_vtkjs_file, target_vtkjs_file)

        try:
            shutil.rmtree(temp_folder)
        except Exception:
            pass

        return target_vtkjs_file
