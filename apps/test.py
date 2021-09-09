# -*- coding: utf-8 -*-

#import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output, State
from math import inf

from app import app

import UI.inputs.components as IC
import UI.layout

idTab = "test"
titulo = "testeando ando"

UI.layout.asignarIdTabAComponentes(idTab)

layout = UI.layout.layout(titulo)

@app.callback(Output(
    IC.numeroFilasMapa.idSeleccion,
    'children'
    ),
    [Input(
        IC.numeroFilasMapa.idInput,
        IC.numeroFilasMapa.formatoValor,
        )
    ]
)
def display_value(value):
    return "Número de filas: {}".format(value)


@app.callback(Output(
    IC.numeroColumnasMapa.idSeleccion,
    'children'
    ),
    [Input(
        IC.numeroColumnasMapa.idInput,
        IC.numeroColumnasMapa.formatoValor,
        )
    ]
)
def display_value(value):
    return "Número de columnas: {}".format(value)


@app.callback(Output(
    IC.radioEsferaInfluencia.idSeleccion,
    'children'
    ),
    [Input(
        IC.radioEsferaInfluencia.idInput,
        IC.radioEsferaInfluencia.formatoValor,
        )
    ]
)
def display_value(value):
    return "Radio de la esfera de influencia: {}".format(value)


@app.callback(Output(
    IC.densidadPoblacion.idSeleccion,
    'children'
    ),
    [Input(
        IC.densidadPoblacion.idInput,
        IC.densidadPoblacion.formatoValor,
        )
    ]
)
def display_value(value):
    return "Densidad de población: {}".format(value)


@app.callback(Output(
    IC.numeroCiclos.idSeleccion,
    'children'
    ),
    [Input(
        IC.numeroCiclos.idInput,
        IC.numeroCiclos.formatoValor,
        )
    ]
)
def display_value(value):
    return "Número de ciclos: {}".format(value)


@app.callback(Output(
    IC.numeroReproduccionBasico.idSeleccion,
    'children'
    ),
    [Input(
        IC.numeroReproduccionBasico.idInput,
        IC.numeroReproduccionBasico.formatoValor,
        )
    ]
)
def display_value(value):
    return "R_0: {}".format(value)


@app.callback(Output(
    IC.tiempoInfeccioso.idSeleccion,
    'children'
    ),
    [Input(
        IC.tiempoInfeccioso.idInput,
        IC.tiempoInfeccioso.formatoValor,
        )
    ]
)
def display_value(value):
    return "Tiempo de infeccioso: {}".format(value)


@app.callback(Output(
    IC.caseFatalityRatio.idSeleccion,
    'children'
    ),
    [Input(
        IC.caseFatalityRatio.idInput,
        IC.caseFatalityRatio.formatoValor,
        )
    ]
)
def display_value(value):
    return "Case-fatality risk: {}".format(value)


@app.callback(Output(
    IC.tiempoPrevioInfeccioso.idSeleccion,
    'children'
    ),
    [Input(
        IC.tiempoPrevioInfeccioso.idInput,
        IC.tiempoPrevioInfeccioso.formatoValor,
        )
    ]
)
def display_value(value):
    return "t_I: {}".format(value)


@app.callback(Output(
    IC.probabilidadEntrarCuarentena.idSeleccion,
    'children'
    ),
    [Input(
        IC.probabilidadEntrarCuarentena.idInput,
        IC.probabilidadEntrarCuarentena.formatoValor,
        )
    ]
)
def display_value(value):
    return "p_Q: {}".format(value)


@app.callback(Output(
    IC.tiempoPrevioEntrarCuarentena.idSeleccion,
    'children'
    ),
    [Input(
        IC.tiempoPrevioEntrarCuarentena.idInput,
        IC.tiempoPrevioEntrarCuarentena.formatoValor,
        )
    ]
)
def display_value(value):
    return "t_Q: {}".format(value)


@app.callback(Output(
    IC.tiempoPrevioACierreDeActividades.idSeleccion,
    'children'
    ),
    [Input(
        IC.tiempoPrevioACierreDeActividades.idInput,
        IC.tiempoPrevioACierreDeActividades.formatoValor,
        )
    ]
)
def display_value(value):
    #if value > 0:
    #    return "t_L: {}".format(value)
    #return "t_L: inf"
    return "t_L: {}".format(value)


@app.callback(Output(
    IC.tiempoPrevioARecuperadoOFallecido.idSeleccion,
    'children'
    ),
    [Input(
        IC.tiempoPrevioARecuperadoOFallecido.idInput,
        IC.tiempoPrevioARecuperadoOFallecido.formatoValor,
        )
    ]
)
def display_value(value):
    return "t_R: {}".format(value)


@app.callback(Output(
    IC.numeroInicialDeExpuestos.idSeleccion,
    'children'
    ),
    [Input(
        IC.numeroInicialDeExpuestos.idInput,
        IC.numeroInicialDeExpuestos.formatoValor,
        )
    ]
)
def display_value(value):
    return "E_in: {}".format(value)


@app.callback(Output(
    IC.numeroInicialDeInfectados.idSeleccion,
    'children'
    ),
    [Input(
        IC.numeroInicialDeInfectados.idInput,
        IC.numeroInicialDeInfectados.formatoValor,
        )
    ]
)
def display_value(value):
    return "I_in: {}".format(value)
