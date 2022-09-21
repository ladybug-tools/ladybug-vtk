"""A module to support exporting a visualization set object to VTK."""
from typing import List

from .model import Model
from .model_dataset import ModelDataSet, DisplayMode
from .polydata import PolyData
from ladybug_display_schema.visualization import AnalysisGeometry, VisualizationSet

from enum import Enum


class DataMapping(Enum):
    """An enumerator for how the data is expected to be mapped."""
    object = 0
    face = 1
    vertices = 2


def from_visualization_set(vis_set: VisualizationSet) -> Model:
    # translate analysis geometry
    ag = from_analysis_geometry(vis_set.analysis_geometry)
    # translate context geometry
    # TODO: Add context geometry once we make the decision about grouping/layers
    # I also need an example with context geometry for testing
    # cg = from_context_geometry(vis_set.context_geometry)
    model = Model(datasets=ag)
    return model


def _data_mapping(analysis_geo: AnalysisGeometry) -> List[DataMapping]:
    """Check if the data is cell data or point data for each dataset.

    This function might be a useful method for the AnalysisGeometry itself.
    """
    mapping = []
    objects_count = len(analysis_geo.geometry)
    # for now let's assume all the geometries follow the same rule for how the values
    # will be assigned
    geometry = analysis_geo.geometry[0]
    try:
        # mesh
        face_count = len(geometry.faces)
    except AttributeError:
        try:
            # polyface
            face_count = len(geometry.face_indices)
        except AttributeError:
            face_count = 1 # a face 3d
    try:
        # mesh or polyface
        vertices_count = len(geometry.vertices)
    except AttributeError:
        vertices_count = 0

    for dataset in analysis_geo.data_sets:
        if len(dataset.values) == objects_count:
            mapping.append(DataMapping.object)
        elif len(dataset.values) == face_count:
            mapping.append(DataMapping.face)
        elif len(dataset.values) == vertices_count:
            mapping.append(DataMapping.vertices)
        else:
            # we should never end up here if the input analysis geometry is valid
            raise ValueError(
                'Length of input data does not match the length of the geometry.'
            )

    return mapping


def from_analysis_geometry(analysis_geo: AnalysisGeometry) -> List[ModelDataSet]:
    """Convert analysis geometry to a list of VTK ModelDataSets."""

    # translate geometry
    poly_datas: List[PolyData] = [geometry.to_polydata() for geometry in analysis_geo.geometry]
    mappings = _data_mapping(analysis_geo)

    for count, (data_set, mapping) in enumerate(zip(analysis_geo.data_sets, mappings)):
        # try to get the name for dataset
        if data_set.data_type:
            name = data_set.data_type.name
        else:
            name = 'untitled'

        if mapping == DataMapping.object:
            # TODO: support per object coloring
            # to support this case we need to get the number of faces/cells in PolyData
            # and duplicate the values to match the number of cells. PolyData should have
            # a method that returns the number of cells. We just need to expose it.
            raise NotImplementedError(
                'Mapping data per object is not currently supported.'
            )
        # add this dataset to polydatas
        is_cell_data = True if mapping != DataMapping.vertices else False
        for poly_data in poly_datas:
            poly_data.add_data(
                data_set.values, name=name, cell=is_cell_data,
                # we have the same challenge here as the Revit plugin. It expects a 
                # color-set instead of a length of colors. We can change that in
                # ladybug-vtk and pollination viewer
                # colors=data_set.legend_parameters.colors,
                data_range=(
                    data_set.legend_parameters.min, data_set.legend_parameters.max
                )
            )
        if count == analysis_geo.active_data:
            color_by = name

    vtk_data_set = ModelDataSet(name='Analysis_Geometry', data=poly_datas)
    vtk_data_set.color_by = color_by
    vtk_data_set.display_mode = DisplayMode.SurfaceWithEdges

    return vtk_data_set
