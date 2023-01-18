"""DisplayPolyData object to control the representation of a Polydata object."""

import pathlib
import uuid
from typing import List, Union

from ladybug.color import Color
from ladybug_display.visualization import AnalysisGeometry, ContextGeometry, \
    DisplayMesh3D, Mesh3D, Point3D, DisplayPoint3D, Mesh2D, DisplayMesh2D

from .from_geometry import from_points3d
from .polydata import PolyData
from .joined_polydata import JoinedPolyData
from .vtkjs.schema import DataSetProperty, DataSet, DisplayMode, DataSetMapper


display_mode_mapper = {
    'Surface': DisplayMode.Surface,
    'SurfaceWithEdges': DisplayMode.SurfaceWithEdges,
    'Wireframe': DisplayMode.Wireframe,
    'Points': DisplayMode.Points
}


class DisplayPolyData:
    """A collection of PolyData with display attributes.

    All the PolyData must have data with the same names attached to them.

    This object is similar to an AnalysisGeometry object in ladybug-display.

    Args:
        name: A display name.
        identifier: A unique identifier for this DisplayPolyData. This identifier should
            be unique among all the DisplayPolyData in a VisualizationSet.
        polydata: A list of PolyData objects.
        color: A Ladybug color to set the diffuse color for DisplayPolyData to use when
            there is no data available.
        display_mode: Display model. It can be set to Surface, SurfaceWithEdges,
            Wireframe and Points.
        hidden: A boolean to note whether the geometry is hidden by default and must be
            un-hidden to be visible in the 3D scene. Default is False.

    """

    def __init__(
        self, name: str, identifier: str, *, polydata: List[PolyData] = None,
        color: Color = None, display_mode: DisplayMode = DisplayMode.Surface,
        hidden: bool = False
            ) -> None:
        self.name = name
        self.identifier = identifier or str(uuid.uuid4())
        polydata = polydata or []
        self.polydata = [pd for pd in polydata if pd]  # remove None values
        if len(self.polydata) != len(polydata):
            print(f'{self.name} includes invalid Polydata.')
        self.color = color or Color(204, 204, 204, 255)
        self.display_mode = display_mode
        self.hidden = hidden

    @classmethod
    def from_visualization_geometry(
        cls, geometry: Union[AnalysisGeometry, ContextGeometry]
            ) -> 'DisplayPolyData':

        if isinstance(geometry, AnalysisGeometry):
            return cls.from_analysis_geometry(geometry)
        else:
            return cls.from_context_geometry(geometry)

    @classmethod
    def from_analysis_geometry(cls, geometry: AnalysisGeometry) -> 'DisplayPolyData':
        """Create DisplayPolyData from an AnalysisGeometry."""
        geometries = geometry.geometry
        poly_datas: List[PolyData] = [geo.to_polydata() for geo in geometries]
        matching_method = geometry.matching_method

        all_mesh = all(
            isinstance(geo, (DisplayMesh3D, Mesh3D, Mesh2D, DisplayMesh2D))
            for geo in geometries
        )

        all_points = all(
            isinstance(geo, (DisplayPoint3D, Point3D)) for geo in geometries
        )
        if all_points:
            # all the geometries are Points - translate them to a single Polydata
            poly_datas = [from_points3d(geometries)]
            matching_method = 'vertices'

        for ds_count, data_set in enumerate(geometry.data_sets):
            ds_name = PolyData._get_dataset_name(data_set)
            if matching_method == 'geometries' and not all_points:
                data_set_values = []
                # generate the data per face of based on the number of faces of geometry
                for value, poly_data in zip(data_set.values, poly_datas):
                    face_count = poly_data.GetNumberOfCells()
                    values = [value] * face_count
                    data_set_values.append(values)
                matching_method = 'faces'
            elif all_points:
                data_set_values = [data_set.values]
            elif all_mesh:
                # break down the values for each mesh based on the number of faces
                # or the number of vertices
                if len(geometries) == 1:
                    data_set_values = [data_set.values]
                else:
                    data_set_values = []
                    starting_index = 0
                    for geo in geometries:
                        if matching_method == 'faces':
                            count = len(geo.faces)
                        else:
                            count = len(geo.vertices)
                        values = data_set.values[starting_index: starting_index + count]
                        data_set_values.append(values)
                        starting_index += count
            else:
                print(data_set)
                for geometry in geometries:
                    print(type(geometry))
                assert False, '^ Unknown data mapping combination.'

            # add this dataset to polydatas
            for count, poly_data in enumerate(poly_datas):
                values = data_set_values[count]
                poly_data.add_data(
                    data=values, name=ds_name,
                    per_face=not matching_method == 'vertices',
                    legend_parameters=data_set.legend_parameters,
                    unit=data_set.unit, data_type=data_set.data_type
                )
            if ds_count == geometry.active_data:
                color_by = ds_name

        vtk_data_set = cls(
            name=geometry.display_name, identifier=geometry.identifier,
            polydata=poly_datas,
            display_mode=display_mode_mapper[geometry.display_mode],
            hidden=geometry.hidden
        )
        vtk_data_set.color_by = color_by

        return vtk_data_set

    @classmethod
    def from_context_geometry(cls, geometry: ContextGeometry) -> 'DisplayPolyData':
        """Create DisplayPolyData from a ContextGeometry."""
        # context geometry
        # the assumption is that all the geometries under the same context geometry
        # have the same display mode and color. We pick the first item.
        first_geometry = geometry.geometry[0]
        all_points = all(
            isinstance(geo, (DisplayPoint3D, Point3D)) for geo in geometry.geometry
        )
        if all_points:
            poly_datas = [from_points3d(geometry.geometry)]
        else:
            poly_datas = [geometry.to_polydata() for geometry in geometry.geometry]

        try:
            display_mode = first_geometry.display_mode
        except AttributeError:
            # not a display geometry
            display_mode = DisplayMode.Surface
        else:
            display_mode = display_mode_mapper[display_mode]

        try:
            color = first_geometry.color
        except AttributeError:
            color = None

        vtk_data_set = cls(
            name=geometry.display_name,
            identifier=geometry.identifier,
            polydata=poly_datas,
            display_mode=display_mode,
            color=color,
            hidden=geometry.hidden
        )

        return vtk_data_set

    @property
    def is_empty(self):
        return len(self.polydata) == 0

    @property
    def color(self) -> Color:
        """Diffuse color.

        By default the dataset will be colored by this color unless color_by property
        is set to a dataset value.
        """
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value if value else Color(204, 204, 204, 255)

    @property
    def color_by(self) -> str:
        """Get and set the field that the DataSet should colored-by when exported to vtkjs.

        By default the dataset will be colored by surface color and not data.
        """
        return self.polydata[0].color_by

    @color_by.setter
    def color_by(self, value: str):
        for data in self.polydata:
            data.color_by = value

    @property
    def opacity(self) -> float:
        """Get and set the visualization opacity."""
        return self.color.a

    @opacity.setter
    def opacity(self, value):
        color = self.color.duplicate()
        color.a = value

    @property
    def display_mode(self) -> DisplayMode:
        """Display model (AKA Representation) mode in VTK Glance viewer.

        Valid values are:
            * Surface
            * SurfaceWithEdges
            * Wireframe
            * Points

        Default is 0 for Surface mode.

        """
        return self._display_mode

    @display_mode.setter
    def display_mode(self, mode: DisplayMode = DisplayMode.Surface):
        self._display_mode = mode

    @property
    def hidden(self) -> bool:
        """Visualization default state on load.

        A boolean to note whether the geometry is hidden by default and must be
        un-hidden to be visible in the 3D scene.
        """
        return self._hidden

    @hidden.setter
    def hidden(self, value: bool):
        self._hidden = bool(value)

    @property
    def edge_visibility(self) -> bool:
        """Edge visibility.

        The edges will be visible in Wireframe or SurfaceWithEdges modes.
        """
        if self.display_mode.value in (0, 2):
            return False
        else:
            return True

    def to_folder(self, folder, sub_folder=None) -> str:
        """Write data information to a folder.

        Args:
            folder: Target folder to write the dataset.
            sub_folder: Subfolder name for this dataset. By default it will be set to
                the name of the dataset.
        """
        sub_folder = sub_folder or self.identifier
        target_folder = pathlib.Path(folder, sub_folder)

        if len(self.polydata) == 0:
            return
        elif len(self.polydata) == 1:
            data = self.polydata[0]
        else:
            data = JoinedPolyData.from_polydata(self.polydata)
        return data.to_folder(target_folder.as_posix())

    def to_vtk_dataset(self) -> DataSet:
        """Convert to a vtkjs DataSet object."""
        prop = {
            'representation': min(self.display_mode.value, 2),
            'edgeVisibility': int(self.edge_visibility),
            'diffuseColor': [self.color.r / 255, self.color.g / 255, self.color.b / 255],
            'opacity': self.opacity / 255
        }

        ds_prop = DataSetProperty.parse_obj(prop)

        mapper = DataSetMapper()
        if self.color_by:
            mapper.colorByArrayName = self.color_by

        # Collect meta data for each data attached to polydata. Since all the polydata
        # in a DisplayPolyData most have the same metadata we pick the first one
        metadata = [
            metadata.to_vtk_metadata().dict()
            for metadata in self.polydata[0].data.values()
        ]

        data = {
            'name': self.name,
            'httpDataSetReader': {'url': self.identifier},
            'property': ds_prop.dict(),
            'mapper': mapper.dict(),
            'metadata': metadata,
            'hidden': self.hidden
        }

        return DataSet.parse_obj(data)

    def __repr__(self) -> str:
        return f'DisplayPolyData: {self.name}' \
            f'\n  DataSets: #{len(self.polydata)}\n  Color: {self.color}'
