import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import renderEvolucionPlusCasosYDecesos

app.layout = html.Div(
    [
        html.H2("Modelación de la complejidad usando estructuras matemáticas discretas"),
            dcc.Tabs(id='tabs-disertation',
                value= "tab-covid19owid",
                children=[
                    dcc.Tab(label='OWID', value='tab-covid19owid'),
                    ]
                ),
        html.Div(id='tab-fig')
    ]
)

@app.callback(Output('tab-fig', 'children'),
              Input('tabs-disertation', 'value'))
def render_content(tab):
    if tab == 'tab-covid19owid':
        return html.Div(
            [
                renderEvolucionPlusCasosYDecesos.layout
            ]
        )



if __name__ == '__main__':
    app.run_server(debug=True)
