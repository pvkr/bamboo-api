import requests

BAMBOO_URL = 'http://localhost:8085'
AUTH = ('admin', 'admin')


def create_project(name, key, desc=""):
    """Creates project.
    REST API doesn't have API to create project, this solution is based on current behaviour of Bamboo
    project create page"""
    try:
        response = requests.post(
            url="{}/project/saveNewProject.action".format(BAMBOO_URL),
            headers={"Content-Type": "application/x-www-form-urlencoded", "X-Atlassian-Token": "no-check"},
            auth=AUTH,
            data={"projectName": name,
                  "projectKey": key,
                  "projectDescription": desc,
                  "checkBoxFields": "projectAccessPublic",
                  "projectAccessPublic": "true"},
        )
        print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(content=response.content))

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def run():
    # create_project("Qwerty2", "QW2")
    pass


if __name__ == "__main__":
    run()
