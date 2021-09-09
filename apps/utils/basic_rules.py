# -*- coding: utf-8 -*-
# este archivo será el usado por todos los demás
from random import randint, uniform, sample
import numpy as np
from scipy.stats import lognorm

from copy import deepcopy

def f_getNeigh(sz_r, sz_c,r,c,d, d_variable = True):
    '''
    función que da la vecindad para el elemento ubicado en
    la fila r y columna c
    sz_r y sz_c corresponden al tamaño del array
    d -> radio máximo de la esfera de influencia
    d_variable -> radio de la esfera de influencia es variable o es d
    '''
    if d_variable:
        rd = randint(0,d)
    else:
        rd = d

    ng = []
    for i in range(-rd, rd +1):
        for j in range(-rd, rd+1):
            if r + i >= 0 and r + i < sz_r and c + j>= 0 and c + j < sz_c and \
                not (i == 0 and j == 0):
                ng.append((r+i,c+j))
    return ng


def s_2_e(p_E, npa, ng, arr_population):
    '''
    función que determina si la celda puede pasar de S a E
    para ello, la celda debe ser suceptible
    Se requiere la vecindad, y la probabilidad de pasar a E
    así como la población arr_population
    también se requiere de un número pseudo-aleatorio npa, para determinar si
    pasa o no a E
    '''
    cnt = 0
    for r,c in ng:
        if arr_population[r][c] == 2 or arr_population[r][c] == 3:
            cnt += 1

    if npa <= p_E * cnt:
        return 2 # pasa a Expuesto
    return 1    # queda en Suceptible


def e_2_i(l_p_I, npa, t_I, t):
    '''
    función que determina si la celda pasa de Expuesto (2) a Infectado (3)
    p_I -> probabilidad de pasar a infectado
    npa -> número pseudo aleatorio
    t_I -> tiempo mínimo de permanencia en expuesto
    t -> tiempo que la celda ha pasado en Expuesto
    '''
    # si el tiempo que ha pasado la celda en Expuesto es mayor a la cantidad
    # de entradas en la lista, consideramos el valor de la última entrada--->??
    #   ----->>> POR QUÉ??
    if t >= len(l_p_I):
        p_I = l_p_I[-1]
    else:
        p_I = l_p_I[t]

    if t_I <= t and npa <= p_I:
        return 3
    return 2


def i_2qr(p_Q, ff_p_R, p_dec , npa, t_Q, t_R, t):
    '''
    función que determina si la celda en infectado (3) pasa a
    en cuarentena (4) o a recuperado (5)
    p_Q -> probabilidad de pasar a en cuarentena
    ff_p_R -> función que indica la probabilidad de pasar a R como f(t)
    npa -> número pseudo aleatorio
    t_Q -> tiempo mínimo para entrar a Q
    t_R -> tiempo mínimo para entrar a recuperado
    t   -> tiempo en I
    '''

    if t_Q <= t and npa <= p_Q:
        return 4

    if t_R <= t:
        if p_Q < npa <= ff_p_R(t):
            return 5 # recuperado
        elif p_Q + ff_p_R(t) < npa <= p_Q + ff_p_R(t) + p_dec:
            return 6 #fallecido

    return 3


def q_2_r(f_p_R, p_dec, npa, t_R, t):
    '''
    función que determina si de Q (4) pasa a R (5)
    f_p_R -> función que indica la probabilidad de pasar a R como f(t)
    npa -> número pseudo aleatorio
    t_R -> tiempo mínimo para que entre a R
    t   -> tiempo que ha pasado en Q
    '''
    if t_R <= t and npa <= f_p_R(t):
        return 5
    elif t_R <=t and f_p_R(t) < npa <= f_p_R(t) + p_dec:
        return 6 # fallecido

    return 4

def f_initPop(sz_r, sz_c, D):
    '''
    función para inicializar la población
    '''
    arr_population = [[0 for i in range(sz_c)] for j in range(sz_r)]
    # total de la población
    t_pop = int(D * sz_r * sz_c)

    # se eligen t_pop celdas de arr_population para que sean los habitantes
    lst = [(r,c) for c in range(sz_c) for r in range(sz_r)]

    habs = sample(lst, t_pop)

    # todos los habitantes son suceptibles en el arreglo de la población
    for r,c in habs:
        arr_population[r][c] = 1

    return arr_population, habs


