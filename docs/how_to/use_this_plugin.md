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

The following column names will be recognized and mapped into the NOMAD schema:
    - `catalyst`
    - `sample_id` or `FHI-ID`
    - `mass (mg)` or `mass (g)`
    - `step`
    - `x {reagent_name}` or `x {reagent_name} %`
    - `temperature (*unit*)` if *unit* is not K or Kelvin, degree Celsius is assumed
    - `set_temperature (*unit*)`
    - `TOS (*unit*)` *unit* can be s or min or h
    - `C-balance`
    - `GHSV *unit*` unit can be 1/h or h^-1
    - `Vflow (ml/min)`
    - `pressure` or `set_pressure`
    - `r {name}`
    - `x_p {name} (%)` product based conversion
    - `x_r {name} (%)` reactant based conversion
    - `y {name} (%)` concentration out
    - `S_p {name} (%)` selectivity
    -