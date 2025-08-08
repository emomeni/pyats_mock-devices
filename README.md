# pyATS Mock EVPN Fabric (BGP VXLAN EVPN)

This project shows how to use **pyATS/Genie** with **Unicon mock devices** to test an EVPN fabric offline.

## Setup
```bash
cd evpn-mock
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run the aetest suite (offline / mock)
```bash
pyats run job jobs/basic_job.py
# or
pyats run testbed-file testbed.yaml tests/test_evpn_mock.py
```

## Run the Blitz example
```bash
genie run blitz --testbed-file testbed.yaml --trigger-datafile tests/blitz_evpn_mock.yaml
```

## Negative testing
Edit `testbed.yaml` for `leaf1` to use `leaf1_bad.yaml`:
```yaml
command: "mock_device_cli --os nxos --state connect --mock_data_dir tests/mock_data --mock_data_file leaf1_bad.yaml"
```
Re-run the tests; they should fail on neighbor Idle / VNI Down.

## Notes
- Mock outputs live in `tests/mock_data/*.yaml`. Adjust them to mirror your real `show` outputs for best parser compatibility.
- Tests reuse Genie **parsers** so they behave like against real devices.
