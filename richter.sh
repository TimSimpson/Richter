#!/usr/bin/env bash
###############################################################################
#  Conan StIV
###############################################################################
#
# Builds various projects using Conan.
#
###############################################################################
set -e

bashi_base_command="${bashi_base_command:-$0}"
readonly c_root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ "" == "${WINDIR}" ]; then
    readonly this_is_windows=
    function conan() {
        conan $@
    }
else
    readonly this_is_windows=true
    function conan() {
        cmd //c conan $@
    }
fi

function cmd_cereal() {
    # Package and test Cereal
    pushd "${c_root}/Lib/cereal"
    cowsay "Testing Cereal with ${CONAN_USERNAME}/testing"
    conan export "${CONAN_USERNAME}"/testing
    conan test_package
    popd
}

function cmd_glm() {
    # Package and test GLM
    pushd "${c_root}/Lib/glm"
    cowsay "Testing GLM with ${CONAN_USERNAME}/testing"
    conan export "${CONAN_USERNAME}"/testing
    conan test_package
    popd
}

function cmd_lua() {
    # Package and test Cereal
    pushd "${c_root}/Lib/lua"
    cowsay "Testing Lua with ${CONAN_USERNAME}/testing"
    conan export "${CONAN_USERNAME}"/testing
    conan test_package
    popd
}

function cmd_refresh () {
    # Refresh the command list.
    mkdir -p Output
    python "${c_root}/Lib/BashiBazook/bashi.py" "${c_root}/richter.sh" > "${c_root}/richter.bashi-q"
    cp "${c_root}/richter.bashi-q" "${c_root}/richter.bashi"
}

bashi_help_preamble="
     _  E_E
     -=-'_'                 R I C H T E R
      \"'''-----------*       =============
      ''||
       )) \\
      /   |
'' :'' :'' :'' :'' :'' :'' :'' :'' :'' :''"

set +e
source "${c_root}/richter.bashi" || set -e && cmd_refresh
set -e

source "${c_root}/richter.bashi"

bashi_run $@
