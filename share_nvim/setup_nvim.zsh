#!/usr/bin/env zsh


cwd=`dirname "${0}"`
cd ${cwd}
mkdir -p ~/.config/nvim
echo 'XDG_BASE_HOME=${HOME}:./config' >> ~/.zshrc
source ~/.zshrc
cp ./init.vim ~/.config/nvim/
