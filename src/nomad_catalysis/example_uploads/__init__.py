from nomad.config.models.plugins import ExampleUploadEntryPoint

catalysis = ExampleUploadEntryPoint(
    title='Heterogeneous Catalysis Example',
    category='Examples',
    description='Set examples files for catalyst sample and catalytic reaction',
    resources=['example_uploads/het_catalysis_example/*'],
)