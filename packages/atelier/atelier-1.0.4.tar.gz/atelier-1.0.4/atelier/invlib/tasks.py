# -*- coding: UTF-8 -*-
# Copyright 2013-2016 by Luc Saffre & Hamza Khchine.
# License: BSD, see LICENSE for more details.

"""A library for `invoke <http://www.pyinvoke.org/>`__ with tasks we
use for managing our Python projects.

See :doc:`/invlib`

"""

from __future__ import print_function
from __future__ import unicode_literals

import os
from contextlib import contextmanager
import glob
import time
import datetime
from datetime import timedelta

from builtins import str
from builtins import object
from atelier.utils import i2d
from babel.dates import format_date
from atelier import rstgen
from unipath import Path

try:
    from invoke import ctask as task, tasks
    # before version 0.13 (see http://www.pyinvoke.org/changelog.html)
except ImportError:
    from invoke import task, tasks

from invoke.exceptions import Exit
from invoke import run

import atelier
from atelier.utils import confirm

LASTREL_INFO = "Last PyPI release was %(filename)s \
(%(upload_time)s,  %(downloads)d downloads)."

RELEASE_CONFIRM = """
This is going to officially release %(name)s %(version)s to PyPI.
It will fail if version %(version)s of %(name)s has previously been released.
Your `docs/changes.rst` should have a section about this version.
Your working directory should be clean (otherwise answer 'n' and run `inv ci`).
Are you sure?"""


def local(*args, **kwargs):  # probably no longer used
    """Call :func:`invoke.run` with `pty=True
    <http://www.pyinvoke.org/faq.html#why-is-my-command-behaving-differently-under-invoke-versus-being-run-by-hand>`_.

    This is useful e.g. to get colors in a terminal.

    """
    kwargs.update(pty=True)
    # kwargs.update(encoding='utf-8')
    run(*args, **kwargs)


@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)


def get_current_date(today=None):
    """
    """

    if today is None:
        # return datetime.datetime.utcnow()
        return datetime.date.today()
    return i2d(today)


def must_confirm(*args, **kwargs):
    if not confirm(''.join(args)):
        raise Exit("User failed to confirm.")


def must_exist(p):
    if not p.exists():
        raise Exception("No such file: %s" % p.absolute())


def rmtree_after_confirm(p, batch=False):
    if not p.exists():
        return
    if batch or confirm(
                    "OK to remove %s and everything under it?" % p.absolute()):
        p.rmtree()


def cleanup_pyc(p, batch=False):
    """Thanks to oddthinking on http://stackoverflow.com/questions/2528283
    """
    for root, dirs, files in os.walk(p):
        pyc_files = [filename for filename in files if filename.endswith(".pyc")]
        py_files = set([filename for filename in files if filename.endswith(".py")])
        excess_pyc_files = [pyc_filename for pyc_filename in pyc_files if pyc_filename[:-1] not in py_files]
        for excess_pyc_file in excess_pyc_files:
            full_path = os.path.join(root, excess_pyc_file)
            if batch or confirm("Remove excess file %s:" % full_path):
                os.remove(full_path)


def sphinx_clean(ctx, batch=False):
    """Delete all generated Sphinx files.

    """
    for docs_dir in get_doc_trees(ctx):
        rmtree_after_confirm(docs_dir.child(ctx.build_dir_name), batch)


def py_clean(ctx, batch=False):
    """Delete dangling `.pyc` files.

    """
    if atelier.current_project.module is not None:
        p = Path(atelier.current_project.module.__file__).parent
        cleanup_pyc(p, batch)
    p = ctx.root_dir.child('tests')
    if p.exists():
        cleanup_pyc(p, batch)

    files = []
    for pat in ctx.cleanable_files:
        for p in glob.glob(os.path.join(ctx.root_dir, pat)):
            files.append(p)
    if len(files):
        if batch or confirm(
                "Remove {0} cleanable files".format(len(files))):
            for p in files:
                os.remove(p)



