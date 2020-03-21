import neovim
import os
import sys
import subprocess
import configparser
from io import StringIO


@neovim.plugin
class CScope(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self._keys_mapped = False

    def __parse_config(self):
        self.config = dict()

        config = configparser.ConfigParser()
        with open(self.project_conf) as stream:
            stream = StringIO("[root]\n" + stream.read())
            config.readfp(stream)

        try:
            self.config['project_name'] = config.get('root', 'name')
            self.config['project_path'] = os.path.expanduser(
                config.get('root', 'path'))
            self.config['file_types'] = config.get('root', 'files').split(',')
            self.config['project_libs'] = [
                os.path.expanduser(l)
                for l in config.get('root', 'libs', fallback='').split('\n')
                if l != '' ]
        except configparser.NoOptionError as e:
            return (
                False,
                "Error parsing file: '{0}': {1}".format(
                    self.project_conf,
                    str(e)))

        if not os.path.isdir(self.config['project_path']):
            return (
                False, "Project path: '{0}' does not exist".format(
                    self.config['project_path']))
        return (True, '')

    def __create_cscope_dir(self):
        try:
            if not os.path.isdir(self.cscope_dir):
                os.mkdir(self.cscope_dir, 0o755)
            if not os.path.isdir(
                os.path.join(
                    self.cscope_dir,
                    self.config['project_name'])):
                os.mkdir(
                    os.path.join(
                        self.cscope_dir,
                        self.config['project_name']),
                    0o755)
        except OSError as e:
            return(False, "Couldn't setup cscope directory: '{0}'".format(str(e)))
        return (True, '')

    def __gen_cscope_files(self):
        self.cmd_cscope_files = None
        if self.cscope_ready:
            cmd = ['find']
            for lib_path in self.config['project_libs']:
                cmd.append(lib_path)
            first = True
            for file_type in self.config['file_types']:
                if first:
                    cmd.append(self.config['project_path'])
                    first = False
                else:
                    cmd.append('-o')
                cmd.append('-name')
                cmd.append(file_type)
            self.cmd_cscope_files = cmd

    def __update_cscope_files(self):
        if self.cmd_cscope_files:
            self.nvim.vars['cscope_debug'] = self.cmd_cscope_files
            try:
                with open(os.path.join(self.cscope_dir, self.config['project_name'], 'cscope.files'), 'w+') as cscope_files:
                    subprocess.call(self.cmd_cscope_files, stdout=cscope_files)
            except (IOError, subprocess.CalledProcessError) as e:
                return(False, "Couldn't setup cscope.files: '{0}'".format(str(e)))
            return(True, '')
        return(False, "Couldn't setup cscope.files: Command not ready")

    def __update_cscope_out(self):
        cscope_files = os.path.join(
            self.cscope_dir,
            self.config['project_name'],
            'cscope.files')
        cscope_out = os.path.join(
            self.cscope_dir,
            self.config['project_name'],
            'cscope.out')
        if os.path.isfile(cscope_files):
            try:
                subprocess.call(['cscope', '-q', '-R', '-b',
                                 '-i', cscope_files, '-f', cscope_out])
            except subprocess.CalledProcessError as e:
                return(False, "Couldn't setup cscope.out: '{0}'".format(str(e)))
            return(True, '')
        return(False, "Couldn't setup cscope.out: 'cscope.files' not ready")

    def __init_cscope(self):
        cscope_out = os.path.join(
            self.cscope_dir,
            self.config['project_name'],
            'cscope.out')
        if os.path.isfile(cscope_out):
            if self.cscope_connection_ready:
                self.nvim.command('cscope reset')
            else:
                self.nvim.command('cscope add {0}'.format(cscope_out))
                self.cscope_connection_ready = True

    @neovim.command('CScopeMapKeys', range='', nargs='*', sync=False)
    def cscope_map_keys_handler(self, args, range):
        if self._keys_mapped:
            return

        self.nvim.command(
            'nmap <unique> <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-\>g :cs find g <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-\>t :cs find t <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-\>e :cs find e <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-\>f :cs find f <C-R>=expand("<cfile>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-\>i :cs find i ^<C-R>=expand("<cfile>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-\>d :cs find d <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space>s :scs find s <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space>g :scs find g <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space>c :scs find c <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space>t :scs find t <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space>e :scs find e <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space>f :scs find f <C-R>=expand("<cfile>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space>i :scs find i ^<C-R>=expand("<cfile>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space>d :scs find d <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space><C-Space>s :vert scs find s <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space><C-Space>g :vert scs find g <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space><C-Space>c :vert scs find c <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space><C-Space>t :vert scs find t <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space><C-Space>e :vert scs find e <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space><C-Space>f :vert scs find f <C-R>=expand("<cfile>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space><C-Space>i :vert scs find i ^<C-R>=expand("<cfile>")<CR><CR>')
        self.nvim.command(
            'nmap <unique> <C-Space><C-Space>d :vert scs find d <C-R>=expand("<cword>")<CR><CR>')
        self.nvim.command(
            'imap <C-@> <C-Space>')
        self._keys_mapped = True

    @neovim.command('CScopeUpdate', range='', nargs='*', sync=False)
    def cscope_update_files_handler(self, args, range):
        check = self.__update_cscope_files()
        if not check[0]:
            self.nvim.command(
                'echo "Couldn\'t update cscope.files: {0}"'.format(
                    check[1]))

        check = self.__update_cscope_out()
        if not check[0]:
            self.nvim.command(
                'echo "Couldn\'t update cscope.out: {0}"'.format(
                    check[1]))
        self.__init_cscope()

    @neovim.command('CScopeStart', range='', nargs='*', sync=True)
    def cscope_start_handler(self, args, range):
        self.cscope_ready = False
        self.cscope_connection_ready = False

        # setup cscope base dir
        if 'cscope_dir' not in self.nvim.vars:
            self.nvim.vars['cscope_dir'] = '~/.cscope'
        self.cscope_dir = os.path.expanduser(self.nvim.vars['cscope_dir'])

        # get default configuration name
        if 'cscope_config' not in self.nvim.vars:
            self.nvim.vars['cscope_config'] = 'cscope.cfg'

        # setup project configuration
        if len(args) == 1:
            if os.path.isfile(args[0]):
                self.project_conf = os.path.expanduser(args[0])
            else:
                self.nvim.command(
                    'echo "Couldn\'t start CScope: \'{0}\' does not exist."'.format(
                        args[0]))
                return
        else:
            if os.path.isfile(
                os.path.join(
                    os.getcwd(),
                    self.nvim.vars['cscope_config'])):
                self.project_conf = os.path.join(
                    os.getcwd(), self.nvim.vars['cscope_config'])
            else:
                self.nvim.command(
                    'echo "Couldn\'t start CScope: \'{0}\' does not exist."'.format(
                        self.nvim.vars['cscope_config']))
                return

        check = self.__parse_config()
        if not check[0]:
            self.nvim.command(
                'echo "Couldn\'t start CScope: {0}"'.format(
                    check[1]))
            return

        # create directories for project
        check = self.__create_cscope_dir()
        if not check[0]:
            self.nvim.command(
                'echo "Couldn\'t start CScope: {0}"'.format(
                    check[1]))
            return

        # cscope is ready to process files
        self.cscope_ready = True

        # generate cscope file
        self.__gen_cscope_files()

        # initial update
        if 'cscope_update_on_start' in self.nvim.vars:
            self.nvim.command('CScopeUpdate')

        # key mapping
        if 'cscope_map_keys' in self.nvim.vars:
            self.nvim.command('CScopeMapKeys')
