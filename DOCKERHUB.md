# How to setup a MAX model repository on Docker Hub

## Prerequisites

Before adding a repository to [Docker Hub](https://hub.docker.com) you will need to meet the following requirements:

- Be a member of the [codait organization](https://hub.docker.com/u/codait/) on Docker Hub
- Have write access to the repository on GitHub
- Choose `Public and Private` access when linking your GitHub and Docker Hub accounts

## Adding the repository to Docker Hub

> Note: Only MAX repositories with a Dockerfile should to be added to Docker Hub

1. Select `Create Automated Build` from the `Create` dropdown menu in the upper right corner of [Docker Hub](https://hub.docker.com)

2. Select `Create Auto-build Github` option

3. Select `IBM` in the `Users/Organizations` list

4. Find and select the repository using the `Type to filter` feature to search

5. Fill out the `Create Automated Build` form

    1. Choose `codait` in the `Namespace` dropdown (not your username)

    2. Leave the `Name` and `Visibility` fields to the defaults (should be the GitHub repository name and `public` respectively)

    3. Fill in the `Description` field with the following:
       
       ```
       IBM Code Model Asset Exchange - <Model Name>
       ```
       
6. Click `Create`

## Triggering the initial build

An initial build of the docker image is **NOT** triggered on creation.

There are two ways to trigger a build:

1. Push a commit to `master` on the GitHub repository

2. Trigger the build manually by following the steps below

### Manually triggering a build on Docker Hub

1. In the repository on Docker Hub go to the `Build Settings` tab

2. Click the `Activate Trigger` button in the `Build Triggers` section

3. Copy the `Trigger URL` that appears and run the following in a terminal:

   ```
   curl -X POST <Trigger URL>
   ```

4. Refresh the web page and check that a build was triggered in the `Last 10 Trigger Logs` table.

5. Click the `Deactivate Trigger` button since you will not need to manually trigger a build again.

6. Once the build finishes the `Full Description` section in the `Repo Info` tab will populate with the GitHub repository README content
