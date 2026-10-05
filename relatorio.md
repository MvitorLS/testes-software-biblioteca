---
title: "Aproveitamento de Conhecimentos – Testes de Software"
subtitle: "Módulo: Empréstimo e devolução de livros com multa por atraso"
author: "Aluno: Matheus Vitor — Bacharelado em Ciências da Computação"
date: "Prof. Gerson Peres — Entrega: 08/10/2026"
lang: pt-BR
geometry: margin=2.5cm
fontsize: 11pt
---

# 1. Cenário e regras de negócio

Módulo de um sistema fictício de biblioteca: o usuário pega livros emprestados, devolve e paga multa se atrasar. Regras definidas:

| ID | Regra |
|----|-------|
| RN1 | O prazo de empréstimo é de 7 dias corridos. |
| RN2 | Cada dia de atraso gera multa de R$ 2,00. |
| RN3 | A multa tem teto de R$ 50,00 por devolução. |
| RN4 | Cada usuário pode ter no máximo 3 livros emprestados ao mesmo tempo. |
| RN5 | Usuário com multa pendente não pode pegar novo livro (até pagar). |
| RN6 | Livro sem exemplar disponível não pode ser emprestado. |

# 2. Parte 1 – Fundamentação e planejamento

## 2.1 Erro, defeito e falha; verificação e validação

- **Erro:** engano humano. O desenvolvedor escreve `>` no lugar de `>=` ao comparar o limite de livros do usuário.
- **Defeito (bug):** o resultado do erro dentro do código, ou seja, a linha `if emprestimos > LIMITE_LIVROS`.
- **Falha:** o comportamento errado visto na execução. O sistema empresta o 4º livro ao mesmo usuário, violando a RN4.

Um erro gera um defeito, e o defeito só vira falha quando aquele trecho é executado com os dados certos.

- **Verificação** ("estamos construindo o sistema *corretamente*?"): conferir se o código segue as regras RN1 a RN6, por meio de revisão e testes automatizados. Exemplo: o teste que confere que 3 dias de atraso resultam em R$ 6,00.
- **Validação** ("estamos construindo o sistema *certo*?"): conferir se o sistema atende a necessidade real. Exemplo: o bibliotecário usa o sistema e confirma que R$ 2,00 por dia e teto de R$ 50,00 é a política que a biblioteca quer.

## 2.2 Plano de teste resumido

| Item | Descrição |
|------|-----------|
| **Escopo** | Cálculo de multa, empréstimo, devolução, pagamento de multa e notificação ao usuário. |
| **Itens a testar** | `calcular_multa`, `Biblioteca.emprestar`, `devolver`, `pagar_multa`, `emprestimos_ativos` e a chamada ao notificador. |
| **Fora do escopo** | Interface gráfica, banco de dados, cadastro de livros e usuários, envio real de e-mail/SMS, renovação e reserva de livros. |
| **Tipos e níveis** | Unitário e integração automatizados (pytest); regressão a cada alteração; sistema e aceitação de forma manual/simulada (ver 2.3). |
| **Critério de entrada** | Regras RN1–RN6 definidas; ambiente Python instalado; código compilando/importando sem erro. |
| **Critério de saída** | 100% dos testes passando; cobertura de linhas e branches ≥ 90%; nenhum defeito crítico aberto. |
| **Riscos** | Regras ambíguas (ex.: dia do vencimento conta como atraso?); erro de limite (off-by-one) nas datas; notificador real indisponível; módulo só em memória. |
| **Ambiente** | Linux, Python 3.14, pytest 9, pytest-cov, git. |
| **Papéis** | Aluno: analista de requisitos, desenvolvedor, testador e responsável pelos relatórios de defeito. Professor: avaliador/cliente. |

## 2.3 Níveis e tipos de teste do módulo

| Nível | O que testaria | Justificativa |
|-------|----------------|---------------|
| Unitário | `calcular_multa` com várias datas; regras isoladas de `emprestar`. | Funções pequenas e puras, rápidas de testar, concentram as regras RN1–RN6. |
| Integração | `Biblioteca` junto com o notificador (mock). | Garante que a devolução com multa realmente avisa o usuário. |
| Sistema | Fluxo completo: emprestar → atrasar → devolver → multa → pagar → emprestar de novo. | Valida as regras trabalhando juntas. |
| Aceitação | Bibliotecário confirma os valores e as mensagens. | Valida que o sistema serve ao negócio. |

| Tipo | Aplicação |
|------|-----------|
| Funcional | Todas as regras RN1–RN6 (principal foco deste trabalho). |
| Regressão | Rodar o pytest completo a cada mudança, para garantir que corrigir uma regra não quebra outra. |
| Desempenho | Muitos empréstimos simultâneos no horário de pico (ex.: início do semestre). |
| Usabilidade | Tela do balcão: mensagem clara quando o empréstimo é negado e o motivo. |
| Segurança | Só funcionário autorizado pode registrar devolução e baixar multa (evita perdão indevido de multa). |

