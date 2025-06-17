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


class CatalysisCollectionParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_catalysis.parsers.catalysis_parsers import CatalysisCollectionParser

        return CatalysisCollectionParser(**self.dict())


catalysis_collection = CatalysisCollectionParserEntryPoint(
    name='CatalysisCollectionParser',
    description='A parser for a collection of catalysis entries.',
    mainfile_name_re=r'.*Cataly.+Collection\.(xlsx|csv)',
)
