from datetime import timedelta


def calcular_multa(emprestimo, devolucao):
    vencimento = emprestimo + timedelta(days=7)
    atraso = (devolucao - vencimento).days
    if atraso <= 0:
        return 0
    return atraso * 2