def get_doc_trees(ctx):
    for rel_doc_tree in ctx.doc_trees:
        docs_dir = ctx.root_dir.child(rel_doc_tree)
        if not docs_dir.exists():
            msg = "Directory %s does not exist." % docs_dir
            msg += "\nCheck your project's `doc_trees` setting."
            raise Exception(msg)
        yield docs_dir


def sync_docs_data(ctx, docs_dir):
    build_dir = docs_dir.child(ctx.build_dir_name)
    for data in ('dl', 'data'):
        src = docs_dir.child(data).absolute()
        if src.isdir():
            target = build_dir.child('dl')
            target.mkdir()
            cmd = 'cp -ur %s %s' % (src, target.parent)
            ctx.run(cmd, pty=True)
    if False:
        # according to http://mathiasbynens.be/notes/rel-shortcut-icon
        for n in ['favicon.ico']:
            src = docs_dir.child(n).absolute()
            if src.exists():
                target = build_dir.child(n)
                cmd = 'cp %s %s' % (src, target.parent)
                ctx.run(cmd, pty=True)


def sphinx_build(ctx, builder, docs_dir,
                 cmdline_args=[], language=None, build_dir_cmd=None):
    args = ['sphinx-build', '-b', builder]
    args += cmdline_args
    # ~ args += ['-a'] # all files, not only outdated
    # ~ args += ['-P'] # no postmortem
    # ~ args += ['-Q'] # no output
    # build_dir = docs_dir.child(ctx.build_dir_name)
    build_dir = Path(ctx.build_dir_name)
    if language is not None:
        args += ['-D', 'language=' + language]
        # needed in select_lang.html template
        args += ['-A', 'language=' + language]
        if language != ctx.languages[0]:
            build_dir = build_dir.child(language)
            # print 20130726, build_dir
    if ctx.tolerate_sphinx_warnings:
        args += ['-w', 'warnings_%s.txt' % builder]
    else:
        args += ['-W']  # consider warnings as errors
        # args += ['-vvv']  # increase verbosity
    # args += ['-w'+Path(ctx.root_dir,'sphinx_doctest_warnings.txt')]
    args += ['.', build_dir]
    cmd = ' '.join(args)
    with cd(docs_dir):
        ctx.run(cmd, pty=True)
    if build_dir_cmd is not None:
        with cd(build_dir):
            ctx.run(build_dir_cmd, pty=True)


class RstFile(object):
    def __init__(self, local_root, url_root, parts):
        self.path = local_root.child(*parts) + '.rst'
        self.url = url_root + "/" + "/".join(parts) + '.html'
        # if parts[0] == 'docs':
        #     self.url = url_root + "/" + "/".join(parts[1:]) + '.html'
        # else:
        #     raise Exception("20131125")
        # self.url = url_root + "/" + "/".join(parts) + '.html'


class MissingConfig(Exception):
    def __init__(self, name):
        msg = "Must set `config.{0}` in `tasks.py`!"
        msg = msg.format(name)
        Exception.__init__(self, msg)


@task(name='test')
def run_tests(ctx):
    """Run the test suite of this project."""
    # assert os.environ['COVERAGE_PROCESS_START']
    if not ctx.root_dir.child('setup.py').exists():
        return
    if ctx.root_dir.child('pytest.ini').exists():
        ctx.run('py.test', pty=True)
    else:
        ctx.run('python setup.py -q test', pty=True)


