from datetime import date

from biblioteca import calcular_multa


def test_sem_atraso_nao_tem_multa():
    assert calcular_multa(date(2026, 10, 1), date(2026, 10, 8)) == 0


def test_atraso_de_3_dias_gera_multa_de_6_reais():
    assert calcular_multa(date(2026, 10, 1), date(2026, 10, 11)) == 6


def test_multa_nao_passa_do_teto_de_50_reais():
    assert calcular_multa(date(2026, 1, 1), date(2026, 12, 31)) == 50
