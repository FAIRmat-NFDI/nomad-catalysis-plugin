# References

## ELN Schemas

This plugin provides the following ELN schemas:

- **Catalyst Sample**
- **Catalytic Reaction**
- **Catalysis Collection Parser Entry**

---

## Catalyst Sample

**Quantities:**

- `name` (string)
- `datetime` (string)
- `lab_id` (string)
- `description` (rich text)
- `storing_institution` (string)
- `catalyst_type` (string)
- `form` (string)

**Subsections:**

??? info "elemental_composition (repeating)"
    - `element`
    - `atomic_fraction`
    - `mass_fraction`

??? info "components (repeating)"
    - `component_label`
    - `mass`
    - `mass_fraction`

??? info "preparation_details"
    - `preparation_method` (string)
    - `preparator`
    - `preparing_institution`

??? info "surface"
    - `surface_area` (float)
    - `method_surface_area_determination` (string)
    - `dispersion` (float)

---

## Catalytic Reaction

**Quantities:**

- `name`
- `starting_time`
- `data_file`
- `ID`
- `reaction_type`
- `reaction_name`
- `experiment_handbook`
- `description`
- `location`
- `experimenter`

**Subsections:**

??? info "steps (repeating)"
    - `name`
    - `start_time`
    - `comment`

??? info "samples (repeating)"
    - `name`
    - `reference`
    - `lab_id`

??? info "instruments / reactor setup (repeating)"
    - `name`
    - `reference`
    - `lab_id`
    - `reactor_type`
    - `bed_length`
    - `reactor_cross_section_area`
    - `reactor_diameter`
    - `reactor_volume`

??? info "reactor_filling (repeating)"
    - `catalyst_name`
    - `sample_section_reference`
    - `catalyst_mass`
    - `catalyst_density`
    - `catalyst_volume`
    - `catalyst_sievefraction_upper_limit`
    - `catalyst_sievefraction_lower_limit`
    - `particle_size`
    - `diluent`
    - `diluent_sievefraction_upper_limit`
    - `diluent_sievefraction_lower_limit`

??? info "pretreatment (repeating)"
    Same structure as **reaction_conditions** below.

??? info "reaction_conditions (repeating)"
    - `set_temperature`
    - `set_pressure`
    - `set_total_flow_rate`
    - `contact_time` (label: W|F)
    - `sampling_frequency`
    - `time_on_stream`
    - `weight_hourly_space_velocity`
    - `gas_hourly_space_velocity`
    - `runs`

    **Sub-subsection: reagents**

    - `name`
    - `gas_concentration_in`
    - `flow_rate`
    - `pure_component`: `name`, `iupac_name`, ...

??? info "results (repeating)"
    - `name`
    - `temperature`
    - `pressure`
    - `total_flow_rate`
    - `runs`
    - `time_on_stream`
    - `c_balance`

    **reactants_conversions:**

    - `name`, `gas_concentration_in`, `gas_concentration_out`, `flow_rate`
    - `conversion`, `conversion_type`, `conversion_product_based`, `conversion_reactant_based`
    - `pure_component`: `name`, `iupac_name`, ...

    **rates:**

    - `name`, `reaction_rate`, `specific_mass_rate`, `specific_surface_area_rate`, `rate`, `turn_over_frequency`

    **products:**

    - `name`, `gas_concentration_in`, `flow_rate`, `gas_concentration_out`
    - `selectivity`, `product_yield`, `space_time_yield`
    - `pure_component`: `name`, `iupac_name`

---

## Catalysis Collection Parser Entry

**Quantities:**

- `data_file`

**Subsections:**

- `samples` (repeating)
- `measurements` (repeating)
