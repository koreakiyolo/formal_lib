#!/usr/bin/zsh


setup_environment(){
    PYTHON_PATH=${HOME}/.local
###    IGNORE_ERRORS=E221,E701,E202
                    }

main(){
    setup_environment
    which $PYTHON_PATH/bin/pyflakes > /dev/null || exit 254
    which $PYTHON_PATH/bin/pycodestyle > /dev/null || exit 254
    $PYTHON_PATH/bin/pyflakes $*
    $PYTHON_PATH/bin/pycodestyle --ignore=$IGNORE_ERRORS --repeat $*
    exit 0
}

main $*
