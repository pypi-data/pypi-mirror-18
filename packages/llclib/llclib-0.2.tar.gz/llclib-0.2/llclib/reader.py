# -*- encoding: utf-8 -*-
'''Provê um leitor personalizado para uma gramática livre do contexto'''

from llclib.grammar import GrammarReader, Grammar
from llclib.exceptions import MultipleStartsError

class GrammarTReader(GrammarReader):
    '''
    Faz a importação de uma gramática, de um arquivo para um objeto, seguindo a
    especificação do trabalho de autômatos.

    Atributos
        text       : str
        re_limiter : re
    '''

    '''
    Expressão regular para os limitadores de um símbolo.

    Um símbolo qualquer, terminal ou não terminal, na especificação normal, está
    no formato:
    [ S ]
    Essa expressão regular deve obter o símbolo "S", separando-o dos seus
    limitadores.
    '''
    SYMBOL_WRAPPER = r'\[\ (.*?)\ \]'

    def __init__(self, text):
        if not isinstance(text, list):
            text = self.text_to_sentences(text)

        self.sentences = text  # text é uma lista

        super(GrammarTReader, self).__init__(text)

    def extract_symbol(self, sentence):
        '''
        Extrai um símbolo de dentro dos seus limitadores.

        Usa a expressão regular já compilada que está no atributo re_limiter
        da classe, para extrair um símbolo de seus limitadores.
        '''
        symbol = self.re_limiter.findall(sentence)
        try:
            return symbol[0]
        except IndexError:
            return None

    @staticmethod
    def state_sentence(sentence):
        '''Verifica a qual estado pertence a sentence'''
        if sentence[0:9] == 'Terminais' or sentence[0:10] == '#Terminais':
            return 1
        elif sentence[0:9] == 'Variaveis' or sentence[0:10] == '#Variaveis':
            return 2
        elif sentence[0:7] == 'Inicial' or sentence[0:8] == '#Inicial':
            return 3
        elif sentence[0:6] == 'Regras' or sentence[0:7] == '#Regras':
            return 4
        return 0

    def generate_grammar(self):
        '''
        Transforma o texto de entrada ou conjunto de sentenças em uma gramática.

        Usa as regras definidas na especificação do trabalho para realizar a
        extração de terminais, não-terminais, símbolo inicial e regras de
        produção, do texto de entrada. Para efetuar a extração, usa os
        marcadores de bloco como estados.
        O conjunto de dados extraídos é utilizado para a criação de uma
        gramática da biblioteca libllc.
        '''
        state, start = 0, None
        terminals, nonterminals, productions = [], [], {}

        sentences = self.sentences
        for sentence in sentences:
            sentence = self.remove_spaces(sentence)
            # verifica se a sentença é uma mudança de estado
            new_state = self.state_sentence(sentence)
            if new_state > 0:
                state = new_state
                continue

            # remove comentários particionando a partir do símbolo '#'
            sentence = sentence.split('#')[0]
            if sentence == '':
                continue

            # se está em um estado de definição de símbolos, extrai o símbolo
            if state > 0 and state < 4:
                symbol = self.extract_symbol(sentence)

            # extração de acordo com o estado
            if state == 1:
                terminals.append(symbol)
            elif state == 2:
                nonterminals.append(symbol)
            elif state == 3:
                if start is None:
                    start = symbol
                else:
                    # múltiplos símbolos de entrada encontrados
                    raise MultipleStartsError()
            elif state == 4:
                # [ S ] > [ A ] [ B ]
                sentence = sentence.split('>')
                production = sentence[1]
                origin = self.extract_symbol(sentence[0])

                s_productions = self.re_limiter.findall(production)
                try:
                    productions[origin].append(s_productions)
                except KeyError:
                    productions[origin] = [s_productions]

        return Grammar(nonterminals, terminals, productions, start)
