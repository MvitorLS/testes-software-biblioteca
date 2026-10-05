from datetime import timedelta

PRAZO_DIAS = 7
MULTA_POR_DIA = 2
MULTA_MAXIMA = 50


def calcular_multa(emprestimo, devolucao):
    vencimento = emprestimo + timedelta(days=PRAZO_DIAS)
    atraso = (devolucao - vencimento).days
    return min(max(atraso, 0) * MULTA_POR_DIA, MULTA_MAXIMA)
