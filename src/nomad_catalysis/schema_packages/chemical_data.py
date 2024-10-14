chemical_data = {
    'carbon monoxide': {
        'pub_chem_id': 281,
        'iupac_name': 'carbon monoxide',
        'molecular_formula': 'CO',
        'molar_mass': 28.01,
        'inchi': 'InChI=1S/CO/c1-2',
        'inchi_key': 'UGFAIRIUMAVXCW-UHFFFAOYSA-N',
        'molecular_mass': 27.994914619,
        'monoisotopic_mass': 27.994914619,
        'smile': '[C-]#[O+]',
        'canonical_smile': '[C-]#[O+]',
        'cas_number': '630-08-0',
    },
    'CO': 'carbon monoxide',  # Reference to 'CO'
    'carbon dioxide': {
        'pub_chem_id': 280,
        'iupac_name': 'carbon dioxide',
        'molecular_formula': 'CO2',
        'molecular_mass': 43.989829239,
        'molar_mass': 44.009,
        'monoisotopic_mass': 43.989829239,
        'inchi': 'InChI=1S/CO2/c2-1-3',
        'inchi_key': 'CURLTUGMZLYLDI-UHFFFAOYSA-N',
        'smile': 'C(=O)=O',
        'canonical_smile': 'C(=O)=O',
        'cas_number': '124-38-9',
    },
    'CO2': 'carbon dioxide',  # Reference to 'carbon dioxide'
    'propanoic acid': {
        'pub_chem_id': 1032,
        'iupac_name': 'propanoic acid',
        'molecular_formula': 'C3H6O2',
        'molar_mass': 74.08,
    },
    'propionic acid': 'propanoic acid',  # Reference to 'propanoic acid'
    'ammonia': {
        'pub_chem_id': 222,
        'iupac_name': 'ammonia',  # actually 'azane'
        'molecular_formula': 'H3N',
        'molecular_mass': 17.0265491,
        'molar_mass': 17.031,
        'monoisotopic_mass': 17.0265491,
        'inchi': 'InChI=1S/H3N/h1H3',
        'inchi_key': 'QGZKDVFQNNGYKY-UHFFFAOYSA-N',
        'smile': 'N',
        'canonical_smile': 'N',
        'cas_number': '7664-41-7',
    },
    'NH3': 'ammonia',  # Reference to 'ammonia'
    'Ammonia': 'ammonia',  # Reference to 'ammonia'
    'molecular hydrogen': {
        'pub_chem_id': 783,
        'iupac_name': 'molecular hydrogen',
        'molecular_formula': 'H2',
        'molecular_mass': 2.0156500638,
        'molar_mass': 2.016,
        'monoisotopic_mass': 2.0156500638,
        'inchi': 'InChI=1S/H2/h1H',
        'inchi_key': 'UFHFLCQGNIYNRP-UHFFFAOYSA-N',
        'smile': '[HH]',
        'canonical_smile': '[HH]',
        'cas_number': '1333-74-0',
    },
    'H2': 'molecular hydrogen',  # Reference to 'molecular hydrogen'
    'hydrogen': 'molecular hydrogen',  # Reference to 'molecular hydrogen'
    'water': {
        'pub_chem_id': 962,
        'iupac_name': 'water',  # actually 'oxidane'
        'molecular_formula': 'H2O',
        'molecular_mass': 18.010564683,
        'molar_mass': 18.015,
        'monoisotopic_mass': 18.010564683,
        'inchi': 'InChI=1S/H2O/h1H2',
        'inchi_key': 'XLYOFNOQVPJJNP-UHFFFAOYSA-N',
        'smile': 'O',
        'canonical_smile': 'O',
        'cas_number': '7732-18-5',
    },
    'H2O': 'water',  # Reference to 'water'
    'argon': {
        'pub_chem_id': 23968,
        'iupac_name': 'argon',
        'molecular_formula': 'Ar',
        'molecular_mass': 39.96238312,
        'molar_mass': 39.9,
        'monoisotopic_mass': 39.96238312,
        'inchi': 'InChI=1S/Ar',
        'inchi_key': 'XKRFYHLGVUSROY-UHFFFAOYSA-N',
        'smile': '[Ar]',
        'canonical_smile': '[Ar]',
        'cas_number': '7440-37-1',
    },
    'Ar': 'argon',  # Reference to 'argon'
    'helium': {
        'pub_chem_id': 23987,
        'iupac_name': 'helium',
        'molecular_formula': 'He',
        'molecular_mass': 4.002603254,
        'molar_mass': 4.0026,
        'monoisotopic_mass': 4.002603254,
        'inchi': 'InChI=1S/He',
        'inchi_key': 'SWQJXJOGLNCZEY-UHFFFAOYSA-N',
        'smile': '[He]',
        'canonical_smile': '[He]',
        'cas_number': '7440-59-7',
    },
    'He': 'helium',  # Reference to 'helium'
    'molecular nitrogen': {
        'pub_chem_id': 947,
        'iupac_name': 'molecular nitrogen',
        'molecular_formula': 'N2',
        'molecular_mass': 28.006148008,
        'molar_mass': 28.014,
        'monoisotopic_mass': 28.006148008,
        'inchi': 'InChI=1S/N2/c1-2',
        'inchi_key': 'IJGRMHOSHXDMSA-UHFFFAOYSA-N',
        'smile': 'N#N',
        'canonical_smile': 'N#N',
        'cas_number': '7727-37-9',
    },
    'nitrogen': 'molecular nitrogen',  # Reference to 'molecular nitrogen'
    'N2': 'molecular nitrogen',  # Reference to 'molecular nitrogen'
    'molecular oxygen': {
        'pub_chem_id': 977,
        'iupac_name': 'molecular oxygen',
        'molecular_formula': 'O2',
        'molecular_mass': 31.989829239,
        'molar_mass': 31.999,
        'monoisotopic_mass': 31.989829239,
        'inchi': 'InChI=1S/O2/c1-2',
        'inchi_key': 'MYMOFIZGZYHOMD-UHFFFAOYSA-N',
        'smile': 'O=O',
        'canonical_smile': 'O=O',
        'cas_number': '7782-44-7',
    },
    'oxygen': 'molecular oxygen',  # Reference to 'molecular oxygen'
    'O2': 'molecular oxygen',  # Reference to 'molecular oxygen'
    'methane': {
        'pub_chem_id': 297,
        'iupac_name': 'methane',
        'molecular_formula': 'CH4',
        'molecular_mass': 16.0313001276,
        'molar_mass': 16.043,
        'monoisotopic_mass': 16.0313001276,
        'inchi': 'InChI=1S/CH4/h1H4',
        'inchi_key': 'VNWKTOKETHGBQD-UHFFFAOYSA-N',
        'smile': 'C',
        'canonical_smile': 'C',
        'cas_number': '74-82-8',
    },
    'CH4': 'methane',  # Reference to 'methane'
    'ethane': {
        'pub_chem_id': 6324,
        'iupac_name': 'ethane',
        'molecular_formula': 'C2H6',
        'molar_mass': 30.07,
        'inchi': 'InChI=1S/C2H6/c1-2/h1-2H3',
        'inchi_key': 'OTMSDBZUPAUEDD-UHFFFAOYSA-N',
        'cas_number': '74-84-0',
    },
    'C2H6': 'ethane',  # Reference to 'ethane'
    'ethene': {
        'pub_chem_id': 6325,
        'iupac_name': 'ethene',
        'molecular_formula': 'C2H4',
        'molar_mass': 28.05,
        'inchi': 'InChI=1S/C2H4/c1-2/h1-2H2',
        'inchi_key': 'VGGSQFUCUMXWEO-UHFFFAOYSA-N',
        'cas_number': '74-85-1',
    },
    'ethylene': 'ethene',  # Reference to 'ethene'
    'C2H4': 'ethene',  # Reference to 'ethene'
    'ethyne': {
        'pub_chem_id': 6326,
        'iupac_name': 'ethyne',
        'molecular_formula': 'C2H2',
        'molar_mass': 26.04,
        'inchi': 'InChI=1S/C2H2/c1-2/h1-2H',
        'inchi_key': 'HSFWRNGVRCDJHI-UHFFFAOYSA-N',
        'cas_number': '74-86-2',
    },
    'acetylene': 'ethyne',  # Reference to 'ethyne'
    'C2H2': 'ethyne',  # Reference to 'ethyne'
    'ethin': 'ethyne',  # Reference to 'ethyne'
    'acetic acid': {
        'pub_chem_id': 176,
        'iupac_name': 'acetic acid',
        'molecular_formula': 'C2H4O2',
        'molecular_mass': 60.021129366,
        'molar_mass': 60.05,
        'monoisotopic_mass': 60.021129366,
        'inchi': 'InChI=1S/C2H4O2/c1-2(3)4/h1H3,(H,3,4)',
        'inchi_key': 'QTBSBXVTEAMEQO-UHFFFAOYSA-N',
        'smile': 'CC(=O)O',
        'canonical_smile': 'CC(=O)O',
        'cas_number': '64-19-7',
    },
    'aceticacid': 'acetic acid',  # Reference to 'acetic acid'
    'propane': {
        'pub_chem_id': 6334,
        'iupac_name': 'propane',
        'molecular_formula': 'C3H8',
        'molar_mass': 44.10,
        'inchi': 'InChI=1S/C3H8/c1-3-2/h3H2,1-2H3',
        'inchi_key': 'ATUOYWHBWRKTHZ-UHFFFAOYSA-N',
        'cas_number': '74-98-6',
    },
    'C3H8': 'propane',  # Reference to 'propane'
    'propene': {
        'pub_chem_id': 8252,
        'iupac_name': 'prop-1-ene',
        'molecular_formula': 'C3H6',
        'molar_mass': 42.08,
        'inchi': 'InChI=1S/C3H6/c1-3-2/h3H,1H2,2H3',
        'cas_number': '115-07-1',
    },
    'propylene': 'propene',  # Reference to 'propene'
    'C3H6': 'propene',  # Reference to 'propene'
    'propyne': {
        'pub_chem_id': 6335,
        'iupac_name': 'propyne',
        'molecular_formula': 'C3H4',
        'molar_mass': 40.06,
        'inchi': 'InChI=1S/C3H4/c1-3-2/h1H,3H2',
    },
    'propine': 'propyne',  # Reference to 'propyne'
    'propin': 'propyne',  # Reference to 'propyne'
    'C3H4': 'propyne',  # Reference to 'propyne'
    'prop-2-enoic acid': {
        'pub_chem_id': 6581,
        'iupac_name': 'prop-2-enoic acid',
        'molecular_formula': 'C3H4O2',
        'molar_mass': 72.06,
        'inchi': 'InChI=1S/C3H4O2/c1-2-3(4)5/h2H,1H2,(H,4,5)',
        'inchi_key': 'NIXOWILDQLNWCW-UHFFFAOYSA-N',
        'cas_number': '79-10-7',
    },
    'acrylic acid': 'prop-2-enoic acid',
    'acetaldehyde': {
        'pub_chem_id': 177,
        'iupac_name': 'acetaldehyde',
        'molecular_formula': 'C2H4O',
        'molecular_mass': 44.026214747,
        'molar_mass': 44.05,
        'monoisotopic_mass': 44.026214747,
        'inchi': 'InChI=1S/C2H4O/c1-2-3/h2H,1H3',
        'inchi_key': 'IKHGUXGNUITLKF-UHFFFAOYSA-N',
        'smile': 'CC=O',
        'canonical_smile': 'CC=O',
        'cas_number': '75-07-0',
    },
    'butane': {
        'pub_chem_id': 7843,
        'iupac_name': 'butane',
        'molecular_formula': 'C4H10',
        'molecular_mass': 58.078250319,
        'molar_mass': 58.12,
        'monoisotopic_mass': 58.078250319,
        'inchi': 'InChI=1S/C4H10/c1-3-4-2/h3-4H2,1-2H3',
        'inchi_key': 'IJDNQMDRQITEOD-UHFFFAOYSA-N',
        'smile': 'CCCC',
        'canonical_smile': 'CCCC',
        'cas_number': '106-97-8',
    },
    'n-butane': 'butane',  # Reference to 'butane'
    'n-Butane': 'butane',  # Reference to 'butane'
    'nbutane': 'butane',  # Reference to 'butane'
    '2-methylpropane': {
        'pub_chem_id': 6360,
        'iupac_name': '2-methylpropane',
        'molecular_formula': 'C4H10',
        'molecular_mass': 58.078250319,
        'molar_mass': 58.12,
        'monoisotopic_mass': 58.078250319,
        'inchi': 'InChI=1S/C4H10/c1-4(2)3/h4H,1-3H3',
        'inchi_key': 'NNPPMTNAJDCUHE-UHFFFAOYSA-N',
        'smile': 'CC(C)C',
        'canonical_smile': 'CC(C)C',
    },
    'isobutane': '2-methylpropane',
    'Isobutane': '2-methylpropane',
    'ibutane': '2-methylpropane',
    'butan-1-ol': {
        'pub_chem_id': 263,
        'iupac_name': 'butan-1-ol',
        'molecular_formula': 'C4H10O',
        'molecular_mass': 74.073164938,
        'molar_mass': 74.12,
        'monoisotopic_mass': 74.073164938,
        'inchi': 'InChI=1S/C4H10O/c1-2-3-4-5/h5H,2-4H2,1H3',
        'inchi_key': 'LRHPLDYGYMQRHN-UHFFFAOYSA-N',
        'smile': 'CCCCO',
        'canonical_smile': 'CCCCO',
        'cas_number': '71-36-3',
    },
    'butanol': 'butan-1-ol',  # Reference to 'butan-1-ol'
    'butanal': {
        'pub_chem_id': 261,
        'iupac_name': 'butanal',
        'molecular_formula': 'C4H8O',
        'molecular_mass': 72.057514874,
        'molar_mass': 72.11,
        'monoisotopic_mass': 72.057514874,
        'inchi': 'InChI=1S/C4H8O/c1-2-3-4-5/h4H,2-3H2,1H3',
        'inchi_key': 'ZTQSAGDEMFDKMZ-UHFFFAOYSA-N',
        'smile': 'CCCC=O',
        'canonical_smile': 'CCCC=O',
    },
    'butyraldehyde': 'butanal',  # Reference to 'butanal'
    'pent-1-ene': {
        'pub_chem_id': 8004,
        'iupac_name': 'pent-1-ene',
        'molecular_formula': 'C5H10',
        'molecular_mass': 70.078250319,
        'molar_mass': 70.13,
        'monoisotopic_mass': 70.078250319,
        'inchi': 'InChI=1S/C5H10/c1-3-5-4-2/h3H,1,4-5H2,2H3',
        'inchi_key': 'YWAKXRMUMFPDSH-UHFFFAOYSA-N',
        'smile': 'CCCC=C',
        'canonical_smile': 'CCCC=C',
    },
    'n-pentene': 'pent-1-ene',
    'npentene': 'pent-1-ene',
    'ethanol': {
        'pub_chem_id': 702,
        'iupac_name': 'ethanol',
        'molecular_formula': 'C2H6O',
        'molar_mass': 46.07,
        'inchi': 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3',
        'inchi_key': 'LFQSCWFLJHTTHZ-UHFFFAOYSA-N',
        'cas_number': '64-17-5',
    },
    'EtOH': 'ethanol',  # Reference to 'ethanol'
    'CH3CH2OH': 'ethanol',  # Reference to 'ethanol'
    'methanol': {
        'pub_chem_id': 887,
        'iupac_name': 'methanol',
        'molecular_formula': 'CH4O',
        'molar_mass': 32.04,
        'inchi': 'InChI=1S/CH4O/c1-2/h2H,1H3',
        'inchi_key': 'OKKJLVBELUTLKV-UHFFFAOYSA-N',
        'cas_number': '67-56-1',
    },
    'methyl alcohol': 'methanol',  # Reference to 'methanol'
    'MeOH': 'methanol',  # Reference to 'methanol'
    'CH3OH': 'methanol',  # Reference to 'methanol'
    'formic acid': {
        'pub_chem_id': 284,
        'iupac_name': 'formic acid',
        'molecular_formula': 'CH2O2',
        'molar_mass': 46.03,
        'inchi': 'InChI=1S/CH2O2/c2-1-3/h1H,(H,2,3)',
        'inchi_key': 'BDAGIHXWWSANSR-UHFFFAOYSA-N',
        'cas_number': '64-18-6',
    },
    'HCOOH': 'formic acid',  # Reference to 'formic acid'
    'methanoic acid': 'formic acid',  # Reference to 'formic acid'
    'prop-2-enal': {
        'pub_chem_id': 7847,
        'iupac_name': 'prop-2-enal',
        'molecular_formula': 'C3H4O',
        'molar_mass': 56.06,
        'inchi': 'InChI=1S/C3H4O/c1-2-3-4/h2-3H,1H2',
    },
    'acrolein': 'prop-2-enal',  # Reference to 'prop-2-enal'
    'C3H4O': 'prop-2-enal',  # Reference to 'prop-2-enal'
    'propanal': {
        'pub_chem_id': 527,
        'iupac_name': 'propanal',
        'molecular_formula': 'C3H6O',
        'molar_mass': 58.08,
        'inchi': 'InChI=1S/C3H6O/c1-2-3-4/h3H,2H,1H3',
    },
    'propionaldehyde': 'propanal',  # Reference to 'propanal'
    'propan-2-one': {
        'pub_chem_id': 180,
        'iupac_name': 'propan-2-one',
        'molecular_formula': 'C3H6O',
        'molar_mass': 58.08,
        'inchi': 'InChI=1S/C3H6O/c1-3(2)2/h1-2H3',
        'inchi_key': 'CSCPPACGZOOCGX-UHFFFAOYSA-N',
        'cas_number': '67-64-1',
    },
    'acetone': 'propan-2-one',  # Reference to 'propan-2-one'
    'propan-2-ol': {
        'pub_chem_id': 3776,
        'iupac_name': 'propan-2-ol',
        'molecular_formula': 'C3H8O',
        'molar_mass': 60.10,
        'inchi': 'InChI=1S/C3H8O/c1-3(2)4/h3-4H,1-2H3',
        'inchi_key': 'KZBMWSRVAYFASW-UHFFFAOYSA-N',
        'cas_number': '67-63-0',
    },
    '2-propanol': 'propan-2-ol',  # Reference to 'propan-2-ol'
    'isopropanol': 'propan-2-ol',  # Reference to 'propan-2-ol'
    'prop-2-en-1-ol': {
        'pub_chem_id': 7858,
        'iupac_name': 'prop-2-en-1-ol',
        'molecular_formula': 'C3H6O',
        'molar_mass': 58.08,
        'inchi': 'InChI=1S/C3H6O/c1-2-3-4/h2,4H,1,3H2',
        'inchi_key': 'QWVGKYWNOKOFNN-UHFFFAOYSA-N',
        'cas_number': '107-18-6',
    },
    'allyl alcohol': 'prop-2-en-1-ol',  # Reference to 'allyl alcohol'
    'allylalcohol': 'prop-2-en-1-ol',  # Reference to 'prop-2-en-1-ol'
    'propan-1-ol': {
        'pub_chem_id': 1031,
        'iupac_name': 'propan-1-ol',
        'molecular_formula': 'C3H8O',
        'molar_mass': 60.10,
        'inchi': 'InChI=1S/C3H8O/c1-2-3-4/h4H,2-3H2,1H3',
        'inchi_key': 'XNWBBONJTDVZCF-UHFFFAOYSA-N',
        'cas_number': '71-23-8',
    },
    '1-propanol': 'propan-1-ol',  # Reference to 'propan-1-ol'
    'n-propanol': 'propan-1-ol',  # Reference to 'propan-1-ol'
    'npropanol': 'propan-1-ol',  # Reference to 'propan-1-ol'
    'propanol': 'propan-1-ol',  # Reference to 'propan-1-ol'
    'methyl acetate': {
        'pub_chem_id': 6589,
        'iupac_name': 'methyl acetate',
        'molecular_formula': 'C3H6O2',
        'molecular_mass': 74.03677943,
        'molar_mass': 74.08,
        'monoisotopic_mass': 74.03677943,
        'inchi': 'InChI=1S/C3H6O2/c1-3(4)5-2/h1-2H3',
        'inchi_key': 'KXKVLQRXCPHEJC-UHFFFAOYSA-N',
        'smile': 'CC(=O)OC',
        'canonical_smile': 'CC(=O)OC',
    },
    'methylacetate': 'methyl acetate',  # Reference to 'methyl acetate'
    'ethyl acetate': {
        'pub_chem_id': 8857,
        'iupac_name': 'ethyl acetate',
        'molecular_formula': 'C4H8O2',
        'molecular_mass': 88.052429494,
        'molar_mass': 88.11,
        'monoisotopic_mass': 88.052429494,
        'inchi': 'InChI=1S/C4H8O2/c1-3-6-4(2)5/h3H2,1-2H3',
        'inchi_key': 'XEKOWRVHYACXOJ-UHFFFAOYSA-N',
        'smile': 'CCOC(=O)C',
        'canonical_smile': 'CCOC(=O)C',
    },
    'ethylacetate': 'ethyl acetate',  # Reference to 'ethyl acetate'
    '1-butene': {
        'pub_chem_id': 7844,
        'iupac_name': 'but-1-ene',
        'molecular_formula': 'C4H8',
        'molar_mass': 56.11,
        'inchi': 'InChI=1S/C4H8/c1-3-4-2/h3H,1,4H2,2H3',
    },
    'butylene': '1-butene',  # Reference to '1-butene'
    'n-Butene': '1-butene',  # Reference to '1-butene'
    'butene': {
        'iupac_name': 'butene',
        'molecular_formula': 'C4H8',
    },  # unspecified isomer
    'nictbutene': 'butene',  # Reference to 'butene', unspecified isomer
    'furan': {
        'pub_chem_id': 8029,
        'iupac_name': 'furan',
        'molecular_formula': 'C4H4O',
        'molar_mass': 68.07,
        'inchi': 'InChI=1S/C4H4O/c1-2-4-5-3-1/h1-4H',
        'inchi_key': 'NNTHXFGICWXRPZ-UHFFFAOYSA-N',
        'cas_number': '110-00-9',
    },
    'furfuran': 'furan',  # Reference to 'furan'
    'furan-2,5-dione': {
        'pub_chem_id': 7923,
        'iupac_name': 'furan-2,5-dione',
        'molecular_formula': 'C4H2O3',
        'molar_mass': 98.06,
        'inchi': 'InChI=1S/C4H2O3/c5-3-1-2-4(6)7-3/h1-2H',
    },
    '2,5-dihydrofuran': {
        'pub_chem_id': 15570,
        'iupac_name': '2,5-dihydrofuran',
        'molecular_formula': 'C4H6O',
        'molecular_mass': 70.041864811,
        'molar_mass': 70.09,
        'monoisotopic_mass': 70.041864811,
        'inchi': 'InChI=1S/C4H6O/c1-2-4-5-3-1/h1-2H,3-4H2',
        'inchi_key': 'ARGCQEVBJHPOGB-UHFFFAOYSA-N',
        'smile': 'C1C=CCO1',
        'canonical_smile': 'C1C=CCO1',
    },
    '25-dihydrofuran': '2,5-dihydrofuran',  # Reference to '2,5-dihydrofuran'
    'maleic anhydride': 'furan-2,5-dione',  # Reference to 'furan-2,5-dione'
    'MAN': 'furan-2,5-dione',  # Reference to 'furan-2,5-dione'
    'p>=5c': {
        'name': 'p>=5c',
        'iupac_name': 'C5+',
    },  # unspecified longer hydrocarbon
}
