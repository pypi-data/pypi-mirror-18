import unittest

from pybel.parser.parse_abundance_modifier import *
from pybel.parser.parse_pmod import PmodParser

log = logging.getLogger(__name__)


class TestHgvsParser(unittest.TestCase):
    def test_protein_del(self):
        statement = 'p.Phe508del'
        expected = ['Phe', 508, 'del']
        result = hgvs_protein_del.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_protein_mut(self):
        statement = 'p.Gly576Ala'
        expected = ['Gly', 576, 'Ala']
        result = hgvs_protein_mut.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_unspecified(self):
        statement = '='
        expected = ['=']
        result = hgvs.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_frameshift(self):
        statement = 'p.Thr1220Lysfs'
        expected = ['Thr', 1220, 'Lys', 'fs']
        result = hgvs_protein_fs.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_snp(self):
        statement = 'delCTT'
        expected = ['del', 'CTT']
        result = hgvs_snp.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_chromosome_1(self):
        statement = 'g.117199646_117199648delCTT'
        expected = [117199646, 117199648, 'del', 'CTT']
        result = hgvs_chromosome.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_chromosome_2(self):
        statement = 'c.1521_1523delCTT'
        expected = [1521, 1523, 'del', 'CTT']
        result = hgvs_dna_del.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_rna_del(self):
        statement = 'r.1653_1655delcuu'
        expected = [1653, 1655, 'del', 'cuu']
        result = hgvs_rna_del.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_protein_trunc(self):
        statement = 'p.C65*'
        result = hgvs_protein_truncation.parseString(statement)
        expected = ['C', 65, '*']
        self.assertEqual(expected, result.asList())


class TestPmod(unittest.TestCase):
    def setUp(self):
        self.parser = PmodParser()

    def test_pmod1(self):
        statement = 'pmod(Ph, Ser, 473)'
        expected = ['ProteinModification', 'Ph', 'Ser', 473]
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_pmod2(self):
        statement = 'pmod(Ph, Ser)'
        expected = ['ProteinModification', 'Ph', 'Ser']
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_pmod3(self):
        statement = 'pmod(Ph)'
        expected = ['ProteinModification', 'Ph']
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_pmod4(self):
        statement = 'pmod(P, S, 9)'
        expected = ['ProteinModification', 'P', 'S', 9]
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asList())

    def test_pmod5(self):
        statement = 'pmod(MOD:PhosRes, Ser, 473)'
        expected = ['ProteinModification', ['MOD', 'PhosRes'], 'Ser', 473]
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asList())


class TestPsub(unittest.TestCase):
    def setUp(self):
        self.parser = PsubParser()

    def test_psub(self):
        statement = 'sub(A, 127, Y)'
        result = self.parser.parseString(statement)

        expected_list = ['Variant', 'A', 127, 'Y']
        self.assertEqual(expected_list, result.asList())

        expected_dict = {
            'reference': 'A',
            'position': 127,
            'variant': 'Y'
        }
        self.assertEqual(expected_dict, result.asDict())


class TestGsubParser(unittest.TestCase):
    def setUp(self):
        self.parser = GsubParser()

    def test_gsub(self):
        statement = 'sub(G,308,A)'
        result = self.parser.parseString(statement)

        expected_dict = {
            'reference': 'G',
            'position': 308,
            'variant': 'A'
        }
        self.assertEqual(expected_dict, result.asDict())


class TestFragmentParser(unittest.TestCase):
    """See http://openbel.org/language/web/version_2.0/bel_specification_version_2.0.html#_examples_2"""

    def setUp(self):
        self.parser = FragmentParser()

    def test_known_length(self):
        """test known length"""
        s = 'frag(5_20)'
        result = self.parser.parseString(s)
        expected = {
            'start': 5,
            'stop': 20
        }
        self.assertEqual(expected, result.asDict())

    def test_unknown_length(self):
        """amino-terminal fragment of unknown length"""
        s = 'frag(1_?)'
        result = self.parser.parseString(s)
        expected = {
            'start': 1,
            'stop': '?'
        }
        self.assertEqual(expected, result.asDict())

    def test_unknown_start_stop(self):
        """fragment with unknown start/stop"""
        s = 'frag(?_*)'
        result = self.parser.parseString(s)
        expected = {
            'start': '?',
            'stop': '*'
        }
        self.assertEqual(expected, result.asDict())

    def test_descriptor(self):
        """fragment with unknown start/stop and a descriptor"""
        s = 'frag(?, 55kD)'
        result = self.parser.parseString(s)
        expected = {
            'missing': '?',
            'description': '55kD'
        }
        self.assertEqual(expected, result.asDict())


class TestTruncationParser(unittest.TestCase):
    def setUp(self):
        self.parser = TruncParser()

    def test_trunc_1(self):
        statement = 'trunc(40)'
        result = self.parser.parseString(statement)

        expected = ['Variant', 'C', 40, '*']
        self.assertEqual(expected, result.asList())


class TestFusionParser(unittest.TestCase):
    def setUp(self):
        self.parser = FusionParser()

    def test_261a(self):
        """RNA abundance of fusion with known breakpoints"""
        statement = 'fus(HGNC:TMPRSS2, r.1_79, HGNC:ERG, r.312_5034)'
        result = ['Fusion', ['HGNC', 'TMPRSS2'], ['r', 1, 79], ['HGNC', 'ERG'], ['r', 312, 5034]]
        self.assertEqual(result, self.parser.parseString(statement).asList())

    def test_261b(self):
        """RNA abundance of fusion with unspecified breakpoints"""
        statement = 'fus(HGNC:TMPRSS2, ?, HGNC:ERG, ?)'
        expected = ['Fusion', ['HGNC', 'TMPRSS2'], '?', ['HGNC', 'ERG'], '?']
        self.assertEqual(expected, self.parser.parseString(statement).asList())


class TestLocation(unittest.TestCase):
    def setUp(self):
        self.parser = LocationParser()

    def test_a(self):
        statement = 'loc(GOCC:intracellular)'
        result = self.parser.parseString(statement)
        expected = {
            'location': dict(namespace='GOCC', name='intracellular')
        }
        self.assertEqual(expected, result.asDict())
