# -*- coding: utf-8 -*-

#import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly.graph_objects import Figure, Scatter
from plotly.express import imshow
from math import inf
import xarray as xr

from app import app
import UI.inputs.components as IC
import UI.outputs.plots as GC
import UI.layout
from apps.evolucionPlusCasosYDecesos import iterations
import apps.utils.save_data as sd

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

@app.callback(
     [Output(GC.nuevosCasosConfirmados.idGraph, "figure"),
     Output(GC.acumuladoCasosConfirmados.idGraph, "figure"),
     Output(GC.nuevasMuertesConfirmadas.idGraph, "figure"),
     Output(GC.acumuladoMuertesConfirmadas.idGraph, "figure"),
     Output(GC.animacion.idGraph, "figure")],
    [Input(IC.botonStart.idInput, 'n_clicks')],
    [State(IC.numeroFilasMapa.idInput,'value'),
     State(IC.numeroColumnasMapa.idInput,'value'),
     State(IC.radioEsferaInfluencia.idInput, 'value'),
     State(IC.densidadPoblacion.idInput,'value'),
     State(IC.numeroCiclos.idInput,'value'),
     State(IC.numeroReproduccionBasico.idInput,'value'),
     State(IC.tiempoInfeccioso.idInput,'value'),
     State(IC.tiempoPrevioInfeccioso.idInput,'value'),
     State(IC.probabilidadEntrarCuarentena.idInput,'value'),
     State(IC.tiempoPrevioEntrarCuarentena.idInput,'value'),
     State(IC.caseFatalityRatio.idInput,'value'),
     State(IC.tiempoPrevioACierreDeActividades.idInput,'value'),
     State(IC.tiempoPrevioARecuperadoOFallecido.idInput,'value'),
     State(IC.numeroInicialDeExpuestos.idInput,'value'),
     State(IC.numeroInicialDeInfectados.idInput,'value'),
     State(IC.funcionDeTransicionExpuestoAInfectado.idInput,'value'),
     ])
def display_values_tot(btn_start,
                       sz_r,
                       sz_c,
                       d,
                       D,
                       n_cycles,
                       R_0,
                       t_infec,
                       t_I,
                       p_Q,
                       t_Q,
                       cfr,
                       t_L,
                       t_R,
                       E_in,
                       I_in,
                       pdfORcdf
                       ):

    print("sz_r: %d" %(sz_r))
    print("sz_c: %d" %(sz_c))
    print("d: %d" %(d))
    print("D: %f" %(D))
    print("n_cycles: %d" %(n_cycles))
    print("R_0: %f" %(R_0))
    print("t_infec: %d" %(t_infec))
    print("t_I: %d" %(t_I))
    print("p_Q: %f" %(p_Q))
    print("t_Q: %d" %(t_Q))
    print("p_D: %d" %(cfr))
    if t_L < 0: t_L = inf;
    print('t_L: %f' %(t_L))
    print("t_R: %d" %(t_R))
    print("E_in: %d" %(E_in))
    print("I_in: %d" %(I_in))
    print("Funcion a usar: %s" %(pdfORcdf))
    df, l_frames = iterations(
               sz_r,
               sz_c,
               d,
               D,
               n_cycles,
               R_0,
               t_infec,
               t_I,
               p_Q,
               t_Q,
               cfr,
               t_L,
               t_R,
               E_in,
               I_in,
               pdfORcdf,
              )
    print(df.keys())
    # print(df["% nuevas muertes confirmadas"])
    # print(df["% acumulado muertes confirmadas"])
    # print(df["% nuevas muertes confirmadas"] == df["% acumulado muertes confirmadas"])

    # nuevos casos confirmados
    fig_ncc = Figure(data = Scatter(x = df["t"],
                                      y = df["% nuevos casos confirmados"],
                                      mode="lines+markers"))
    fig_ncc.update_layout(title = "Nuevos casos confirmados",
                      xaxis_title="t",
                      yaxis_title="% nuevos casos confirmados")

    # acumulado de casos confirmados
    fig_ccc = Figure(data = Scatter(x = df["t"],
                                      y = df["% de casos confirmados acumulados"],
                                      mode="lines+markers"))
    fig_ccc.update_layout(title = "Acumulado casos confirmados",
                      xaxis_title="t",
                      yaxis_title="% de casos confirmados acumulados")

    # nuevas muertes confirmadas
    fig_ndc = Figure(data = Scatter(x = df["t"],
                                      y = df["% nuevas muertes confirmadas"],
                                      mode="lines+markers"))
    fig_ndc.update_layout(title = "Nuevas muertes confirmadas",
                      xaxis_title="t",
                      yaxis_title="% nuevas muertes confirmadas")

    # acumulado miertes confirmadas
    fig_cdc = Figure(data = Scatter(x = df["t"],
                                      y = df["% acumulado muertes confirmadas"],
                                      mode="lines+markers"))
    fig_cdc.update_layout(title = "Acumulado de muertes confirmadas",
                      xaxis_title="t",
                      yaxis_title="% acumulado muertes confirmadas")


    # frames para la animación
    frames = xr.DataArray(l_frames,
                          dims=("tiempo", "row", "col"),
                          coords={"tiempo":[t for t in range(n_cycles)]}
                          )
    colors =  ["#000000",
               "#FFFFFF",
               "#0000FF",
               "#FFFFFF",
               "#FF00FF",
               "#FFFFFF",
               "#FF0000",
               "#FFFFFF",
               "#00FF00",
               "#FFFFFF",
               "#FFFF00",
               "#FFFFFF",
               "#800080"]
    fig_animation = imshow(frames,
                            animation_frame="tiempo",
                            #labels={"x":None, "y":None, "color":None},
                            range_color=[0,6],
                            #width=1400,
                            height=800,
                            aspect="equal",
                            #color_continuous_scale = "Rainbow"
                            color_continuous_scale = colors
                            #x=None,
                            #y=None
                            )
    ##################
    ########### ALMACENAMIENTO DE LA INFO
    #################
    inpt_params = {
                    "numero_columnas":sz_r,
                    "numero_filas":sz_c,
                    "radio_vecindad_Moore":d,
                    "densidad":D,
                    "numero_ciclos":n_cycles,
                    "numero_infeccion_basico":R_0,
                    "tiempo_puede_infectar":t_infec,
                    "tiempo_incubacion":t_I,
                    "probabilidad_entrar_cuarentena":p_Q,
                    "tiempo_minimo_previo_cuarentena":t_Q,
                    "case-fatality_risk":cfr,
                    "tiempo_hasta_lockdown":t_L,
                    "tiempo_previo_r":t_R,
                    "numero_expuestos_inicial":E_in,
                    "numero_infectados_inicial":I_in,
                    "funcion_de_transicion_Expuesto_A_Infectado": pdfORcdf,
                    }
    # creacion del folder necesario
    folder, date_info = sd.create_folder()
    print("|------- DIRECTORIO CREADO -------|")
    # guardado de los parámetros
    sd.save_info_txt(inpt_params, folder, date_info)
    print("|------- PARÁMETROS GUARDADOS -------|")
    # creacion del video
    sd.mk_video(l_frames, folder)
    print("|------- VIDEO GUARDADO -------|")
    # creación del csv + plots
    sd.generate_plots_csv(df, folder)
    print("|------- GRÁFICAS GUARDADAS -------|")

    print("|------- CARPETA: %s -------|" % date_info )

    return fig_ncc, fig_ccc, fig_ndc, fig_cdc, fig_animation
