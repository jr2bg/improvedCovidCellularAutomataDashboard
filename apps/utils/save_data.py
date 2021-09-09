import os
from datetime import datetime
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd

def create_folder():
    current = datetime.now()
    date_info = current.strftime("%Y%m%d_%H%M%S")
    parent = os.path.dirname(os.getcwd())

    folder = os.path.join(parent,"pruebas_covid19AC", date_info)

    os.mkdir(folder)

    return folder, date_info

def save_info_txt(inpt_params, folder, date_info):
    '''
    función para escribir la info de los parámetros de entrada en un TXT
    '''
    file = os.path.join(folder, "general_info.txt")
    with open(file, "w") as fl:
        fl.write("fecha y hora:\t{}".format(date_info))
        fl.write("\nParámetros:\n")
        for k,v in inpt_params.items():
            fl.write("{}:{}\n".format(k,v))

# def animate(i, l_frames):
#     '''
#     función para hacer la animación de la lista de frames
#     '''
#     return
def mk_video(l_frames, folder):
    '''
    función para generar un video de la información obtenida
    '''
    cmap = ListedColormap(["#000000",
               "#0000FF",
               "#FF00FF",
               "#FF0000",
               "#00FF00",
               "#FFFF00",
               "#800080"])
    fig = plt.figure(dpi = 200, tight_layout = False, constrained_layout = True)
    #fig, ax = plt.subplots(dpi = 200, tight_layout = False, constrained_layout = True)
    plots = []
    for i in range(len(l_frames)):
        plt.axis("off")
        #ax.set_axis_off()
        #img = ax.imshow(l_frames[i], vmin = 0, vmax = 6, cmap = cmap)
        img = plt.imshow(l_frames[i], vmin = 0, vmax = 6, cmap = cmap)
        plots.append([img])
        #ax.clear()
    # # generar la animación
    ani = animation.ArtistAnimation(fig, plots, interval=100, blit=True,
                                    repeat_delay=1000)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    # nombre del archivo
    fl = os.path.join(folder, "videoEvolution.mp4")
    # guardado del archivo
    ani.save(fl, writer = writer)



def generate_plots_csv(d_data, folder):
    '''
    función que genera el csv y las gráficas a partir del diccionario usado para
    los plots en el dashboard
    '''
    #print(d_data)
    df = pd.DataFrame(d_data)
    df.to_csv(os.path.join(folder, "datos.csv"))
    l_names = [
               "% nuevas muertes confirmadas",
               "% acumulado muertes confirmadas",
               "% de casos confirmados acumulados",
               "% nuevos casos confirmados"
              ]
    #fig = plt.figure(dpi = 200, tight_layout = False, constrained_layout = True)

    for name in l_names:
        fig, ax = plt.subplots()
        ax.plot(df["t"], df[name])
        ax.set(xlabel = "tiempo (d)", ylabel = name)
        plt.savefig(os.path.join(folder, name+".jpg"), bbox_inches = 'tight')


def mk_video2(l_frames, folder):
    FFMpegW = animation.writers["ffmpeg"]
    d_data_vid = dict(title= "evolucion", artist="B190368", comment="evolucion del sistema")
    cmap = ListedColormap(["#000000",
               "#0000FF",
               "#FF00FF",
               "#FF0000",
               "#00FF00",
               "#FFFF00",
               "#800080"])
    writer = FFMpegW(fps=15, metadata=d_data_vid)

    fig, ax = plt.subplots()
    n_t = len(l_frames)

    with writer.saving(fig, os.path.join(folder, "videoEvolution.mp4"), n_t):
        for i in range(n_t):
            ax.imshow(l_frames[i], vmin = 0, vmax = 6, cmap = cmap)
            writer.grab_frame()
