import dash_html_components as html
import dash_core_components as dcc


class GraphComponent():
    def __init__(self, sucesoEstudiado):
        self.sucesoEstudiado = sucesoEstudiado

    def establecerIdTab(self, idTab):
        self.idTab = idTab
        self.idGraph  = idTab + self.sucesoEstudiado + '-graph'
        self.idLoader = idTab + self.sucesoEstudiado + '-loader'

    def establecerGraphRender(self):
        self.graphRender = dcc.Loading(
            id = self.idLoader,
            children=html.Div([
                dcc.Graph(
                    id = self.idGraph
                    )
                ]),
            type="default"
            )

animacion = GraphComponent(sucesoEstudiado = "evolucion")

nuevosCasosConfirmados = GraphComponent(
    sucesoEstudiado = "nuevos-casos-confirmados"
    )

acumuladoCasosConfirmados = GraphComponent(
    sucesoEstudiado = "acumulado-casos-confirmados"
    )

nuevasMuertesConfirmadas = GraphComponent(
    sucesoEstudiado = "nuevas-muertes-confirmadas"
    )

acumuladoMuertesConfirmadas = GraphComponent(
    sucesoEstudiado = 'acumulado-muertes-confirmadas'
    )


componentes = [
    animacion,
    nuevosCasosConfirmados,
    acumuladoCasosConfirmados,
    nuevasMuertesConfirmadas,
    acumuladoMuertesConfirmadas
    ]