def f_newPop(sz_r, sz_c, arr_population, change_pop):
    '''
    función que modificará el arr_population de acuerdo con change_pop
    change_pop -> int
    '''
    # si se agregan nuevos elementos
    if change_pop > 0:
        lp2add = []
        for i in range(sz_r):
            for j in range(sz_c):
                # celda vacía
                if arr_population[i][j] == 0:
                    lp2add.append((i,j))
        # condición  para asegurarnos de que se anexará un valor que no sea
        # mayor que la cantidad de celdas disponibles
        np2add = min(change_pop, len(lp2add))

        l_n_habs = sample(lp2add, np2add)

        # todos los habitantes son suceptibles en el arreglo de la población
        for r,c in l_n_habs:
            arr_population[r][c] = 1

    # se remueven elementos
    elif change_pop < 0:
        lp2rm = []
        for i in range(sz_r):
            for j in range(sz_c):
                # celda con una persona en cualquier estado
                if arr_population[i][j] != 0:
                    lp2rm.append((i,j))
        # condición para asegurarnos de que se anexará un valor que no sea
        # mayor que la cantidad de celdas disponibles
        np2rm = min(abs(change_pop), len(lp2rm))

        l_n_habs = sample(lp2rm, np2rm)

        # todos los habitantes en l_n_habs serán convertidos a celdas vacías
        for r,c in l_n_habs:
            arr_population[r][c] = 0




def f_evolution(sz_r, sz_c, d_params, arr_tiempo, arr_nt, arr_population, arr_evo):
    '''
    función de evolución, cambia los array
    d_params -> diccionario que contendrá la información de:
                    p_E,
                    p_I,
                    t_I,
                    p_Q,
                    t_Q,
                    p_R,
                    p_D,
                    t_R,
                    d,
                    t_L,
                    t,
                    d_variable,
                    step            **opcional

    '''
    d_params["t"] += 1
    cnt = [0 for i in range(6)]

    # diccionario para almacenar los cambios de uno a otro
    d_changes = {2:[], 3:[], 4:[], 5:[], 6:[]}

    for i in range(sz_r):
        for j in range(sz_c):

            ############## Reglas

            # si es suceptible
            if arr_population[i][j] == 1:

                d = d_params["d"] if d_params["t"] <= d_params["t_L"] else 1
                # obtenemos vecindad
                ng = f_getNeigh(sz_r, sz_c,i,j, d, d_params["d_variable"])

                # obtenemos el popsible cambio
                npa = uniform(0,1)
                nv = s_2_e(d_params["p_E"], npa, ng, arr_population)
                if nv == 2:
                    cnt[0] += 1

                    d_changes[nv].append((i,j))

            # si es expuesto
            elif arr_population[i][j] == 2:
                cnt[2] += 1
                npa = uniform(0,1)
                nv = e_2_i(d_params["p_I"], npa, d_params["t_I"], arr_tiempo[i][j])
                if nv != 2:
                    d_changes[nv].append((i,j))
                else:
                    arr_tiempo[i][j] += 1

            # si es infectado
            elif arr_population[i][j] == 3:
                npa = uniform(0,1)
                p_dec = f_dec_t(d_params["p_D"], arr_tiempo[i][j])
                # if "step" in d_params.keys():
                #     nv = i_2qr(d_params["p_Q"], d_params["p_R"], p_dec, npa,
                #                 d_params["t_Q"], d_params["t_R"],
                #                 arr_tiempo[i][j], step = d_params["step"])
                # else:
                nv = i_2qr(d_params["p_Q"], d_params["p_R"], p_dec, npa,
                            d_params["t_Q"], d_params["t_R"], arr_tiempo[i][j])
                if nv != 3:
                    d_changes[nv].append((i,j))
                else:
                    arr_tiempo[i][j] += 1

            # si está en cuarentena
            elif arr_population[i][j] == 4:
                npa = uniform(0,1)
                p_dec = f_dec_t(d_params["p_D"], arr_tiempo[i][j])
                # if "step" in d_params.keys():
                #     nv = q_2_r(d_params["p_R"],p_dec, npa, d_params["t_R"],
                #                 arr_tiempo[i][j], step = d_params["step"])
                # else:
                nv = q_2_r(d_params["p_R"],p_dec, npa, d_params["t_R"],
                            arr_tiempo[i][j])
                if nv != 4:
                    d_changes[nv].append((i,j))
                else:
                    arr_tiempo[i][j] += 1

            # recuperados o casillas vacías
            else:
                nv = arr_population[i][j]
                arr_tiempo[i][j] += 1

            ############## Fin de las REGLAS
    for key, value in d_changes.items():
        for r,c in value:
            arr_population[r][c] = key
            arr_tiempo[r][c] = 0


