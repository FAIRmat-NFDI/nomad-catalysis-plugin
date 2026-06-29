# Collection Parser

The `CatalysisCollectionParserEntry` is a convenience schema that automatically generates multiple [Catalyst Sample](catalyst-sample.md) and [Catalytic Reaction](catalytic-reaction.md) entries from a single Excel or CSV file.

## Overview

This schema provides a batch-creation workflow:

- Upload a single `*CatalysisCollection.xlsx` (or `.csv`) file
- The parser reads the tabular data and creates individual entries for each catalyst sample and catalytic reaction
- Sample and reaction entries are linked automatically via lab IDs

## Typical Usage

1. **Prepare a collection file**: Use the [CatalysisCollection template](https://raw.githubusercontent.com/FAIRmat-NFDI/nomad-catalysis-plugin/main/src/nomad_catalysis/example_uploads/template_example/template_CatalysisCollection.xlsx) with both sample and reaction data
2. **Upload to NOMAD**: Drop the file into an upload — the parser automatically creates entries
3. **Reprocess if needed**: When generating samples and reactions together, reprocess the upload to resolve cross-references

!!! note "File Naming Convention"
    The parser recognizes files by their name suffix:

    - `*CatalysisCollection.xlsx` — creates both sample and reaction entries
    - `*CatalystSampleCollection.xlsx` — creates sample entries only
    - `*CatalyticReactionCollection.xlsx` — creates reaction entries only

## Related Schemas

- **Creates**: [Catalyst Sample](catalyst-sample.md), [Catalytic Reaction](catalytic-reaction.md)

---

See the [full auto-generated schema documentation](schema-docs.md) for detailed property tables, types, units, and inheritance.
