"""A VTK Polydata object with additional methods."""

import vtk
import warnings
from typing import Dict, List, Tuple, Union
from .data_field_info import DataFieldInfo
from .writer import write_to_folder, write_to_file
from .legend_parameter import ColorSets


class PolyData(vtk.vtkPolyData):
    """A thin wrapper around vtk.vtkPolyData.

    PolyData has additional fields for metadata information.
    """

    def __init__(self) -> None:
        super().__init__()
        self.identifier = None
        self.name = None
        self.type = None
        self.boundary = None
        self.construction = None
        self.modifier = None
        self._fields = {}  # keep track of information for each data field.

    @ staticmethod
    def _resolve_array_type(data):
        if isinstance(data, float):
            return vtk.vtkFloatArray()
        elif isinstance(data, int):
            return vtk.vtkIntArray()
        elif isinstance(data, str):
            return vtk.vtkStringArray()
        else:
            raise ValueError(f'Unsupported input data type: {type(data)}')

    @ property
    def data_fields(self) -> Dict[str, DataFieldInfo]:
        """Get data fields for this Polydata."""
        return self._fields

    def add_data(self, data: List, name, *, cell=True, colors=None,
                 data_range=None):
        """Add a list of data to a vtkPolyData.

        Data can be added to cells or points. By default the data will be added to cells.

        Args:
            data: A list of values. The length of the data should match the length of
                DataCells or DataPoints in Polydata.
            name: Name of data (e.g. Useful Daylight Autonomy.)
            cell: A Boolean to indicate if the data is per cell or per point. In
                most cases except for sensor points that are loaded as sensors the data
                are provided per cell.
            colors: A Colors object that defines colors for the legend.
            data_range: A list with two values for minimum and maximum values for legend
                parameters.
        """
        assert name not in self._fields, \
            f'A data filed by name "{name}" already exist. Try a different name.'

        if isinstance(data[0], (list, tuple)):
            values = self._resolve_array_type(data[0][0])
            values.SetNumberOfComponents(len(data[0]))
            values.SetNumberOfTuples(len(data))
            iterator = True
        else:
            values = self._resolve_array_type(data[0])
            iterator = False

        if name:
            values.SetName(name)

        if iterator:
            # NOTE: This is my (mostapha's) understanding from the original code for
            # tuple data. This needs to be tested.
            for d in data:
                values.InsertNextValue(*d)
        else:
            for d in data:
                values.InsertNextValue(d)

        if cell:
            self.GetCellData().AddArray(values)
        else:
            self.GetPointData().AddArray(values)

        self.Modified()

        # set data range
        data_range = self._get_data_range(name, data_range, values)

        # set colors
        if not colors:
            colors = ColorSets.ecotect

        self._fields[name] = DataFieldInfo(name, data_range, colors, cell)

        # if it's a string array don't publish the legend
        if isinstance(values, vtk.vtkStringArray):
            self._fields[name].legend_parameter.hide_legend = True

    def color_by(self, name: str, cell=True) -> None:
        """Set the name for active data that should be used to color PolyData."""
        assert name in self._fields, \
            f'{name} is not a valid data field for this PolyData. Available ' \
            f'data fields are: {list(self._fields)}'

        if cell:
            self.GetCellData().SetActiveScalars(name)
        else:
            self.GetPointData().SetActiveScalars(name)

        self.Modified()

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

    def __repr__(self) -> Tuple[str]:
        return (
            f'Name: {self.name} |'
            f' Boundary: {self.boundary} |'
            f' Construction: {self.construction} |'
            f' Modifier: {self.modifier}'
        )

    @staticmethod
    def _get_data_range(
            name: str,
            data_range: List[Union[float, int]],
            array: Union[vtk.vtkFloatArray, vtk.vtkIntArray]) -> List[Union[float, int]]:
        """Calculate data range for data based on data array and user provided legend range.

        Args:
            name: Name of data (e.g. Useful Daylight Autonomy.)
            data_range: A list of numbers.
            array: A vtk float array or a vtk int array.

        Returns:
            A list of min and max values to be used as a range for the data.
        """

        # calculate range based on the data
        if not isinstance(array, vtk.vtkStringArray):

            auto_range = array.GetRange()

            if not data_range:
                warnings.warn(
                    f'In data {name.capitalize()}, since min and max'
                    ' values of legend are not provided, those values will be auto'
                    ' calculated based on data. \n'
                )
                return tuple(auto_range)

            min, max = data_range
            if min == None and max == None:
                warnings.warn(
                    f'In data {name.capitalize()}, since min and max'
                    ' values of legend are not provided, those values will be auto'
                    ' calculated based on data. \n'
                )
                return tuple(auto_range)

            elif min == None and max:
                warnings.warn(
                    f'In data {name.capitalize()}, since min'
                    ' value of the legend is not provided, that value will be auto'
                    ' calculated based on data. \n'
                )
                return (auto_range[0], max)

            elif min and max == None:
                warnings.warn(
                    f'In data {name.capitalize()}, since max'
                    ' value of the legend is not provided, that value will be auto'
                    ' calculated based on data. \n'
                )
                return (min, auto_range[1])

            elif min == 0 and max == 0:
                raise ValueError(
                    f'In data {name.capitalize()}, min and max values'
                    ' of legend cannot be both 0. \n'
                )

            elif isinstance(min, (float, int)) and isinstance(max, (float, int)):
                if min >= max:
                    raise ValueError(
                        f'In data {name.capitalize()} Min value cannot be greater'
                        ' than the max value.')
                if min == max:
                    raise ValueError(
                        f'In data {name.capitalize()} Min and max values cannot'
                        ' be the same.')
                else:
                    return (min, max)

        else:
            return tuple(data_range)
