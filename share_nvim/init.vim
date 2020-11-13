"dein Scripts-----------------------------
if &compatible
  set nocompatible               " Be iMproved
endif


" Required:
set runtimepath+=<HOME>/.config/nvim/repos/github.com/Shougo/dein.vim



" Required:
if dein#load_state('<HOME>/.config/nvim/')
  call dein#begin('<HOME>/.config/nvim')
  let g:rc_dir = expand("~/.config/nvim/")
  let s:toml = g:rc_dir . '/dein.toml'
  let s:lazy_toml = g:rc_dir . '/dein_lazy.toml'

  call dein#load_toml(s:toml, {'lazy': 0})
  call dein#load_toml(s:lazy_toml, {'lazy': 1})



  " Let dein manage dein
  " Required:
  call dein#add('<HOME>/.config/nvim/repos/github.com/Shougo/dein.vim/')

  " Add or remove your plugins here like this:
  call dein#add('Shougo/neosnippet.vim')
  call dein#add('Shougo/neosnippet-snippets')

  " Required:
  call dein#end()
  call dein#save_state()
endif

" Required:
filetype plugin indent on
syntax enable

" If you want to install not installed plugins on startup.
if dein#check_install()
  call dein#install()
endif



let mapleader = "\<space>"
vmap <Leader>y "+y
vmap <Leader>d "+d
nmap <Leader>p "+p
nmap <Leader>P "+P
vmap <Leader>p "+p
vmap <Leader>P "+P
nmap <Leader><Leader> V
vmap v <Plug>(expand_reigion_expand)
vmap <C-v> <Plug>(expand_reigion_expand)
set ignorecase
set smartcase
set wrapscan
set incsearch
set tabstop=4
set shiftwidth=4
set softtabstop=4
set textwidth=78
set expandtab
set smarttab
set autoindent
set shiftround
set inccommand=split
let fortan_free_source=1
let fortran_fold=1
au! BufRead, BufNewFeile *.f90 let b:fortran_do_enddo=1
au FileType python setlocal foldmethod=indent
