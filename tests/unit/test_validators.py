import pytest
from genie.testbed import load
from tests.helpers.validators import (
    all_bgp_neighbors_established,
    vnis_active,
)


@pytest.fixture(scope="module")
def leaf1():
    tb = load("testbed.yaml")
    dev = tb.devices["leaf1"]
    dev.connect(log_stdout=False)
    yield dev
    dev.disconnect()


@pytest.fixture(scope="module")
def leaf1_bad():
    tb = load("testbed.yaml")
    bad_cmd = tb.devices["leaf1"].connections.cli.command.replace(
        "leaf1.yaml", "leaf1_bad.yaml"
    )
    tb.devices["leaf1"].connections.cli.command = bad_cmd
    dev = tb.devices["leaf1"]
    dev.connect(log_stdout=False)
    yield dev
    dev.disconnect()


def test_bgp_neighbors_up(leaf1):
    parsed = leaf1.parse("show bgp l2vpn evpn summary")
    ok, msg = all_bgp_neighbors_established(parsed)
    assert ok, msg


def test_bgp_neighbor_failure(leaf1_bad):
    parsed = leaf1_bad.parse("show bgp l2vpn evpn summary")
    ok, msg = all_bgp_neighbors_established(parsed)
    assert not ok and "state" in msg


def test_vni_down_detected(leaf1_bad):
    parsed = leaf1_bad.parse("show nve vni")
    ok, msg = vnis_active(parsed)
    assert not ok and "VNI(s) not up" in msg
