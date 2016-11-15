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
PYPIRC_EXT=pypirc
PYPIRC_FILES=*.${PYPIRC_EXT}
NUM_PYPIRC_FILES=${#PYPIRC_FILES[@]}
if [ -z "$1" ]; then
    if [ "$NUM_PYPIRC_FILES" -gt 1 ]; then
        for FILE in $PYPIRC_FILES; do
            CHOICE=${FILE%\.*}
            CHOICES=${CHOICE}"|"${CHOICES}
        done
        echo -e -n "\n>> available targets: ["${CHOICES%?}"]"
        echo -e -n "\n>> choose target ["${CHOICE}"]: "
        read INPUT
        PYPIRC=${INPUT:-$CHOICE}
    else
        PYPIRC_FILE="${PYPIRC_FILES%.*}"
    fi
else
    PYPIRC=$1
fi
if [ -n "$PYPIRC"  ]; then
    PYPIRC_FILE=${PYPIRC}.${PYPIRC_EXT}
fi

MASK="\.dev"
for FILE in dist/*; do
    if [[ ! $FILE =~ $MASK ]] && [ -f ${FILE} ] && [ -f ${PYPIRC_FILE} ]; then
        echo -e "Uploading `${FILE}` ..."
        twine upload ${FILE} --config-file ${PYPIRC_FILE}
    else
        echo -e "Skipping \`${FILE}\`"
    fi
done
