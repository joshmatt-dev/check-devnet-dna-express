#!/bin/bash
path_var=$(whereis python | grep "python")
requirements=$1

# No argument provided - show file Usage
if [ -z "$1" ] ; then
    echo 'Usage: '$0' <Requirements_file>'
    exit 1
fi

# Read requirements file line by line
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "$line"
    pip install $line
done < "$1"

pip list


