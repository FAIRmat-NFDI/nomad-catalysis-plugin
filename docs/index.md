# ![nomad plugin logo](assets/nomad-plugin-logo.png)

This is the NOMAD plugin for **heterogeneous catalysis** data. It provides schemas, parsers, and a dedicated search app to manage, visualize, and share catalyst and reactivity data following FAIR principles.

<div markdown="block" class="action-buttons">
  <a href="https://chemrxiv.org/doi/full/10.26434/chemrxiv-2025-kx99k/v2" class="md-button md-button--primary action-button" target="_blank" rel="noopener">📄 Preprint</a>
  <a href="https://nomad-lab.eu/prod/v1/gui/search/heterogeneouscatalyst" class="md-button md-button--primary action-button">🔍 Explore in NOMAD</a>
  <a href="https://github.com/FAIRmat-NFDI/nomad-catalysis-plugin" class="md-button action-button"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="14" height="14"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg> Plugin Repository</a>
</div>

This plugin was developed as part of Task Area E2 "Heterogeneous Catalysis" of the
[FAIRmat](https://www.fairmat-nfdi.eu/fairmat) project within the German National Research Data
Infrastructure ([NFDI](https://www.nfdi.de)). The release v1.0.2 is part of the [central NOMAD repository](https://nomad-lab.eu/prod/v1/gui/search/heterogeneouscatalyst) deployment. The latest features of the main branch can be tested in the
[Example Oasis](https://nomad-lab.eu/prod/v1/oasis/gui/) provided by FAIRmat/NOMAD-lab.

## Included Entry Types

This plugin includes the following NOMAD entry types:

- `CatalystSample` — Describes a catalyst material, its composition, preparation, and surface properties.
- `CatalyticReaction` — Describes a catalytic reaction measurement, including reactor setup, conditions, and results.
- `CatalysisCollectionParserEntry` — Enables batch creation of sample and reaction entries from a single Excel/CSV file.

More information can be found in the [Reference](reference/references.md) section.

## Getting Started

<div markdown="block" class="framework-grid">

<div markdown="block">

### 📚 Tutorial
**Learning-oriented guide**

Follow a step-by-step walkthrough using real catalysis data: upload a catalyst sample and a catalytic reaction, then explore the results.

[Start the tutorial →](tutorial/tutorial.md){.md-button}

</div>

<div markdown="block">

### 📖 How-to Guides
**Task-oriented instructions**

- [Install this plugin](how_to/install_this_plugin.md)
- [Create catalysis entries](how_to/use_this_plugin.md)
- [Search catalysis data](how_to/search_catalysis_data.md)
- [Contribute to this plugin](how_to/contribute_to_this_plugin.md)

</div>

<div markdown="block">

### 📋 Reference
**Information-oriented documentation**

Complete schema reference for all entry types, including quantities, subsections, and data file formats.

[View reference →](reference/references.md){.md-button}

</div>

<div markdown="block">

### 🔬 About NOMAD
**Open data platform**

NOMAD is an open-source data management platform for materials science, designed to follow FAIR principles. [Learn more →](https://nomad-lab.eu/nomad-lab/)

</div>

</div>

## How to Cite

??? note "Citation"
    If you use this plugin, please cite the accompanying preprint and the software:

    **Preprint:**

    > Schumann, J., Näsström, H., Götte, M., Himanen, L., Moshantaf, A., Scheidgen, M., Márquez Prieto, J. A., Draxl, C., & Trunschke, A. *Towards a new era for open and FAIR data in catalysis research – A catalysis plugin for NOMAD.* ChemRxiv, 2026. [https://doi.org/10.26434/chemrxiv-2025-kx99k/v2](https://doi.org/10.26434/chemrxiv-2025-kx99k/v2)

    **Software:**

    > Schumann, J., Näsström, H., *NOMAD Catalysis Plugin* (all versions). [https://doi.org/10.5281/zenodo.17534066](https://doi.org/10.5281/zenodo.17534066)

    **BibTeX:**
    ```bibtex
    @article{doi:10.26434/chemrxiv-2025-kx99k/v2,
      author  = {Julia Schumann and Hampus Näsström and Michael Götte and
                 Lauri Himanen and Abdulrhman Moshantaf and Markus Scheidgen and
                 José A. Márquez Prieto and Claudia Draxl and Annette Trunschke},
      title   = {Towards a new era for open and FAIR data in catalysis research
                 – A catalysis plugin for NOMAD},
      journal = {ChemRxiv},
      volume  = {2026},
      number  = {0205},
      year    = {2026},
      doi     = {10.26434/chemrxiv-2025-kx99k/v2},
      url     = {https://chemrxiv.org/doi/abs/10.26434/chemrxiv-2025-kx99k/v2}
    }

    @software{nomad_catalysis,
      author  = {Schumann, Julia and Näsström, Hampus},
      title   = {NOMAD Catalysis Plugin},
      url     = {https://github.com/FAIRmat-NFDI/nomad-catalysis-plugin},
      doi     = {10.5281/zenodo.17534066}
    }
    ```

## Contact

Feel free to reach out with questions or feedback via:

- Opening an issue in the [GitHub repository](https://github.com/FAIRmat-NFDI/nomad-catalysis-plugin)
- Asking in the [NOMAD Discord](https://discord.gg/nomad-lab) channel
- Contacting the [FAIRmat project](https://www.fairmat-nfdi.eu/fairmat/about-fairmat/contact-fairmat) directly