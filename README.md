cscope.nvim
===========

CScope for nvim is a minimalistic neovim cscope wrapper.
It supports project files and will create the cscope files
inside of subfolders, depending on the given project name.

## Installation

**Note:** cscope.nvim requires Neovim with python enabled.

1. Extract the files and put them in your Neovim directory
   ('$XDG_CONFIG_HOME/nvim/rplugin/python/').
2. Inside nvim run ':UpdateRemotePlugins' and restart nvim

For vim-plug
```
Plug 'mfulz/cscope.nvim'
```

## Configuration

```vim
" Path to store the cscope files (cscope.files and cscope.out)
" Defaults to '~/.cscope'
let g:cscope_dir = '~/.nvim-cscope'

" Map the default keys on startup
" These keys are prefixed by CTRL+\ <cscope param>
" A.e.: CTRL+\ d for goto definition of word under cursor
" Defaults to off
let g:cscope_map_keys = 1

" Update the cscope files on startup of cscope.
" Defaults to off
let g:cscope_update_on_start = 1
```

## Usage

CScopeStart <file>

This function will start cscope for nvim. If no file is provided as argument
it will try to open cscope.cfg inside the actual directory or fail.


CScopeMapKeys

This function will map all cscope functions to useful keys:

```vim
nmap <unique> <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-\>g :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-\>t :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-\>e :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-\>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
nmap <unique> <C-\>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap <unique> <C-\>d :cs find d <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space>s :scs find s <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space>g :scs find g <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space>c :scs find c <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space>t :scs find t <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space>e :scs find e <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space>f :scs find f <C-R>=expand("<cfile>")<CR><CR>
nmap <unique> <C-Space>i :scs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap <unique> <C-Space>d :scs find d <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space><C-Space>s :vert scs find s <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space><C-Space>g :vert scs find g <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space><C-Space>c :vert scs find c <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space><C-Space>t :vert scs find t <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space><C-Space>e :vert scs find e <C-R>=expand("<cword>")<CR><CR>
nmap <unique> <C-Space><C-Space>f :vert scs find f <C-R>=expand("<cfile>")<CR><CR>
nmap <unique> <C-Space><C-Space>i :vert scs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap <unique> <C-Space><C-Space>d :vert scs find d <C-R>=expand("<cword>")<CR><CR>
```


CScopeUpdate

This function will update all the cscope files and the connection.


## Configuration File

This configuration file has to be under the actual directory where nvim
is started as cscope.cfg or can be provided to CScopeStart as parameter.

```bash
# Project name will be created as subdir under cscope directory
name = Example

# Project path. The path to the project root.
# Where find will start searching the files.
path = ~/Projects/cscope.nvim

# file patterns to scan
files = *.h,*.c,*.hh,*.cc
```
