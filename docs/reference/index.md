# Schema Reference Overview

This section provides the complete technical documentation for all data models in the nomad-catalysis plugin. These schemas capture the heterogeneous catalysis research workflow, from catalyst sample characterization to catalytic reaction measurements.

!!! tip "Getting Started"
    If you're new to the plugin, start with the [Tutorial](../tutorial/tutorial.md) or the [How-to Guides](../how_to/use_this_plugin.md) for practical usage instructions. This reference section focuses on technical schema details.

## Schemas at a Glance

| Schema | Purpose |
|--------|---------|
| [**Catalyst Sample**](catalyst-sample.md) | Describes a catalyst material: composition, preparation, surface properties |
| [**Catalytic Reaction**](catalytic-reaction.md) | Records a catalytic reaction measurement: conditions, reagents, products, conversions |
| [**Collection Parser**](collection-parser.md) | Batch-creates sample and reaction entries from a single Excel/CSV file |

## How the Schemas Relate

```
CatalysisCollectionParserEntry
    ├── generates → CatalystSample entries
    └── generates → CatalyticReaction entries
                        └── references → CatalystSample (via reactor_filling)
```

- A **CatalystSample** describes the material being tested.
- A **CatalyticReaction** records experimental conditions, reactor setup, and measured results for a specific catalytic test. It references the catalyst sample used.
- A **CatalysisCollectionParserEntry** is a convenience schema that parses an Excel/CSV file and automatically creates multiple sample and reaction entries in one upload.

## Additional Resources

- [How to Create Catalysis Entries](../how_to/use_this_plugin.md) — formats for Excel, CSV, HDF5, JSON, and GUI creation
- [Search for Catalysis Data](../how_to/search_catalysis_data.md) — using the dedicated catalysis app
- [NOMAD Metainfo Browser](https://nomad-lab.eu/prod/v1/gui/analyze/metainfo/nomad_catalysis){:target="_blank" rel="noopener"} — interactive schema exploration
