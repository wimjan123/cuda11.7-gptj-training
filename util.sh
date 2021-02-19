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
        export json_data="{\"status\": \"success\", \"gitlab_pipeline_url\": \"${CI_PIPELINE_URL}\", \"image_name\": \"${a_image_name}\", \"tags\": $(cat TAG_MANIFEST | jq -R . | jq -s . | jq 'map(select(length > 0))' | jq -c .)}"
        echo curl -v -H "Content-Type: application/json" -d "${json_data}" "${WEBHOOK_URL}"
        curl -v -H "Content-Type: application/json" -d "${json_data}" "${WEBHOOK_URL}"
    fi
}

kitmaker_webhook_failed() {
    if [ ! -z $KITMAKER ] && [ ! -z $TRIGGER ]; then
        export json_data="{\"status\": \"failed\", \"gitlab_pipeline_url\": \"${CI_PIPELINE_URL}\"}"
        echo curl -v -H "Content-Type: application/json" -d "${json_data}" ${WEBHOOK_URL}
        curl -v -H "Content-Type: application/json" -d "${json_data}" ${WEBHOOK_URL}
    fi
}
