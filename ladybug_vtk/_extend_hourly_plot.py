from pathlib import Path
from ladybug.hourlyplot import HourlyPlot
from ladybug_geometry.geometry3d import Vector3D
from ladybug.color import Color

from ladybug_vtk.vtkjs.schema import DisplayMode
from .from_geometry import from_text
from .display_polydata import DisplayPolyData
from .visualization_set import VisualizationSet


def hourly_plot_to_vtkjs(
    self, output_folder: str, file_name: str = 'hourly plot'
) -> Path:
    """
    Export the HourlyPlot to a vtkjs file.

    Args:
        output_folder: Path to the target folder to write the vtkjs file.
        file_name: Output file name. Defaults to hourly plot.

    Returns:
        A pathlib Path object to the vtkjs file.
    """

    datasets = []

    lines = []
    # hour lines
    hour_lines3d_polydata = [line.to_polydata() for line in self.custom_hour_lines3d(
        hour_labels=[0, 6, 12, 18, 24])]
    lines.extend(hour_lines3d_polydata)

    # month lines
    month_lines3d_polydata = [line.to_polydata() for line in self.month_lines3d]
    lines.extend(month_lines3d_polydata)

    # border polyline
    border_polydata = self.chart_border3d.to_polydata()
    lines.append(border_polydata)
    datasets.append(
        DisplayPolyData('Hourly Plot::Lines', 'lines', polydata=lines, color=Color()))

    # labels
    labels = []
    left_vector = Vector3D(-1, 0, 0) * 5
    down_vector = Vector3D(0, -1, 0) * 3

    # month labels
    month_labels_polydata = [
        from_text(label, plane=self.month_label_points3d[count].
                move(left_vector).move(down_vector), height=4)
        for count, label in enumerate(self.month_labels)]
    labels.extend(month_labels_polydata)

    # hour labels
    hour_left_vector = Vector3D(-1, 0, 0) * 15
    hour_labels_polydata = [
        from_text(label, plane=self.hour_label_points3d[count].
                move(hour_left_vector).move(down_vector), height=4)
        for count, label in enumerate(self.hour_labels)]
    labels.extend(hour_labels_polydata)

    # title text
    title_polydata = from_text(self.title_text, plane=self.lower_title_location.o.move(
        left_vector).move(down_vector), height=4)
    labels.append(title_polydata)
    datasets.append(
        DisplayPolyData('Hourly Plot::Labels', 'labels', polydata=labels, color=Color()))

    # data
    mesh_polydata = self.colored_mesh3d.to_polydata()
    name = self.data_collection.header.data_type.name
    mesh_polydata.add_data(
        self.data_collection.values, name=name, per_face=True,
        data_type=self.data_collection.header.data_type,
        unit=self.data_collection.header.unit
    )

    mesh_dataset = DisplayPolyData(
        name='Data', identifier='data', polydata=[mesh_polydata],
        display_mode=DisplayMode.SurfaceWithEdges
    )
    mesh_dataset.color_by = name
    datasets.append(mesh_dataset)

    # write all datasets to a vtkjs file
    hourly_plot = VisualizationSet(datasets=datasets)

    return Path(hourly_plot.to_vtkjs(output_folder, file_name))


HourlyPlot.to_vtkjs = hourly_plot_to_vtkjs
