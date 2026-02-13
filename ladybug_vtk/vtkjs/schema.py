"""Schema for VTKJS objects."""
import json
import pathlib
from typing import Dict, List, Union
import enum

from pydantic import BaseModel, Field, field_validator
from ladybug_display_schema.visualization import LegendParameters, DataType, GenericDataType


class DisplayMode(enum.Enum):
    """Display mode."""
    Surface = 2
    SurfaceWithEdges = 3
    Wireframe = 1
    Points = 0


class Camera(BaseModel):
    """Camera in vtkjs viewer."""
    focalPoint: List[float] = Field(
        [2.5, 5, 1.5],
        description='Camera focal point.',
        max_length=3, min_length=3
    )
    position: List[float] = Field(
        [19.3843, -6.75305, 10.2683],
        description='Camera position.',
        max_length=3, min_length=3
    )
    viewUp: List[float] = Field(
        [-0.303079, 0.250543, 0.919441],
        description='View up vector.',
        max_length=3, min_length=3
    )


class DataSetResource(BaseModel):
    """Path to a data resource."""
    url: str = Field(
        ..., description='Relative path to data resource.'
    )


class DataSetActor(BaseModel):
    """A Dataset actor."""
    # Using lambda for simple list factories to avoid shared state
    origin: List[float] = Field(default_factory=lambda: [0, 0, 0])
    scale: List[float] = Field(default_factory=lambda: [1, 1, 1])
    position: List[float] = Field(default_factory=lambda: [0, 0, 0])


class DataSetMapper(BaseModel):
    colorByArrayName: str = Field('')
    colorMode: int = Field(0)
    scalarMode: int = Field(4)


class DataSetProperty(BaseModel):
    representation: int = Field(2)
    edgeVisibility: int = Field(0)
    diffuseColor: List[float] = Field(
        [0.8, 0.8, 0.8],
        description='Surface color.',
        max_length=3, min_length=3
    )
    pointSize: int = Field(5)
    opacity: float = Field(1)


class DataSetMetaData(BaseModel):
    legend_parameters: Union[LegendParameters, None] = Field(None, description='Legend Parameters.')
    unit: str = Field('', description='Unit as a string')
    data_type: Union[DataType, GenericDataType] = Field(
        default_factory=lambda: GenericDataType(name='', base_unit=''),
        description='Data type for data set.'
    )


class DataSet(BaseModel):
    """A VTKJS dataset."""
    name: str = Field(..., description='DataSet name.')
    type: str = Field('httpDataSetReader')
    httpDataSetReader: DataSetResource = Field(...)

    actor: DataSetActor = Field(default_factory=DataSetActor)

    actorRotation: List[float] = Field(
        [0, 0, 0, 1],
        description='Actor rotation axis.',
        max_length=4, min_length=4
    )

    mapper: DataSetMapper = Field(default_factory=DataSetMapper)
    property: DataSetProperty = Field(default_factory=DataSetProperty)

    legends: List[dict] = Field(
        default_factory=list,
        deprecated=True,
        description='This field is deprecated. Use the metadata field instead.'
    )
    metadata: List[DataSetMetaData] = Field(
        default_factory=list,
        description='List of metadata objects for each dataset.'
    )
    hidden: bool = Field(
        False, description='A boolean to note whether the geometry is hidden by default '
        'and must be un-hidden to be visible in the 3D scene.'
    )


class IndexJSON(BaseModel):
    """VTKJS index class.

    These information will be translated to an index.json file.
    """
    version: int = 1
    background: List[float] = Field(
        [1, 1, 1],
        description='Background color.',
        max_length=3, min_length=3
    )
    camera: Camera = Field(
        default_factory=Camera,
        description='Initial camera in the viewer.'
    )
    centerOfRotation: List[float] = Field(
        [2.5, 5, 1.5],
        description='X, Y, Z for center of rotation.',
        max_length=3, min_length=3
    )
    scene: List[DataSet] = Field(
        default_factory=list,
        description='List of data set in viewer.'
    )
    lookupTables: Dict = Field(
        default_factory=dict
    )

    @field_validator('scene', mode='before')
    @classmethod
    def empty_list(cls, v):
        return [] if v is None else v

    @field_validator('lookupTables', mode='before')
    @classmethod
    def empty_dict(cls, v):
        return {} if v is None else v

    def to_json(self, folder: str) -> str:
        """Write the settings as index.json."""
        data = self.model_dump()
        target_folder = pathlib.Path(folder)
        target_folder.mkdir(parents=True, exist_ok=True)
        index_file = pathlib.Path(target_folder, 'index.json')
        index_file.write_text(json.dumps(data))
        return index_file.as_posix()
