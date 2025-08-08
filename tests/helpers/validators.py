def all_bgp_neighbors_established(parsed_summary):
    if not parsed_summary or 'vrf' not in parsed_summary:
        return False, "No VRF data in BGP EVPN summary"
    bad = []
    for vrf_name, vrf in parsed_summary['vrf'].items():
        for peer, pdata in vrf.get('neighbor', {}).items():
            if pdata.get('state','').lower() != 'established':
                bad.append(f"VRF {vrf_name} peer {peer} state={pdata.get('state')}")
    return (not bad, "; ".join(bad))

def vnis_active(parsed_nve_vni):
    down = []
    for vni, data in parsed_nve_vni.get('vni', {}).items():
        if data.get('vni_state','').lower() != 'up':
            down.append(str(vni))
    return (not down, f"VNI(s) not up: {', '.join(down)}" if down else "")
