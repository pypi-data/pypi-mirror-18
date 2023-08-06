# -*- encoding: utf-8 -*-
'''
Objetos para a manipulação de uma gramática livre do contexto.

Todos os algoritmos de Simplifier são implementações dos algoritmos do livro
"Linguagens Formais e Autômatos", do professor Paulo Blauth de Menezes, da 
UFRGS.
'''

from llclib.exceptions import EmptyGrammarError

class Simplifier(object):
    '''
    Atributos:
        grammar : Grammar
    '''
    def __init__(self, grammar):
        self.grammar = grammar

    def remove_empty(self):
        '''Algoritmo para exclusão de produções vazias da gramática.'''
        productions = self.grammar.productions

        '''
        Etapa 1: cria o conjunto de variáveis que chegam na palavra vazia.

        Procura pelas variáveis que geram diretamente a palavra vazia.
        Depois de encontrá-las, procura pelas palavras que indiretamente geram
        a palavra vazia, ou seja, geram uma variável que estava no conjunto
        encontrado no passo anterior.
        '''
        # Lista de não-terminais que geram a palavra vazia
        eps_set = [_ for _ in productions if ['V'] in productions[_]]

        old_len = 0     # cardinal de eps_set
        while len(eps_set) != old_len:
            old_len = len(eps_set)
            for x in [x for x in productions if not x in eps_set]:
                for y in productions[x]:
                    # Passa por todas as produções com x no lado direito
                    gen_empty = True
                    for _ in y:
                        if not _ in eps_set:
                            # Se já foi identificada como geradora de vazia
                            gen_empty = False
                            break
                    if gen_empty:
                        eps_set.append(x)

        '''
        Etapa 2: puxa as produções das variáveis geradoras da palavra vazia para
        as variáveis que as originam.

        Para todas as variáveis geradoras da palavra vazia encontradas na etapa
        anterior, puxa suas produções para a variável que as originam, sem as
        variáveis geradoras.
        '''

        '''
        Cria um dict de produções que NÃO geram a palavra vazia, associadas
        às suas variáveis geradoras.
        Exemplo:
        A -> BA|AB|V -----> {'A': [['B', 'A'], ['A', 'B']]}
        '''
        n_prod = {_: [__ for __ in productions[_] if __ != ['V']]
                  for _ in productions}

        for x in n_prod:
            '''
            Passa por todas as as variáveis que possuem produções, podendo
            o conjunto de produções estar vazio.
            '''
            for y in n_prod[x]:
                # y = produções da variável x
                i = 0
                for z in y:
                    '''
                    z = símbolo individual do não-terminal y
                    Exemplo:
                        x: [['A', 'b']]
                        y: ['A', 'b']
                        z: 'A'
                    '''
                    if z in eps_set:
                        '''
                        O símbolo individual z é uma não-terminal gerador,
                        então cria uma produção nova igual a y, porém sem o
                        símbolo z, com x no lado direito.
                        '''
                        production = y[:i] + y[i+1:]
                        if len(production) > 0 and not production in n_prod[x]:
                            n_prod[x].append(production)
                    i += 1

        '''
        Etapa 3: atualiza as produções da gramática. Como o algoritmo não aceita
        palavras vazias, não faz sua inclusão.
        '''
        self.grammar.productions = n_prod

        return True

    def get_fecho(self, producoes, fecho=[]):
        '''
        Constrói o fecho de uma lista de produções.

        Para toda produção da lista, verifica quais são unitárias e pega o fecho
        de suas produções de forma recursiva.

        Exemplo:
            Considerando a gramática G = ([A, B], [a], p, S), onde:
            P = {
                'S': [['A'], ['A','B']],
                'A': [['B'], ['a']],
                'B': [['a']]
                }
            A função get_fecho(P['S']), que pega o fecho das produções da
            variável S, tem a seguinte execução:
            get_fecho([['A'], ['A','B']])
            -> get_fecho([['B'], ['a']], ['A'])
            -> get_fecho([['a']], ['A', 'B'])
            -> get_fecho([], ['A', 'B'])
            -> ['A', 'B']
        '''
        if len(producoes) == 0:
            return fecho

        z = []
        # adiciona produções unitarias com variavel que não esteja no fecho a
        # lista z e ao fecho
        [(z.append(_[0]) or fecho.append(_[0])) for _ in producoes
         if len(_) == 1 and self.grammar.is_nonterminal(_[0])
         and not _[0] in z and not _[0] in fecho]

        n_prod = []
        for _ in z:
            try:
                for __ in self.grammar.productions[_]:
                    n_prod.append(__)
            except KeyError:
                pass

        return self.get_fecho(n_prod, fecho)

    def remove_unit(self):
        '''Remove produções unitárias.'''
        productions, fecho = self.grammar.productions, []

        for _ in productions:
            '''
            Etapa 1: construção do fecho da variável e já remove as produções
            unitárias.
            '''
            fecho = self.get_fecho(productions[_], [])

            # Remove as produções unitárias
            for left in fecho:
                if [left] in productions[_]:
                    productions[_].remove([left])

            '''
            Etapa 2: puxa as produções de terminais das variáveis unitárias para
            as produções das variáveis de seu fecho.
            '''
            for __ in fecho:
                try:
                    for x in productions[__]:
                        if len(x) != 1 or self.grammar.is_terminal(x[0]):
                            if not x in productions[_]:
                                productions[_].append(x)
                except KeyError:
                    '''
                    A variável do fecho não possui produções. Exemplo:
                    Variáveis: [S, A, B], Terminais: [a]
                    S -> A|B
                    A -> a
                    O fecho de S é [A, B], porém B não possui produções, logo,
                    nada será copiado para S de B, apenas de A.
                    '''
        return True

    def remove_useless(self):
        '''
        Etapa 1: verifica quais variáveis geram terminais.
        Caso uma variável não gere terminais, suas produções são excluídas, com
        exceção da variável inicial.
        Caso a variável inicial não gere terminais, a gramática é vazia.
        '''
        productions, v = self.grammar.productions, []

        old_len = -1
        while old_len != len(v):
            old_len = len(v)
            for x in productions:
                for y in productions[x]:
                    gen = True
                    for z in y:
                        if self.grammar.is_nonterminal(z) and z not in v:
                            gen = False
                            break
                    if gen and x not in v:
                        v.append(x)
                        break

        if not self.grammar.start in v:
            # o inicial não gera terminais
            raise EmptyGrammarError()

        # remove todas as produções que possuam um elemento não presente em v
        for x in productions.keys():
            if not x in v:
                del productions[x]
            else:
                for y in productions[x]:
                    for z in y:
                        if self.grammar.is_nonterminal(z) and not z in v:
                            productions[x].remove(y)
                            break

        # refaz as variaveis
        self.grammar.nonterminals = v

        # etapa 2: verificações
        t2 = []
        v2 = [self.grammar.start]

        lv, lt = -1, -1
        while len(v2) != lv or len(t2) != lt:
            lv = len(v2)
            lt = len(t2)
            for x in v2:
                # v2 + todos x que alcancam
                for y in productions[x]:
                    for z in y:
                        if self.grammar.is_nonterminal(z) and not z in v2:
                            v2.append(z)
                        elif self.grammar.is_terminal(z) and not z in t2:
                            t2.append(z)


        for x in productions.keys():
            if x not in v2:
                del productions[x]
            else:
                for y in productions[x]:
                    for z in y:
                        if (self.grammar.is_nonterminal(z) and not z in v2 or
                                self.grammar.is_terminal(z) and not z in t2):
                            productions[x].remove(y)
                            break

        self.grammar.productions = productions
        self.grammar.nonterminals = v2  # necessário?
        self.grammar.terminals = t2

        return True

    def create_nonterminal(self, terminal):
        '''
        Cria um não-terminal baseado em um terminal, inclusive com uma
        produção.
        '''
        if not 'T'+terminal in self.grammar.nonterminals:
            self.grammar.nonterminals.append('T'+terminal)
            self.grammar.productions['T'+terminal] = [terminal]

        return 'T'+terminal

    def fnc(self):
        '''Transforma a gramática para a FNC'''
        productions = self.grammar.productions

        # etapa 1: simplifica a gramatica

        '''
        Etapa 2: garante que o lado direito de todas as produções é composto
        unicamente por variáveis.
        Substitui terminais do lado direito por variáveis correspondentes,
        que caso não existam, são criadas.
        '''
        n_nonterminals = [] # novas variaveis
        for x in productions:
            for y in productions[x]:
                if len(y) >= 2:
                    i = 0
                    for z in y:
                        if self.grammar.is_terminal(z):
                            if not z in n_nonterminals:
                                n_nonterminals.append(z)
                            y[i] = 'T'+z
                        i += 1

        for x in n_nonterminals:
            self.grammar.nonterminals.append('T'+x)
            self.grammar.productions['T'+x] = [x]

        '''
        Etapa 3: garante que o lado direito de todas as produções é composto
        unicamente por 2 variáveis.
        '''
        n_nonterminals = []
        for x in productions:
            j = 0
            for y in productions[x]:
                while len(y) > 2:
                    for i in range(0, len(y), 2):
                        try:
                            a = y[i]
                            b = y[i+1]
                        except IndexError:
                            break

                        if (not ('T'+a+b in self.grammar.nonterminals or
                                 [a, b] in n_nonterminals)):
                            n_nonterminals.append([a, b])

                        productions[x][j][i] = 'T'+a+b
                        try:
                            del productions[x][j][i+1]
                        except IndexError:
                            pass
                    j += 1

        for x in n_nonterminals:
            self.grammar.nonterminals.append('T'+x[0]+x[1])
            self.grammar.productions['T'+x[0]+x[1]] = [x]

        return True
