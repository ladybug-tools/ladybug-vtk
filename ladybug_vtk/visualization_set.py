"""A module to support exporting a visualization set object to VTK."""
from typing import List

from .model import Model
from .model_dataset import ModelDataSet, DisplayMode
from .polydata import PolyData
from ladybug_display.visualization import AnalysisGeometry, VisualizationSet


def from_visualization_set(vis_set: VisualizationSet) -> Model:
    # translate analysis geometry
    data_sets = [
        from_analysis_geometry(ag, f'analysis_geometry_{count}')
        for count, ag in enumerate(vis_set.analysis_geometry)
    ]
    # translate context geometry
    context_data_sets = from_context_geometry(vis_set.context_geometry)
    data_sets.extend(context_data_sets)
    model = Model(datasets=data_sets)
    return model


def from_analysis_geometry(analysis_geo: AnalysisGeometry, name='Analysis_Geometry') -> List[ModelDataSet]:
    """Convert analysis geometry to a list of VTK ModelDataSets.

    Args:
        analysis_geo: An analysis geometry.
        name: An optional name for this dataset.
    """

    # translate geometry
    poly_datas: List[PolyData] = [
        geometry.to_polydata() for geometry in analysis_geo.geometry
    ]
    mappings = analysis_geo.matching_method

    for count, (data_set, mapping) in enumerate(zip(analysis_geo.data_sets, mappings)):
        # try to get the name for dataset
        if data_set.data_type:
            ds_name = data_set.data_type.name
        else:
            ds_name = 'untitled'

        if mapping == 'geometry':
            # TODO: support per object coloring
            # to support this case we need to get the number of faces/cells in PolyData
            # and duplicate the values to match the number of cells. PolyData should have
            # a method that returns the number of cells. We just need to expose it.
            raise NotImplementedError(
                'Mapping data per object is not currently supported.'
            )
        # add this dataset to polydatas
        is_cell_data = True if mapping != 'vertices' else False
        for poly_data in poly_datas:
            poly_data.add_data(
                data_set.values, name=ds_name, cell=is_cell_data,
                # we have the same challenge here as the Revit plugin. It expects a 
                # color-set instead of a length of colors. We can change that in
                # ladybug-vtk and pollination viewer
                # colors=data_set.legend_parameters.colors,
                data_range=(
                    data_set.legend_parameters.min, data_set.legend_parameters.max
                )
            )
        if count == analysis_geo.active_data:
            color_by = ds_name

    vtk_data_set = ModelDataSet(name=name, data=poly_datas)
    vtk_data_set.color_by = color_by
    vtk_data_set.display_mode = DisplayMode.SurfaceWithEdges

    return vtk_data_set


def from_context_geometry(context_geometry) -> List[ModelDataSet]:
    """Convert context geometry to a list of VTK ModelDataSets."""

    # translate geometry
    context_display = {
        'Shaded': [], 'Surface': [], 'SurfaceWithEdges': [], 'Wireframe': []
    }

    display_mode_mapper = {
        'Shaded': DisplayMode.Shaded,
        'Surface': DisplayMode.Surface,
        'SurfaceWithEdges': DisplayMode.SurfaceWithEdges,
        'Wireframe': DisplayMode.Wireframe
    }
    
    for geometry in context_geometry:
        poly_data = geometry.to_polydata()
        context_display[geometry.display_mode].append(poly_data)

    for display_mode, poly_data in context_display.items():
        if not poly_data:
            continue
        vtk_data_set = ModelDataSet(
            name=f'Context_Geometry_{display_mode}', data=poly_data
        )
        vtk_data_set.display_mode = display_mode_mapper[display_mode]

        yield vtk_data_set