@task(name='readme')
def write_readme(ctx):
    """Generate or update `README.txt` or `README.rst` file from `SETUP_INFO`. """
    if not ctx.main_package:
        return
    atelier.current_project.load_tasks()
    info = atelier.current_project.SETUP_INFO
    if not info.get('long_description'):
        return
    # if len(ctx.doc_trees) == 0:
    #     # when there are no docs, then the README file is manually maintained
    #     return
    if ctx.revision_control_system == 'git':
        readme = ctx.root_dir.child('README.rst')
    else:
        readme = ctx.root_dir.child('README.txt')

    # for k in ('name', 'description', 'long_description', 'url'):
    #     if k not in env.current_project.SETUP_INFO:
    #         msg = "SETUP_INFO for {0} has no key '{1}'"
    #         raise Exception(msg.format(env.current_project, k))

    title = rstgen.header(1, "The ``{}`` package".format(info['name']))

    txt = """\
{title}

{long_description}
""".format(title=title, **info)
    txt = txt.encode('utf-8')
    if readme.exists() and readme.read_file() == txt:
        return
    must_confirm("Overwrite %s" % readme.absolute())
    readme.write_file(txt)
    docs_index = ctx.root_dir.child('docs', 'index.rst')
    if docs_index.exists():
        docs_index.set_times()


@task(write_readme, name='bd')
def build_docs(ctx, *cmdline_args):
    """Build docs. Build all Sphinx HTML doctrees for this project. """
    for docs_dir in get_doc_trees(ctx):
        print("Invoking Sphinx in in directory %s..." % docs_dir)
        builder = 'html'
        if ctx.use_dirhtml:
            builder = 'dirhtml'
        sphinx_build(ctx, builder, docs_dir, cmdline_args)
        sync_docs_data(ctx, docs_dir)


@task(name='clean')
def clean(ctx, batch=False):
    # def clean(ctx, *cmdline_args):
    """Remove temporary and generated files."""
    sphinx_clean(ctx, batch)
    py_clean(ctx, batch)
    # clean_demo_caches()


@task(name='sdist')
def setup_sdist(ctx):
    "Create a source distribution."
    if not atelier.current_project.SETUP_INFO.get('version'):
        return
    show_pypi_status(ctx)
    # dist_dir = Path(ctx.sdist_dir).child(
    #     atelier.current_project.SETUP_INFO['name'])
    dist_dir = ctx.sdist_dir
    args = ["python", "setup.py"]
    args += ["sdist", "--formats=gztar"]
    args += ["--dist-dir", dist_dir]
    ctx.run(' '.join(args), pty=True)


@task(name='release')
def pypi_release(ctx):
    "Publish a new version to PyPI."
    info = atelier.current_project.SETUP_INFO
    if not info.get('version'):
        return
    version = info['version']
    # dist_dir = Path(ctx.sdist_dir).child(info['name'])
    dist_dir = ctx.sdist_dir

    show_revision_status(ctx)
    show_pypi_status(ctx)

    must_confirm(RELEASE_CONFIRM % info)

    if ctx.revision_control_system == 'git':
        args = ["git", "tag"]
        args += ["-a", version]
        args += ["-m", "'Release %(name)s %(version)s.'" % info]
        ctx.run(' '.join(args), pty=True)

    pypi_register(ctx)
    args = ["python", "setup.py"]
    args += ["sdist", "--formats=gztar"]
    args += ["--dist-dir", dist_dir]
    args += ["upload"]
    ctx.run(' '.join(args), pty=True)


@task(name='test_sdist')
def test_sdist(ctx):
    """Install a previously created sdist into a temporary virtualenv and
    run test suite.

    """
    info = atelier.current_project.SETUP_INFO
    if not info.get('version'):
        return
    # from atelier.projects import load_projects
    # projects = [p for p in load_projects() if p.SETUP_INFO.get('version') and p['name'] != info['name']]

    with cd(ctx.root_dir):
        ctx.run("rm -Rf tmp/tmp", pty=True)
        ctx.run("virtualenv tmp/tmp", pty=True)
        activate = ". tmp/tmp/bin/activate"
        
        def vrun(cmd):
            cmd = activate + ';' + cmd
            ctx.run(cmd, pty=True)
            
        vrun("pip install --download {0} {1}".format(ctx.pypi_dir, info['name']))
        # DEPRECATION: pip install --download has been deprecated and will be removed in the future. Pip now has a download command that should be used instead.


        # vrun("pip download {0}".format(info['name']))        
        
        vrun("pip install --no-allow-external --no-index --no-cache-dir -f {} -f {} {}".format(
            ctx.sdist_dir, ctx.pypi_dir, info['name']))
        # vrun("pip install -f {0} {1}".format(ctx.sdist_dir, info['name'])
             
        vrun("inv test")


