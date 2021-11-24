"""ModelDataSet object to control the representation of a Polydata object."""

import pathlib
from typing import List
from .polydata import PolyData
from .data_field_info import DataFieldInfo
from ladybug.color import Color
from .vtkjs.schema import DataSetProperty, DataSet, DisplayMode, DataSetMapper
from .joined_polydata import JoinedPolyData


class ModelDataSet:
    """A dataset object in honeybee VTK model.

    This data set holds the PolyData objects as well as representation information
    for those PolyData. All the objects in ModelDataSet will have the same
    representation.
    """

    def __init__(self, name, data: List[PolyData] = None, color: Color = None) -> None:
        self.name = name
        self.data = data or []
        self.color = color
        self.display_mode = DisplayMode.Shaded
        self.color_by = None

    @ property
    def fields_info(self) -> dict:
        return {} if not self.data else self.data[0]._fields

    @ property
    def active_field_info(self) -> DataFieldInfo:
        """Get information for active field info.

        It will be the field info for the field that is set in color_by. If color_by
        is not set the first field will be used. If no field is available a default
        field will be generated.

        """
        info = self.fields_info
        color_by = self.color_by
        if not info:
            return DataFieldInfo()
        if not color_by:
            return next(iter(info.values()))
        return info[color_by]

    def add_data_fields(
        self, data: List[List], name: str, per_face: bool = True, colors=None,
            data_range=None):
        """Add data fields to PolyData objects in this dataset.

        Use this method to add data like temperature or illuminance values to PolyData
        objects. The length of the input data should match the length of the data in
        DataSet.

        Args:
            data: A list of list of values. There should be a list per data in DataSet.
                The order of data should match the order of data in DataSet. You can
                use data.identifier to match the orders before assigning them to DataSet.
            name: Name of data (e.g. Useful Daylight Autonomy.)
            per_face: A Boolean to indicate if the data is per face or per point. In
                most cases except for sensor points that are loaded as sensors the data
                are provided per face.
            colors: A Colors object that defines colors for the legend.
            data_range: A list with two values for minimum and maximum values for legend
                parameters.
        """

        assert len(self.data) == len(data), \
            f'Length of input data {len(data)} does not match the length of'\
            f' {name} in this dataset {len(self.data)}.'

        for count, d in enumerate(data):
            self.data[count].add_data(
                d, name=name, cell=per_face, colors=colors, data_range=data_range)

    @ property
    def is_empty(self):
        return len(self.data) == 0

    @ property
    def color(self) -> Color:
        """Diffuse color.

        By default the dataset will be colored by this color unless color_by property
        is set to a dataset value.
        """
        return self._color

    @ color.setter
    def color(self, value: Color):
        self._color = value if value else Color(204, 204, 204, 255)

    @ property
    def color_by(self) -> str:
        """Set the field that the DataSet should colored-by when exported to vtkjs.

        By default the dataset will be colored by surface color and not data fields.
        """
        return self._color_by

    @ color_by.setter
    def color_by(self, value: str):
        fields_info = self.fields_info
        if not value:
            self._color_by = None
            return
        else:
            assert value in fields_info, \
                f'{value} is not a valid data field for this ModelDataSet. Available ' \
                f'data fields are: {list(fields_info.keys())}'

        for data in self.data:
            data.color_by(value, fields_info[value].per_face)

        self._color_by = value

    @ property
    def opacity(self) -> float:
        """Visualization opacity."""
        return self.color.a

    @ property
    def display_mode(self) -> DisplayMode:
        """Display model (AKA Representation) mode in VTK Glance viewer.

        Valid values are:
            * Surface / Shaded
            * SurfaceWithEdges
            * Wireframe
            * Points

        Default is 0 for Surface mode.

        """
        return self._display_mode

    @ display_mode.setter
    def display_mode(self, mode: DisplayMode = DisplayMode.Surface):
        self._display_mode = mode

    @ property
    def edge_visibility(self) -> bool:
        """Edge visibility.

        The edges will be visible in Wireframe or SurfaceWithEdges modes.
        """
        if self.display_mode.value in (0, 2):
            return False
        else:
            return True

    def rgb_to_decimal(self):
        """RGB color in decimal."""
        return (self.color[0] / 255, self.color[1] / 255, self.color[2] / 255)

    def to_folder(self, folder, sub_folder=None) -> str:
        """Write data information to a folder.

        Args:
            folder: Target folder to write the dataset.
            sub_folder: Subfolder name for this dataset. By default it will be set to
                the name of the dataset.
        """
        sub_folder = sub_folder or self.name
        target_folder = pathlib.Path(folder, sub_folder)

        if len(self.data) == 0:
            print(f'ModelDataSet: {self.name} has no data to be exported to folder.')
            return
        elif len(self.data) == 1:
            data = self.data[0]
        else:
            data = JoinedPolyData.from_polydata(self.data)
        return data.to_folder(target_folder.as_posix())

    def as_data_set(self, url=None) -> DataSet:
        """Convert to a vtkjs DataSet object.

        Args:
            url: Relative path to where PolyData information should be sourced from.
                By default url will be set to ModelDataSet name assuming data is dumped
                to a folder with the same name.

        """
        prop = {
            'representation': min(self.display_mode.value, 2),
            'edgeVisibility': int(self.edge_visibility),
            'diffuseColor': [self.color.r / 255, self.color.g / 255, self.color.b / 255],
            'opacity': self.opacity / 255
        }

        ds_prop = DataSetProperty.parse_obj(prop)

        mapper = DataSetMapper()
        if self.color_by is not None:
            mapper.colorByArrayName = self.color_by

        # Getting legend information for each data added to the ModelDataSet object.
        legends = []
        if self.name == 'Grid' and self.fields_info:
            for field_info in self.fields_info.values():
                legends.append(field_info.legend_parameter._to_dict())

        data = {
            'name': self.name,
            'httpDataSetReader': {'url': url if url is not None else self.name},
            'property': ds_prop.dict(),
            'mapper': mapper.dict(),
            'legends': legends
        }

        return DataSet.parse_obj(data)

    def __repr__(self) -> str:
        return f'ModelDataSet: {self.name}' \
            f'\n  DataSets: {len(self.data)}\n  Color:{self.color}'
