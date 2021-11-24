"""A VTK Appended Polydata object with additional methods."""

import vtk
from typing import List
from .writer import write_to_file, write_to_folder
from .polydata import PolyData


class JoinedPolyData(vtk.vtkAppendPolyData):
    """A thin wrapper around vtk.vtkAppendPolyData."""

    def __init__(self) -> None:
        super().__init__()

    @ classmethod
    def from_polydata(cls, polydata: List[PolyData]):
        """Join several polygonal datasets.

        This function merges several polygonal datasets into a single polygonal datasets.
        All geometry is extracted and appended, but point and cell attributes (i.e.,
        scalars, vectors, normals) are extracted and appended only if all datasets have
        the point and/or cell attributes available. (For example, if one dataset has
        point scalars but another does not, point scalars will not be appended.)
        """
        joined_polydata = cls()

        for vtk_polydata in polydata:
            joined_polydata.AddInputData(vtk_polydata)

        joined_polydata.Update()

        return joined_polydata

    def append(self, polydata: PolyData) -> None:
        """Append a new polydata to current data."""
        self.AddInputData(polydata)
        self.Update()

    def extend(self, polydata: List[PolyData]) -> None:
        """Extend a list of new polydata to current data."""
        for data in polydata:
            self.AddInputData(data)
        self.Update()

    def to_vtk(self, target_folder, name, writer):
        """Write to a VTK file.

        The file extension will be set to vtk for ASCII format and vtp for binary format.
        """
        return write_to_file(self, target_folder, name, writer)

    def to_folder(self, target_folder='.'):
        """Write data to a folder with a JSON meta file.

        This method generates a folder that includes a JSON meta file along with all the
        binary arrays written as standalone binary files.

        The generated format can be used by vtk.js using the reader below
        https://kitware.github.io/vtk-js/examples/HttpDataSetReader.html

        Args:
            target_folder: Path to target folder. Default: .

        """
        return write_to_folder(self, target_folder)
