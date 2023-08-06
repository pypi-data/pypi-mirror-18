# -*- encoding: utf-8 -*-
'''
Importação e abstração de uma gramática livre do contexto.

Provê um leitor genérico, GrammarReader, para facilitar a criação de leitores
para outros formatos. 
'''

import re
from llclib.exceptions import GrammarException

class Grammar(object):
    '''
    Armazena uma gramática.

    Atributos:
        nonterminals    : list
        terminals       : list
        productions     : dict
        start           : str
    '''
    def __init__(self, nonterminals, terminals, productions, start):
        '''
        Terminais e não-terminais são armazenados em uma list de strings, onde
        cada string representa um terminal ou um não-terminal.
        '''
        self.nonterminals = nonterminals
        self.terminals = terminals

        '''
        O atributo production é uma lista de listas, onde o primeiro elemento
        de cada lista é um símbolo não-terminal e o segundo elemento da lista é
        uma lista de símbolos, terminais ou não terminais.
        Exemplo: [['S', ['A', 'B', 'a']], ['A', ['Aa', 'aaaa']]]
        '''
        self.productions = productions

        '''O símbolo inicial, que deve estar na lista de não-terminais'''
        self.start = start

    def test(self):
        '''
        Verifica se a gramática é válida ou não.
        Exceções possíveis dadas pelo reader:
            MultipleStartsError
            EmptyGrammarError
            InvalidNonterminalError
        '''
        if len(self.productions) == 0:
            raise GrammarException('Gramática sem produções.')
        if ('V' in self.nonterminals or 'V' in self.productions or
                'V' in self.terminals):
            raise GrammarException('Gramática usando vazio como produção.')


    @staticmethod
    def len(productions):
        '''Retorna a quantidade de regras de produções de uma gramática'''
        length = 0
        for production in productions:
            length += len(productions[production])
        return length

    def is_terminal(self, symbol):
        '''
        Verifica se um símbolo é terminal.
        '''
        for terminal in self.terminals:
            if terminal == symbol:
                return True
        return False

    def is_nonterminal(self, symbol):
        '''Verifica se um símbolo é variável.'''
        for nonterminal in self.nonterminals:
            if nonterminal == symbol:
                return True
        return False

class GrammarReader(object):
    '''
    Leitor genérico de gramáticas.

    Atributos:
        text        : str
        re_limiter  : regexp
    '''
    SYMBOL_WRAPPER = '<(.*?)>'

    def __init__(self, text):
        self.text = text
        self.re_limiter = re.compile(self.SYMBOL_WRAPPER)

    @staticmethod
    def remove_spaces(text):
        '''Remove espaços em branco da str'''
        return text.replace('\r', '').replace('\n', '').replace('\t', '')

    @staticmethod
    def text_to_sentences(text):
        '''Transforma str em lista'''
        return text.split('\n')
