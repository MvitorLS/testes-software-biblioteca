# Biblioteca: empréstimo e devolução com multa por atraso

Trabalho de Aproveitamento / Certificação de Conhecimentos Anteriores da disciplina **Testes de Software**
(Bacharelado em Ciências da Computação, Prof. Gerson Peres).

**Aluno:** Matheus Vitor Lourenço Schionato

Módulo de um sistema fictício de biblioteca, desenvolvido com **TDD** (Red-Green-Refactor) em **Python 3.14** e testado com **pytest**.

## Regras de negócio

| ID | Regra |
|----|-------|
| RN1 | Prazo de empréstimo de 7 dias corridos |
| RN2 | Multa de R$ 2,00 por dia de atraso |
| RN3 | Teto da multa de R$ 50,00 |
| RN4 | Máximo de 3 livros emprestados por usuário |
| RN5 | Usuário com multa pendente não pode pegar novo livro |
| RN6 | Livro sem exemplar disponível não pode ser emprestado |

## Como rodar

```
python3 -m venv .venv
.venv/bin/pip install pytest pytest-cov
.venv/bin/pytest -v
```

Cobertura de código:

```
.venv/bin/pytest --cov=biblioteca --cov-branch
```

Menu de demonstração (testes, cobertura, defeitos e ciclos TDD):

```
./rodar_tudo.sh
```

## Estrutura

| Arquivo | O que é |
|---------|---------|
| `biblioteca.py` | Código do módulo: `calcular_multa` e a classe `Biblioteca` |
| `test_biblioteca.py` | 18 testes automatizados (pytest, com testes parametrizados e mock) |
| `rodar_tudo.sh` | Menu que roda os testes, a cobertura, os 2 defeitos e os ciclos TDD |
| `relatorio.pdf` / `.docx` / `.md` | Relatório do trabalho (Partes 1 a 5) |

## Resultados

- 18 testes, todos aprovados
- 100% de cobertura de linhas e de desvios (branches)
- 4 ciclos Red-Green-Refactor, um commit por etapa (`git log --oneline --reverse`)
- 2 defeitos introduzidos propositalmente e detectados pelos testes (BUG-01 e BUG-02, descritos no relatório)
