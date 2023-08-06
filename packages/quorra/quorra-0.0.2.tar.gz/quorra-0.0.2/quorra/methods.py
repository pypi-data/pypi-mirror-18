# -*- coding: utf-8 -*-
#
# Methods for interacting with quorra plots.
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import os
import uuid
import webbrowser


# config
# ------
_phantom = None
_open = None
_app = None
__src__ = os.path.dirname(os.path.realpath(__file__))
__cwd__ = os.getcwd()
__templates__ = os.path.join(__src__, 'tmpl')


# methods
# -------
def export(plot, filename, width=800, height=600):
    """
    Export plot to file.

    Args:
        plot (quorra.Plot): Quorra plot object to export.
        width (int): Width for plot (pixels).
        height (int): Height for plot (pixels).
        filename (str): Filename to export to.
    """
    global _phantom, __templates__, __cwd__
    if _phantom is None:
        from selenium.webdriver import PhantomJS
        _phantom = PhantomJS(service_log_path=os.path.devnull)
    tmpl = os.path.join(__templates__, 'export.html')
    exp = os.path.join(__cwd__, '.' +  str(uuid.uuid1()) + '.html')
    try:
        with open(tmpl, 'r') as fi, open(exp, 'w') as fo:
            dat = fi.read()
            dat = dat.replace('var plot = undefined;', 'var plot = {};'.format(str(plot)))
            dat = dat.replace('width: 800px;', 'width: {}px;'.format(width))
            dat = dat.replace('height: 500px;', 'height: {}px;'.format(height))
            fo.write(dat)
        _phantom.get('file://' + exp)
        _phantom.save_screenshot(filename.replace('.png', '') + '.png')
    finally:
        os.remove(exp)
    return


def render(plot, width=800, height=600, append=False):
    """
    Update current view with new plot.

    Args:
        plot (quorra.Plot): Quorra plot object to render.
        width (int): Width for plot (pixels).
        height (int): Height for plot (pixels).
        append (bool): Whether or not to append the plot
            to the current view.
    """
    global _open, __templates__
    if _open is None:
        # this should change later to an actual server that
        # waits for data and can support multiple plots at
        # the same time
        _open = os.path.join('/tmp/quorra-server.html')
    tmpl = os.path.join(__templates__, 'render.html')
    with open(tmpl, 'r') as fi, open(_open, 'w') as fo:
        dat = fi.read()
        dat = dat.replace('var plot = undefined;', 'var plot = {};'.format(str(plot)))
        dat = dat.replace('width: 800px;', 'width: {}px;'.format(width))
        dat = dat.replace('height: 500px;', 'height: {}px;'.format(height))
        fo.write(dat)
    webbrowser.open(_open)
    return

