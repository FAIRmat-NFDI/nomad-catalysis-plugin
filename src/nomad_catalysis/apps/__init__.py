from nomad.config.models.plugins import AppEntryPoint

from nomad_catalysis.apps.py_het_cat_app import heterogeneous_catalysis_app

catalysis = AppEntryPoint(
    name='Catalysis App',
    description="""
    This app allows you to search **heterogeneous catalysis data** within NOMAD.
    """,
    app=heterogeneous_catalysis_app,
)
