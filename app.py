import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import openpyxl

FILEPATH = 'dados/Planilha_de_Controle_de_Gastos_-_Autnomos.xlsx'

MONTH_NAMES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
               'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

CATEGORY_HEADERS = {
    'Alimentação', 'Moradia', 'Educação', 'Animal de Estimação',
    'Saúde', 'Transporte', 'Pessoal', 'Lazer', 'Serviços Financeiros'
}


def format_month(dt):
    """Converte datetime para string 'Mmm/AA'. Retorna str(dt) se não for datetime."""
    if hasattr(dt, 'month'):
        return f"{MONTH_NAMES[dt.month - 1]}/{str(dt.year)[2:]}"
    return str(dt)


def load_pj_data(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb['Pessoa Jurídica']
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    months = [format_month(r) for r in rows[0][1:13]]

    receitas = {}
    despesas = {}
    totais_receita = []
    totais_despesa = []
    resultado = []
    current_section = None

    for row in rows[1:]:
        if row[0] is None:
            continue
        name = str(row[0])
        values = [v if v is not None else 0 for v in row[1:len(months)+1]]

        if name == 'Receitas':
            current_section = 'receitas'
        elif name == 'Despesas':
            current_section = 'despesas'
        elif name == 'Total de Receitas':
            totais_receita = values
        elif name == 'Total das Despesas':
            totais_despesa = values
        elif name.startswith('Resultado Operacional'):
            resultado = values
        elif name.startswith('Alterar'):
            continue
        elif name.startswith('- '):
            item_name = name[2:]
            if current_section == 'receitas':
                receitas[item_name] = values
            elif current_section == 'despesas':
                despesas[item_name] = values

    return {
        'months': months,
        'receitas': receitas,
        'despesas': despesas,
        'totais_receita': totais_receita,
        'totais_despesa': totais_despesa,
        'resultado': resultado,
    }


def load_pf_data(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb['Pessoa Física']
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    # Índices de valores mensais e meios de pagamento
    val_indices = list(range(1, 25, 2))    # [1,3,5,...,23]
    pay_indices = list(range(2, 26, 2))    # [2,4,6,...,24]

    months = [format_month(rows[0][i]) for i in val_indices]

    categories = {}
    payment_totals = {}
    totais_despesa = []
    renda = []
    resultado = []
    investimentos = []
    current_category = None

    def get_vals(row):
        return [row[i] if i < len(row) and row[i] is not None else 0 for i in val_indices]

    def get_methods(row):
        return [row[i] if i < len(row) and row[i] is not None else '' for i in pay_indices]

    for row in rows[1:]:
        if row[0] is None:
            continue
        name = str(row[0])

        if name in ('Despedas', 'Despesas'):
            continue
        if name == 'Alterar somente os campos em azul':
            continue

        if name in CATEGORY_HEADERS:
            current_category = name
            categories[current_category] = {}
            continue

        if name == 'Total das Despesas':
            totais_despesa = get_vals(row)
            continue
        if name == 'Renda Mensal':
            renda = get_vals(row)
            continue
        if name.startswith('Resultado Operacional'):
            resultado = get_vals(row)
            continue
        if name == 'Investimentos Mensais':
            investimentos = get_vals(row)
            continue

        # Item de despesa
        if current_category is not None:
            vals = get_vals(row)
            methods = get_methods(row)
            categories[current_category][name] = {'values': vals, 'methods': methods}
            # Acumular totais por meio de pagamento
            for v, m in zip(vals, methods):
                if m and v:
                    payment_totals[m] = payment_totals.get(m, 0) + v

    return {
        'months': months,
        'categories': categories,
        'payment_totals': payment_totals,
        'totais_despesa': totais_despesa,
        'renda': renda,
        'resultado': resultado,
        'investimentos': investimentos,
    }


def render_pj_tab(data):
    # KPIs
    total_receita = sum(data['totais_receita'])
    total_despesa = sum(data['totais_despesa'])
    resultado_total = sum(data['resultado'])
    melhor_idx = data['resultado'].index(max(data['resultado']))
    melhor_mes = data['months'][melhor_idx]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Receita Total', f"R$ {total_receita:,.0f}".replace(',', '.'))
    col2.metric('Despesas Total', f"R$ {total_despesa:,.0f}".replace(',', '.'))
    col3.metric('Resultado Operacional', f"R$ {resultado_total:,.0f}".replace(',', '.'))
    col4.metric('Melhor Mês', melhor_mes)

    st.divider()

    col_l, col_r = st.columns(2)

    # Gráfico 1: Receitas vs Despesas por mês (barras agrupadas)
    with col_l:
        fig = go.Figure()
        fig.add_bar(
            x=data['months'], y=data['totais_receita'],
            name='Receitas', marker_color='#4ade80'
        )
        fig.add_bar(
            x=data['months'], y=data['totais_despesa'],
            name='Despesas', marker_color='#f87171'
        )
        fig.update_layout(
            title='Receitas vs Despesas por Mês',
            barmode='group',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico 2: Composição das despesas (pizza)
    with col_r:
        desp_names = list(data['despesas'].keys())
        desp_totals = [sum(data['despesas'][k]) for k in desp_names]
        # Filtrar itens com valor zero
        pairs = [(n, v) for n, v in zip(desp_names, desp_totals) if v > 0]
        if pairs:
            names, vals = zip(*pairs)
            fig = px.pie(names=list(names), values=list(vals),
                         title='Composição das Despesas')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    # Gráfico 3: Resultado Operacional por mês (linha)
    with col_l2:
        colors = ['#4ade80' if v >= 0 else '#f87171' for v in data['resultado']]
        fig = go.Figure(go.Scatter(
            x=data['months'], y=data['resultado'],
            mode='lines+markers',
            line=dict(color='#60a5fa', width=2),
            marker=dict(color=colors, size=8)
        ))
        fig.add_hline(y=0, line_dash='dash', line_color='gray', opacity=0.5)
        fig.update_layout(
            title='Resultado Operacional por Mês',
            yaxis_title='R$'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico 4: Top categorias de despesa (barras horizontais)
    with col_r2:
        desp_sorted = sorted(
            [(n, sum(data['despesas'][n])) for n in data['despesas'] if sum(data['despesas'][n]) > 0],
            key=lambda x: x[1], reverse=True
        )
        if desp_sorted:
            names, vals = zip(*desp_sorted)
            fig = px.bar(
                x=list(vals), y=list(names),
                orientation='h',
                title='Top Categorias de Despesa',
                labels={'x': 'Total (R$)', 'y': ''},
                color=list(vals),
                color_continuous_scale='Reds'
            )
            fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange='reversed'))
            st.plotly_chart(fig, use_container_width=True)


def render_pf_tab(data):
    pass


def main():
    st.set_page_config(page_title='Dashboard Autônomos', layout='wide')
    st.title('Controle de Gastos — Autônomos')

    pj_data = load_pj_data(FILEPATH)
    pf_data = load_pf_data(FILEPATH)

    tab_pj, tab_pf = st.tabs(['Pessoa Jurídica', 'Pessoa Física'])
    with tab_pj:
        render_pj_tab(pj_data)
    with tab_pf:
        render_pf_tab(pf_data)


if __name__ == '__main__':
    main()
