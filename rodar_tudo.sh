#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
export PYTHONDONTWRITEBYTECODE=1
RAIZ=$PWD
if [ -x "$RAIZ/.venv/bin/pytest" ]; then PYBIN="$RAIZ/.venv/bin/pytest"; else PYBIN="pytest"; fi
if ! command -v "$PYBIN" >/dev/null 2>&1; then
    echo "pytest nao encontrado. Instale com: pip install pytest pytest-cov" >&2
    exit 1
fi
PYTEST="$PYBIN -p no:cacheprovider"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"; rm -f "$RAIZ/.coverage"' EXIT

titulo() { printf '\n########## %s ##########\n\n' "$1"; }

testes() {
    titulo "TESTES (todos devem passar)"
    $PYTEST -v
}

cobertura() {
    titulo "COBERTURA"
    $PYTEST -q --cov=biblioteca --cov-branch --cov-report=term-missing
}

defeito() {
    titulo "$1"
    local dir="$TMP/$2"
    rm -rf "$dir" && mkdir "$dir" && cp biblioteca.py test_biblioteca.py "$dir/"
    sed -i "$3" "$dir/biblioteca.py"
    (cd "$dir" && $PYTEST -q --tb=line)
}

bug1() { defeito "DEFEITO BUG-01: 4o livro permitido (>= virou >)" b1 's/>= LIMITE_LIVROS/> LIMITE_LIVROS/'; }
bug2() { defeito "DEFEITO BUG-02: prazo de 8 dias em vez de 7" b2 's/^PRAZO_DIAS = 7/PRAZO_DIAS = 8/'; }

tdd() {
    titulo "CICLOS TDD (git log)"
    git log --oneline --reverse --grep='^\(test\|feat\|refactor\):'
}

passo() {
    local nome=$1 hash=$2 dir="$TMP/$1$2"
    mkdir -p "$dir" && git archive "$hash" | tar -x -C "$dir"
    printf '  %-9s %s  %s\n' "$nome" "$hash" "$(git log -1 --format=%s "$hash")"
    (cd "$dir" && $PYTEST -q --tb=no 2>&1 | tail -1 | sed 's/^/            => /')
}

ciclo() {
    titulo "CICLO $1: $2"
    passo RED "$3"
    passo GREEN "$4"
    passo REFACTOR "$5"
}

tdd_ao_vivo() {
    ciclo 1 "multa por atraso (RN1, RN2)" 365969d 030e541 a43b60d
    ciclo 2 "teto da multa (RN3)" 9943459 30b13a2 2715822
    ciclo 3 "regras de emprestimo (RN4, RN5, RN6)" 5f4a0ea c278c69 7c9f261
    ciclo 4 "pagar multa e notificador (mock)" b46a015 3e6eb96 d6e7ccf
}

executar() {
    case "$1" in
        7) tdd_ao_vivo ;;
        1) testes ;;
        2) cobertura ;;
        3) bug1 ;;
        4) bug2 ;;
        5) tdd ;;
        6) testes; cobertura; bug1; bug2; tdd ;;
        *) echo "Opcao invalida: $1" ;;
    esac
}

menu() {
    cat <<'EOF'

==================== MENU ====================
 1 - Funcional: roda os testes (tudo passa)
 2 - Cobertura de codigo
 3 - Com erro 1: BUG-01 (4o livro permitido)
 4 - Com erro 2: BUG-02 (prazo de 8 dias)
 5 - Ciclos TDD (commits Red/Green/Refactor)
 6 - Tudo em sequencia
 7 - Ao vivo: RED, GREEN e REFACTOR de cada ciclo
 0 - Sair
==============================================
EOF
}

if [ -n "$1" ]; then
    executar "$1"
    exit 0
fi

while true; do
    menu
    read -r -p "Escolha: " opcao || break
    [ "$opcao" = "0" ] && break
    executar "$opcao"
done
