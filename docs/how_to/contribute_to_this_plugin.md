# Contribute to This Plugin

Contributions to the development of the catalysis plugin are highly welcome. Whether you have example datasets, bug reports, feature requests, or code improvements — we'd love to hear from you.

## Reporting Issues

Open an issue in the [GitHub repository](https://github.com/FAIRmat-NFDI/nomad-catalysis-plugin/issues) to:

- Report a bug or unexpected behavior
- Request a new feature or schema extension
- Suggest improvements to the documentation

## Development Setup

The recommended way to develop NOMAD plugins is using [nomad-distro-dev](https://github.com/FAIRmat-NFDI/nomad-distro-dev), which provides a complete development environment with all NOMAD dependencies.

```bash
# Clone nomad-distro-dev if you haven't already
git clone https://github.com/FAIRmat-NFDI/nomad-distro-dev.git
cd nomad-distro-dev

# Clone this plugin into the packages directory
cd packages
git clone https://github.com/FAIRmat-NFDI/nomad-catalysis-plugin.git
cd ..

# Install with uv
uv sync --all-extras
source .venv/bin/activate
```

For a comprehensive guide on developing NOMAD plugins — including how to create schemas, parsers, apps, and normalizers — see the [NOMAD plugin development documentation](https://nomad-lab.eu/prod/v1/docs/howto/plugins/plugins.html).

## Running Tests

```sh
pytest -svx tests
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```sh
ruff check .   # lint
ruff format .  # auto-format
```

## Contributing to the Documentation

The documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). To preview locally:

```sh
mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Contact

You can also reach us by email or through the [FAIRmat project](https://www.fairmat-nfdi.eu/fairmat/about-fairmat/contact-fairmat) contact page.
