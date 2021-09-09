import dash_core_components as dcc
#import dash_html_components as html
from dash_html_components import Div, Button


class InputComponent():
    def __init__(self, idComponent, formatoValor, mostrarInput = True):
        self.idComponent = idComponent
        self.formatoValor = formatoValor
        self.mostrarInput = mostrarInput


    def establecerIdTab(self, idTab):
        self.idTab = idTab
        self.idInput = idTab + self.idComponent
        self.idSeleccion = idTab + self.idComponent + "-output"

    def renderizarSeleccion(self):
        return Div(
            id= self.idSeleccion,
            style={"margin-top":1}
        )

    def establecerFuncionInputRender(self, functionInputRender):
        self.funcionInputRender = functionInputRender

    def establecerInputRender(self):
        self.inputRender = self.funcionInputRender(self.idInput)

    def obtenerInputRender(self):
        return self.inputRender


numeroFilasMapa = InputComponent(
    idComponent = "-sz-r",
    formatoValor = 'drag_value'
    )

numeroFilasMapa.establecerFuncionInputRender(
    lambda idInput:
        dcc.Slider(
            min   = 25,
            max   = 400,
            step  = 25,
            value = 100,
            marks = {
                25: {
                    'label': '25',
                    'style': {'color': '#77b0b1'}
                    },
                100: {'label': '100'},
                200: {'label': '200'},
                300: {'label': '300'},
                400: {
                    'label': '400',
                    'style': {'color': '#f50'}
                    }
                },
            id= idInput,
        )
)


numeroColumnasMapa = InputComponent(
    idComponent = "-sz-c",
    formatoValor = 'drag_value'
    )
numeroColumnasMapa.establecerFuncionInputRender(
    lambda idInput: dcc.Slider(
        min   = 25,
        max   = 400,
        step  = 25,
        value = 100,
        marks = {
            25: {
                'label': '25',
                'style': {'color': '#77b0b1'}
                },
            100: {'label': '100'},
            200: {'label': '200'},
            300: {'label': '300'},
            400: {
                'label': '400',
                'style': {'color': '#f50'}
                }
            },
        id= idInput,
    )
)


radioEsferaInfluencia = InputComponent(
    idComponent = "-d",
    formatoValor = 'drag_value'
    )

