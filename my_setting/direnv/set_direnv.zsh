#!/usr/bin/env zsh
mkdir ~/.go
echo "export GOPATH=${HOME}/.go"
sudo apt-get install go-lang
go get github.com/direnv/direnv
echo "export EDITOR=/usr/bin/vim" >> ~/.zshrc
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc
