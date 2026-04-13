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
    pass


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
