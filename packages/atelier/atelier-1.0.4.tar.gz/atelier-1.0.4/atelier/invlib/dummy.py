# -*- coding: UTF-8 -*-
# Copyright 2016 by Luc Saffre & Hamza Khchine.
# License: BSD, see LICENSE for more details.
"""A little hack because otherwise commands like :cmd:`pp inv initdb`
would fail on non-Lino projects like e.g. atelier because they
wouldn't know what :cmd:`inv initdb` means.

"""

from .ns import ns

from invoke import task

@task(name='initdb')
def initdb_demo(ctx, *args, **kwargs):
    """Does nothing. """

ns.add_task(initdb_demo)
