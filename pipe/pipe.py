import requests
from bitbucket_pipes_toolkit import Pipe

schema = {
    'SLACK_WEBHOOK_URL': {'type': 'string', 'required': True},
    'DEBUG': {'type': 'boolean', 'required': False, 'default': False}
}


class SlackNotificationPipe(Pipe):

    def run(self):
        super().run()

        uuid = self.env.get('BITBUCKET_STEP_TRIGGERER_UUID')
        user_name = requests.get(f"https://api.bitbucket.org/2.0/users/{uuid}").json()['display_name']
        title = f"{self.env.get('BITBUCKET_REPO_FULL_NAME')} - {self.env.get('BITBUCKET_DEPLOYMENT_ENVIRONMENT')} - {user_name}"

        if self.env.get('BITBUCKET_EXIT_CODE'):
            status_color = "#ff6961"
            title = f"Failed - {title}"
        else:
            status_color = "#00bb00"
            title = f"Deployed - {title}"

        payload = {
            "text": title,
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": title
                    }
                },
                {
                    "type": "divider"
                }
            ],
            "attachments": [
                {
                    "color": status_color,
                    "blocks": [
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Project:*\n{self.env.get('BITBUCKET_REPO_FULL_NAME')}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Branch:*\n{self.env.get('BITBUCKET_BRANCH')}"},
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Deployed by:*\n{user_name}"},
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Pipeline Link:*\n"
                                            f"<{self.env.get('BITBUCKET_GIT_HTTP_ORIGIN')}/addon/pipelines/home#!/results/{self.env.get('BITBUCKET_BUILD_NUMBER')}|View>"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        requests.post(self.get_variable('SLACK_WEBHOOK_URL'), json=payload)


if __name__ == '__main__':
    pipe = SlackNotificationPipe(schema=schema)
    pipe.run()
