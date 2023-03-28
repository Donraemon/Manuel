import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import date,datetime,timedelta
from flask import Flask
from sqlalchemy import create_engine

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.FLATLY])
app.title = 'Dashboard'

engine = 'mysql+pymysql://sistemesbd:bigdata2223@192.168.193.133/alumnes'
sqlEngine=create_engine(engine)
dbConnection = sqlEngine.connect()
df_query = pd.read_sql('Manuel', dbConnection)

navbar = dbc.Navbar(
    [dbc.NavbarBrand(html.H2("Muertes del dinosaurio"), className="ms-2",style={'textAlign': 'center','height':'50px'}),
    ],
    color="info",
    dark=True
)

grafica1=dcc.Graph(id='histo', figure = 
                            px.histogram(df_query,
                            x='jugada',
                            nbins=len(df_query['jugada']),
                            width=2000,
                            title= 'Puntos en los que cae muerto el dino'
                            ),
        )

df = df_query[-100:]

df1 = df[df['jugada']<df.mean()[1]]
df2 = df[df['jugada']<2]
df_numero_querer_apostar = df.count()[0] - df2.count()[0]
df_apuesta_a_la_media = df.count()[0] - df1.count()[0]
app.layout =  html.Div(children=[navbar,
    dbc.Row([
        dbc.Col(html.Div([grafica1]),width=11, style={"position":"relative"}),    
        dbc.Col(html.Div([dbc.Alert([html.H3("Probabilidad de ganancia apostando al número 2 "+str(df_numero_querer_apostar)+" %", className="alert-heading",id="recupNombre",style={'textAlign': 'center'})])]),width=4),
        dbc.Col(html.Div([dbc.Alert([html.H3("Probabilidad de ganancia " + str(df_apuesta_a_la_media)+"% " + "apostando a la media actual  "+str(df.mean()[1]),className="alert-heading",id="recup",style={'textAlign': 'center',"position":"absolute","margin-top":"10%"})])]),width=4)
            
    ])
    ])


@app.callback(Output('graficaScatter','figure'),
                Output('recup','children'),
                Output('recupNombre','children'),
              [Input('tempselector', 'value'),Input('graficaScatter','clickData')])        
def update_graph(tempselector,datografica):
    dfj = pd.concat([df2021,df2022])
    dfrecup = dfj.loc[dfj['Ejercicio']==tempselector]
    dfestadis= dfj.loc[dfj['Ejercicio']==tempselector]
    indiceEquipo = datografica['points'][0]['curveNumber']
    dfequipo = dfrecup[dfestadis.index == indiceEquipo]['Recup.'][indiceEquipo]
    dfNombre = dfrecup[dfestadis.index == indiceEquipo]['Equipo'][indiceEquipo]
    recupNombre= str(dfNombre)
    recup = str(dfequipo)+" Balones recuperados"
    print(datografica)
    
    dfdia= dfj.loc[dfj['Ejercicio']==tempselector]
    grafica1= px.scatter(dfdia,
                x='TA',
                y='Fls',
                color ='Equipo',
                title='Tarjetas amarillas por faltas cometidas'
                            )
                    

    return grafica1,recup,recupNombre

if __name__=='__main__':
    app.run_server()