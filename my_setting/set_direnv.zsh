#!/usr/bin/env zsh

git clone git://github.com/yyuu/pyenv.git ~/.pyenv
git clone https://github.com/yyuu/pyenv-pip-rehash.git ~/.pyenv/plugins/pyenv-pip-rehash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

echo "export EDITOR=/usr/bin/vim" >> ~/.zshrc
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
