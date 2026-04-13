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
