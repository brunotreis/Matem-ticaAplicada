from dash import Dash, html, dcc
import pandas as pd
import numpy as np
from scipy.integrate import odeint
import plotly.express as px
from dash.dependencies import Input, Output

app = Dash(__name__, title='Página Bruno Trindade')

server = app.server


#####################




texto = 'No instante $t=0$, um tanque contém $Q_0$ kg de sal dissolvidos em $100 l$ de água. ' \
        'Suponha que água contendo $\\frac{1}{4}$ kg de sal por litro está entrando no tanque' \
        ' a uma taxa de $r$ litros por minuto e que o líquido, bem misturado, está saindo' \
        ' do tanque à mesma taxa. Seja $Q(t)$ a quantidade de sal no tempo $t$ e suponha ' \
        ' que o sal não é criado nem destruído no tanque. Logo, temos a seguinte equação ' \
        ' diferencial para a taxa de variação de sal no tanque:'

formula = '$\\displaystyle  \\frac{dQ}{dt}= \\frac{r}{4} - \\frac{rQ}{100}$'


app.layout = html.Div(
    [
        html.Div(html.H1('Matemática Aplicada'),id= 'cabeçalho'),
        html.Div([html.H3('Exercício', id='exercicio'), html.P(dcc.Markdown(texto,  mathjax=True)), html.P(dcc.Markdown(formula,  mathjax=True)) ],className= 'container'),
        html.Div([html.Div([html.H4('Digite o valor final de t:', className='texto_caixa'),html.Div(dcc.Input(id='tempo', value=50, type='number'), className='ent')],className='entrada'), html.Div([html.H4(dcc.Markdown('Digite o valor de r:', mathjax=True),className='texto_caixa'), dcc.Input(id='r', value=8.69, type='number')],className='entrada'), html.Div([html.H4(dcc.Markdown('Digite o valor de $Q_0$:', mathjax=True), className='texto_caixa'), dcc.Input(id='q', value=30, type='number')],className='entrada' )],className='container2'),
        html.Div(dcc.Graph(id='fig', style={'margin':'10px', 'padding': '10px'}), id='figura')
    ]

)

colors = {'background': '#d3d3d3'}



#app.layout = html.Div([html.Div([html.H1('MATEMÁTICA APLICADA', id='cabeçalho'), html.Div([html.P(dcc.Markdown('### Exemplo:', mathjax=True), style={'margin': '20px'}), html.P(dcc.Markdown(texto, mathjax=True), style={'margin': '20px'}), html.P(dcc.Markdown(formula, mathjax=True), style={'margin': '20px', 'padding-bottom': '20px'})])]), html.Div([html.Div([html.H3('Digite o valor de r:'), dcc.Input(id='r', value=8.69, type='number')], style={'background-color': '#add8e6', 'width': '200px', 'height': '100px',
#                      'border-radius': '20px', 'text-align': 'center', 'padding': '10px', 'border': '2px solid bisque'}), html.Div([html.H3(dcc.Markdown('Digite o valor de $Q_0:$', mathjax=True)), dcc.Input(id='entrada', value=30, type='number')], style={'background-color': '#add8e6', 'width': '200px', 'height': '100px', 'border-radius': '20px', 'text-align': 'center', 'padding': '10px', 'border': '2px solid bisque'})], style={'display': 'flex', 'textAlign': 'center', 'margin-left': '10px'}), dcc.Graph(id='fig', mathjax=True)])


@app.callback(
    Output(component_id='fig', component_property='figure'),
    Input(component_id='tempo', component_property='value'),
    Input(component_id='r', component_property='value'),
    Input(component_id='q', component_property='value')
)
def g(tf, r, y0):
    if (r == None) or (y0 == None) or (tf==None):
        fig = px.line()
        return fig
    else:
        t = np.linspace(0, tf, 1000)
        def f(y, t):
            f = r / 4 - r * y / 100
            return f
        sol = odeint(f, y0, t)
        df = pd.DataFrame()
        df['tempo'] = pd.DataFrame(t)
        df['Q(t)'] = pd.DataFrame(sol)
        fig = px.line(df, x=df['tempo'], y=df['Q(t)'], title='Solução Gráfica')
        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
        )
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
