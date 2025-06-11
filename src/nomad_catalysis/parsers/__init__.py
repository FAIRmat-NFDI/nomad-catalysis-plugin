from nomad.config.models.plugins import ParserEntryPoint


class CatalysisParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_catalysis.parsers.catalysis_parsers import CatalysisParser

        return CatalysisParser(**self.dict())


catalysis = CatalysisParserEntryPoint(
    name='CatalysisParser',
    description='A parser for catalysis data.',
    mainfile_name_re=r'.*CatalyticReaction\.(xlsx|csv)',
)


class CatalystCollectionParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_catalysis.parsers.catalysis_parsers import CatalystCollectionParser

        return CatalystCollectionParser(**self.dict())


catalyst_sample_collection = CatalystCollectionParserEntryPoint(
    name='CatalystSampleCollectionParser',
    description='A parser for a collection of catalyst samples.',
    mainfile_name_re=r'.*CatalystSampleCollection\.(xlsx|csv)',
)