# 3. Parte 2 – Projeto de casos de teste

## 3.1 Particionamento de equivalência e valor limite

**Campo 1 – dias de atraso na devolução (RN1, RN2, RN3).** Os "dias após o empréstimo" são contados a partir da data do empréstimo, e o atraso é esse valor menos 7.

| Partição | Atraso (dias) | Multa esperada |
|----------|---------------|----------------|
| P1 – no prazo | ≤ 0 | R$ 0,00 |
| P2 – atraso proporcional | 1 a 24 | 2 × atraso |
| P3 – teto atingido | ≥ 25 | R$ 50,00 |

Valores limite escolhidos (dias após o empréstimo → atraso → multa): 6 → −1 → 0; **7 → 0 → 0**; **8 → 1 → 2**; **31 → 24 → 48**; **32 → 25 → 50**; 33 → 26 → 50. Foram escolhidos porque erros de "um a mais/um a menos" costumam aparecer nas fronteiras entre as partições (último dia sem multa, primeiro dia com multa, e o dia em que o teto é atingido).

**Campo 2 – quantidade de livros emprestados ao usuário (RN4).**

| Partição | Livros ativos | Resultado |
|----------|---------------|-----------|
| P1 – dentro do limite | 0 a 2 | Empréstimo permitido |
| P2 – limite atingido | 3 | Empréstimo negado |

Valores limite: **2** (permite o 3º livro) e **3** (nega o 4º livro).

## 3.2 Tabela de decisão (concessão do empréstimo)

Condições: C1 = usuário sem multa pendente; C2 = usuário com menos de 3 livros; C3 = livro com exemplar disponível.

| Regra | C1 | C2 | C3 | Ação |
|-------|----|----|----|------|
| R1 | S | S | S | **Emprestar** |
| R2 | S | S | N | Negar (sem exemplar) |
| R3 | S | N | S | Negar (limite de 3 livros) |
| R4 | S | N | N | Negar |
| R5 | N | S | S | Negar (multa pendente) |
| R6 | N | S | N | Negar |
| R7 | N | N | S | Negar |
| R8 | N | N | N | Negar |

Apenas R1 permite o empréstimo. R2, R3 e R5 estão cobertas por testes automatizados. As demais combinações negam por mais de um motivo.

## 3.3 Casos de teste formais

| ID | Pré-condição | Passos | Dados de entrada | Resultado esperado | Prior. |
|----|--------------|--------|------------------|--------------------|--------|
| CT01 | Livro emprestado em 01/01 | Devolver no dia 7 | Devolução 08/01 | Multa R$ 0,00 | Alta |
| CT02 | Livro emprestado em 01/01 | Devolver no dia 6 | Devolução 07/01 | Multa R$ 0,00 | Média |
| CT03 | Livro emprestado em 01/01 | Devolver com 1 dia de atraso | Devolução 09/01 | Multa R$ 2,00 | Alta |
| CT04 | Livro emprestado em 01/10 | Devolver com 3 dias de atraso | Devolução 11/10 | Multa R$ 6,00 | Alta |
| CT05 | Livro emprestado em 01/01 | Devolver com 24 dias de atraso | Devolução 01/02 | Multa R$ 48,00 | Média |
| CT06 | Livro emprestado em 01/01 | Devolver com 25 dias de atraso | Devolução 02/02 | Multa R$ 50,00 (teto) | Alta |
| CT07 | Livro emprestado em 01/01 | Devolver quase um ano depois | Devolução 31/12 | Multa R$ 50,00 (teto) | Alta |
| CT08 | Usuário sem pendências; 1 exemplar | Emprestar o livro L1 | usuário "ana", L1 | Empréstimo registrado (1 ativo) | Alta |
| CT09 | "ana" com 3 livros | Tentar emprestar o 4º | L4 | Negado (limite de 3) | Alta |
| CT10 | L1 com 0 exemplares livres | "bia" tenta emprestar L1 | "bia", L1 | Negado (sem exemplar) | Alta |
| CT11 | "ana" com multa de R$ 6,00 | Tentar emprestar L2 | "ana", L2 | Negado (multa pendente) | Alta |
| CT12 | "ana" com multa de R$ 6,00 | Pagar a multa e emprestar L2 | "ana", L2 | Empréstimo permitido | Média |
| CT13 | Notificador ativo | Devolver com 3 dias de atraso | "ana", L1 | Aviso enviado: ("ana", R$ 6,00) | Média |
| CT14 | Notificador ativo | Devolver no prazo | "ana", L1 | Nenhum aviso enviado | Baixa |
| CT15 | "ana" com 2 livros | Emprestar o 3º | L3 | Empréstimo permitido (limite não atingido) | Média |

Todos os casos serão automatizados em `test_biblioteca.py` (CT01–CT03 e CT05–CT06 pelo teste parametrizado `test_valores_limite_da_multa`).