@task(name='mm')
def make_messages(ctx):
    "Extract messages, then initialize and update all catalogs."
    extract_messages(ctx)
    init_catalog_code(ctx)
    update_catalog_code(ctx)

    # if False:
    #     pass
    # extract_messages_userdocs()
    # setup_babel_userdocs('init_catalog')
    # setup_babel_userdocs('update_catalog')


@task(name='register')
def pypi_register(ctx):
    """Register this project (and its current version) to PyPI. """
    args = ["python", "setup.py"]
    args += ["register"]
    ctx.run(' '.join(args), pty=True)


@task(name='ci')
def checkin(ctx, today=None):
    """Checkin and push to repository, using today's blog entry as commit message."""

    if ctx.revision_control_system is None:
        return

    if ctx.revision_control_system == 'git':
        from git import Repo
        repo = Repo(ctx.root_dir)
        if not repo.is_dirty():
            print("No changes to commit in {0}.".format(ctx.root_dir))
            return

    show_revision_status(ctx)

    today = get_current_date(today)

    entry = get_blog_entry(ctx, today)
    if not entry.path.exists():
        quit("%s does not exist!" % entry.path.absolute())

    msg = entry.url

    if not confirm("OK to checkin %s %s?" % (ctx.project_name, msg)):
        return
    # ~ puts("Commit message refers to %s" % entry.absolute())

    if ctx.revision_control_system == 'hg':
        args = ["hg", "ci"]
    else:
        args = ["git", "commit", "-a"]
    args += ['-m', msg]
    cmd = ' '.join(args)
    ctx.run(cmd, pty=True)
    if ctx.revision_control_system == 'hg':
        ctx.run("hg push %s" % ctx.project_name, pty=True)
    else:
        ctx.run("git push", pty=True)


@task(name='blog')
def edit_blog_entry(ctx, today=None):
    """Edit today's blog entry, create an empty file if it doesn't yet exist.

    :today: Useful when a working day lasted longer than midnight, or
            when you start some work in the evening, knowing that you
            won't commit it before the next morning.  Note that you
            must specify the date using the YYYYMMDD format.

            Usage example::

                $ fab blog:20150727

    """
    if not ctx.editor_command:
        raise MissingConfig("editor_command")
    today = get_current_date(today)
    entry = get_blog_entry(ctx, today)
    if not entry.path.exists():
        if ctx.languages is None:
            txt = today.strftime(ctx.long_date_format)
        else:
            txt = format_date(
                today, format='full', locale=ctx.languages[0])
        content = rstgen.header(1, txt)
        content = ":date: {0}\n\n".format(today) + content
        msg = "{0}\nCreate file {1}?".format(content, entry.path)
        if not confirm(msg):
            return
        # for every year we create a new directory.
        yd = entry.path.parent
        if not yd.exists():
            if not confirm("Happy New Year! Create directory %s?" % yd):
                return
            yd.mkdir()
            txt = ".. blogger_year::\n"
            yd.child('index.rst').write_file(txt.encode('utf-8'))

        entry.path.write_file(content.encode('utf-8'))
        # touch it for Sphinx:
        entry.path.parent.child('index.rst').set_times()
    args = [ctx.editor_command.format(entry.path)]
    args += [entry.path]
    # raise Exception("20160324 %s", args)
    ctx.run(' '.join(args), pty=True)


