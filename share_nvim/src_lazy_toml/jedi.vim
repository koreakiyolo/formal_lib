let g:deoplete#enable_at_startup = 1
        let g:jedi#auto_initialization = 1
        let g:jedi#auto_vim_configuration = 1
          nnoremap [jedi] <Nop>
          xnoremap [jedi] <Nop>
          nmap <Leader>j [jedi]
          xmap <Leader>j [jedi]

     let g:jedi#goto_assignments_command = "<C-g>"
     let g:jedi#goto_definitions_command = "<C-d>"  
         let g:jedi#documentation_command = "<C-k>"     
    let g:jedi#rename_command = "[jedi]r"
        let g:jedi#usages_command = "[jedi]n"
        let g:jedi#popup_select_first = 0
        let g:jedi#popup_on_dot = 0
        let g:jedi#show_call_signatures = 1
        
        autocmd FileType python setlocal completeopt-=preview

