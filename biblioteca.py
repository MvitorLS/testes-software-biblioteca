from datetime import timedelta

PRAZO_DIAS = 7
MULTA_POR_DIA = 2
MULTA_MAXIMA = 50


def calcular_multa(emprestimo, devolucao):
    vencimento = emprestimo + timedelta(days=PRAZO_DIAS)
    dias_atraso = max((devolucao - vencimento).days, 0)
    return min(dias_atraso * MULTA_POR_DIA, MULTA_MAXIMA)
