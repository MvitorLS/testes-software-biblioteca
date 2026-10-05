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
