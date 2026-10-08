from datetime import timedelta

PRAZO_DIAS = 7
# BUG-02: comente a linha acima e descomente a de baixo
# PRAZO_DIAS = 8
MULTA_POR_DIA = 2
MULTA_MAXIMA = 50
LIMITE_LIVROS = 3


def calcular_multa(emprestimo, devolucao):
    vencimento = emprestimo + timedelta(days=PRAZO_DIAS)
    dias_atraso = max((devolucao - vencimento).days, 0)
    return min(dias_atraso * MULTA_POR_DIA, MULTA_MAXIMA)


class EmprestimoNegado(Exception):
    pass


class Biblioteca:
    def __init__(self, notificador=None):
        self.notificador = notificador
        self.exemplares = {}
        self.emprestimos = {}
        self.multas = {}

    def adicionar_livro(self, livro, exemplares):
        self.exemplares[livro] = exemplares

    def emprestimos_ativos(self, usuario):
        return len(self.emprestimos.get(usuario, {}))

    def _validar_emprestimo(self, usuario, livro):
        if self.multas.get(usuario, 0) > 0:
            raise EmprestimoNegado("usuario com multa pendente")
        # BUG-01: comente a linha abaixo e descomente a seguinte
        if self.emprestimos_ativos(usuario) >= LIMITE_LIVROS:
        # if self.emprestimos_ativos(usuario) > LIMITE_LIVROS:
            raise EmprestimoNegado(f"limite de {LIMITE_LIVROS} livros atingido")
        if self.exemplares.get(livro, 0) < 1:
            raise EmprestimoNegado("livro sem exemplar disponivel")

    def emprestar(self, usuario, livro, data):
        self._validar_emprestimo(usuario, livro)
        self.exemplares[livro] -= 1
        self.emprestimos.setdefault(usuario, {})[livro] = data

    def devolver(self, usuario, livro, data):
        emprestimo = self.emprestimos[usuario].pop(livro)
        self.exemplares[livro] += 1
        multa = calcular_multa(emprestimo, data)
        self.multas[usuario] = self.multas.get(usuario, 0) + multa
        if multa > 0 and self.notificador:
            self.notificador.avisar(usuario, multa)
        return multa

    def pagar_multa(self, usuario):
        self.multas[usuario] = 0
