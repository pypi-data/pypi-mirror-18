#!/bin/sh

if [[ "$TEST_NOTEBOOK" == "yes" ]]; then
    sleep 3
    # sudo /home/travis/miniconda/envs/myenv/bin/jupyter notebook --port=8889 --browser=google-chrome --ip=127.0.0.1 &
    jupyter notebook --port=8889 --browser=google-chrome --ip=127.0.0.1 &
    sleep 3
    nightwatch
else
  (cd nglview/tests && py.test --cov=nglview -vs .) 
fi
