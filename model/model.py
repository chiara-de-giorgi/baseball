import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapT={}
        self._codeT={}

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsYear(self, year):
        return DAO.getTeamsYear(year)

    def buildGraph(self, year):
        self._graph.clear()

        nodes=DAO.getTeamsYear(year)
        self._graph.add_nodes_from(nodes)
        for n in nodes:
            self._idMapT[n.ID]=n
            self._codeT[n.teamCode]=n

        allEdges=DAO.getAllEdges(self._idMapT, year)
        for e in allEdges:
            self._graph.add_edge(e.t1, e.t2, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getVicini(self, teamCode):
        source=self._codeT[teamCode]
        vicini=self._graph.neighbors(source)
        viciniTuples=[]
        for v in vicini:
            peso_arco = self._graph[source][v]["weight"]
            #Lista di tuple con vicino e peso dell'arco che ti porta
            viciniTuples.append((v, peso_arco))

        viciniTuples.sort(key=lambda x: x[1], reverse=True)
        return source, viciniTuples


    def getBestPath(self, teamCode):
        source = self._codeT[teamCode]
        parziale=[source]

        self._bestPath=[]
        self._bestScore=0

        self._ricorsione(parziale)

        return self._bestPath, self._bestScore



    def _ricorsione(self, parziale):
        #1) Verifico la condizione di ottimalità
        if len(parziale)>1:
            score=self._getScore(parziale)
            if score > self._bestScore:
                self._bestScore=score
                self._bestPath=copy.deepcopy(parziale)

        #2)Condizione terminale --> Assente

        #2) Condizione ricorsiva
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                if len(parziale)>1 and self._graph[parziale[-2]][parziale[-1]]["weight"] > self._graph[parziale[-1]][n]["weight"]:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()


    def _getScore(self, path):
        score=0
        for i in range(len(path)-1):
            score += self._graph[path[i]][path[i+1]]["weight"]
        return score