@task(name='pd')
def publish(ctx):
    """Publish docs. Upload docs to public web server. """
    if not ctx.docs_rsync_dest:
        raise MissingConfig("docs_rsync_dest")

    for docs_dir in get_doc_trees(ctx):
        build_dir = docs_dir.child(ctx.build_dir_name)
        if build_dir.exists():
            # name = '%s_%s' % (ctx.project_name, docs_dir.name)
            # dest_url = ctx.docs_rsync_dest % name
            if "%" in ctx.docs_rsync_dest:
                name = '%s_%s' % (ctx.project_name, docs_dir.name)
                dest_url = ctx.docs_rsync_dest % name
            else:
                dest_url = ctx.docs_rsync_dest.format(
                    prj=ctx.project_name, docs=docs_dir.name)
            publish_docs(ctx, build_dir, dest_url)

            # build_dir = ctx.root_dir.child('userdocs', ctx.build_dir_name)
            # if build_dir.exists():
            #     dest_url = ctx.docs_rsync_dest % (ctx.project_name + '-userdocs')
            #     publish_docs(ctx, build_dir, dest_url)


def publish_docs(ctx, build_dir, dest_url):
    with cd(build_dir):
        args = ['rsync', '-e', 'ssh', '-r']
        args += ['--verbose']
        args += ['--progress']  # show progress
        args += ['--delete']  # delete files in dest
        args += ['--times']  # preserve timestamps
        args += ['--exclude', '.doctrees']
        args += ['./']  # source
        args += [dest_url]  # dest
        cmd = ' '.join(args)
        # must_confirm("%s> %s" % (build_dir, cmd))
        ctx.run(cmd, pty=True)


def show_revision_status(ctx):
    if ctx.revision_control_system == 'hg':
        args = ["hg", "st"]
    elif ctx.revision_control_system == 'git':
        args = ["git", "status"]
    else:
        print("Invalid revision_control_system %r !" %
              ctx.revision_control_system)
        return
    print("-" * 80)
    ctx.run(' '.join(args), pty=True)
    print("-" * 80)


def show_pypi_status(ctx):
    """Show project status on PyPI before doing a release.
    """
    info = atelier.current_project.SETUP_INFO
    version = info['version']
    name = info['name']

    assert name and version

    from xmlrpc.client import ServerProxy
    client = ServerProxy('https://pypi.python.org/pypi')
    released_versions = client.package_releases(name)
    if len(released_versions) == 0:
        print("This is your first PyPI release of %(name)s." % info)
    else:
        urls = client.release_urls(name, released_versions[-1])
        if len(urls) == 0:
            msg = "Last PyPI release was {0} (no files available)."
            msg = msg.format(released_versions[-1])
            print(msg)
        else:
            lastrel = urls[-1]
            # dt = lastrel['upload_time']
            # lastrel['upload_time'] = dt.ISO()
            print(LASTREL_INFO % lastrel)
        if version in released_versions:
            raise Exit(
                "ABORT: %(name)s %(version)s has already been "
                "released." % info)


def get_blog_entry(ctx, today):
    """Return an RstFile object representing the blog entry for that date
    in the current project.

    """
    parts = ('blog', str(today.year), today.strftime("%m%d"))
    return RstFile(Path(ctx.blog_root), ctx.blogref_url, parts)


def get_locale_dir(ctx):
    locale_dir = ctx.locale_dir
    if locale_dir is None:
        return
    return Path(locale_dir)


# @task(name='bh')
# def build_help_texts(ctx):
#     """Build help_texts.py file for this project."""
#     if not ctx.help_texts_source:
#         return
#     src_dir = ctx.help_texts_source
#     dest_dir = Path(ctx.build_dir_name)
#     args = ["sphinx-build", "-b", "help_texts"]
#     args += [src_dir, dest_dir]
#     cmd = ' '.join(args)
#     ctx.run(cmd, pty=True)


