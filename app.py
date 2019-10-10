import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'DC Housing'
myheading='Analysis of housing prices in Washington DC'
neighborhood='Petworth'
color1='#004209'
color2='#BFFFC8'
sourceurl = 'https://www.kaggle.com/christophercorrea/dc-residential-properties/'
githublink = 'https://github.com/mgeisreiter/dash-scatterplot-housing'


########### Prepare the dataframe
df = pd.read_csv('DC_Properties.csv')
df=df[df['ASSESSMENT_NBHD']==neighborhood]
df=df[(df['PRICE']<=1000000) & (df['PRICE']>=10000)]
df=df[df['LANDAREA']<4000]
df=df[df['PRICE']<900000]
df=df[df['BEDRM']<8]
df=df[df['BATHRM']<8]
df=df[df['FIREPLACES']<8]

avg_bath = round(df['BATHRM'].mean(),1)
avg_bed = round(df['BEDRM'].mean(),1)


########### Set up the chart
trace = go.Scatter(
    x = df['PRICE'],
    y = df['LIVING_GBA'],
    mode = 'markers',
    marker=dict(
        size=8,
        color = df['BATHRM'], # set color equal to a third variable
        colorscale=[color1, color2],
        colorbar=dict(title='Fireplaces'),
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title = f'The Average Home in {neighborhood} has {avg_bed} Bedrooms and {avg_bath} Bathrooms!', # Graph title
    xaxis = dict(title = 'Sales Price'), # x-axis label
    yaxis = dict(title = 'Square Feet'), # y-axis label
    hovermode ='closest' # handles multiple points landing on the same vertical
)
fig = go.Figure(data=data, layout=layout)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='figure-1',
        figure=fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Deploy
if __name__ == '__main__':
    app.run_server()
