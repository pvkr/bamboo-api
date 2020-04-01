import requests
from lxml import html

BAMBOO_URL = 'http://localhost:8085'
AUTH = ('admin', 'admin')

PROJ_KEY="QW" # You can't change project key, because it is hardcoded in yaml spec file in git repo
GIT_REPO = "https://github.com/pvkr/bamboo-api.git"

LINKED_REPO_FORM_DATA = {
    "repositoryId": "0",
    "selectedRepository": "com.atlassian.bamboo.plugins.atlassian-bamboo-plugin-git:gitv2",
    "repository.git.repositoryUrl": GIT_REPO,
    "repository.git.authenticationType": "NONE",
}
ADD_SPEC_REPO_FORM = {
    "projectTypeOption": "BUILD",
    "repositoryTypeOption": "LINKED",
    "linkedRepositoryAccessOption": "ALL_USERS"
}


def create_project(*, proj_name, proj_key, proj_desc=""):
    """Creates project.
    REST API doesn't have API to create project, this solution is based on current behaviour of Bamboo
    project create page"""
    try:
        response = requests.post(
            url="{}/project/saveNewProject.action".format(BAMBOO_URL),
            headers={"Content-Type": "application/x-www-form-urlencoded", "X-Atlassian-Token": "no-check"},
            auth=AUTH,
            data={"projectName": proj_name,
                  "projectKey": proj_key,
                  "projectDescription": proj_desc,
                  "checkBoxFields": "projectAccessPublic",
                  "projectAccessPublic": "true"},
        )
        print('create_project Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def add_linked_repo(*, repo_name):
    """Add spec .
    REST API doesn't have API to create plan, this solution is based on current behaviour of Bamboo
    add spec page"""
    try:
        response = requests.post(
            url="{}/admin/createLinkedRepository.action".format(BAMBOO_URL),
            headers={"Content-Type": "application/x-www-form-urlencoded", "X-Atlassian-Token": "no-check"},
            auth=AUTH,
            data={**LINKED_REPO_FORM_DATA, "repositoryName": repo_name},
        )
        print('add_linked_repo Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# I found only one way to get id - parse html
def get_linked_repo_id(*, repo_name):
    # <div id="repository-selector-linked">
    try:
        response = requests.get(url="{}/build/admin/create/newSpecs.action".format(BAMBOO_URL),
                                auth=AUTH)
        dom = html.fromstring(response.content)
        val = dom.xpath('//div[@id="repository-selector-linked"]/select/option[@data-repo-name="{}"]/@value'
                        .format(repo_name))[0:]+[None]

        print("get repo_id = {}".format(val[0]))
        return val[0]
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return None


def add_spec(*, proj_key, repo_id):
    """Add spec .
    REST API doesn't have API to create plan, this solution is based on current behaviour of Bamboo
    add spec page"""
    try:
        response = requests.post(
            url="{}/build/admin/create/createSpecs.action".format(BAMBOO_URL),
            headers={"Content-Type": "application/x-www-form-urlencoded", "X-Atlassian-Token": "no-check"},
            auth=AUTH,
            data={**ADD_SPEC_REPO_FORM, "selectProjectKey": proj_key, "selectedRepository": repo_id}
        )
        print('add_spec HTTP Status Code: {status_code}'.format(status_code=response.status_code))

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def run():
    create_project(proj_name="Qwerty", proj_key=PROJ_KEY)
    add_linked_repo(repo_name="bamboo-api")
    repo_id = get_linked_repo_id(repo_name="bamboo-api")
    add_spec(proj_key=PROJ_KEY, repo_id=repo_id)


if __name__ == "__main__":
    run()
