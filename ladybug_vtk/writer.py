"""Writer class to Support Polydata and JoindPolydata Class."""
import pathlib
import vtk
from enum import Enum
from typing import Union


class VTKWriters(Enum):
    """Vtk writers."""
    legacy = 'vtk'
    binary = 'vtp'


def write_to_file(
        polydata: Union[vtk.vtkPolyData, vtk.vtkAppendPolyData],
        target_folder: str, file_name: str,
        writer: VTKWriters = VTKWriters.binary):
    """Write vtkPolyData to a file."""

    extension = writer.value

    if writer.name == 'legacy':
        _writer = vtk.vtkPolyDataWriter()
    else:
        _writer = vtk.vtkXMLPolyDataWriter()
        if writer.name == 'binary':
            _writer.SetDataModeToBinary()
        else:
            _writer.SetDataModeToAscii()

    file_path = pathlib.Path(target_folder, f'{file_name}.{extension}')

    _writer.SetFileName(file_path.as_posix())

    if isinstance(polydata, vtk.vtkPolyData):
        _writer.SetInputData(polydata)
    else:
        _writer.SetInputConnection(polydata.GetOutputPort())

    _writer.Write()
    return file_path.as_posix()


def write_to_folder(polydata: Union[vtk.vtkPolyData, vtk.vtkAppendPolyData],
                    target_folder: str):
    """Write PolyData to a folder using vtkJSONDataSetWriter."""

    writer = vtk.vtkJSONDataSetWriter()
    folder = pathlib.Path(target_folder)
    folder.mkdir(parents=True, exist_ok=True)
    try:
        writer.SetFileName(folder.as_posix())
    except:
        writer.SetArchiveName(folder.as_posix())

    if isinstance(polydata, vtk.vtkPolyData):
        writer.SetInputData(polydata)
    else:
        writer.SetInputConnection(polydata.GetOutputPort())
    writer.Write()
    return folder.as_posix()