def extract_messages(ctx):
    """Extract messages from source files to `django.pot` file"""
    ld = get_locale_dir(ctx)
    if not ld:
        return
    args = ["python", "setup.py"]
    args += ["extract_messages"]
    args += ["-o", ld.child("django.pot")]
    cmd = ' '.join(args)
    # ~ must_confirm(cmd)
    ctx.run(cmd, pty=True)


def init_catalog_code(ctx):
    """Create code .po files if necessary."""
    from lino.core.site import to_locale
    ld = get_locale_dir(ctx)
    if not ld:
        return
    for loc in ctx.languages:
        if loc != 'en':
            f = ld.child(loc, 'LC_MESSAGES', 'django.po')
            if f.exists():
                print("Skip %s because file exists." % f)
            else:
                args = ["python", "setup.py"]
                args += ["init_catalog"]
                args += ["--domain django"]
                args += ["-l", to_locale(loc)]
                args += ["-d", ld]
                # ~ args += [ "-o" , f ]
                args += ["-i", ld.child('django.pot')]
                cmd = ' '.join(args)
                must_confirm(cmd)
                ctx.run(cmd, pty=True)


def update_catalog_code(ctx):
    """Update .po files from .pot file."""
    from lino.core.site import to_locale
    ld = get_locale_dir(ctx)
    if not ld:
        return
    for loc in ctx.languages:
        if loc != ctx.languages[0]:
            args = ["python", "setup.py"]
            args += ["update_catalog"]
            args += ["--domain django"]
            args += ["-o", ld.child(loc, 'LC_MESSAGES', 'django.po')]
            args += ["-i", ld.child("django.pot")]
            args += ["-l", to_locale(loc)]
            cmd = ' '.join(args)
            # ~ must_confirm(cmd)
            ctx.run(cmd, pty=True)


# @task(name='ls')
# def list_projects(ctx, *cmdline_args):
#     """List your projects."""


@task(name='ct')
def commited_today(ctx, today=None):
    """Print all today's commits to stdout."""
    from atelier.projects import load_projects
    from git import Repo

    today = get_current_date(today)
    rows = []

    def load(prj):

        # prj.load_fabfile()
        prj.load_tasks()

        # tsk, cfg = prj.ns.task_with_config('ci')
        cfg = prj.ns.configuration()

        if cfg['revision_control_system'] != 'git':
            # if cfg.revision_control_system != 'git':
            # print("20160816 {}".format(cfg))
            return

        repo = Repo(cfg['root_dir'])

        kw = dict()
        ONEDAY = timedelta(days=1)
        yesterday = today - ONEDAY
        tomorrow = today + ONEDAY
        kw.update(after=yesterday.strftime("%Y-%m-%d"),
                  before=tomorrow.strftime("%Y-%m-%d"))
        it = list(repo.iter_commits(**kw))
        if len(it) == 0:
            # print("20160816 no commits in {}".format(prj.nickname))
            return

        def fmtcommit(c):

            url = repo.remotes.origin.url
            if url.startswith("git@github.com"):
                url = "https://github.com/" + url[15:-4] \
                      + "/commit/" + c.hexsha
            elif url.startswith("git+ssh://git@github.com"):
                url = "https://github.com/" + url[25:-4] \
                      + "/commit/" + c.hexsha

            s = "`{0} <{1}>`__".format(c.hexsha[-7:], url)
            if c.message and not c.message.startswith("http://"):
                s += " " + c.message
            return s

        url = prj.SETUP_INFO.get('url', "oops")
        desc = "`%s <%s>`__" % (prj.name, url)

        for c in it:
            # ts = time.strftime("%H:%M", time.gmtime(c.committed_date))
            ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(c.committed_date))
            rows.append([ts, desc, fmtcommit(c)])

    for p in load_projects():
        load(p)

    def mycmp(a, b):
        return cmp(a[0], b[0])

    rows.sort(mycmp)
    print(rstgen.ul(["{0} : {1}\n{2}".format(*row) for row in rows]))
    # print rstgen.table(headers, rows)


