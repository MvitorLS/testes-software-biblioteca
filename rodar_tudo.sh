#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
export PYTHONDONTWRITEBYTECODE=1
RAIZ=$PWD
PYTEST="$RAIZ/.venv/bin/pytest -p no:cacheprovider"
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

executar() {
    case "$1" in
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
