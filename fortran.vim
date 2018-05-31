" \file fortran.vim
if exists("b:did_ftplugin_fortran") | finish | endif
let b:did_ftplugin_fortran = 1

"" 新規作成時の構文ハイライトに固定形式か自由形式のどちらを使うかの判定
let s:ext = expand("%:e")
if s:ext !=? "f" && s:ext !=? "for"
  let b:fortran_free_source=1
  let b:fortran_fixed_source=0
endif

let fortran_more_precise=1 " より高精度な構文ハイライト。時間がかかる
" let b:fortran_have_tabs=1 " プログラム内でタブ文字を使う

"" 折りたたみ設定
let b:fortran_fold=1 " プログラム、サブルーチン、関数などで折りたたみを定義
let b:fortran_fold_conditionals=1 " doループ、ifブロックなどで折りたたみを定義
let b:fortran_fold_multilinecomments=1 " 3行以上のコメントに折りたたみを定義

"" インデント設定
let b:fortran_do_enddo=1 " do-endoブロックをインデント
let b:fortran_indent_less=1 " プログラム単位でのインデントを無効化
