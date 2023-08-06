# -*- encoding: utf-8 -*-
'''Exceptions possíveis das transformações das gramáticas'''

class MultipleStartsError(Exception):
    '''A gramática tem múltiplas variáveis iniciais.'''
    def __init__(self):
        self.strerror = 'Múltiplas variáveis iniciais.'
        super(MultipleStartsError, self).__init__(self.strerror)

class EmptyGrammarError(Exception):
    '''Gramática vazia, sua variável inicial não gera terminais.'''
    def __init__(self):
        self.strerror = 'Gramática vazia.'
        super(EmptyGrammarError, self).__init__(self.strerror)

class InvalidNonterminalError(Exception):
    '''A variável tem uma variável não permitida.'''
    def __init__(self):
        self.strerror = 'Variável não-terminal inválida.'
        super(InvalidNonterminalError, self).__init__(self.strerror)

class GrammarException(Exception):
    '''Exceção genérica para erros da gramática.'''
    def __init__(self, strerror=''):
        self.strerror = strerror
        super(GrammarException, self).__init__(self.strerror)
