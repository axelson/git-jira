#!/bin/bash

# Copy jira
cp jira.sh "$(git --exec-path)"/git-jira
echo "Copied git-jira file to $(git --exec-path)"

# Record the installation location in the git-script file
sed -i.bak "s+CHANGE_INSTALL_LOCATION+`pwd`+" "$(git --exec-path)/git-jira"

python --version
if [ $? -eq 0 ]; then
    echo "Python seems to be installed correctly, you should be good to go!"
else
    echo "Please install python and add it to your path"
fi
