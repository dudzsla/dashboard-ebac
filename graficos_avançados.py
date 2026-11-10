import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import gaussian_kde
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('ecommerce_estatistica.csv')

fig1 = px.histogram(df, x='Preço', nbins=30, title='Distribuição de Preços')

fig1.update_layout(xaxis_title='Preço', yaxis_title='Frequência')

fig2 = px.scatter(df, x='N_Avaliações', y='Preço', color='N_Avaliações', hover_data=['N_Avaliações'], title='Relação entre Avaliações e Preços')

fig2.update_layout(xaxis_title='Quantidade de Avaliações', yaxis_title='Preço')

corr = df[['Nota', 'N_Avaliações', 'Desconto']].corr()

fig3 = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', title='Correlação entre as Variáveis')

fig3.update_layout(xaxis_title='Variáveis', yaxis_title='Variáveis')

marcas = df['Marca'].value_counts().head(10)

marcas = marcas.rename_axis('Marca').reset_index(name='Quantidade')

fig4 = px.bar(marcas, x='Marca', y='Quantidade', title='Quantidade de Produtos por Marca', text='Quantidade')

fig4.update_layout(xaxis_title='Marca', yaxis_title='Quantidade de Produtos', xaxis_tickangle=-45)

marcas = df['Marca'].value_counts()

top5 = marcas.head(5)
outras = marcas.iloc[5:].sum()

dados_pizza = pd.concat([top5, pd.Series({'Outras': outras})])

dados_pizza = dados_pizza.rename_axis('Marca').reset_index(name='Quantidade')

fig5 = px.pie(dados_pizza, names='Marca', values='Quantidade', title='Distribuição dos Produtos por Marca')

fig5.update_traces(textposition='inside', textinfo='percent+label')

precos = df['Preço'].dropna()

densidade = gaussian_kde(precos)

x_precos = np.linspace(precos.min(), precos.max(), 200)
y_densidade = densidade(x_precos)

fig6 = px.line(x=x_precos, y=y_densidade, title='Densidade dos Preços dos Produtos', labels={'x': 'Preço', 'y': 'Densidade'})

fig6.update_traces(fill='tozeroy')

dados = df[['N_Avaliações', 'Preço']].dropna()

coef = np.polyfit(dados['N_Avaliações'], dados['Preço'],1)

x_linha = np.linspace(dados['N_Avaliações'].min(), dados['N_Avaliações'].max(), 100)

y_linha = coef[0] * x_linha + coef[1]

fig7 = px.scatter(dados, x='N_Avaliações', y='Preço', title='Regressão entre Avaliações e Preço')

fig7.add_scatter(x=x_linha, y=y_linha, mode='lines', name='Linha de tendência')

fig7.update_layout(xaxis_title='Quantidade de Avaliações', yaxis_title='Preço')

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Dashboard EBAC'),

    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7)
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)