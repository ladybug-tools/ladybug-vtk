"""A VTK Polydata object with additional methods."""

import vtk
from typing import Dict, List, Tuple

from ladybug_display.visualization import VisualizationData, \
    LegendParameters, DataTypeBase

from .metadata import PolyDataMetaData
from .writer import write_to_folder, write_to_file, VTKWriters


class PolyData(vtk.vtkPolyData):
    """A thin wrapper around vtk.vtkPolyData.

    See here for more information: https://vtk.org/doc/nightly/html/classvtkPolyData.html#details

    A PolyData object holds the geometry information in addition to several layers of
    data. All these data are aligned with the geometry. For instance, you can use a
    PolyData to represent a sensor grid and then add data for irradiance and daylight
    factor values to it.

    A PolyData can be exported to a VTK object directly but in most cases you should use
    the DisplayPolyData object to group the PolyData and set their display attributes.

    """

    def __init__(self) -> None:
        super().__init__()
        self._data: Dict[str, PolyDataMetaData] = {}
        self._color_by = ''

    @ property
    def data(self) -> Dict[str, PolyDataMetaData]:
        """Get data for this Polydata.

        The keys are the name for each data and the values are the visualization
        metadata.
        """
        return self._data

    def add_visualization_data(
            self, data: VisualizationData, matching_method: str = 'faces'
    ):
        """Add visualization data to this polyData.

        Args:
            data: A visualization data object.
            matching_method: Either faces or vertices. Use faces if one value is
                assigned per each face and vertices if one value is assigned per each
                vertex. Default is faces.

        """
        per_face = True if matching_method == 'faces' else False
        name = 'generic_data' if not data.data_type else data.data_type.name
        return self.add_data(
            data.values, name, per_face=per_face,
            legend_parameters=data.legend_parameters,
            unit=data.unit, data_type=data.data_type
        )

    def add_data(
            self, data: List, name: str, *, per_face: bool = True,
            legend_parameters: LegendParameters = None,
            data_type: DataTypeBase = None, unit: str = None
    ):
        """Add a list of data to a vtkPolyData.

        Data can be added to cells or points. By default the data will be added to cells.

        Args:
            data: A list of values. The length of the data should match the length of
                DataCells or DataPoints in Polydata.
            name: Name of data (e.g. Useful Daylight Autonomy.)
            per_face: A Boolean to indicate if the data is per cell or per point. In
                most cases except for sensor points that are loaded as sensors the data
                are provided per cell.
            legend_parameters: An Optional LegendParameters object to override default
                parameters of the legend. None indicates that default legend parameters
                will be used. (Default: None).
            data_type: Optional DataType from the ladybug datatype subpackage (ie.
                Temperature()) , which will be used to assign default legend properties.
                If None, the legend associated with this object will contain no units
                unless a unit below is specified. (Default: None).
            unit: Optional text string for the units of the values. (ie. "C"). If None
                or empty, the default units of the data_type will be used. If no data
                type is specified in this case, this will simply be an empty
                string. (Default: None).
        """
        assert name not in self._data, \
            f'A data by name "{name}" already exist. Try a different name.'

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
            for d in data:
                values.InsertNextValue(*d)
        else:
            for d in data:
                values.InsertNextValue(d)

        if per_face:
            self.GetCellData().AddArray(values)
        else:
            self.GetPointData().AddArray(values)

        self.Modified()

        self._data[name] = PolyDataMetaData(legend_parameters, data_type, unit, per_face)

    @property
    def color_by(self) -> str:
        return self._color_by

    @color_by.setter
    def color_by(self, name: str) -> None:
        """Set the name for active data that should be used to color PolyData."""
        assert name in self._data, \
            f'{name} is not a valid data for this PolyData. Available ' \
            f'data are: {list(self._data.keys())}'

        cell = self._data[name].per_face

        if cell:
            self.GetCellData().SetActiveScalars(name)
        else:
            self.GetPointData().SetActiveScalars(name)

        self.Modified()
        self._color_by = name

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

    def to_vtk(self, target_folder, name, writer: VTKWriters = VTKWriters.binary):
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
        return (f'PolyData: #{len(self.data)}')
