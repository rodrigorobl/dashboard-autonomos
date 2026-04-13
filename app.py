import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import openpyxl

FILEPATH = 'dados/Planilha_de_Controle_de_Gastos_-_Autnomos.xlsx'

MONTH_NAMES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
               'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


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
    pass


def render_pj_tab(data):
    pass


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
