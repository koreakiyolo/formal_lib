#!/usr/bin/env zsh
mkdir ~/.go
echo "export GOPATH=${HOME}/.go" >> ~/.zshrc
sudo apt-get install golang
go get github.com/direnv/direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc
