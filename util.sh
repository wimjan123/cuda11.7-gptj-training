retry() {
    counter=1
    maxtries=$1; shift;
    delay=$1; shift;
    echo Retrying "$@" with maxtries:$maxtries and delay:$delay
    while [[ $counter -le $maxtries ]]; do
        $@
        if [[ "$?" = "0" ]]; then
            break
        else
            >&2 echo Failed attempt $counter/$maxtries
            ((counter++))
            sleep $delay
        fi
    done
    if [[ $counter -gt $maxtries ]]; then
        >&2 echo RETRIES FAILED
        return 1
    fi
}

kitmaker_cleanup_webhook_success() {
    if [ ! -z $KITMAKER ] && [ ! -z $TRIGGER ]; then
        [[ ! -f TAG_MANIFEST ]] && exit 0  # Only call the success webhook in the deploy stage
        export a_image_name=$(awk '/./{line=$0} END{print line}' TAG_MANIFEST) # get the artifactory repo name
        sed -i '$ d' TAG_MANIFEST # delete the last line containing the artifactory repo
        export json_data="{\"status\": \"success\", \"CI_PIPELINE_ID\": \"${CI_PIPELINE_ID}\", \"CI_JOB_ID\": \"${CI_JOB_ID}\", \"CI_COMMIT_SHORT_SHA\": \"${CI_COMMIT_SHORT_SHA}\", \"gitlab_pipeline_url\": \"${CI_PIPELINE_URL}\", \"image_name\": \"${a_image_name}\", \"tags\": $(cat TAG_MANIFEST | jq -R . | jq -s . | jq 'map(select(length > 0))' | jq -c .)}"
        echo curl -v -H "Content-Type: application/json" -d "${json_data}" "${WEBHOOK_URL}"
        curl -v -H "Content-Type: application/json" -d "${json_data}" "${WEBHOOK_URL}"
    fi
}

kitmaker_webhook_failed() {
    if [ ! -z $KITMAKER ] && [ ! -z $TRIGGER ]; then
        if cat cmd_output | grep -q "ERROR"; then
            json_data="{\"status\": \"failed\", \"CI_PIPELINE_ID\": \"${CI_PIPELINE_ID}\", \"CI_JOB_ID\": \"${CI_JOB_ID}\", \"CI_COMMIT_SHORT_SHA\": \"${CI_COMMIT_SHORT_SHA}\", \"gitlab_pipeline_url\": \"${CI_PIPELINE_URL}\", \"cmd_output\": \"$(cat cmd_output)\"}"
            echo curl -v -H "Content-Type: application/json" -d "${json_data}" ${WEBHOOK_URL}
            curl -v -H "Content-Type: application/json" -d "${json_data}" ${WEBHOOK_URL}
            exit 1
        elif cat cmd_output | grep -q "DONE"; then
            echo "Seems the last 'run_cmd' command succeeded! Not calling webhook."
        fi
    fi
}

run_cmd() {
    printf "===== %s\n\n" "Running command:"
    printf "%s " "${@}"
    printf "\n\n"
    printf "===== Output: \n\n"
    echo -e "$@" | source /dev/stdin 2>&1 | tee cmd_output
    run_cmd_return=$?
    echo
    printf "===== Command returned: %s\n\n" "${run_cmd_return}"
    return $run_cmd_return
}
