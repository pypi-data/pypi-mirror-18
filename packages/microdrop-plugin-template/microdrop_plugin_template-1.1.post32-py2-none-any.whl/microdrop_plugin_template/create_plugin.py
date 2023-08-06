from argparse import ArgumentParser
import fnmatch
import pkg_resources
import re
import sys
import tempfile as tmp

import git
import path_helpers as ph
import rename_package_files as rp


CRE_PLUGIN_NAME = re.compile(r'^[A-Za-z_][\w_]+$')



def create_plugin(output_directory, overwrite=False, init_git=True):
    '''
    Parameters
    ----------
    output_directory : str
        Output directory path.  Directory name must be a valid Python module
        name.
    overwrite : bool, optional
        Overwrite existing output directory.

    Returns
    -------
    path_helpers.path
        Output directory path.

    Raises
    ------
    ValueError
        If `output_directory` name is not a valid Python module name.
    IOError
        If `output_directory` exists and `overwrite` is ``False``.
    '''
    output_directory = ph.path(output_directory).realpath()
    new_name = output_directory.name
    if not CRE_PLUGIN_NAME.match(new_name):
        raise ValueError('Invalid plugin name, "{}".  Name must be valid '
                         'Python module name.'.format(new_name))

    # TODO Load ignore list from `.templateignore`
    ignore_list = ('*.pyc __init__.py create_plugin.py init_hooks.py rename.py'
                   '*bash.exe.stackdump'.split(' '))

    def collect_package_resource_files(root=''):
        files = []

        for p_i in pkg_resources.resource_listdir('microdrop_plugin_template',
                                                root):
            path_i = ph.path(root).joinpath(p_i)
            if pkg_resources.resource_isdir('microdrop_plugin_template', path_i):
                files.extend(collect_package_resource_files(path_i))
            elif pkg_resources.resource_exists('microdrop_plugin_template',
                                            path_i):
                files.append(path_i)
        return files

    if output_directory.isdir() and not overwrite:
        raise IOError('Output directory already exists.  Use `overwrite=True` '
                      'to overwrite.')

    working_directory = ph.path(tmp.mkdtemp(prefix='create_plugin-'))

    try:
        #  1. Get list of all files in template directory.
        template_files = collect_package_resource_files()
        #  2. Filter template files in *ignore* list.
        filtered_files = [f for f in template_files
                          if not any(fnmatch.fnmatch(f, i)
                          for i in ignore_list)]
        #  3. Copy filtered files to output directory.
        for f in filtered_files:
            resource_filename = \
                ph.path(pkg_resources
                        .resource_filename('microdrop_plugin_template', f))
            target_filename = working_directory / f
            target_filename.parent.makedirs_p()
            resource_filename.copy(target_filename)
        #  4. Rename `__init__.py.template` to `__init__.py`.
        source_file = working_directory / '__init__.py.template'
        target_file = working_directory / '__init__.py'
        source_file.rename(target_file)
        #  5. Rename all occurrences of `microdrop-plugin-template` to new name.
        #         - Do not rename contents of `on_plugin_install.py`, since it
        #           contains an import of `microdrop_plugin_template`.
        rp.rename_package_files(working_directory, 'microdrop-plugin-template',
                                new_name.replace('_', '-'),
                                exclude='*on_plugin_install.py')

        #  6. Initialize version to 0.1 (a version is required by `release.py`)
        #         - If `git` is available, initialize plugin directory as `git`
        #           repository, and tag contents as `v0.1`.
        #         - Otherwise, create `RELEASE-VERSION` file containing "0.1".
        #
        # TODO **N.B.**, File permissions prevent Git repositories from being
        # removed (at least on Windows).  See if this happens on Linux too and
        # report as bug to [`GitPython`][1] developers if it does.
        #
        # [1]: https://github.com/gitpython-developers/GitPython
        version_initialized = False
        if init_git:
            try:
                files = sorted(list(working_directory.walkfiles()))
                repo = git.Repo.init(working_directory)
                repo.index.add(files)
                repo.index.commit('Initial commit')
                tag = 'v0.1'
                repo.git.tag('-a', tag, '-m', 'Initial release')
                repo.git.clear_cache()
                print 'Initialized plugin as git repo (tag={})'.format(tag)
            except Exception, exception:
                print >> sys.stderr, 'Error initializing git repo.'
                print >> sys.stderr, exception
            else:
                version_initialized = True
        if not version_initialized:
            version_path = working_directory.joinpath('RELEASE-VERSION')
            with version_path.open('w') as version_output:
                version_output.write('0.1')
            print 'Wrote version to file: RELEASE-VERSION'

        #  7. Rename created plugin directory to output path.
        if output_directory.isdir():
            output_directory.rmtree()
        working_directory.rename(output_directory)

        return output_directory
    except Exception, exception:
        print exception
        raise
    finally:
        # Clean up working directory if necessary.
        if working_directory.isdir():
            working_directory.rmtree()


def parse_args(args=None):
    '''Parses arguments, returns ``(options, args)``.'''
    from mpm.bin import LOG_PARSER

    if args is None:
        args = sys.argv

    parser = ArgumentParser(description='Create a new Microdrop plugin',
                            parents=[LOG_PARSER])
    parser.add_argument('-f', '--force-overwrite', action='store_true',
                        help='Force overwrite of existing directory')
    parser.add_argument('--no-git', action='store_true',
                        help='Disable git repo initialization')
    parser.add_argument('output_directory', type=ph.path, help='Output '
                        'directory.  Directory name must be a valid Python '
                        'module.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    try:
        output_directory = create_plugin(args.output_directory,
                                         overwrite=args.force_overwrite,
                                         init_git=not args.no_git)
    except IOError, exception:
        print >> sys.stderr, 'Output directory exists.  Use `-f` to overwrite'
        raise SystemExit(-5)
    except ValueError, exception:
        print >> sys.stderr, exception
        raise SystemExit(-10)
    else:
        print 'Wrote plugin to: {}'.format(output_directory)
