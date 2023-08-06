#!/bin/bash
#
# Copyright (c) 2016, BlueData Software, Inc.
#

SELF=$(readlink -nf $0)
SELF_DIR=$(dirname ${SELF})

BUILD_AMI='false'          # Build ami image(s), valid only for CentOS image
BUILD_AMI_ONLY='false'     # Build the ami image(s) only using the existing CentOS image
DOCKER_IMAGE_FILENAME=''
AMI_DEBUG_SUFFIX=""

print_help() {
    echo
    echo "USAGE: $0 [ -h | -i | -f ]"
    echo
    echo "      -h/--help      : Prints usage details and exits."
    echo "        -b/--basedir : Directory where the Dockerfile and related "
    echo "                       files are located"
    echo "       -f/--filename : File name/path to save the docker image."
    echo "        -n/--nametag : Name and optionally a tag in the 'name:tag' "
    echo "                       format."
    echo
}

parse_options() {
    while [ $# -gt 0 ]; do
        case $1 in
            -h|--help)
                print_help
                exit 0
                ;;
            -b|--basedir)
                BASE_DIRECTORY=$2

                TEMP_FILE=$(mktemp)
                DOCKER_FILE=${BASE_DIRECTORY}/Dockerfile
                cp -f ${DOCKER_FILE} ${TEMP_FILE} ## Backup the existing docker
                shift 2
                ;;
            -n|--nametag)
                DOCKER_IMAGE_NAME=$2
                shift 2
                ;;
            -f|--filename)
                DOCKER_IMAGE_FILENAME=$2
                shift 2
                ;;
            --)
                shift
                ;;
            *)
                echo "Unknown option $1."
                print_help
                exit 1
                ;;
        esac
    done
}

trap docker_file_restore INT EXIT

## FIXME! This is an unfortunate piece of code forced by the fact that we are
##         still using docker 1.7. Starting from 1.9, docker build supports a
##         --build-arg which is ideal for this usecase.
rhel_credentials_replace() {
    sed -i "s/\${RHEL_USERNAME}/${RHEL_USERNAME}/g; s/\${RHEL_PASSWORD}/${RHEL_PASSWORD}/g" \
            ${DOCKER_FILE}

    # Just in case the developer missed the {}, try this replacement as well.
    sed -i "s/\$RHEL_USERNAME/${RHEL_USERNAME}/g; s/\$RHEL_PASSWORD/${RHEL_PASSWORD}/g" \
            ${DOCKER_FILE}
}

docker_file_restore() {
    [[ -e ${TEMP_FILE} ]] && mv -f ${TEMP_FILE} ${DOCKER_FILE}
}

docker_build_image() {
    rhel_credentials_replace
    docker build -t ${DOCKER_IMAGE_NAME} ${BASE_DIRECTORY}
    if [[ $? -ne 0 ]]; then
        echo "failed to build docker image"
        exit 1
    fi

    echo
    echo "Successfully built ${DOCKER_IMAGE_NAME}."
}

docker_save_image() {
    echo
    echo "Saving ${DOCKER_IMAGE_NAME} as ${DOCKER_IMAGE_FILENAME}"

    TAR_FILENAME=$(sed s/.gz// <<< ${DOCKER_IMAGE_FILENAME})

    docker save -o ${TAR_FILENAME} ${DOCKER_IMAGE_NAME}
    if [[ $? -ne 0 ]]; then
        echo "failed to save docker image"
        exit 1
    fi

    DEST_DIR=$(dirname ${DOCKER_IMAGE_FILENAME})
    [[ ! -e ${DEST_DIR} ]] && mkdir -p ${DEST_DIR}

    gzip -f ${TAR_FILENAME}
    if [[ $? -ne 0 ]]; then
        echo "failed to gzip docker image"
        exit 1
    fi

    md5sum ${DOCKER_IMAGE_FILENAME} > ${DOCKER_IMAGE_FILENAME}.md5sum
}

create_docker_image_snapshot() {
    docker_build_image
    docker_save_image
}

SHORTOPTS="b:n:f:h"
LONGOPTS="basedir:,nametag:,filename:,help"
OPTS=$(getopt -u --options=$SHORTOPTS --longoptions=$LONGOPTS -- "$@")

if [ $? -ne 0 ]; then
    echo "ERROR: Unable to parse the option(s) provided."
    print_help
    exit 1
fi

parse_options $OPTS

create_docker_image_snapshot
