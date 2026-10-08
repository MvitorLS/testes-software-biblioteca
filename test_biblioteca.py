from datetime import date, timedelta
from unittest.mock import Mock

import pytest

from biblioteca import Biblioteca, EmprestimoNegado, calcular_multa


def test_sem_atraso_nao_tem_multa():
    assert calcular_multa(date(2026, 10, 1), date(2026, 10, 8)) == 0


def test_atraso_de_3_dias_gera_multa_de_6_reais():
    assert calcular_multa(date(2026, 10, 1), date(2026, 10, 11)) == 6


def test_multa_nao_passa_do_teto_de_50_reais():
    assert calcular_multa(date(2026, 1, 1), date(2026, 12, 31)) == 50


def test_usuario_sem_pendencias_pode_emprestar():
    biblioteca = Biblioteca()
    biblioteca.adicionar_livro("L1", exemplares=1)
    biblioteca.emprestar("ana", "L1", date(2026, 10, 1))
    assert biblioteca.emprestimos_ativos("ana") == 1


def test_empresta_terceiro_livro_dentro_do_limite():
    biblioteca = Biblioteca()
    for livro in ["L1", "L2", "L3"]:
        biblioteca.adicionar_livro(livro, exemplares=1)
        biblioteca.emprestar("ana", livro, date(2026, 10, 1))
    assert biblioteca.emprestimos_ativos("ana") == 3


def test_nao_empresta_quarto_livro():
    biblioteca = Biblioteca()
    for livro in ["L1", "L2", "L3", "L4"]:
        biblioteca.adicionar_livro(livro, exemplares=1)
    for livro in ["L1", "L2", "L3"]:
        biblioteca.emprestar("ana", livro, date(2026, 10, 1))
    with pytest.raises(EmprestimoNegado):
        biblioteca.emprestar("ana", "L4", date(2026, 10, 1))


def test_nao_empresta_livro_sem_exemplar():
    biblioteca = Biblioteca()
    biblioteca.adicionar_livro("L1", exemplares=1)
    biblioteca.emprestar("ana", "L1", date(2026, 10, 1))
    with pytest.raises(EmprestimoNegado):
        biblioteca.emprestar("bia", "L1", date(2026, 10, 1))


def test_nao_empresta_com_multa_pendente():
    biblioteca = Biblioteca()
    biblioteca.adicionar_livro("L1", exemplares=1)
    biblioteca.adicionar_livro("L2", exemplares=1)
    biblioteca.emprestar("ana", "L1", date(2026, 10, 1))
    biblioteca.devolver("ana", "L1", date(2026, 10, 11))
    with pytest.raises(EmprestimoNegado):
        biblioteca.emprestar("ana", "L2", date(2026, 10, 12))


def test_pagar_multa_libera_novo_emprestimo():
    biblioteca = Biblioteca()
    biblioteca.adicionar_livro("L1", exemplares=1)
    biblioteca.adicionar_livro("L2", exemplares=1)
    biblioteca.emprestar("ana", "L1", date(2026, 10, 1))
    biblioteca.devolver("ana", "L1", date(2026, 10, 11))
    biblioteca.pagar_multa("ana")
    biblioteca.emprestar("ana", "L2", date(2026, 10, 12))
    assert biblioteca.emprestimos_ativos("ana") == 1


def test_devolucao_com_multa_notifica_usuario():
    notificador = Mock()
    biblioteca = Biblioteca(notificador)
    biblioteca.adicionar_livro("L1", exemplares=1)
    biblioteca.emprestar("ana", "L1", date(2026, 10, 1))
    biblioteca.devolver("ana", "L1", date(2026, 10, 11))
    notificador.avisar.assert_called_once_with("ana", 6)


def test_devolucao_no_prazo_nao_notifica():
    notificador = Mock()
    biblioteca = Biblioteca(notificador)
    biblioteca.adicionar_livro("L1", exemplares=1)
    biblioteca.emprestar("ana", "L1", date(2026, 10, 1))
    biblioteca.devolver("ana", "L1", date(2026, 10, 8))
    notificador.avisar.assert_not_called()


@pytest.mark.parametrize(
    "dias_apos_emprestimo, esperado",
    [(6, 0), (7, 0), (8, 2), (31, 48), (32, 50), (33, 50)],
)
def test_valores_limite_da_multa(dias_apos_emprestimo, esperado):
    emprestimo = date(2026, 1, 1)
    devolucao = emprestimo + timedelta(days=dias_apos_emprestimo)
    assert calcular_multa(emprestimo, devolucao) == esperado


def test_multa_de_um_usuario_nao_bloqueia_outro():
    biblioteca = Biblioteca()
    biblioteca.adicionar_livro("L1", exemplares=1)
    biblioteca.adicionar_livro("L2", exemplares=1)
    biblioteca.emprestar("ana", "L1", date(2026, 10, 1))
    biblioteca.devolver("ana", "L1", date(2026, 10, 11))
    biblioteca.emprestar("bia", "L2", date(2026, 10, 12))
    assert biblioteca.emprestimos_ativos("bia") == 1
