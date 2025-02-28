#! /usr/bin/env bash

# Install fish terminal
sudo apt update -y
sudo apt-get install fish -y

# Repo Initialization
git config --global --add safe.directory /workspaces/expressly

# Install Dependencies
pip install crewai