radioEsferaInfluencia.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0,
        max=5,
        step=1,
        value=3,
        marks={
            0: {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            3: {'label': '3'},
            5: {
                'label': '5',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


densidadPoblacion = InputComponent(
    idComponent = "-D",
    formatoValor = 'drag_value'
    )

densidadPoblacion.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0,
        max=1,
        step=0.01,
        value=0.5,
        marks={
            0: {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            0.25: {'label': '0.25'},
            0.5: {'label': '0.5'},
            0.75: {'label': '0.75'},
            1: {
                'label': '1',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


numeroCiclos = InputComponent(
    idComponent = "-n-cycles",
    formatoValor = 'drag_value'
    )

numeroCiclos.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
            min=0,
            max=1000,
            step=10,
            value=10,
            marks={
                0: {
                    'label': '0',
                    'style': {'color': '#77b0b1'}
                    },
                10: {'label': '10'},
                1000: {
                    'label': '1000',
                    'style': {'color': '#f50'}
                    },
                100: {'label': '100'},
                200: {'label': '200'},
                300: {'label': '300'},
                400: {'label': '400'},
                500: {'label': '500'},
                600: {'label': '600'},
                700: {'label': '700'},
                800: {'label': '800'},
                900: {'label': '900'}
                },
            id = idInput,
        )
)


numeroReproduccionBasico = InputComponent(
    idComponent = "-R-0",
    formatoValor = 'drag_value'
    )

numeroReproduccionBasico.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0.01,
        max=10,
        step=0.01,
        value=1.5,
        marks={
            0.01: {
                'label': '0.01',
                'style': {'color': '#77b0b1'}
                },
            1.5: {'label': '1.5'},
            10: {
                'label': '10',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


tiempoInfeccioso = InputComponent(
    idComponent = "-t-infec",
    formatoValor = 'drag_value'
    )

tiempoInfeccioso.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0,
        max=20,
        step=1,
        value=10,
        marks={
            0: {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            10: {'label': '10'},
            20: {
                'label': '20',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


caseFatalityRatio = InputComponent(
    idComponent = "-cfr",
    formatoValor = 'drag_value'
    )

caseFatalityRatio.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0,
        max=1,
        step=0.001,
        value=0.1,
        marks={
            0: {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            0.1: {'label': '0.1'},
            1: {
                'label': '1',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


tiempoPrevioInfeccioso = InputComponent(
    idComponent = "-t-I",
    formatoValor = 'drag_value'
    )

tiempoPrevioInfeccioso.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0,
        max=20,
        step=1,
        value=8,
        marks={
            0: {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            8: {'label': '8'},
            20: {
                'label': '20',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


probabilidadEntrarCuarentena = InputComponent(
    idComponent = "-p-Q",
    formatoValor = 'drag_value'
    )

probabilidadEntrarCuarentena.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0,
        max=1,
        step=0.01,
        value=0.5,
        marks={
            0: {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            0.5: {'label': '0.5'},
            1: {
                'label': '1',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


tiempoPrevioEntrarCuarentena = InputComponent(
    idComponent = "-t-Q",
    formatoValor = 'drag_value'
    )

tiempoPrevioEntrarCuarentena.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0,
        max=21,
        step=1,
        value=15,
        marks={
            0 : {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            15: {'label': '15'},
            21: {
                'label': '21',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


tiempoPrevioACierreDeActividades = InputComponent(
    idComponent = "-t-L",
    formatoValor = 'drag_value'
    )

tiempoPrevioACierreDeActividades.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=-1,
        max=21,
        step=1,
        value=-1,
        marks={
            -1: {
                'label': 'inf',
                'style': {'color': '#f50'}
                },
            0: {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            15: {'label': '15'},
            21: {
                'label': '21',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


tiempoPrevioARecuperadoOFallecido = InputComponent(
    idComponent = "-t-R",
    formatoValor = 'drag_value'
    )

tiempoPrevioARecuperadoOFallecido.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=0,
        max=21,
        step=1,
        value=15,
        marks={
            0: {
                'label': '0',
                'style': {'color': '#77b0b1'}
                },
            15: {'label': '15'},
            21: {
                'label': '21',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


numeroInicialDeExpuestos = InputComponent(
    idComponent = "-E-in",
    formatoValor = 'drag_value'
    )

numeroInicialDeExpuestos.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=75,
        max=600,
        step=25,
        value=200,
        marks={
            75: {
                'label': '75',
                'style': {'color': '#77b0b1'}
                },
            200: {'label': '200'},
            600: {
                'label': '600',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


numeroInicialDeInfectados = InputComponent(
    idComponent = "-I-in",
    formatoValor = 'drag_value'
    )

numeroInicialDeInfectados.establecerFuncionInputRender(
    lambda idInput : dcc.Slider(
        min=5,
        max=50,
        step=1,
        value=6,
        marks={
            5: {
                'label': '5',
                'style': {'color': '#77b0b1'}
                },
            6: {'label': '6'},
            50: {
                'label': '50',
                'style': {'color': '#f50'}
                }
            },
        id = idInput,
    )
)


funcionDeTransicionExpuestoAInfectado = InputComponent(
    idComponent = "-f-E2I",
    formatoValor = '',
    mostrarInput = False
    )

funcionDeTransicionExpuestoAInfectado.establecerFuncionInputRender(
    lambda idInput : dcc.RadioItems(
        options=[
            {
                'label': "Función de densidad de probabilidad",
                'value': 'pdf'
            },
            {
                'label': "Función de distribución acumulada",
                'value': 'cdf'
            },
        ],
        value = 'pdf',
        labelStyle={'display': 'inline-block'},
        id = idInput,
    )
)


botonStart = InputComponent(
    idComponent = "-button-start",
    formatoValor = ''
    mostrarInput = False
    )

botonStart.establecerFuncionInputRender(
    lambda idInput : Button("START",
        id = idInput,
        n_clicks=0
    )
)



componentes = [
    numeroFilasMapa,
    numeroColumnasMapa,
    radioEsferaInfluencia,
    densidadPoblacion,
    numeroCiclos,
    numeroReproduccionBasico,
    tiempoInfeccioso,
    caseFatalityRatio,
    tiempoPrevioInfeccioso,
    probabilidadEntrarCuarentena,
    tiempoPrevioEntrarCuarentena,
    tiempoPrevioACierreDeActividades,
    tiempoPrevioARecuperadoOFallecido,
    numeroInicialDeExpuestos,
    numeroInicialDeInfectados,
    funcionDeTransicionExpuestoAInfectado,
    botonStart
]
