#!/usr/bin/env zsh

git clone https://github.com/yyuu/pyenv.git ~/.pyenv
git clone https://github.com/yyuu/pyenv-pip-rehash.git ~/.pyenv/plugins/pyenv-pip-rehash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
# pyenv-virtualenvのインストール。
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
# .xxxrcに初期設定を追記する
# 何故evalを使っているのか、オプションの`-`ってなんだ、と疑問に思ったのでスタックオーバーフローで質問してみました。
#  http://ja.stackoverflow.com/questions/32043/xxxenv-の初期化時のeval-xxxenv-init-の意味
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
