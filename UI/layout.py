import dash_html_components as html

import UI.inputs.components as IC
import UI.outputs.plots as GC
#from UI.outputs import selectedInputs

def asignarIdTabAComponentes(idTab):
    for componente in IC.componentes:
        componente.establecerIdTab(idTab)
        componente.establecerInputRender()

    for componente in GC.componentes:
        componente.establecerIdTab(idTab)
        componente.establecerGraphRender()


def layout(titulo):

    renderComponentesInput = []
    for componente in IC.componentes:
        if componente.mostrarInput:
            renderComponentesInput += [componente.renderizarSeleccion()]
        renderComponentesInput += [componente.obtenerInputRender()]

    return html.Div([
        # titulo
        html.Div([
            html.H4(titulo)
            ]),
        ] +
        # parametros
        renderComponentesInput +

        [html.Div([
            GC.animacion.graphRender
            ])] +

        [html.Div([
            html.Div([
                html.Div([
                    GC.nuevosCasosConfirmados.graphRender,
                    ], className = 'six columns'),
                html.Div([
                    GC.acumuladoCasosConfirmados.graphRender,
                    ], className = 'six columns'),
                ], className = "row"),

            html.Div([
                html.Div([
                    GC.nuevasMuertesConfirmadas.graphRender,
                    ], className = 'six columns'),
                html.Div([
                    GC.acumuladoMuertesConfirmadas.graphRender,
                    ], className = 'six columns'),
                ], className = "row"),
            ])
        ]
        )
