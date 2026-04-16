from ome_zarr_models._v06.coordinate_transforms import Identity
from ngff_transform_protocols.protocols.transform_protocols import IdentityProtocol, TransformProtocol

from typing import Literal, NamedTuple

class FakeTransform(NamedTuple):
    invalid_name: str
    type: Literal["identity"]
    input: str
    output: str

def test_identity_protocol():
    transform = Identity(name="example", type="identity", input="input_cs", output="output_cs")
    assert isinstance(transform, IdentityProtocol)
