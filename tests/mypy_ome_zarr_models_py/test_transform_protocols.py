from typing import Literal, Sequence
from ome_zarr_models._v06.coordinate_transforms import Identity, MapAxis
from ngff_transform_protocols.protocols.transform_protocols import (  # type: ignore[import-untyped]
    TCoordSysIdentifier,
    TransformProtocol,
    AffineProtocol,
    IdentityProtocol,
)


class FakeAffine:
    type: Literal["affine"] = "affine"
    input: TCoordSysIdentifier = None
    output: TCoordSysIdentifier = None
    name: str | None = None
    has_inverse: bool = False
    affine: tuple[tuple[float, ...], ...] | None = None
    path: str | None = None

    @property
    def ndim(self) -> int:
        return 0

    @property
    def affine_matrix(self) -> tuple[tuple[float, ...], ...]:
        return ((1.0,),)

    def get_inverse(self) -> TransformProtocol:
        return self  # type: ignore[return-value]

    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]:
        return tuple(point)

    def as_affine(self) -> AffineProtocol:
        return self  # type: ignore[return-value]


class FakeTransform:
    """Conforms to IdentityProtocol."""
    type: Literal["identity"] = "identity"
    name: str | None = "example"
    input: TCoordSysIdentifier = None
    output: TCoordSysIdentifier = None
    has_inverse: bool = False

    def get_inverse(self) -> TransformProtocol:
        return self  # type: ignore[return-value]

    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]:
        return tuple(point)

    def as_affine(self) -> AffineProtocol:
        return FakeAffine()


class FakeBadTransform:
    """Does NOT conform to IdentityProtocol, type is str, not Literal["identity"]."""
    type: str = "identity"
    name: str | None = "example"
    input: TCoordSysIdentifier = None
    output: TCoordSysIdentifier = None
    has_inverse: bool = False

    def get_inverse(self) -> TransformProtocol:
        return self  ## type: ignore[return-value]

    def transform_point(self, point: Sequence[float]) -> tuple[float, ...]:
        return tuple(point)

    def as_affine(self) -> AffineProtocol:
        return FakeAffine()


def test_compliant_transform() -> None:
    _: IdentityProtocol = FakeTransform()  # mypy passes, FakeTransform satisfies the protocol


def test_non_compliant_transform() -> None:
    _: IdentityProtocol = FakeBadTransform()  # type: ignore[assignment]

def test_identity_protocol() -> None:
    transform = Identity(name="example", type="identity", input="input_cs", output="output_cs")
    _: IdentityProtocol = transform

def test_map_axis_not_identity() -> None:
    transform = MapAxis(input="input_cs", output="output_cs", mapAxis=(2, 0, 1))
    _: IdentityProtocol = transform