def data_exp(n_habs , d_cont,arr_population):
    s = 0
    e = 0
    i = 0
    q = 0
    r = 0
    for rw in arr_population:
        for val in rw:
            if val == 1:
                s += 1
            elif val == 2:
                e += 1
            elif val == 3:
                i += 1
            elif val == 4:
                q += 1
            elif val == 5 or val == 6:
                r += 1
    d_cont["s"].append(s / n_habs)
    d_cont["e"].append(e / n_habs)
    d_cont["i"].append(i / n_habs)
    d_cont["q"].append(q / n_habs)
    d_cont["r"].append(r / n_habs)

    return d_cont

######
###   Conteo del número nuevo de personas que ingresaron a otro estado
######
def data_number_nstates(sz_r, sz_c, n_habs, d_ncont, arr_population, arr_tiempo):
    s = 0
    e = 0
    i_s = 0
    q = 0
    r_r = 0
    r_d = 0
    #print(len(arr_population) * len(arr_population[0]), len(arr_tiempo) * len(arr_tiempo[0]))
    for i in range(sz_r):
        for j in range(sz_c):
            try:
                if   arr_population[i][j] == 1 and arr_tiempo[i][j] == 0:
                        s += 1
                elif arr_population[i][j] == 2 and arr_tiempo[i][j] == 0:
                    e += 1
                elif arr_population[i][j] == 3 and arr_tiempo[i][j] == 0:
                    i_s += 1
                elif arr_population[i][j] == 4 and arr_tiempo[i][j] == 0:
                    q += 1
                elif arr_population[i][j] == 5 and arr_tiempo[i][j] == 0:
                    r_r += 1
                elif arr_population[i][j] == 6 and arr_tiempo[i][j] == 0:
                    r_d += 1
            except :
                print("sz_r: %d\tsz_c: %d"%(sz_r,sz_c))
                print("Error in row:\t%d\tcolumn:\t%d"%(i,j))
                print(arr_population[i][j])
                print(arr_tiempo[i][j])
    d_ncont["s"].append(s / n_habs)
    d_ncont["e"].append(e / n_habs)
    d_ncont["i"].append(i_s / n_habs)
    d_ncont["q"].append(q / n_habs)
    d_ncont["r"].append(r_r / n_habs)
    d_ncont["d"].append(r_d / n_habs)

    return d_ncont

################################
##########################
#############              PROBABILIDADES DE TRANSICIÓN
##########################
################################


# Probabilidad de que una persona que estuvo en contacto con una persona contagiada
# pase a expuesto
# https://www.news18.com/news/lifestyle/for-how-long-a-covid-19-patient-can-infect-others-myupchar-2888611.html
def f_p_E(R_0, D, d, t_infeccioso = 10):
    # número de personas que pudieron entrar en contacto con alguien
    n_p = D * ((2 * d + 1 ) **2 -1)

    return R_0 / (n_p * t_infeccioso)


# probabilidad de que E pase a I
# lauer etal 2020
# consideraremos los siguientes valores obtenidos de tratar de reproducir la
# gráfica del artículo de Lauer etal 2020
# Se calculará al principio
def f_p_I(s= 0.465, loc = 0, scale = 5.5, fst_q = 0.0001, lst_q = 0.9999 ,step = 1):
    '''
    s -> escala
    loc -> ubicación del origen
    scale -> ???
    fst_q -> 1er cuantil
    lst_q -> último cuantil
    step  -> tamaño del paso (en días)
    '''

    # start
    st = lognorm.ppf(fst_q, s, scale = scale)
    # end
    nd = lognorm.ppf(lst_q, s, scale = scale)

    # np array con 100 entradas que van desde st hasta nd
    x_cont = np.linspace(st,nd,100)
    # pdf de la función lognormal con los parámetros especificados
    lognm_pdf = lognorm.pdf(x_cont,s, loc, scale)

    # convertimos a una lista de enteros con índices los días y
    # las entradas los valores de la probabilidad
    # prob_step[i] = sum ( lognm_pdf[j] | x_cont[j] = i div) / cont
    prob_step = []
    i = 0
    sm = 0
    cont = 0

    for j in range(len(x_cont)):

        # función monótona creciente
        if i <= x_cont[j] < i + step:
            sm += lognm_pdf[j]
            cont += 1
        else:
            if i == 0: cont = 1;
            prob_step.append(sm / cont)
            i += step
            cont = 1
            sm = lognm_pdf[j]

    # la última prob se debe anexar al terminar de ejecutarse el código
    prob_step.append(sm / cont)

    return prob_step



