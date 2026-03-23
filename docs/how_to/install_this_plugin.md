# Install This Plugin

The recommended way to include this plugin in your NOMAD Oasis is through a [NOMAD distribution](https://github.com/FAIRmat-NFDI/nomad-distro-template). Add the plugin to the `pyproject.toml` of your distribution repository:

```toml
[project.optional-dependencies]
plugins = [
  "nomad-catalysis @ git+https://github.com/FAIRmat-NFDI/nomad-catalysis-plugin.git@main"
]
```

!!! tip "Using Specific Versions"
    For production deployments, pin a version tag or commit hash instead of `@main`:
    ```toml
    "nomad-catalysis @ git+https://github.com/FAIRmat-NFDI/nomad-catalysis-plugin.git@v1.0.2"
    ```

Then rebuild your Oasis Docker image. The distribution template uses `uv sync` to install all plugins automatically.

For detailed instructions on setting up an Oasis and installing plugins, see the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/docs/howto/plugins/plugins.html).