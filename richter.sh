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

if [ "" != "${WINDIR}" ]; then
    readonly this_is_windows=true
    function conan() {
        cmd //c conan $@
    }
fi

# Set the username for the VM.
if [ "ubuntu-xenial" == "${HOSTNAME}" ]; then
    function conan() {
        ~/conan-venv/bin/conan $@
    }
    export CONAN_USERNAME="${CONAN_USERNAME:-demo}"
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

function cmd_install_vm() {
    # Install everything on a VM
    sudo apt-get install python3
    sudo apt-get install python3-venv
    sudo apt-get install python3-dev
    sudo apt-get install cowsay
    sudo apt-get install g++
    sudo apt-get install cmake

    pyvenv ~/conan-venv
    pushd "${c_root}/Lib/conan"
    ~/conan-venv/bin/pip install -r "${c_root}/Lib/conan/conans/requirements.txt"
    ~/conan-venv/bin/pip install -r "${c_root}/Lib/conan/conans/requirements_server.txt"
    ~/conan-venv/bin/pip install gunicorn
    ~/conan-venv/bin/pip install -e ./ --upgrade
    popd

    mkdir -p ~/.conan

    echo '
[storage]
path: ~/.conan/data

[settings_defaults]
arch=x86_64
build_type=Release
os=Linux
compiler=gcc
compiler.libcxx=libstdc++14
compiler.version=5.3
' > ~/.conan/conan.conf

    mkdir -p ~/.conan_server
    echo '
[server]
# WARNING! Change default variable of jwt_secret. You should change it periodically
# It only affects to current authentication tokens, you can change safetely anytime
# When it changes user are just forced to log in again
jwt_secret: hjgASGmSbkGRHfVTKMNNuWHo
jwt_expire_minutes: 120

ssl_enabled: False
port: 9300
public_port:
host_name: localhost

store_adapter: disk
authorize_timeout: 1800

disk_storage_path: ~/.conan_server/data
disk_authorize_timeout: 1800
updown_secret: fcFnReRnnONozqdiIyykpQOZ


[write_permissions]

#
# name,version,user,channel: user1, user2, user3
# The rules are applied in order. If a rule applies to a conan, system wont look further.
#
# Example: All versions of opencv package from lasote user in testing channel is only
# writeable by default_user and default_user2. Rest of packages are not writtable by anything
# except the author.
#
#   "opencv/2.3.4@lasote/testing": default_user, default_user2
#

[read_permissions]

#
# name,version,user,channel: user1, user2, user3
# The rules are applied in order. If a rule applies to a conan, system wont look further.
#
# Example: All versions of opencv package from lasote user in testing channel is only
# readable by default_user and default_user2. Rest of packages are world readable
#
#   opencv/1.2.3@lasote/testing: default_user default_user2
#   *:*@*/*: *
#
# By default all users can read all blocks
*/*@*/*: *


[users]
#default_user: defaultpass
demo: demo
' > ~/.conan_server/server.conf
    echo 'local http://localhost:9300' > ~/.conan/registry.txt
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
    python3 "${c_root}/Lib/BashiBazook/bashi.py" "${c_root}/richter.sh" > "${c_root}/richter.bashi-q"
    cp "${c_root}/richter.bashi-q" "${c_root}/richter.bashi"
}

function cmd_run_server() {
    #pkill gunicorn
    ~/conan-venv/bin/gunicorn -b 0.0.0.0:9300 -w 4 conans.server.server_launcher:app &
}

function cmd_test_packages() {
    pushd "${c_root}/Lib/cereal"
    conan upload "glm/1.2-0@${CONAN_USERNAME}/testing" --all -r=local
    popd
    pushd "${c_root}/Lib/glm"
    conan upload "glm/0.9.8-0@${CONAN_USERNAME}/testing" --all -r=local
    popd
}

function cmd_vagrant() {
    # Start up the VM to test the package.
    pushd "${c_root}/Vagrant"
    vagrant up
    popd
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
