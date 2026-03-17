# Catalytic Reaction

A `CatalyticReaction` entry records a complete catalytic reaction measurement, including reactor setup, operating conditions, reagent feeds, and measured results such as conversions, selectivities, yields, and reaction rates.

## Overview

This schema captures the full experimental context of a catalytic test:

- **Identification**: reaction name, type, experimenter, location, lab ID
- **Reactor setup**: reactor type, dimensions, volume
- **Reactor filling**: catalyst loading, sieve fractions, diluent
- **Pretreatment**: temperature programs, gas compositions before reaction
- **Reaction conditions**: temperature, pressure, flow rates, space velocities, contact time, reagent feeds
- **Results**: conversions, selectivities, yields, reaction rates, carbon balance

## Typical Usage

1. **Create an entry**: Upload an Excel/CSV data file, an HDF5 file, or create manually via the GUI
2. **Specify reactor setup**: Document the reactor type, dimensions, and filling (catalyst mass, diluent)
3. **Record conditions**: The parser extracts operating conditions (temperature, pressure, flow rates) from the data file
4. **View results**: Conversions, selectivities, yields, and rates are automatically populated and plotted

## Supported Data Formats

Reaction data can be populated from:

- **Excel/CSV with column headers**: See the [column header mapping](../how_to/use_this_plugin.md#format-of-the-csv-or-xlsx-data-file) for recognized headers (e.g. `x CO2 (%)`, `S_p methanol (%)`, `set_temperature (K)`)
- **HDF5 files**: From the automated Haber Reactor at Fritz-Haber-Institut Berlin ([details](../how_to/use_this_plugin.md#structure-of-the-hf5-data-file))
- **Excel template**: Use the [CatalyticReaction template](https://raw.githubusercontent.com/FAIRmat-NFDI/nomad-catalysis-plugin/main/docs/assets/template_CatalyticReaction.xlsx) for single reactions, or [CatalyticReactionCollection template](https://raw.githubusercontent.com/FAIRmat-NFDI/nomad-catalysis-plugin/main/docs/assets/template_CatalyticReactionCollection.xlsx) for multiple
- **JSON archive**: Create a `.archive.json` file with `m_def: nomad_catalysis.schema_packages.catalysis.CatalyticReaction`
- **GUI**: Select "Catalytic Reaction" from the Catalysis ELN category

## Related Schemas

- **References**: [Catalyst Sample](catalyst-sample.md) (via reactor filling)
- **Created by**: [Collection Parser](collection-parser.md) (batch creation from Excel)

---

See the [full auto-generated schema documentation](schema-docs.md) for detailed property tables, types, units, and inheritance.
