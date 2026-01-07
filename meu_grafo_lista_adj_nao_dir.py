from bibgrafo.grafo_lista_adj_nao_dir import GrafoListaAdjacenciaNaoDirecionado
from bibgrafo.grafo_errors import *


class MeuGrafo(GrafoListaAdjacenciaNaoDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        '''

        nao_adjacentes = set()
        vertices = self.vertices  # lista de rótulos dos vértices
        arestas_existentes = set()

        # Monta conjunto de pares adjacentes existentes
        for aresta in self.arestas:
            v1 = aresta.vertice1.rotulo
            v2 = aresta.vertice2.rotulo
            arestas_existentes.add(f"{v1}-{v2}")
            arestas_existentes.add(f"{v2}-{v1}")  # grafo não direcionado

        # Verifica todos os pares possíveis
        for v1 in vertices:
            for v2 in vertices:
                if v1 != v2:
                    par = f"{v1}-{v2}"
                    if par not in arestas_existentes:
                        nao_adjacentes.add(par)

        return nao_adjacentes


    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''

        for a in self.arestas:
            if self.arestas[a].v1 == self.arestas[a].v2:
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''

        if V not in [v.rotulo for v in self.vertices]:
            raise VerticeInvalidoError
        grau = 0
        for a in self.arestas.values():
            v1 = a.v1.rotulo
            v2 = a.v2.rotulo

            if V == v1 and V == v2:
                grau += 2
            elif V == v1 or V == v2:
                grau += 1
        return grau


    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''


        pares = set()

        for aresta in self.arestas.values():
            v1 = aresta.v1.rotulo
            v2 = aresta.v2.rotulo

            par = tuple (sorted([v1, v2]))

            if par in pares:
                return True
            pares.add(par)

        return False


    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: Um string com o rótulo do vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''

        lista = []
        for a in self.arestas.values():  # pega os objetos
            if a.v1.rotulo == V or a.v2.rotulo == V:
                lista.append(a)
        return lista


    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''

        for vertice in self.vertices:
            vizinhos = self.arestas[vertice]
            esperados = [v for v in self.vertices if v != vertice]
            if set(vizinhos) != set(esperados):
                return False
        return True


    def dfs(self, V=""):
        if V not in [v.rotulo for v in self.vertices]:
            raise VerticeInvalidoError(f"O vértice {V} não existe no grafo.")

        visitados = set()
        arvore_dfs = MeuGrafo()
        arvore_dfs.adiciona_vertice(V)

        def visitar(v):
            visitados.add(v)

            arestas_v = self.arestas_sobre_vertice(v)
            arestas_v = sorted(arestas_v, key=lambda a: a.rotulo)

            for a in arestas_v:
                v1 = a.v1.rotulo
                v2 = a.v2.rotulo
                vizinho = v2 if v1 == v else v1

                if vizinho not in visitados:
                    arvore_dfs.adiciona_vertice(vizinho)
                    arvore_dfs.adiciona_aresta(a.rotulo, v, vizinho)
                    visitar(vizinho)

        visitar(V)

        return [a.rotulo for a in arvore_dfs.arestas.values()]

    def ha_ciclo(self):
        '''
        Verifica se o grafo possui ciclo.
        :return: Um valor booleano que indica se existe ciclo (True) ou não (False)
        '''
        visitados = set()

        def dfs(v, pai):
            visitados.add(v)
            for nome_aresta in self.arestas_sobre_vertice(v):
                aresta = self.arestas[nome_aresta]
                v1 = aresta.v1.rotulo
                v2 = aresta.v2.rotulo
                vizinho = v2 if v1 == v else v1

                if vizinho not in visitados:
                    if dfs(vizinho, v):  # continua a busca
                        return True
                elif vizinho != pai:
                    # Encontrou um vizinho já visitado que não é o pai → ciclo
                    return True
            return False

        # Verifica todos os componentes do grafo
        for vertice in self.vertices:
            if vertice not in visitados:
                if dfs(vertice, None):
                    return True

        return False

    def eh_arvore(self):
        '''
        Verifica se o grafo é uma árvore.
        :return: False se não for árvore, ou uma lista com os nós folhas se for.
        '''
        visitados = set()

        def dfs(v, pai):
            visitados.add(v)
            for nome_aresta in self.arestas_sobre_vertice(v):
                aresta = self.arestas[nome_aresta]
                v1 = aresta.v1.rotulo
                v2 = aresta.v2.rotulo
                vizinho = v2 if v1 == v else v1

                if vizinho not in visitados:
                    if dfs(vizinho, v):  # ciclo encontrado
                        return True
                elif vizinho != pai:
                    # vizinho já visitado que não é o pai → ciclo
                    return True
            return False

        # Verifica ciclos e conectividade
        primeiro_vertice = next(iter(self.vertices), None)
        if primeiro_vertice is None:
            return False  # grafo vazio não é árvore

        if dfs(primeiro_vertice, None):
            return False  # tem ciclo

        if len(visitados) != len(self.vertices):
            return False  # não é conexo

        # Se chegou aqui → é árvore
        folhas = []
        for v in self.vertices:
            grau = len(self.arestas_sobre_vertice(v))
            if grau == 1:
                folhas.append(v)

        return folhas

    def eh_bipartido(self):
        '''
        Verifica se o grafo é bipartido.
        :return: True se for bipartido, False caso contrário
        '''
        cor = {}  # dicionário para armazenar a cor de cada vértice

        for vertice in self.vertices:
            if vertice not in cor:  # ainda não colorido → novo componente
                cor[vertice] = 0
                fila = [vertice]

                while fila:
                    v = fila.pop(0)
                    for nome_aresta in self.arestas_sobre_vertice(v):
                        aresta = self.arestas[nome_aresta]
                        v1 = aresta.v1.rotulo
                        v2 = aresta.v2.rotulo
                        vizinho = v2 if v1 == v else v1

                        if vizinho not in cor:
                            # atribui cor oposta ao vizinho
                            cor[vizinho] = 1 - cor[v]
                            fila.append(vizinho)
                        elif cor[vizinho] == cor[v]:
                            # vizinho já tem mesma cor → não é bipartido
                            return False
        return True