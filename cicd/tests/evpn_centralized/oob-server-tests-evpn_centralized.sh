#!/bin/bash

check_state(){
if [ "$?" != "0" ]; then
    echo "ERROR Testing: The previous command failed!"
    exit 1
fi
}

set -e
set -x

#use the check_state function above to check return codes after tests 
#so that the outer/calling script test_sim_outside.sh bails out

echo "This is from inside the OOB Server"
echo "Put tests we want in this script"