## Probabilidad de recuperación.
## barman etal 2020
def f_p_R(t):
    ## no aparece probabilidad de recuperación
    if t < 10:
        return 0
    elif 10 <=t < 15:
        return 0.046512
    elif 15 <= t < 18:
        return 0.293023
    elif 18 <= t < 20:
        return 0.395349
    elif 20 <= t < 21:
        return 0.465116
    elif 21 <= t < 23:
        return 0.465116
    elif 23 <= t < 25:
        return 0.477419
    elif 25 <= t < 27:
        return 0.534884
    elif 27 <= t < 37:
        return 0.557634
    elif t >= 37:
        return 0.557634


## probabilidad del deceso al tiempo t
def f_dec_t(prob_dec_d, t):
    '''
    prob_dec_d -> probabilidad diaria de deceso, o función de distribución
    '''
    return prob_dec_d


##### función para los estados de los habitantes de acuerdo a las probs
def f_habs_act_stat(
                    arr_habs,
                    habs,
                    arr_tiempo,
                    env_p_S,
                    env_p_E,
                    env_p_I,
                    env_p_Q,
                    env_p_R
                    ):
    '''
    Función para determinar los estados de los habitantes en determinada zona
    Al arr_habs ser un array, no es necesario retornar nada
    arr_tiempo -> array que
    env_p -> (casa|trans|work)
    '''

    h_E = int(env_p_E * len(habs))
    h_I = int(env_p_I * len(habs))
    h_Q = int(env_p_Q * len(habs))
    h_R = int(env_p_R * len(habs))

    for i in range(len(habs)):
        r, c = habs[i]
        arr_tiempo[r][c] = 1

        if i < h_E:
            arr_habs[r][c] = 2                # expuesto
        elif i < h_E + h_I:
            arr_habs[r][c] = 3                # infectado
        elif i < h_E + h_I + h_Q:
            arr_habs[r][c] = 4                # cuarentena
        elif i < h_E + h_I + h_Q + h_R:
            arr_habs[r][c] = 5                # removido
        else:
            arr_habs[r][c] = 1                # suceptible




def f_habs_stat_N_center(
                    sz_r,
                    sz_c,
                    arr_habs,
                    habs,
                    env_p_S,
                    env_p_E,
                    env_p_I,
                    env_p_Q,
                    env_p_R,
                    stat_cent,
                    time_cent
                    ):
    '''
    Función para determinar los estados de los habitantes en determinada zona
    y cambiar el estado del centro
    Al arr_habs ser un array, no es necesario retornar nada
    env_p -> (casa|trans|work)
    '''

    arr_tiempo = [[0 for i in range(sz_c)] for j in range(sz_r)]
    # consideramos que se van poblando los habitantes con cierta probabilidad
    # para los estados
    f_habs_act_stat(arr_habs, habs, arr_tiempo, env_p_S, env_p_E, env_p_I, env_p_Q, env_p_R)

    # si el cuadrito central NO está ocupado, lo ocupamos
    cnt_r = sz_r // 2
    cnt_c = sz_c // 2

    if arr_habs[cnt_r][cnt_c] == 0:

        # quitamos un elemento de la lista de posiciones de las personas
        r_rem, c_rem = habs.pop()
        arr_habs[r_rem][c_rem] = 0

        habs.append((cnt_r, cnt_c))

    # poblamos con una persona con estado stat_cent
    arr_habs[cnt_r][cnt_c] = stat_cent
    arr_tiempo[cnt_r][cnt_c] = stat_cent
    return arr_tiempo


#########################
#########  Función para la generación de la población en cualquier entorno
######
def f_init_env(
                sz_r,
                sz_c,
                env_D,
                env_p_S,
                env_p_E,
                env_p_I,
                env_p_Q,
                env_p_R,
                stat_cent = 1,
                time_cent = 0
                ):
    '''
    función para inicializar cualquier entorno
    '''
    arr_population, habs = f_initPop(sz_r, sz_c, env_D)
    arr_tiempo = f_habs_stat_N_center(
                        sz_r,
                        sz_c,
                        arr_population,
                        habs,
                        env_p_S,
                        env_p_E,
                        env_p_I,
                        env_p_Q,
                        env_p_R,
                        stat_cent,
                        time_cent
                        )
    return arr_population, habs, arr_tiempo


