#!/usr/bin/env zsh


cwd=`dirname "${0}"`
cd ${cwd}
curl https://raw.githubusercontent.com/Shougo/dein.vim/master/bin/installer.sh > installer.sh
sh ./installer.sh ~/.config/nvim
mkdir -p ~/.config/nvim
echo 'XDG_BASE_HOME=${HOME}:./config' >> ~/.zshrc
source ~/.zshrc
sed -e "s@<HOME>@${HOME}@g" init.vim > ~/.config/nvim/init.vim
cp ./dein.toml ~/.config/nvim/
cp ./dein_lazy.toml ~/.config/nvim/
