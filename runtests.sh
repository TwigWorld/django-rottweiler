#!/bin/bash

args=("$@")
index=0

ci=false
coverage=false

if [ "${args[0]}" == "--ci" ]; then
  ci=true
fi

if [ "${args[0]}" == "--coverage" ]; then
  coverage=true
fi

if [ $ci == true ]; then
  pushd .
  cd tests/testapp
  coverage run manage.py test rottweiler
  status=$?
  popd
  exit $status
elif [ $coverage == true ]; then
  pushd .
  cd tests/testapp
  coverage run manage.py test rottweiler
  status=$?
  coverage html
  open -a Google\ Chrome htmlcov/index.html
  exit $status
else
  pushd .
  cd tests/testapp
  python manage.py test rottweiler
  status=$?
  popd
  exit $status
fi
