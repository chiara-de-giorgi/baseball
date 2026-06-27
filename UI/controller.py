import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._yearValue=None
        self._teamValue=None

    def handleCreaGrafo(self, e):
        year=self._view._ddAnno.value
        if year is None or year=="":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un anno per creare il grafo", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(year)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.update_page()

    def handleDettagli(self, e):
        teamCode=self._view._ddSquadra.value
        if teamCode is None or teamCode=="":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare una squadra!", color="red"))
            self._view.update_page()
            return

        source, listaVicini=self._model.getVicini(teamCode)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {source.name} con relativo peso dell'arco."))

        for nodo, peso  in listaVicini:
            self._view._txt_result.controls.append(ft.Text(f"{peso} - {nodo.name}"))

        self._view.update_page()

    def handlePercorso(self, e):
        teamCode=self._view._ddSquadra.value
        if teamCode is None or teamCode=="":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare una squadra!", color="red"))
            self._view.update_page()
            return

        bestPath, score= self._model.getBestPath(teamCode)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Ho trovato un cammino ottimo che parte dal vertice scelto ({teamCode}) di lunghezza {len(bestPath)} con peso totale pari a {score}."))
        self._view._txt_result.controls.append(ft.Text("Di seguito i nodi che lo compongono:"))
        for n in bestPath:
            self._view._txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()

    def handleYearSelections(self, e):
        year=self._view._ddAnno.value

        teams=self._model.getTeamsYear(year)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(teams)} squadre che hanno giocato nel {year}."))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))

        self.fillDDSqaudre(e, teams)
        self._view.update_page()





    def fillDDYears(self):
        years = self._model.getAllYears()
        yearsDDOption = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceDDyears), years))
        self._view._ddAnno.options = yearsDDOption
        self._view.update_page()

    def _choiceDDyears(self, e):
        self._yearValue = e.control.data

    def fillDDSqaudre(self, e, teams):
        teamsDDOption = list(map(lambda x: ft.dropdown.Option(data=x, key=x.teamCode, on_click=self._choiceDDteams), teams))
        self._view._ddSquadra.options = teamsDDOption
        self._view.update_page()

    def _choiceDDteams(self, e):
        self._teamValue=e.control.data