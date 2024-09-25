# How to Use This Plugin

This plugin can be used in a NOMAD Oasis installation.

## Add This Plugin to Your NOMAD installation

Read the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/staging/docs/plugins/plugins.html#add-a-plugin-to-your-nomad) for all details on how to deploy the plugin on your NOMAD instance.


## Populate the CatalyticReaction schema from a data file

Currently 2 types of data files are recognized in the data_file quantity and information
is extracted directly to populate the `CatalyticReaction` schema.
The first type is an excel or csv table, and as long as the column headers follow some
guidelines, the data can be extracted by NOMAD. The formated originated from the clean
data project and has been extended to allow a bit more flexibility of the input format.
The second type is a h5 file as it is currently produced by the Haber Reactor at the
Inorganic Chemistry Department of the Fritz-Haber-Institute and was presented in the
publication [Advancing catalysis research through FAIR data principles implemented in a
local data infrastructure - a case study of an automated test reactor](
    https://doi.org/10.1039/D4CY00693C)

### Format of the csv or xlsx data file:
For excel files with multiple sheets, only the first sheet is read. If a column is empty,
it will be ignored.

The following column headers will be recognized and mapped into the NOMAD schema:
    - `catalyst` as name of the catalyst
    - `sample_id` or `FHI-ID`
    - `mass (mg)` or `mass (g)` as catalyst mass in the reactor
    - `step` as number of reported measurement point
    - `TOS (*unit*)` time on stream, *unit* can be s or min or h
    - `x {reagent_name}` or `x {reagent_name} (%)` concentration of reagents at the inlet of the reactor
    - `temperature (*unit*)` as reactor temperature, if *unit* is not K or Kelvin, degree Celsius is assumed
    - `set_temperature (*unit*)` as desired or set reactor temperature
    - `C-balance` as carbon-balance
    - `GHSV *unit*` as Gas Hourly Space Velocity, unit can be 1/h or h^-1
    - `Vflow (ml/min)` as set total gas flow rate
    - `pressure` or `set_pressure` as reactor pressure
    - `r {name}` as reaction rate of reactant or product with {name}
    - `x_p {name} (%)` product based conversion of reactant {name}
    - `x_r {name} (%)` reactant based conversion of reactant {name}
    - `y {name} (%)` concentration out
    - `S_p {name} (%)` selectivity of product {name}

### Structure of the hf5 data file:
- Header
- Raw Data
- Sorted Data

#### Header:
- ['Bulk volume [mln]']
        reactor_setup.reactor_cross_section_area = (
            header['Inner diameter of reactor (D) [mm]'] * ureg.millimeter / 2
        ) ** 2 * np.pi
        reactor_setup.reactor_diameter = (
            header['Inner diameter of reactor (D) [mm]'] * ureg.millimeter
        )
        reactor_filling.diluent = header['Diluent material'][0].decode()
        reactor_filling.diluent_sievefraction_upper_limit = (
            header['Diluent Sieve fraction high [um]'] * ureg.micrometer
        )
        reactor_filling.diluent_sievefraction_lower_limit = (
            header['Diluent Sieve fraction low [um]'] * ureg.micrometer
        )
        reactor_filling.catalyst_mass = header['Catalyst Mass [mg]'][0] * ureg.milligram
        reactor_filling.catalyst_sievefraction_upper_limit = (
            header['Sieve fraction high [um]'] * ureg.micrometer
        )
        reactor_filling.catalyst_sievefraction_lower_limit = (
            header['Sieve fraction low [um]'] * ureg.micrometer
        )
        reactor_filling.particle_size = (
            header['Particle size (Dp) [mm]'] * ureg.millimeter
        )

        self.experimenter = header['User'][0].decode()