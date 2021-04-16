#!/usr/bin/env bash

set -e

BITBUCKET_TRIGGERER_USERNAME=$(curl -X GET -g "https://api.bitbucket.org/2.0/users/${BITBUCKET_STEP_TRIGGERER_UUID}" | jq -r ".display_name")

curl -X POST -H 'Content-type: application/json' --data "{\"fallback\": \"Deployed - $BITBUCKET_REPO_FULL_NAME - $BITBUCKET_DEPLOYMENT_ENVIRONMENT - $BITBUCKET_TRIGGERER_USERNAME\", \"attachments\": [{\"color\": \"#00bb00\", \"blocks\": [{\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"Deployed - $BITBUCKET_REPO_FULL_NAME successful\"}}, {\"type\": \"section\", \"fields\": [{\"type\": \"mrkdwn\", \"text\": \"*Project:*\\n$BITBUCKET_REPO_FULL_NAME\"}, {\"type\": \"mrkdwn\", \"text\": \"*Branch:*\\n$BITBUCKET_BRANCH\"}, {\"type\": \"mrkdwn\", \"text\": \"*Deployed by:*\\n$BITBUCKET_TRIGGERER_USERNAME\"}, {\"type\": \"mrkdwn\", \"text\": \"*pipeline-link:*\\n<$BITBUCKET_GIT_HTTP_ORIGIN/addon/pipelines/home#!/results/$BITBUCKET_BUILD_NUMBER|View>\"}]}]}]}" $SLACK_WEBHOOK_URL
