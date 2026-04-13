# Design: Dashboard de Controle de Gastos — Autônomos

**Data:** 2026-04-13  
**Status:** Aprovado

---

## Visão Geral

Dashboard Streamlit de arquivo único (`app.py`) que lê a planilha `dados/Planilha_de_Controle_de_Gastos_-_Autnomos.xlsx` e exibe visualizações interativas para as perspectivas Pessoa Jurídica (PJ) e Pessoa Física (PF).

---

## Arquitetura

- **Tecnologia:** Streamlit + Plotly Express
- **Estrutura:** Arquivo único `app.py` na raiz do projeto
- **Leitura de dados:** `openpyxl` (sem numpy/pandas — bloqueio de DLL no ambiente)
- **Entrada:** `dados/Planilha_de_Controle_de_Gastos_-_Autnomos.xlsx`
- **Execução:** `streamlit run app.py`

### Fluxo de dados

```
Planilha XLSX
  └── openpyxl (leitura)
        └── Dicts Python (transformação)
              └── Plotly Express (gráficos)
                    └── Streamlit (layout + renderização)
```

---

## Abas do Dashboard

### Aba 1 — Pessoa Jurídica (PJ)

Fonte: aba `Pessoa Jurídica` da planilha (12 meses × categorias de receita/despesa).

**KPIs (4 cards no topo):**
- Receita Total anual
- Despesas Total anual
- Resultado Operacional anual (receita − despesa)
- Melhor Mês (mês com maior resultado operacional)

**Gráficos (grid 2×2):**
1. Barras agrupadas — Receitas vs Despesas por mês
2. Pizza — Composição das despesas por categoria
3. Linha — Resultado Operacional mês a mês
4. Barras horizontais — Top categorias de despesa (ranking)

---

### Aba 2 — Pessoa Física (PF)

Fonte: aba `Pessoa Física` da planilha (12 meses × categorias de despesa pessoal + meio de pagamento).

**KPIs (4 cards no topo):**
- Renda Total anual
- Despesas Total anual
- Total de Investimentos no ano
- Meio de Pagamento mais utilizado

**Gráficos (grid 2×2):**
1. Barras agrupadas — Renda vs Despesas por mês
2. Pizza — Composição das despesas por categoria (Alimentação, Moradia, Saúde, etc.)
3. Barras horizontais — Gastos por Meio de Pagamento (Cartão Crédito, Débito, Dinheiro, Transferência)
4. Barras — Saldo Mensal (Renda − Despesas)

---

## Transformação dos Dados

### PJ
- Linha 1: cabeçalho de meses (colunas 2–13)
- Linhas com nome começando em `-`: itens de receita ou despesa
- Linha `Total de Receitas`: soma de receitas
- Linha `Total das Despesas`: soma de despesas
- Linha `Resultado Operacional`: já calculado na planilha

### PF
- Estrutura: par de colunas por mês (valor + meio de pagamento)
- Linhas de categoria pai (ex: `Alimentação`, `Moradia`): ignorar, são agrupadores
- Linhas de sub-item com valor numérico: incluir
- Linha `Total das Despesas`, `Renda Mensal`, `Resultado Operacional`, `Investimentos Mensais`: KPIs

---

## Considerações Técnicas

- `openpyxl` com `data_only=True` para ler valores calculados
- Encoding: nomes das abas têm acentos (`Pessoa Jurídica`, `Pessoa Física`) — tratar corretamente
- Valores `None` nas células devem ser tratados como `0`
- Cores: verde para receita/positivo, vermelho para despesa/negativo, azul para neutro
- Layout Streamlit: `st.tabs()` para as duas abas, `st.columns()` para KPIs e gráficos

---

## Arquivos a Criar

```
app.py                  ← aplicação principal
requirements.txt        ← streamlit, plotly, openpyxl
```
