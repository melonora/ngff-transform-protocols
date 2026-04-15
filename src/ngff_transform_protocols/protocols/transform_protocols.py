from typing import Protocol, runtime_checkable, Sequence, Literal

@runtime_checkable
class TransformProtocol(Protocol):
    type: str
    input: str | None
    output: str | None
    name: str | None

    @property
    def has_inverse(self) -> bool: ...

    def get_inverse(self) -> "TransformProtocol": ...

    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...

    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class InvertibleTransform(Protocol):
    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "TransformProtocol": ...


@runtime_checkable
class AffineConvertible(Protocol):
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class PointTransformable(Protocol):
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...


# ── Concrete transform protocols ──────────────────────────────────────────────

@runtime_checkable
class IdentityProtocol(TransformProtocol, Protocol):
    type: Literal["identity"]

    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "IdentityProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class MapAxisProtocol(TransformProtocol, Protocol):
    type: Literal["mapAxis"]
    mapAxis: tuple[int, ...]

    @property
    def ndim(self) -> int: ...
    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "MapAxisProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class TranslationProtocol(TransformProtocol, Protocol):
    type: Literal["translation"]
    translation: tuple[float, ...] | None
    path: str | None

    @property
    def ndim(self) -> int: ...
    @property
    def translation_vector(self) -> tuple[float, ...]: ...
    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "TranslationProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class ScaleProtocol(TransformProtocol, Protocol):
    type: Literal["scale"]
    scale: tuple[float, ...] | None
    path: str | None

    @property
    def ndim(self) -> int: ...
    @property
    def scale_vector(self) -> tuple[float, ...]: ...
    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "ScaleProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class AffineProtocol(TransformProtocol, Protocol):
    type: Literal["affine"]
    affine: tuple[tuple[float, ...], ...] | None
    path: str | None

    @property
    def ndim(self) -> int: ...
    @property
    def affine_matrix(self) -> tuple[tuple[float, ...], ...]: ...
    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "AffineProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class RotationProtocol(TransformProtocol, Protocol):
    type: Literal["rotation"]
    rotation: tuple[tuple[float, ...], ...] | None
    path: str | None

    @property
    def ndim(self) -> int: ...
    @property
    def rotation_matrix(self) -> tuple[tuple[float, ...], ...]: ...
    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "RotationProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class SequenceProtocol(TransformProtocol, Protocol):
    type: Literal["sequence"]
    transformations: tuple[TransformProtocol, ...]

    @property
    def ndim(self) -> int: ...
    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "SequenceProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...
    def add_transform(self, transform: TransformProtocol) -> "SequenceProtocol": ...


@runtime_checkable
class DisplacementsProtocol(TransformProtocol, Protocol):
    type: Literal["displacements"]
    path: str

    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "DisplacementsProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class CoordinatesProtocol(TransformProtocol, Protocol):
    type: Literal["coordinates"]
    path: str

    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "CoordinatesProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...


@runtime_checkable
class BijectionProtocol(TransformProtocol, Protocol):
    type: Literal["bijection"]
    forward: TransformProtocol
    inverse: TransformProtocol

    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "BijectionProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...

@runtime_checkable
class ByDimensionTransformProtocol(Protocol):
    transformation: TransformProtocol
    input_axes: tuple[int, ...]
    output_axes: tuple[int, ...]

@runtime_checkable
class ByDimensionProtocol(TransformProtocol, Protocol):
    type: Literal["byDimension"]
    transformations: tuple[ByDimensionTransformProtocol, ...]

    @property
    def has_inverse(self) -> bool: ...
    def get_inverse(self) -> "ByDimensionProtocol": ...
    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]: ...
    def as_affine(self) -> "AffineProtocol": ...

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