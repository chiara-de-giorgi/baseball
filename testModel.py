from model.model import Model

myModel=Model()
myModel.getTeamsYear(2012)
myModel.buildGraph(2012)
nodi, archi=myModel.getGraphDetails()
print (f"Grafo creato!")
print (f"Il grafo ha {nodi} nodi e {archi} archi")

#435 archi