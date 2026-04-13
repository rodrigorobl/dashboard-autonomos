# Dashboard Autônomos — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar um dashboard Streamlit de arquivo único que lê `dados/Planilha_de_Controle_de_Gastos_-_Autnomos.xlsx` e exibe KPIs e gráficos interativos para Pessoa Jurídica (PJ) e Pessoa Física (PF).

**Architecture:** Um único `app.py` com funções de carregamento de dados (`load_pj_data`, `load_pf_data`) e funções de renderização (`render_pj_tab`, `render_pf_tab`). Leitura via `openpyxl` (sem numpy/pandas — bloqueio de DLL no ambiente). Gráficos com Plotly, layout com Streamlit tabs.

**Tech Stack:** Python 3.11, Streamlit, Plotly, openpyxl, pytest

---

## Estrutura de arquivos

```
app.py                            ← aplicação principal (criar)
requirements.txt                  ← dependências (criar)
tests/
  test_data.py                    ← testes das funções de carregamento (criar)
dados/
  Planilha_de_Controle_de_Gastos_-_Autnomos.xlsx  ← já existe
```

---

## Task 1: Setup — requirements.txt e esqueleto do app.py

**Files:**
- Create: `requirements.txt`
- Create: `app.py`

- [ ] **Step 1: Criar requirements.txt**

```
streamlit>=1.32.0
plotly>=5.20.0
openpyxl>=3.1.0
pytest>=8.0.0
```

- [ ] **Step 2: Criar app.py com esqueleto**

```python
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
```

- [ ] **Step 3: Instalar dependências**

```bash
pip install streamlit plotly openpyxl pytest
```

Esperado: instalação sem erros.

- [ ] **Step 4: Commit**

```bash
git add requirements.txt app.py
git commit -m "chore: setup projeto dashboard autonomos"
```

---

## Task 2: Carregar dados PJ — load_pj_data

**Estrutura da aba "Pessoa Jurídica":**
- Linha 0: `('Meses', datetime(2018,1,1), datetime(2018,2,1), ..., datetime(2018,12,1))` — 13 colunas
- Linhas de seção: `'Receitas'`, `'Despesas'` — sem valores, apenas marcador
- Linhas de item: começam com `'- '` — possuem valores mensais
- Linhas de total/resultado: `'Total de Receitas'`, `'Total das Despesas'`, `'Resultado Operacional...'`
- Última linha: `'Alterar somente os campos em azul'` — ignorar

**Files:**
- Modify: `app.py` — função `load_pj_data`
- Create: `tests/test_data.py`

- [ ] **Step 1: Criar tests/test_data.py com testes para load_pj_data**

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import load_pj_data, load_pf_data

FILEPATH = 'dados/Planilha_de_Controle_de_Gastos_-_Autnomos.xlsx'


class TestLoadPjData:
    def test_returns_12_months(self):
        data = load_pj_data(FILEPATH)
        assert len(data['months']) == 12

    def test_months_are_strings(self):
        data = load_pj_data(FILEPATH)
        assert all(isinstance(m, str) for m in data['months'])

    def test_first_month_is_jan(self):
        data = load_pj_data(FILEPATH)
        assert data['months'][0] == 'Jan/18'

    def test_receitas_has_items(self):
        data = load_pj_data(FILEPATH)
        assert len(data['receitas']) > 0

    def test_venda_a_exists_in_receitas(self):
        data = load_pj_data(FILEPATH)
        assert 'Venda A' in data['receitas']

    def test_despesas_has_items(self):
        data = load_pj_data(FILEPATH)
        assert len(data['despesas']) > 0

    def test_salario_exists_in_despesas(self):
        data = load_pj_data(FILEPATH)
        assert 'Salário (pro-labore)' in data['despesas']

    def test_totais_receita_janeiro(self):
        data = load_pj_data(FILEPATH)
        assert data['totais_receita'][0] == 2300

    def test_totais_despesa_janeiro(self):
        data = load_pj_data(FILEPATH)
        assert data['totais_despesa'][0] == 5500

    def test_resultado_fevereiro_positivo(self):
        # Fevereiro é o único mês com resultado positivo (2600)
        data = load_pj_data(FILEPATH)
        assert data['resultado'][1] == 2600

    def test_none_values_converted_to_zero(self):
        data = load_pj_data(FILEPATH)
        for vals in data['receitas'].values():
            assert all(v is not None for v in vals)
