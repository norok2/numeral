#!/usr/bin/env bash


# ======================================================================
echo -e "\n :: Update tag..."

echo -e "\nTag History:"
git tag
echo -e "\nProject Status:"
git status

NEW_VERSION=`git describe --abbrev=0 --tags`
echo -e -n "\n>> choose new version number [$NEW_VERSION]: "
read INPUT
NEW_VERSION=${INPUT:-$NEW_VERSION}

MESSAGE="Distribute to PyPI."
echo -e -n "\n>> set commit and tag message [$MESSAGE]: "
read INPUT
MESSAGE=${INPUT:-MESSAGE}

git commit -uno -a -m "$MESSAGE"
git tag -f "$NEW_VERSION" -m "$MESSAGE"
git push


# ======================================================================
echo -e "\n :: Create change log..."
CHANGELOG=CHANGELOG.txt
echo -e "Change Log\n==========\n" > ${CHANGELOG}
git log --oneline --decorate --graph >> ${CHANGELOG}
echo -e "${CHANGELOG} successfully created."


# ======================================================================
echo -e "\n :: Create package..."
python setup.py bdist_wheel --universal


# ======================================================================
echo -e "\n :: Distribute package..."
PYPIRC=release
PYPIRC_EXT=pypirc
if [ -z "$1" ]; then
    for FILE in *.${PYPIRC_EXT}; do
        CHOICE=${FILE%\.*}"|"$CHOICE
    done
    echo -e -n "\n>> choose target ["${CHOICE%?}"]: "
    read INPUT
    PYPIRC=${INPUT:-$PYPIRC}
else
    PYPIRC=$1
fi
PYPIRC_FILE=${PYPIRC}.${PYPIRC_EXT}

for FILE in dist/*; do
    if [ -f ${FILE} ] && [ -f ${PYPIRC_FILE} ]; then
        twine upload ${FILE} --config-file ${PYPIRC_FILE}
    fi
done
