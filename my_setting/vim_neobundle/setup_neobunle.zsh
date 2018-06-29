#!/usr/bin/env zsh

mkdir -p ~/.vim/bundle
# NeoBundleをリポジトリから取得
git clone git://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim
mkdir -p ~/.vim/after/ftplugin/
cwd=`dirname ${0}`
cp ${cwd}/fortran.vim ~/.vim/after/ftplugin/