```

- [ ] **Step 2: Rodar testes — confirmar falha**

```bash
pytest tests/test_data.py::TestLoadPjData -v
```

Esperado: FAILED — `load_pj_data` retorna `None`.

- [ ] **Step 3: Implementar load_pj_data em app.py**

Substitua `def load_pj_data(filepath): pass` por:

```python
def load_pj_data(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb['Pessoa Jurídica']
    rows = list(ws.iter_rows(values_only=True))

    months = [format_month(r) for r in rows[0][1:]]

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
        values = [v if v is not None else 0 for v in row[1:]]

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
```

- [ ] **Step 4: Rodar testes — confirmar aprovação**

```bash
pytest tests/test_data.py::TestLoadPjData -v
```

Esperado: todos os testes PASSED.

- [ ] **Step 5: Commit**

```bash
git add app.py tests/test_data.py
git commit -m "feat: implementa load_pj_data com testes"
```

---

## Task 3: Carregar dados PF — load_pf_data

**Estrutura da aba "Pessoa Física":**
- Linha 0: `('Meses', datetime(Jan), 'Meio de Pagamento', datetime(Fev), 'Meio de Pagamento', ..., datetime(Dez), 'Meio de Pagamento', 'Total')` — 26 colunas
  - Valores mensais: índices 1, 3, 5, ..., 23 → `range(1, 25, 2)`
  - Meios de pagamento: índices 2, 4, 6, ..., 24 → `range(2, 26, 2)`
- Linhas de seção/categoria sem valores: `'Despedas'`, `'Alimentação'`, `'Moradia'`, etc.
- Linhas de item com valores e meios de pagamento
- Linhas de sumário: `'Total das Despesas'`, `'Renda Mensal'`, `'Resultado Operacional...'`, `'Investimentos Mensais'`

**Files:**
- Modify: `app.py` — função `load_pf_data`
- Modify: `tests/test_data.py` — adicionar TestLoadPfData

- [ ] **Step 1: Adicionar testes para load_pf_data em tests/test_data.py**

Adicione ao final do arquivo:

```python
class TestLoadPfData:
    def test_returns_12_months(self):
        data = load_pf_data(FILEPATH)
        assert len(data['months']) == 12

    def test_first_month_is_jan(self):
        data = load_pf_data(FILEPATH)
        assert data['months'][0] == 'Jan/18'

    def test_has_alimentacao_category(self):
        data = load_pf_data(FILEPATH)
        assert 'Alimentação' in data['categories']

    def test_supermercado_in_alimentacao(self):
        data = load_pf_data(FILEPATH)
        assert 'Supermercado' in data['categories']['Alimentação']

    def test_supermercado_janeiro_value(self):
        data = load_pf_data(FILEPATH)
        assert data['categories']['Alimentação']['Supermercado']['values'][0] == 100

    def test_supermercado_janeiro_payment(self):
        data = load_pf_data(FILEPATH)
        assert data['categories']['Alimentação']['Supermercado']['methods'][0] == 'Cartão de Crédito'

    def test_total_despesa_janeiro(self):
        data = load_pf_data(FILEPATH)
        assert data['totais_despesa'][0] == 1670

    def test_renda_mensal_is_2000_all_months(self):
        data = load_pf_data(FILEPATH)
        assert all(r == 2000 for r in data['renda'])

    def test_investimentos_total(self):
        data = load_pf_data(FILEPATH)
        assert sum(data['investimentos']) == 200

    def test_payment_totals_has_cartao_credito(self):
        data = load_pf_data(FILEPATH)
        assert 'Cartão de Crédito' in data['payment_totals']

    def test_none_values_converted_to_zero(self):
        data = load_pf_data(FILEPATH)
        assert all(v is not None for v in data['totais_despesa'])
```

- [ ] **Step 2: Rodar testes — confirmar falha**

```bash
pytest tests/test_data.py::TestLoadPfData -v
```

Esperado: FAILED — `load_pf_data` retorna `None`.

- [ ] **Step 3: Implementar load_pf_data em app.py**

Substitua `def load_pf_data(filepath): pass` por:

```python
CATEGORY_HEADERS = {
    'Alimentação', 'Moradia', 'Educação', 'Animal de Estimação',
    'Saúde', 'Transporte', 'Pessoal', 'Lazer', 'Serviços Financeiros'
}


def load_pf_data(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb['Pessoa Física']
    rows = list(ws.iter_rows(values_only=True))

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
```

Adicione também `CATEGORY_HEADERS` como constante no topo do arquivo, logo após `MONTH_NAMES`.

- [ ] **Step 4: Rodar todos os testes — confirmar aprovação**

```bash
pytest tests/test_data.py -v
```

Esperado: todos os testes PASSED.

- [ ] **Step 5: Commit**

```bash
git add app.py tests/test_data.py
git commit -m "feat: implementa load_pf_data com testes"
```

---

## Task 4: Renderizar aba Pessoa Jurídica — render_pj_tab

**Files:**
- Modify: `app.py` — função `render_pj_tab`

- [ ] **Step 1: Implementar render_pj_tab em app.py**

Substitua `def render_pj_tab(data): pass` por:

```python
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
    delta_color = 'normal' if resultado_total >= 0 else 'inverse'
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
```

- [ ] **Step 2: Verificar visualmente — rodar o app**

```bash
streamlit run app.py
```

Abrir http://localhost:8501. Confirmar:
- 4 KPIs aparecem na aba PJ
- 4 gráficos aparecem no grid 2×2
- Valores batem com a planilha (Receita Jan = R$ 2.300, Melhor Mês = Fev/18)

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: renderiza aba Pessoa Juridica com KPIs e graficos"
```

---

## Task 5: Renderizar aba Pessoa Física — render_pf_tab

**Files:**
- Modify: `app.py` — função `render_pf_tab`

- [ ] **Step 1: Implementar render_pf_tab em app.py**

Substitua `def render_pf_tab(data): pass` por:

```python
def render_pf_tab(data):
    # KPIs
    total_renda = sum(data['renda'])
    total_despesa = sum(data['totais_despesa'])
    total_invest = sum(data['investimentos'])
    meio_mais_usado = (
        max(data['payment_totals'], key=data['payment_totals'].get)
        if data['payment_totals'] else 'N/A'
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Renda Total', f"R$ {total_renda:,.0f}".replace(',', '.'))
    col2.metric('Despesas Total', f"R$ {total_despesa:,.0f}".replace(',', '.'))
    col3.metric('Investimentos', f"R$ {total_invest:,.0f}".replace(',', '.'))
    col4.metric('Meio + Usado', meio_mais_usado)

    st.divider()

    col_l, col_r = st.columns(2)

    # Gráfico 1: Renda vs Despesas por mês (barras agrupadas)
    with col_l:
        fig = go.Figure()
        fig.add_bar(
            x=data['months'], y=data['renda'],
            name='Renda', marker_color='#4ade80'
        )
        fig.add_bar(
            x=data['months'], y=data['totais_despesa'],
            name='Despesas', marker_color='#f87171'
        )
        fig.update_layout(
            title='Renda vs Despesas por Mês',
            barmode='group',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico 2: Despesas por categoria (pizza)
    with col_r:
        cat_totals = {}
        for cat_name, items in data['categories'].items():
            total = sum(sum(item['values']) for item in items.values())
            if total > 0:
                cat_totals[cat_name] = total
        if cat_totals:
            fig = px.pie(
                names=list(cat_totals.keys()),
                values=list(cat_totals.values()),
                title='Despesas por Categoria'
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    # Gráfico 3: Gastos por meio de pagamento (barras horizontais)
    with col_l2:
        if data['payment_totals']:
            pay_sorted = sorted(data['payment_totals'].items(), key=lambda x: x[1], reverse=True)
            methods, vals = zip(*pay_sorted)
            fig = px.bar(
                x=list(vals), y=list(methods),
                orientation='h',
                title='Gastos por Meio de Pagamento',
                labels={'x': 'Total (R$)', 'y': ''},
                color=list(vals),
                color_continuous_scale='Blues'
            )
            fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange='reversed'))
            st.plotly_chart(fig, use_container_width=True)

    # Gráfico 4: Saldo mensal — Renda − Despesas (barras coloridas)
    with col_r2:
        saldo = [r - d for r, d in zip(data['renda'], data['totais_despesa'])]
        colors = ['#4ade80' if s >= 0 else '#f87171' for s in saldo]
        fig = go.Figure(go.Bar(
            x=data['months'], y=saldo,
            marker_color=colors,
            text=[f"R$ {s:,.0f}".replace(',', '.') for s in saldo],
            textposition='outside'
        ))
        fig.add_hline(y=0, line_dash='dash', line_color='gray', opacity=0.5)
        fig.update_layout(title='Saldo Mensal (Renda − Despesas)', yaxis_title='R$')
        st.plotly_chart(fig, use_container_width=True)
```

- [ ] **Step 2: Verificar visualmente — rodar o app**

```bash
streamlit run app.py
```

Abrir http://localhost:8501. Confirmar na aba PF:
- 4 KPIs: Renda Total = R$ 24.000, Despesas Total = R$ 3.205, Investimentos = R$ 200, Meio + Usado = Cartão de Crédito
- Gráfico de pizza mostra categorias (Alimentação, Moradia, Saúde, etc.)
- Gráfico de meios de pagamento mostra Cartão de Crédito, Débito, Dinheiro, Transferência
- Saldo mensal: Jan verde (R$ 330), Fev verde (R$ 465), Mar-Dez verde (R$ 2.000)

- [ ] **Step 3: Rodar todos os testes**

```bash
pytest tests/test_data.py -v
```

Esperado: todos PASSED.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "feat: renderiza aba Pessoa Fisica com KPIs e graficos"
```

---

## Task 6: Polish final e validação

**Files:**
- Modify: `app.py` — ajustes de tema e mensagem de erro

- [ ] **Step 1: Adicionar tratamento de arquivo não encontrado em main()**

Substitua o bloco `main()` por:

```python
def main():
    st.set_page_config(
        page_title='Dashboard Autônomos',
        layout='wide',
        initial_sidebar_state='collapsed'
    )
    st.title('Controle de Gastos — Autônomos')
    st.caption('Fonte: Planilha de Controle de Gastos — Autônomos (2018)')

    import os
    if not os.path.exists(FILEPATH):
        st.error(f'Arquivo não encontrado: `{FILEPATH}`')
        st.stop()

    pj_data = load_pj_data(FILEPATH)
    pf_data = load_pf_data(FILEPATH)

    tab_pj, tab_pf = st.tabs(['📊 Pessoa Jurídica', '🏠 Pessoa Física'])
    with tab_pj:
        render_pj_tab(pj_data)
    with tab_pf:
        render_pf_tab(pf_data)


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Rodar app completo e verificar ambas as abas**

```bash
streamlit run app.py
```

Checklist visual:
- [ ] Aba PJ: KPIs corretos (Receita R$27.600, Despesas R$61.000, Resultado -R$33.400, Melhor Mês Fev/18)
- [ ] Aba PJ: 4 gráficos renderizados e legíveis
- [ ] Aba PF: KPIs corretos (Renda R$24.000, Despesas R$3.205, Investimentos R$200, Cartão de Crédito)
- [ ] Aba PF: 4 gráficos renderizados e legíveis
- [ ] Sem erros no console do Streamlit

- [ ] **Step 3: Rodar todos os testes finais**

```bash
pytest tests/test_data.py -v
```

Esperado: todos PASSED.

- [ ] **Step 4: Commit final**

```bash
git add app.py
git commit -m "feat: dashboard autonomos completo com PJ e PF"
```
