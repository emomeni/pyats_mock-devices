def all_bgp_neighbors_established(parsed_summary):
    """Check that all BGP EVPN neighbors are in the *Established* state.

    Args:
        parsed_summary (dict): Output from parsing ``show bgp l2vpn evpn summary``.

    Returns:
        tuple[bool, str]: ``(True, "")`` if all peers are established, otherwise
        ``(False, message)`` describing the peers in a non-established state.
    """
    if not parsed_summary or 'vrf' not in parsed_summary:
        return False, "No VRF data in BGP EVPN summary"
    bad = []
    for vrf_name, vrf in parsed_summary['vrf'].items():
        for peer, pdata in vrf.get('neighbor', {}).items():
            if pdata.get('state','').lower() != 'established':
                bad.append(f"VRF {vrf_name} peer {peer} state={pdata.get('state')}")
    return (not bad, "; ".join(bad))

def vnis_active(parsed_nve_vni):
    """Verify that all VNIs in the ``show nve vni`` output are up.

    Args:
        parsed_nve_vni (dict): Output from parsing ``show nve vni``.

    Returns:
        tuple[bool, str]: ``(True, "")`` if every VNI is up, otherwise
        ``(False, message)`` listing the VNIs that are not up.
    """
    down = []
    for vni, data in parsed_nve_vni.get('vni', {}).items():
        if data.get('vni_state','').lower() != 'up':
            down.append(str(vni))
    return (not down, f"VNI(s) not up: {', '.join(down)}" if down else "")
