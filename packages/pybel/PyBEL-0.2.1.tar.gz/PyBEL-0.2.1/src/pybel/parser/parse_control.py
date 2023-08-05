import logging

from pyparsing import Suppress, pyparsing_common

from .baseparser import BaseParser, W, quote, delimitedSet
from .parse_exceptions import *

log = logging.getLogger('pybel')


class ControlParser(BaseParser):
    def __init__(self, valid_annotations=None):
        """Builds parser for BEL valid_annotations statements

        :param valid_annotations: A dictionary from {annotation: set of valid values} for parsing
        :type valid_annotations: dict
        """

        self.valid_annotations = dict() if valid_annotations is None else valid_annotations

        self.citation = {}
        self.annotations = {}
        self.statement_group = None

        annotation_key = pyparsing_common.identifier.setResultsName('key')
        annotation_key.setParseAction(self.handle_annotation_key)

        set_tag = Suppress('SET') + W
        unset_tag = Suppress('UNSET') + W

        self.set_statement_group = set_tag + Suppress('STATEMENT_GROUP') + W + Suppress('=') + W + quote('group')
        self.set_statement_group.setParseAction(self.handle_statement_group)

        self.set_citation = set_tag + Suppress('Citation') + W + Suppress('=') + W + delimitedSet('values')
        self.set_citation.setParseAction(self.handle_citation)

        self.set_evidence = set_tag + Suppress('Evidence') + W + Suppress('=') + W + quote('value')
        self.set_evidence.setParseAction(self.handle_evidence)

        set_command_prefix = set_tag + annotation_key + W + Suppress('=') + W
        self.set_command = set_command_prefix + quote('value')
        self.set_command.setParseAction(self.handle_set_command)

        self.set_command_list = set_command_prefix + delimitedSet('values')
        self.set_command_list.setParseAction(self.handle_set_command_list)

        self.unset_command = unset_tag + annotation_key
        self.unset_command.setParseAction(self.handle_unset_command)

        self.unset_evidence = unset_tag + Suppress('Evidence')
        self.unset_evidence.setParseAction(self.handle_unset_evidence)

        self.unset_citation = unset_tag + Suppress('Citation')
        self.unset_citation.setParseAction(self.handle_unset_citation)

        self.unset_statement_group = unset_tag + Suppress('STATEMENT_GROUP')
        self.unset_statement_group.setParseAction(self.handle_unset_statement_group)

        self.commands = (self.set_statement_group | self.set_citation | self.set_evidence |
                         self.set_command | self.set_command_list | self.unset_citation |
                         self.unset_evidence | self.unset_statement_group | self.unset_command)

    def handle_annotation_key(self, s, l, tokens):
        key = tokens['key']
        if key not in self.valid_annotations:
            raise InvalidAnnotationKeyException("Illegal annotation: {}".format(key))
        return tokens

    def handle_unset_evidence(self, s, l, tokens):
        if 'Evidence' not in self.annotations:
            log.debug("PyBEL024 Can't unset missing key: {}".format('Evidence'))
        else:
            del self.annotations['Evidence']
        return tokens

    def handle_unset_citation(self, s, l, tokens):
        if 0 == len(self.citation):
            log.debug("PyBEL024 Can't unset missing key: {}".format('Citation'))
        else:
            self.citation.clear()
        return tokens

    def handle_citation(self, s, l, tokens):
        self.citation.clear()
        self.annotations.clear()

        values = tokens['values']

        if not (3 <= len(values) <= 6):
            raise InvalidCitationException('Invalid citation: {}'.format(s))

        self.citation = dict(zip(('type', 'name', 'reference', 'date', 'authors', 'comments'), values))

        return tokens

    def handle_evidence(self, s, l, tokens):
        value = tokens['value']
        self.annotations['Evidence'] = value
        return tokens

    def handle_statement_group(self, s, l, tokens):
        self.statement_group = tokens['group']
        return tokens

    def handle_set_command(self, s, l, tokens):
        key = tokens['key']
        value = tokens['value']

        if value not in self.valid_annotations[key]:
            raise IllegalAnnotationValueExeption('Illegal annotation value for {}: {}'.format(key, value))

        self.annotations[key] = value
        return tokens

    def handle_set_command_list(self, s, l, tokens):
        key = tokens['key']
        values = tokens['values']

        for value in values:
            if value not in self.valid_annotations[key]:
                raise IllegalAnnotationValueExeption('Illegal annotation value for {}: {}'.format(key, value))

        self.annotations[key] = set(values)
        return tokens

    def handle_unset_statement_group(self, s, l, tokens):
        self.statement_group = None
        return tokens

    def handle_unset_command(self, s, l, tokens):
        key = tokens['key']

        if key not in self.annotations:
            raise MissingAnnotationKeyException("Can't unset missing key: {}".format(key))

        del self.annotations[key]
        return tokens

    def get_language(self):
        return self.commands

    def get_annotations(self):
        annot = self.annotations.copy()
        for key, value in self.citation.items():
            annot['citation_{}'.format(key)] = value
        return annot

    def clear(self):
        self.annotations.clear()
        self.citation.clear()
        self.statement_group = None
