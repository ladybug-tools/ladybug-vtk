"""Data object for Data to be mounted on Polydata."""

from typing import Tuple
from .legend_parameter import LegendParameter, ColorSets


class DataFieldInfo:
    """Data info for metadata that is added to Polydata.

    This object hosts information about the data that is added to polydata.
    This object consists name, min and max values in the data, and the color
    theme to be used in visualization of the data.

    Args:
        name: A string representing the name of for data.
        range: A tuple of min, max values as either integers or floats.
            Defaults to None which will create a range of minimum and maximum
            values in the data.
        colors: A Colors object that defines colors for the legend.
            Defaults to Ecotect colorset.
        per_face : A Boolean to indicate if the data is per face or per point. In
            most cases except for sensor points that are loaded as sensors the data
            are provided per face.
    """

    def __init__(self, name: str = 'default', range: Tuple[float, float] = None,
                 colors: ColorSets = ColorSets.ecotect, per_face: bool = True
                 ) -> None:
        self.name = name
        self._range = range
        self.per_face = per_face
        self._legend_param = LegendParameter(name=name, colors=colors, auto_range=range)

    @property
    def legend_parameter(self) -> LegendParameter:
        """Legend associated with the DataFieldInfo object."""
        return self._legend_param

    @property
    def range(self) -> Tuple[float, float]:
        """Range is a tuple of minimum and maximum values.

        If these minimum and maximum values are not provided, they are calculated
        automatically. In such a case, the minimum and maximum values in the data are
        used.
        """
        return self._range
