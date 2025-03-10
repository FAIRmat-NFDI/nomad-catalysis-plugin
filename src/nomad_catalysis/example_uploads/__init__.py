from nomad.config.models.plugins import ExampleUploadEntryPoint

catalysis = ExampleUploadEntryPoint(
    title='Heterogeneous Catalysis Example',
    category='FAIRmat examples',
    description=(
        'This example contains data entries for a catalyst sample and a catalytic '
        'reaction to demonstrate the new schemas from the '
        '[nomad-catalysis plugin](https://fairmat-nfdi.github.io/nomad-catalysis-plugin/index.html).'
    ),
    resources=['example_uploads/het_catalysis_example/*'],
)