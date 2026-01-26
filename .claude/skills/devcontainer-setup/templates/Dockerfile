FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm
# Remove expired yarn GPG key repo before features run apt-get update
RUN rm -f /etc/apt/sources.list.d/yarn.list
