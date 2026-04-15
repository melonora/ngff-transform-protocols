from typing import Protocol, runtime_checkable, Sequence, Literal

@runtime_checkable
class AxisLike(Protocol):
    """
    Structural contract for a single axis in a coordinate system.
    Matches `Axis` and any duck-typed equivalent.
    """
    name: str | None
    type: str | None
    discrete: bool | None
    # TODO: should we keep this broad?
    unit: object
    longName: str | None


@runtime_checkable
class CoordinateSystemLike(Protocol):
    """
    Structural contract for a full coordinate system.
    Matches `CoordinateSystem` and any duck-typed equivalent.
    """
    name: str
    axes: tuple[AxisLike, ...]

    @property
    def ndim(self) -> int: ...


@runtime_checkable
class CoordinateSystemIdentifiable(Protocol):
    """
    Structural contract for a reference to a coordinate system defined
    elsewhere — carries a name and an optional path.
    Matches `CoordinateSystemIdentifier`.
    """
    name: str
    path: str | None

TCoordSysIdentifier = CoordinateSystemIdentifiable| str | None

@runtime_checkable
class TransformProtocol(Protocol):
    type: str
    input: TCoordSysIdentifier
    output: TCoordSysIdentifier
    name: str | None
    has_inverse: bool

    def get_inverse(self) -> "TransformProtocol": ...

    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...

    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class IdentityProtocol(TransformProtocol, Protocol):
    type: Literal["identity"]


@runtime_checkable
class MapAxisProtocol(TransformProtocol, Protocol):
    type: Literal["mapAxis"]
    mapAxis: tuple[int, ...]

    @property
    def ndim(self) -> int: ...


@runtime_checkable
class TranslationProtocol(TransformProtocol, Protocol):
    type: Literal["translation"]
    translation: tuple[float, ...] | None
    path: str | None

    @property
    def ndim(self) -> int: ...
    @property
    def translation_vector(self) -> tuple[float, ...]: ...


@runtime_checkable
class ScaleProtocol(TransformProtocol, Protocol):
    type: Literal["scale"]
    scale: tuple[float, ...] | None
    path: str | None

    @property
    def ndim(self) -> int: ...
    @property
    def scale_vector(self) -> tuple[float, ...]: ...


@runtime_checkable
class AffineProtocol(TransformProtocol, Protocol):
    type: Literal["affine"]
    affine: tuple[tuple[float, ...], ...] | None
    path: str | None

    @property
    def ndim(self) -> int: ...
    @property
    def affine_matrix(self) -> tuple[tuple[float, ...], ...]: ...


@runtime_checkable
class RotationProtocol(TransformProtocol, Protocol):
    type: Literal["rotation"]
    rotation: tuple[tuple[float, ...], ...] | None
    path: str | None

    @property
    def ndim(self) -> int: ...
    @property
    def rotation_matrix(self) -> tuple[tuple[float, ...], ...]: ...


@runtime_checkable
class SequenceProtocol(TransformProtocol, Protocol):
    type: Literal["sequence"]
    transformations: tuple[TransformProtocol, ...]

    @property
    def ndim(self) -> int: ...

    def add_transform(self, transform: TransformProtocol) -> "SequenceProtocol": ...


@runtime_checkable
class DisplacementsProtocol(TransformProtocol, Protocol):
    type: Literal["displacements"]
    path: str


@runtime_checkable
class CoordinatesProtocol(TransformProtocol, Protocol):
    type: Literal["coordinates"]
    path: str


@runtime_checkable
class BijectionProtocol(TransformProtocol, Protocol):
    type: Literal["bijection"]
    forward: TransformProtocol
    inverse: TransformProtocol


@runtime_checkable
class ByDimensionTransformProtocol(Protocol):
    transformation: TransformProtocol
    input_axes: tuple[int, ...]
    output_axes: tuple[int, ...]

@runtime_checkable
class ByDimensionProtocol(TransformProtocol, Protocol):
    type: Literal["byDimension"]
    transformations: tuple[ByDimensionTransformProtocol, ...]


AnyTransformProtocol = (
        IdentityProtocol |
        MapAxisProtocol |
        TranslationProtocol |
        ScaleProtocol |
        AffineProtocol |
        RotationProtocol |
        SequenceProtocol |
        DisplacementsProtocol |
        CoordinatesProtocol |
        BijectionProtocol |
        ByDimensionProtocol
)