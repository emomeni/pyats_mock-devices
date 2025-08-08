from pyats.easypy import run

def main(runtime):
    run(testscript='tests/test_evpn_mock.py', testbed='testbed.yaml')
