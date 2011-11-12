#!/bin/bash

cp jira.sh "$(git --exec-path)"/git-jira
if [ "$?" -ne 0 ]; then
    echo "Unable to install"
    echo "If on Linux: need to run as sudo $0"
    echo "If on Windows: need to run this git shell as administrator (right
    click on shell shortcut and click run as administrator)"
    exit 1;
fi
echo "Copied git-jira file to $(git --exec-path)"

# Record the installation location in the git-script file
sed -i.bak "s+CHANGE_INSTALL_LOCATION+`pwd`+" "$(git --exec-path)/git-jira"

python --version
if [ $? -eq 0 ]; then
    echo "Python seems to be installed correctly, you should be good to go!"
else
    echo "Please install python and add it to your path"
fi