def f_sum_d_data(d_ncont_hour, arr_population, habs, arr_tiempo,
                 s_env):
    '''
    casi copia de data_number_nstates

    función para hacer la suma de la info de d_data
    consideraremos que d_ncont tiene la siguiente forma al inicio:

    d_ncont_hour = {"s": 0,
               "e": 0,
               "i": 0,
               "q": 0,
               "r": 0,
               "d": 0}
    s_env -> string del ambiente en el que se encuentra (DEBUGGIN)
    '''
    s = 0
    e = 0
    i_s = 0
    q = 0
    r_r = 0
    r_d = 0

    n_habs = len(habs)

    for r,c in habs:

        if   arr_population[r][c] == 1 and arr_tiempo[r][c] == 0:
            s += 1
        elif arr_population[r][c] == 2 and arr_tiempo[r][c] == 0:
            e += 1
        elif arr_population[r][c] == 3 and arr_tiempo[r][c] == 0:
            i_s += 1
        elif arr_population[r][c] == 4 and arr_tiempo[r][c] == 0:
            q += 1
        elif arr_population[r][c] == 5 and arr_tiempo[r][c] == 0:
            r_r += 1
        elif arr_population[r][c] == 6 and arr_tiempo[r][c] == 0:
            r_d += 1

        # else:
        #     raise Exception("Casilla (%d, %d) ocupada por estado %d con tiempo %d en %s" % (r,c, arr_population[r][c], arr_tiempo[r][c], s_env))


    d_ncont_hour["s"] += (s / n_habs)
    d_ncont_hour["e"] += (e / n_habs)
    d_ncont_hour["i"] += (i_s / n_habs)
    d_ncont_hour["q"] += (q / n_habs)
    d_ncont_hour["r"] += (r_r / n_habs)
    d_ncont_hour["d"] += (r_d / n_habs)

    return d_ncont_hour




