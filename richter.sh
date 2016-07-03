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


function cmd_glm() {
    # Package and test GLM
    pushd "${c_root}/Lib/glm"
    cowsay 'Testing GLM with demo/testing'
    CONAN_USERNAME=demo conan export demo/testing
    CONAN_USERNAME=demo conan test_package
    popd
}

function cmd_refresh () {
    # Refresh the command list.
    mkdir -p Output
    python "${c_root}/Lib/BashiBazook/bashi.py" "${c_root}/richter.sh" > "${c_root}/richter.bashi-q"
    cp "${c_root}/richter.bashi-q" "${c_root}/richter.bashi"
}

bashi_help_preamble="
      @'.
      ';:                  ~~~~~~~~~~~~
    ,:'':;                  \\ RICHTER  \\
    '++#;:::::::::::::\`.     \\          \\
    ;,:'                      \\          \\
     :;'                       \\ COMMANDS \\
    '\`+'.                      /          /
   ,:'#+'                     /          /
   ,': ;:                    //\\/\\/\\/\\/\\/
  +'   +
  \`:  .;  "

set +e
source "${c_root}/richter.bashi" || set -e && cmd_refresh
set -e

source "${c_root}/richter.bashi"

bashi_run $@
