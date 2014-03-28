#!/bin/bash

args=("$@")

ci=false

if [ "${args[0]}" == "--ci" ]; then
  ci=true
fi

if [ $ci == true ]; then
  pushd .
  cd tests/testapp
  coverage run manage.py test rottweiler
  coverage xml
  popd
else
  pushd .
  cd tests/testapp
  python manage.py test rottweiler
  popd
fi
