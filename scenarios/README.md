# End-to-end Acceptance Scenarios

This folder contains a set of use-case scenarios that leverage the whole
system and provide a reproduction package for our evaluation. 
Every scenario can contain the following artifacts:

- A `Makefile` that allows for for full reproducibility with the following formulas:
  - `setup`: for generating data artifacts
  - `execute`: for executing the scenario test case
  - `clean`: for removing the generated artifacts
- A `main.go` file that executes the scenario and measures the isolated execution performance
- Zero or more `*.lp` files containing ASP policies and meta-policies
- An optional `nip.json` file for manually recorded Network Information Plane data

Just run `make execute` to execute the selected scenario.
Running `make clean` is not necessary after every test, as the relevant cleanup
is performed within the `main.go` file.

## Requirements

The scenarios are meant for testing the framework within the SCIONLab testbed,
therefore the user should setup a local SCION network following 
[this guide](https://docs.scionlab.org/content/install/).
Therefore, we expect for the SCION daemon to be accessible at the default 
address `127.0.0.1:30255`.

Moreover, during testing we setup our custom SCIONLab AS with the entrypoint
`19-ffaa:0:1303`. Therefore, these scenarios are designed to be run with 
this configuration.

Finally, we expect the framework to be configured within the host network and 
for the services to be accessible at the default addresses 
`127.0.0.1:(27001|27002|27003)`.