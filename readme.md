# Project Setup Guide

This guide will walk you through setting up and running a Python project with a virtual environment (`venv`). The project includes a GitLab CI/CD configuration, a main Python script (`main.py`), and several modules.

## Table of Contents

- [1. Prerequisites](#1-prerequisites)
- [2. Clone the Repository](#2-clone-the-repository)
- [3. Create a Virtual Environment](#3-create-a-virtual-environment)
- [4. Install Project Dependencies](#4-install-project-dependencies)
- [5. Configure Authentication](#5-configure-authentication)
- [6. Run the Project](#6-run-the-project)
- [7. GitLab CI/CD Configuration](#7-gitlab-cicd-configuration)

## 1. Prerequisites

- [Python](https://www.python.org/) (version 3.11 recommended)
- [Git](https://git-scm.com/)

## 2. Clone the Repository

Open a terminal and run the following command to clone the project repository:

```bash
git clone <repository_url>
cd <project_directory>
```

Replace `<repository_url>` with the actual URL of your GitLab repository.

## 3. Create a Virtual Environment

Navigate to the project directory in the terminal and run the following commands to create a virtual environment:

```bash
# On Unix or MacOS
python3.11 -m venv .venv

# On Windows
python -m venv .venv
```

This will create a virtual environment named `.venv` in your project directory.

## 4. Install Project Dependencies

Activate the virtual environment and install the project dependencies using the following commands:

```bash
# On Unix or MacOS
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate
```

Now, install the dependencies:

```bash
pip install -r requirements.txt
```

This will install all the required Python packages for the project.

## 5. Configure Authentication

To run the project, you may need to configure authentication. Update the `private_key/privateKey.pem` file with your Stark Bank private key.
https://starkbank.com/faq/how-to-create-ecdsa-keys

## 6. Run the Project

Run the main script using the following command:

```bash
python main.py
```

You can pass additional arguments, such as `--function generate_all_day_report`, to execute specific functions.

## 7. GitLab CI/CD Configuration

The project includes a GitLab CI/CD configuration file (`.gitlab-ci.yml`). This file defines two jobs: `job_daily` and `create_pix_every_3h`. The jobs are scheduled to run at different intervals and stages.