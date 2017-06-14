#!/bin/bash
path_var=$(whereis python | grep "python")
virt_env=$1

# No argument provided - show file Usage
if [ -z "$1" ] ; then
    echo 'Usage: source '$0' <EnvironmentName>'
    exit 1
fi


# Python doesn't exist
if [ -z "$path_var" ] ; then 
	echo "Python not found in the system path"
	echo "1. Run the Python Installation exe again"
	echo "2. Click Modify"
	echo "3. Click Next on Optional Features page"
	echo "4. Tick 'Add Python to environment variables' and then click install"
	echo "Rerun this script after taking above action to verify installation"
	exit 1
else 
	# Run Python Script to check for Python version and Library requirements
	cur_dir=$(echo "${PWD##*/}")
	cd ..

	python3 -m virtualenv $virt_env || python -m virtualenv $virt_env

	# Get current folder name
	work_dir=$(echo "${PWD##*/}")

	if [ "$work_dir" = "$virt_env" ] ; then 
		echo "Activating Virtual Python Environment"
		chmod u+x ./bin/activate
		source ./bin/activate
	else 
		echo "Activating Virtual Python Environment"
		chmod u+x ./$virt_env/bin/activate
		source ./$virt_env/bin/activate || cd -
	fi
fi
