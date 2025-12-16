# Notes for Developers

## Setup your local machine
We assume you have a local copy of the git repository obtained as described in the [Installation guide](../installation_docs/index_installation.md)
<!-- Here you will find information pertaining to you being able to develop/test new features on your local machine. We assume you have the Ubuntu Linux distribution with version 22.04 or higher.

- If not already installed, install the Git versioning tool via `apt install -y git-all`.
- Choose an appropriate directory for the repository and navigate to it via the `cd` command.
- Download the git repository to your local storage via `git clone https://code.it4i.cz/kra568/ai-surrogate-modelling.git`.
- Navigate to the newly created directory via `cd ai-surrogate-modelling`.
- Setup your environment by calling the installation script via `sudo ./install/install.sh`
- To update the Python packages required by the software in the virtual Python environment, call `./install/install_python.sh` (this script is also called from the command above)
- Now you should be able to develop new features and test them on your local machine. Follow the guidelines below to help you with starting out. -->



## Git Guidelines
We will aim to follow the approach to git development described nicely in [this blog post](https://jeffkreeftmeijer.com/git-flow/).

- Intialize the Git flow wrapper via the `git flow init` command.

    - use `master` branch for production release.
    - use `development` as a future release branch.
    - use `feature/` as Feature branches prefix.
    - use `release/` as Release branches prefix.
    - use `hotfix/` as Hotfix branches prefix.
    - use `support/` as Support branches prefix.
    - use `bugfix/` as Bugfix branches prefix.
    - use nothing for version prefix.

Afterwards, try to follow the suggestions below, in case of any issues or suggestions, contact [Michal Kravčenko](mailto:michal.kravcenko@vsb.cz).

### General Structure of the repo
- The production code is in the branch `master`, this branch contains the latest version of whatever code is available to the users.
- The development is contained in the branch `development`.

### Feature Development
Feature branches are designed for development of new functionalities.

- When the developer wants to work on a feature titled `feature_x`, they should perform the following commands:
    - `git flow feature start feature_x` (initializes the appropriate local branch and switches the developer to it).
    - Then continue developing the feature, add changes via the `git add ...` command, commit the changes via the `git commit -m 'commit message'` command. The commit message should contain a brief description of the changes being commited and, if available, link to an issue in the repository via the `#N` command (where `N` is the number of the issue).
    - Call `git flow feature publish` to push your feature to the remote repository.
    - Once the feature is ready to be pushed to the development branch, call `git flow feature finish`. This switches the developer to the `development` branch and updates its content with that of the branch `feature/feature_x`. The branch `feature/feature_x` is then deleted.
    - Call `git push` to push the updated development branch to the remote repository.
- When the developer wants to work on another feature `feature_y` developed by someone else, call the `git flow feature pull origin feature_y` command.

### Hotfix Development
Hotfixes are urgent bug fixes, the bugs should be pushed to the production branch and development branches as soon as possible.

- When working on a hotfix with version `VERSION`, they should perform the following commands:
    - `git flow hotfix start VERSION` (initializes the appropriate local branch asn switches the developer to it).
    - Then continue developing the hotfix, add changes via the `git add ...` command, commit the changes via the `git commit -m 'commit message'` command.
    - Once the hotfix is ready to be pushed to the development branch, call `git flow hotfix finish VERSION`. This switches the developer to the `development` branch and updates its content with that of the branch `hotfix/VERSION`. The hotfix is also merged to the `master` branch, which is also tagged with the version change caused by the hotfix. The branch `hotfix/VERSION` is then deleted.

### Making a new Release
Release branch is designed for preparation of a new production release.
Hotfixes are urgent bug fixes, the bugs should be pushed to the production branch and development branches as soon as possible.

- To create a new release branch for version `VERSION`, call the `git flow release start RELEASE` command.
- Allow other developers to push changes to the release branch via the `git flow release publish RELEASE` command.
- To finish the relase of a new version (big deal!), call the `git flow release finish RELEASE` command.
- Push the appropriate versioning via the `git push origin --tags` command.

## Code Quality
Developers can call `./install/code_check.sh` script to automatically improve and analyze the quality of the produced code.