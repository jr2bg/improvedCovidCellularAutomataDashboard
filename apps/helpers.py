@app.callback(
     [Output("fig-ncc-covid19owid", "figure"),
     Output("fig-ccc-covid19owid", "figure"),
     Output("fig-ndc-covid19owid", "figure"),
     Output("fig-cdc-covid19owid", "figure"),
     Output("anim-covid19owid", "figure")],
    [Input('fcovid19owid-button-start', 'n_clicks')],
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
                       keyFuncionTransicionExpuestoInfec
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
    df, l_frames = iterations_covid19owid(
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
              )
    print(df.keys())
    # print(df["% nuevas muertes confirmadas"])
    # print(df["% acumulado muertes confirmadas"])
    # print(df["% nuevas muertes confirmadas"] == df["% acumulado muertes confirmadas"])

    # nuevos casos confirmados
    fig_ncc = go.Figure(data = go.Scatter(x = df["t"],
                                      y = df["% nuevos casos confirmados"],
                                      mode="lines+markers"))
    fig_ncc.update_layout(title = "Nuevos casos confirmados",
                      xaxis_title="t",
                      yaxis_title="% nuevos casos confirmados")

    # acumulado de casos confirmados
    fig_ccc = go.Figure(data = go.Scatter(x = df["t"],
                                      y = df["% de casos confirmados acumulados"],
                                      mode="lines+markers"))
    fig_ccc.update_layout(title = "Acumulado casos confirmados",
                      xaxis_title="t",
                      yaxis_title="% de casos confirmados acumulados")

    # nuevas muertes confirmadas
    fig_ndc = go.Figure(data = go.Scatter(x = df["t"],
                                      y = df["% nuevas muertes confirmadas"],
                                      mode="lines+markers"))
    fig_ndc.update_layout(title = "Nuevas muertes confirmadas",
                      xaxis_title="t",
                      yaxis_title="% nuevas muertes confirmadas")

    # acumulado miertes confirmadas
    fig_cdc = go.Figure(data = go.Scatter(x = df["t"],
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
    fig_animation=px.imshow(frames,
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

    return fig_ncc, fig_ccc, fig_ndc, fig_cdc, fig_animation
