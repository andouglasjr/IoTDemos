from flask import Flask
from flask import render_template
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

@app.route("/dashboard/<name>")
def hello_world(name=None):
    data = pd.DataFrame({
        'mes': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'valor': [10, 20, 15, 25, 30, 20]
    })
    # Gráfico usando apenas marcadores
    trace1 = go.Scatter(x = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y = [10, 9, 11, 8, 12],
                        mode = 'lines',
                        name = 'Gráfico com linhas tracejadas',
                        line = {'color': '#ee5253',
                                'dash': 'dash'})
    # Gráfico de apenas linhas
    trace2 = go.Scatter(x = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y = [11, 12, 13, 14, 15],
                        mode = 'lines',
                        name = 'Gráfico com linha pontilhada',
                        line = {'color': '#341f97',
                                'dash': 'dot'})
    data = [trace1, trace2]
    fig = go.Figure(trace1)
    return render_template('dashboard.html', plot=fig.to_html())