###### función de un día
def f_one_day_24h(
                   sz_r,
                   sz_c,
                   d_params,
                   arr_tiempo,
                   arr_nt,
                   arr_casa,
                   arr_work,
                   arr_evo,
                   casa_ps,
                   trans_ps,
                   work_ps,
                   l_frames
                  ):
    '''
    similar a f_evolution
    Consideraremos que en un día hay 24 hrs
    d_params -> diccionario que contendrá la información de:
                    p_E,
                    p_I,
                    t_I,
                    p_Q,
                    t_Q,
                    p_R,
                    p_D,
                    t_R,
                    d,
                    t_L,
                    t,
                    d_variable,
                    step
    arr_casa y arr_work serán listas vacías al inicio
    casa_ps -> parámetros de casa
    trans_ps -> parámetros de transporte
    work_ps -> parámetros del trabajo
    '''
    casa_D = casa_ps["D"]
    casa_S = casa_ps["S"]
    casa_E = casa_ps["E"]
    casa_I = casa_ps["I"]
    casa_Q = casa_ps["Q"]
    casa_R = casa_ps["R"]

    trans_D = trans_ps["D"]
    trans_S = trans_ps["S"]
    trans_E = trans_ps["E"]
    trans_I = trans_ps["I"]
    trans_Q = trans_ps["Q"]
    trans_R = trans_ps["R"]

    work_D = work_ps["D"]
    work_S = work_ps["S"]
    work_E = work_ps["E"]
    work_I = work_ps["I"]
    work_Q = work_ps["Q"]
    work_R = work_ps["R"]

    d_ncont_hour = {
                   "s": 0,
                   "e": 0,
                   "i": 0,
                   "q": 0,
                   "r": 0,
                   "d": 0
                   }


    # si arr_casa es vacío, significa que es la 1era iteración
    if not arr_casa:
        # inicializar el espacio de la casa
        arr_casa, habs_casa, arr_tiempo = f_init_env(sz_r, sz_c, casa_D,
                                         casa_S, casa_E, casa_I, casa_Q, casa_R)


    # 12 hrs -> casa
    # corremos una vez para tener valores nuevos para los estados de los habitantes
    stat_cent = arr_casa[sz_r //2 ][sz_c //2]
    time_cent = arr_tiempo[sz_r //2 ][sz_c //2]
    # inicialización de los estados para casa
    f_habs_stat_N_center(
                        sz_r,
                        sz_c,
                        arr_casa,
                        habs_casa,
                        casa_S,
                        casa_E,
                        casa_I,
                        casa_Q,
                        casa_R,
                        stat_cent,
                        time_cent
                        )
    ##print(arr_tiempo)  ### DEBUGGIN
    # actualización de la información
    d_ncont_hour = f_sum_d_data(d_ncont_hour, arr_casa, habs_casa, arr_tiempo , "casa")
    l_frames.append(deepcopy(arr_casa))

    ##print(arr_tiempo)  ### DEBUGGIN
    # para las 11 hrs restantes
    for j in range(11):
        f_evolution(sz_r, sz_c, d_params, arr_tiempo, arr_nt, arr_casa, arr_evo)
        d_ncont_hour = f_sum_d_data(d_ncont_hour, arr_casa, habs_casa, arr_tiempo, "casa")
        l_frames.append(deepcopy(arr_casa))
        #print(arr_casa)  ### DEBUGGIN



    stat_cent = arr_casa[sz_r //2 ][sz_c //2]
    time_cent = arr_tiempo[sz_r //2 ][sz_c //2]
    # 2 hrs -> trayecto => evoluciona solo una vez
    arr_trans, habs_trans, arr_tiempo = f_init_env(sz_r, sz_c, trans_D,
                                       trans_S, trans_E, trans_I, trans_Q,
                                       trans_R, stat_cent)
    # actualización de la información
    d_ncont_hour = f_sum_d_data(d_ncont_hour, arr_trans, habs_trans, arr_tiempo, "trans1")
    l_frames.append(deepcopy(arr_trans))
    # una evolución adicional
    f_evolution(sz_r, sz_c, d_params, arr_tiempo, arr_nt, arr_trans, arr_evo)
    # actualización de la información
    d_ncont_hour = f_sum_d_data(d_ncont_hour, arr_trans, habs_trans, arr_tiempo, "trans1")
    l_frames.append(deepcopy(arr_trans))




    stat_cent = arr_trans[sz_r //2 ][sz_c //2]
    time_cent = arr_tiempo[sz_r //2 ][sz_c //2]
    # si arr_work es vacío, significa que es la 1era iteración
    if not arr_work:
        # inicializar el espacio del trabajo
        arr_work , habs_work, arr_tiempo = f_init_env(sz_r, sz_c, work_D,
                                          work_S, work_E, work_I, work_Q, work_R,
                                          stat_cent, time_cent)

    # 8hrs -> trabajo
    f_habs_stat_N_center(
                        sz_r,
                        sz_c,
                        arr_work,
                        habs_work,
                        work_S,
                        work_E,
                        work_I,
                        work_Q,
                        work_R,
                        stat_cent,
                        time_cent
                        )
    # actualización de la información
    d_ncont_hour = f_sum_d_data(d_ncont_hour, arr_work, habs_work, arr_tiempo, "work")
    l_frames.append(deepcopy(arr_work))
    for j in range(7):
        f_evolution(sz_r, sz_c, d_params, arr_tiempo, arr_nt, arr_work, arr_evo)
        d_ncont_hour = f_sum_d_data(d_ncont_hour, arr_work, habs_work, arr_tiempo, "work")
        l_frames.append(deepcopy(arr_work))


    stat_cent = arr_work[sz_r //2 ][sz_c //2]
    time_cent = arr_tiempo[sz_r //2 ][sz_c //2]
    # 2 hrs -> trayecto de regreso
    arr_trans, habs_trans, arr_tiempo = f_init_env(sz_r, sz_c, trans_D,
                                       trans_S, trans_E, trans_I, trans_Q, trans_R,
                                       stat_cent)
    # actualización de la información
    d_ncont_hour = f_sum_d_data(d_ncont_hour, arr_trans, habs_trans, arr_tiempo,"trans2")
    l_frames.append(deepcopy(arr_trans))
    # una sola evolución
    f_evolution(sz_r, sz_c, d_params, arr_tiempo, arr_nt, arr_trans, arr_evo)
    # actualización de la información
    d_ncont_hour = f_sum_d_data(d_ncont_hour, arr_trans, habs_trans, arr_tiempo, "trans2")
    l_frames.append(deepcopy(arr_trans))

    # regresar este valor, que ahora correspondera al cambio en un día
    return d_ncont_hour
