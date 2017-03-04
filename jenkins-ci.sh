#!/usr/bin/env bash

REPORT_DIR=report
VENV_PATH=.venv

function init_dir() {
    mkdir -p $REPORT_DIR
}

function setup_env() {
    echo "[Make Virtualenv]"
    sudo virtualenv -p python3 $VENV_PATH
    source $VENV_PATH/bin/activate
}

function setup_package() {
    echo "[Setup Python Packages]"
    pip install -r requirements.txt
}

function unittest_python() {
    echo "[Python Unittest]"

    nosetests bravepeach_tests \
    --with-cov --cov-report xml \
    --xunit-file $REPORT_DIR/py-xunit.xml \
    --with-xunit --cov webapp
    mv coverage.xml $REPORT_DIR
}

function setup_venv() {
    virtualenv $VENV_PATH
}

case "$1" in
    unittest)
        echo "[Jenkins CI] Unittest"
        setup_env
        init_dir
        setup_package
        unittest_python
        ;;
    stage)
        echo "[Jenkins CI] Deploy to Staging Server"
        setup_env
        setup_package
        python deploy_stage.py
        ;;
    *)
        echo "[Jenkins CI] Not Valid"
        ;;
esac
