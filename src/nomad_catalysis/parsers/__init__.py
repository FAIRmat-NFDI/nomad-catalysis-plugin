from nomad.config.models.plugins import ParserEntryPoint


class CatalysisParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_catalysis.parsers.catalysis_parsers import CatalysisParser # noqa: PLC0415, I001

        return CatalysisParser(**self.dict())


catalysis = CatalysisParserEntryPoint(
    name='CatalysisParser',
    description='A parser for catalysis data.',
    mainfile_name_re=r'.*CatalyticReaction\.(xlsx|csv)',
)


class CatalysisCollectionParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_catalysis.parsers.catalysis_parsers import CatalysisCollectionParser # noqa: PLC0415, I001

        return CatalysisCollectionParser(**self.dict())


catalysis_collection = CatalysisCollectionParserEntryPoint(
    name='CatalysisCollectionParser',
    description='A parser for a collection of catalysis entries.',
    mainfile_name_re=r'.*Cataly.+Collection\.(xlsx|csv)',
)
