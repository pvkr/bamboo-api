# Bamboo REST API
Bamboo REST API examples

## Start Bamboo Server, Option 1 (requires license)
```bash
$ docker volume create --name bambooVolume
$ docker run -v bambooVolume:/var/atlassian/application-data/bamboo --name="bamboo" --init -d -p 54663:54663 -p 8085:8085 atlassian/bamboo-server
```
Bamboo is now available on <http://localhost:8085>. 
Generate evaluation license by the link on bottom of welcome page.

*Note: evaluation license is available during 90 days*

#### Add Bamboo Agent on the same host (Optional)
1. Run Bamboo Server
    ```bash
    $ docker network create bamboo
    $ docker volume create --name bambooVolume
    $ docker run -v bambooVolume:/var/atlassian/application-data/bamboo --name bamboo-server --network bamboo --hostname bamboo-server --init -d -p 8085:8085 atlassian/bamboo-server
    ```
2. Build custom agent image (e.g. with Maven and Git)
    ```bash
    docker build -t bamboo-agent-mvn-git .
    ```
3. Run Bamboo agent with custom image (or just use base image atlassian/bamboo-agent-base)
    ```bash
    $ docker volume create --name bambooVolume
    $ docker run -v bambooAgentVolume:/home/bamboo/bamboo-agent-home --name bamboo-agent --network bamboo --hostname bamboo-agent --init -d bamboo-agent-mvn-git http://bamboo-server:8085
    ``` 
4. Accept/Approve agent registration (On Settings->Agents->Remote Agents->Agent authentication)

## Start Bamboo Server, Option 2 (doesn't require license)
1) Download atlassian sdk -  [Win](https://developer.atlassian.com/server/framework/atlassian-sdk/install-the-atlassian-sdk-on-a-windows-system/) or [Mac](https://developer.atlassian.com/server/framework/atlassian-sdk/install-the-atlassian-sdk-on-a-linux-or-mac-system/)
2) Install (requires Java8)
3) Run from console ``atlas-run-standalone --product bamboo --port 8085``

## Prepare Python env
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Run Python (supports project creation)
```bash
python bamboo.py
```

# Run Bamboo Java Spec (creates Project/Plan, configures plan permissions)
1) Run by Maven
    ```bash
    cd bamboo-specs
    mvn -Ppublish-specs
    ```
2) Run by Java
    ```bash
    cd bamboo-specs
    mvn package -Pfat-jar
    java -cp target/bamboo-specs-1.0.0-SNAPSHOT-jar-with-dependencies.jar tutorial.PlanSpec
    ```

## See Also
* [Bamboo Server Docker image](https://hub.docker.com/r/atlassian/bamboo-server)
* [Bamboo Agent Docker image](https://hub.docker.com/r/atlassian/bamboo-agent-base)
* [Bamboo REST API](https://docs.atlassian.com/atlassian-bamboo/REST/6.2.5/)
