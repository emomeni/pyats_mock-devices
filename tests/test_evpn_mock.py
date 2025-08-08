from pyats import aetest
from genie.testbed import load
from tests.helpers.validators import all_bgp_neighbors_established, vnis_active

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed):
        self.parent.parameters['testbed'] = load(testbed) if isinstance(testbed, str) else testbed
        tb = self.parent.parameters['testbed']
        for dev in tb.devices.values():
            dev.connect(log_stdout=False)

class BgpEvpnChecks(aetest.Testcase):
    @aetest.test
    def neighbors_established(self, testbed):
        failures = []
        for dev in testbed.find_devices(os='nxos'):
            parsed = dev.parse('show bgp l2vpn evpn summary')
            ok, msg = all_bgp_neighbors_established(parsed)
            if not ok: failures.append(f'{dev.name}: {msg}')
        if failures: self.failed('\n'.join(failures))

    @aetest.test
    def route_types_present(self, testbed):
        for rt in (2, 5):
            missing = []
            for dev in testbed.find_devices(os='nxos'):
                parsed = dev.parse(f'show bgp l2vpn evpn route-type {rt}')
                total = 0
                for _, vrf in parsed.get('vrf', {}).items():
                    total += len(vrf.get('routes', {}))
                if total == 0:
                    missing.append(f'{dev.name}: no type-{rt} routes')
            if missing:
                self.failed('\n'.join(missing))

class NveChecks(aetest.Testcase):
    @aetest.test
    def nve_state(self, testbed):
        issues = []
        for dev in testbed.find_devices(os='nxos'):
            nve_if = dev.parse('show nve interface')
            for ifname, data in nve_if.get('nve_if', {}).items():
                if data.get('state','').lower() != 'up':
                    issues.append(f'{dev.name}: {ifname} state {data.get("state")}')
            peers = dev.parse('show nve peers')
            for _, pdata in peers.get('peer', {}).items():
                if pdata.get('peer_state','').lower() != 'up':
                    issues.append(f'{dev.name}: NVE peer state {pdata.get("peer_state")}')
            vni = dev.parse('show nve vni')
            ok, msg = vnis_active(vni)
            if not ok: issues.append(f'{dev.name}: {msg}')
        if issues: self.failed('\n'.join(issues))

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed):
        for dev in testbed.devices.values():
            dev.disconnect()
