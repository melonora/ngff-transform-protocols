from ome_zarr_models._v06.coordinate_transforms import Identity, Translation
from ngff_transform_protocols.protocols.transform_protocols import IdentityProtocol, TransformProtocol

from typing import Literal, NamedTuple

def test_identity_protocol():
    transform = Identity(name="example", type="identity", input="input_cs", output="output_cs")
    assert isinstance(transform, TransformProtocol)


    # transform = FakeTransform(name="example", type="identity", input="input_cs", output="output_cs")
    # protocol_members = set(IdentityProtocol.__protocol_attrs__)
    # missing = [m for m in protocol_members if not hasattr(transform, m)]
    # print("Missing members:", missing)
    #
    # assert isinstance(transform, IdentityProtocol)

