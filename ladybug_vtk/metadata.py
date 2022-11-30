from ladybug_display.visualization import VisualizationMetaData, LegendParameters
from ladybug_display_schema.visualization import GenericDataType
from .vtkjs.schema import DataSetMetaData


class PolyDataMetaData(VisualizationMetaData):
    """Metadata for a PolyData object.

    Args:
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
        per_face: A Boolean to indicate if the data is per cell or per point. In
            most cases except for sensor points that are loaded as sensors the data
            are provided per cell.

    """

    def __init__(self, legend_parameters=None, data_type=None, unit=None, per_face=True):
        legend_parameters = legend_parameters or LegendParameters()
        super().__init__(legend_parameters, data_type, unit)
        self.per_face = per_face  # indicate if data is per cell or per point

    def to_vtk_metadata(self):
        default_data_type = GenericDataType(name='', base_unit='')
        data = {
            'legend_parameters': None if not self.legend_parameters
            else self.legend_parameters.to_dict(),
            'data_type': default_data_type if not self.data_type
            else self.data_type.to_dict(),
            'unit': self.unit or ''
        }

        return DataSetMetaData.parse_obj(data)
