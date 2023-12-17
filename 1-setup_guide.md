# Python & Visual Studio Code Installation Guide 🛠

Embark on your Python programming journey with this comprehensive installation guide! By the end, you'll have Python, Visual Studio Code, and all the necessary extensions for Jupyter set up, along with an environment tailored for this course.

Bear in mind that whilst you can use these notebooks in Google Colab, you will still need to load the environment in order to run the Streamlit chatbots.

## Table of Contents
- [Installing Python](#installing-python)
    - [Windows](#windows)
    - [Mac](#mac)
- [Installing Visual Studio Code](#installing-visual-studio-code)
- [Installing GIT](#instaling-git)
- [Setting Up Jupyter in VS Code](#setting-up-jupyter-in-vs-code)
- [Setting up the Python and Jupyter Environment](#setting-up-the-python-and-jupyter-environment)
- [Setting Up Credentials 🗝️](#Setting-Up-Credentials-🗝️)

## Installing Python 3.10

### Windows

1. **Download the Installer**:
    - Visit the official [Python Downloads page](https://www.python.org/downloads/).
    - Download 3.10.x using the recommended installer for Windows or use this [Link](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)


2. **Run the Installer**:
    - Launch the installer.
    - **Important**: Check the box that says "Add Python 3.X to PATH" at the bottom.
    - Click on "Install Now".

### Mac

1. **Download the Installer**:
    - Head to the [Python Downloads page](https://www.python.org/downloads/).
    - Choose the MacOS installer for version 3.10 or use this [Link](https://www.python.org/ftp/python/3.10.11/python-3.10.11-macos11.pkg)

    1. **Rust on MAC**: You might have issues with a python module called `tiktoken` complaining about rust. Perform the following:
        - Install homebrew if you dont have it already. Run this command in terminal `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
        - Run this command in terminal `brew install rust`
        - You can continue with deploying your environment or run `pip install -r requirements.txt` to reinstall the python modules.


2. **Run the Installer**:
    - Open the downloaded `.pkg` file and follow the on-screen instructions.

## Installing Visual Studio Code

1. **Download & Install**:
    - Visit the [Visual Studio Code website](https://code.visualstudio.com/).
    - Download the version suitable for your OS (Windows or macOS).
    - Launch the installer and follow the steps.

2. **Launch Visual Studio Code**:
    - Once installed, open Visual Studio Code.

## Instaling Git
- In mac, open a terminal and simply run the command "git version". This will eventually prompt you to install git.
- In windows, try running "git version". If you dont get a response then you can install it on by downloading from this link: [Git for Windows Installer](https://gitforwindows.org/) 


## Setting Up Jupyter in VS Code

1. **Install the Jupyter Extension**:
    - In Visual Studio Code, head to the Extensions view by clicking on the square icon on the sidebar.
    - Search for "Jupyter".
    - Click 'Install' on the relevant result.

2. **(Optional) Install Python Extension**:
    - Similarly, search for the "Python" extension and install it for enhanced Python support in VS Code.



## Setting up the Python and Jupyter Environment

1. **Cloning the environment to your computer**:
   1. Go to the repo at: https://github.com/elabbarw/GenAI_Course/
   2. Click on "Code" and copy the url in there
   3. Go back to VS Code, click on "View", "Command Palette", type "git clone" and you should get the menu option that will allow you to clone. Paste the url in there and press enter.
   4. When asked, please click on "Add to Workspace".
   5. All of the files for the course should show up on the left of the screen.

2. **Configuring and selecting the Kernel**:
    1. Open one of the notebooks.
    2. In the top-right corner of the Jupyter interface within VS Code, you'll see the kernel that's currently being used.
    3. Click on it, and from the dropdown, select the "Python Environments".
    4. Click on "Create Python Environment"
    5. Click Venv
    6. Select the Python Interpreter (In our case Python 3.10.0)
    7. select our requirements.txt file and click on Ok.
    8. Your venv environment will now be created and the required Python modules will be installed.


2. **Awareness**: Always ensure you're in the correct environment (in this case, `venv`) when working on the course materials. This ensures consistency and avoids potential library conflicts.
    - To do this you can always run the following commands to switch the environment:
        Windows
        Run the below under powershell or terminal as admin:
        ```
        Set-ExecutionPolicy RemoteSigned
        ```
        Once that's done you can run the following in VS Code:
        ```
        ./venv/scripts/activate.ps1
        ```
        in Cmd you can run
        ```
        c:\pathtovenv\scripts\activate.bat
        ```
        On *nix/mac you can run this command
        ```
        source ./venv/bin/activate
        ```


# Setting Up Credentials for the chatbot 🗝️

For seamless integration with various services, it's paramount to have all your credentials in one place. We'll use a `.env` file for this purpose, which will store sensitive information securely.

## 1. Creating the `.env` File

In the root of your project directory, create a new file named `.env`. This file will house all your essential credentials. Check out the `.env.demo` file to get an idea on what's required...

## 2. OpenAI Key

After signing up for an account at [OpenAI Platform](https://platform.openai.com/), you can generate your API key. 

Add it to your `.env` file:

- OPENAI_KEY=your_openai_key_here


## 4. Qdrant VectorDB Credentials

Refer to the "Using a Vector Database to provide RAG" notebook for detailed steps. Once you have the key and endpoint, add them to your `.env` file:

VECTORDB_ENDPOINT=your_qdrant_endpoint_here
VECTORDB_KEY=your_qdrant_api_key_here


## 🚫 **Important**: Always keep your `.env` file private. Never push or share this file to prevent potential misuse of your credentials.

---

With your credentials all set up, you're primed to dive deep into the world of Generative AI without any hitches!



---

Happy Coding! 🎉
