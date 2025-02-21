from nomad.config.models.plugins import ExampleUploadEntryPoint

catalysis = ExampleUploadEntryPoint(
    title='Heterogeneous Catalysis Example',
    category='FAIRmat examples',
    description=(
        'Examples files for catalyst sample and catalytic reaction to demonstrate '
        'the new classes from the nomad-catalysis plugin.'
    ),
    resources=['example_uploads/het_catalysis_example/*'],
)