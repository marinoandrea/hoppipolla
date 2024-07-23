# End-to-end Acceptance Scenarios

This folder contains a set of use-case scenarios that leverage the whole
system. Every scenario contains a `Makefile` that allows for generating the
necessary artifacts with full reproducibility (using seeds for pseudo-random
values). Every scenario comprises of the following artifacts:

- A topology `.topo` file for configuring the SCION network locally
- A `hoppipolla.ini` file containing configuration variables for Hoppipolla
  services and for the data generation.
- A `data` folder containing one or more of the following mock files to feed to
  the `nip-proxy`:
  - A `energy-readings.json` file for the energy readings for each AS in the
    topology and a number of machines per AS.
  - A `geography.json` file for geographical data about the ASes
- A `policies` folder containing one or more ASP files
- An `assets` folder for any visualization and other documentation assets

Every `Makefile` contains at least the following targets:

- `scion`: for setting up the SCION network locally and other prerequisites
- `setup`: for generating data artifacts
- `clean`: for removing the generated artifacts

Just run `make scion` and `make setup` in any order to be able to execute
the selected scenario.

## Requirements

The scenarios are meant for testing the framework, therefore the user should
setup a local SCION network following [this guide](https://docs.scion.org/en/latest/dev/run.html).

In order to allow SCION to run with `docker compose`, make sure to also run
`make docker-images` after you built the SCION project.

Once you have installed SCION locally, you should set the `HOPPIPOLLA_SCION_HOME`
variable to wherever your [`scion`](https://github.com/scionproto/scion) source
code has been cloned. You can do this in a `.env` file that must be placed in
the scenario folder as shown in the `.env.example` files in every scenario.
