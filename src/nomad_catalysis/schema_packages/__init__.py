from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class CatalysisPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_catalysis.schema_packages.catalysis import m_package

        return m_package


catalysis = CatalysisPackageEntryPoint(
    name='Catalysis',
    description='Catalysis Schema package defined using the new plugin mechanism.',
)
