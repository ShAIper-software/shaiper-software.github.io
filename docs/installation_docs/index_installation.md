# Downloading the repository

In order to download the git repository, follow these steps:

- If not already installed, install the Git versioning tool via `apt install -y git-all`.
- Choose an appropriate directory for the repository and navigate to it via the `cd` command.
- Download the git repository to your local storage via `git clone https://code.it4i.cz/kra568/ai-surrogate-modelling.git`.
- Navigate to the newly created directory via `cd ai-surrogate-modelling`.
- Setup your environment by calling the installation script via `sudo ./install/install.sh`
- To update the Python packages required by the software in the virtual Python environment, call `./install/install_python.sh` (this script is also called from the command above)

Now you have access to the source codes and can either start [developing](../developer_docs/index_developer.md) or install the package via pip.

# Wheel Installation

You have downloaded the git repository, but do not wish to work on development. For this reason, we include a simple installation script.

Navigate to the project directory and run the command `sudo bash install/install_wheel.sh`. This installs a Python virtual environment `python_venv/.ai-for-surrogate-modelling` in your home directory, constructs the installation files and installs this software to the newly created virtual environment via pip.

Once installed, you can start [experimenting](../user_docs/index_user.md) with the software.


# Uninstall the Wheel
To uninstall this software from the virtual environment, run the following series of commands from the terminal:

```
. $ai_for_surrogate_modelling_path/bin/activate
pip uninstall -y SHAIPER-AI-for-Surrogate-Modelling
```