# Catalyst Sample

A `CatalystSample` entry describes a heterogeneous catalyst material, including its chemical composition, preparation method, and surface properties.

## Overview

This schema captures all metadata needed to identify and reproduce a catalyst:

- **Identification**: name, lab ID, storing institution
- **Composition**: elemental composition with atomic and mass fractions, named components
- **Preparation**: method, preparator, institution
- **Surface properties**: BET surface area, dispersion, characterization method

## Typical Usage

1. **Register a catalyst**: Create a `CatalystSample` entry — either manually via the GUI, by uploading a `*CatalystSampleCollection.xlsx` file, or as part of a combined `*CatalysisCollection.xlsx` upload
2. **Fill composition**: Add elemental composition entries (element, mass fraction, atomic fraction) and named components
3. **Document preparation**: Record the synthesis method, responsible person, and institution
4. **Add surface data**: Enter BET surface area and dispersion measurements
5. **Reference from reactions**: [CatalyticReaction](catalytic-reaction.md) entries link back to the sample via the reactor filling section

## Supported Data Formats

Catalyst samples can be created from:

- **Excel/CSV**: Upload a `*CatalystSampleCollection.xlsx` (or `.csv`) file using the [template](https://raw.githubusercontent.com/FAIRmat-NFDI/nomad-catalysis-plugin/main/docs/assets/template_CatalystSampleCollection.xlsx)
- **Combined collection**: Include sample data in a `*CatalysisCollection.xlsx` file alongside reaction data
- **JSON archive**: Create a `.archive.json` file with `m_def: nomad_catalysis.schema_packages.catalysis.CatalystSample`
- **GUI**: Select "Catalyst Sample" from the Catalysis ELN category in NOMAD's schema picker

## Related Schemas

- **Referenced by**: [Catalytic Reaction](catalytic-reaction.md) (via reactor filling sample reference)
- **Created by**: [Collection Parser](collection-parser.md) (batch creation from Excel)

---

See the [full auto-generated schema documentation](schema-docs.md) for detailed property tables, types, units, and inheritance.
