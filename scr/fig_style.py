"""
Shared figure style module for all publication figures.

Centralises rcParams, regime colour palette, and common annotation helpers
so that individual figure scripts stay DRY and visually consistent.
"""

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


# ─────────────────────────────────────────────────────────────────────────────
# Palette: Paul Tol Light  (0=GH, 1=GC, 2=BS, 3=SC, 4=NS)
# ─────────────────────────────────────────────────────────────────────────────

REGIME_COLORS = ['#44BB99', '#EE8866', '#EEDD88', '#77AADD', '#DDDDDD']
REGIME_NAMES  = {
    0: 'GH (Global Honesty)',
    1: 'GC (Global Corruption)',
    2: 'BS (Bistability)',
    3: 'SC (Stable Coexistence)',
    4: 'NS (No Submission)',
}
REGIME_CMAP = ListedColormap(REGIME_COLORS)


# ─────────────────────────────────────────────────────────────────────────────
# Style application
# ─────────────────────────────────────────────────────────────────────────────

def apply_style():
    """Set seaborn paper context + project-specific rcParams."""
    sns.set_context("paper", font_scale=1.0)
    sns.set_style("ticks", {"font.family": "serif"})
    mpl.rcParams.update({
        'text.usetex':        True,
        'pdf.fonttype':       42,
        'savefig.dpi':        300,
        'axes.linewidth':     0.6,
        'xtick.major.width':  0.6,
        'ytick.major.width':  0.6,
        'xtick.direction':    'out',
        'ytick.direction':    'out',
        'lines.linewidth':    1.5,
    })


# ─────────────────────────────────────────────────────────────────────────────
# Common annotation helpers
# ─────────────────────────────────────────────────────────────────────────────

def regime_legend(ax, present_codes, loc='lower center', bbox_to_anchor=None,
                  ncol=None, **kwargs):
    """
    Add a discrete colour legend for regime codes present in the figure.

    Parameters
    ----------
    ax : matplotlib Axes (or Figure for fig-level legend)
    present_codes : list[int]
        Which regime codes (0-4) appear and should be shown.
    loc, bbox_to_anchor, ncol : legend positioning
    **kwargs : forwarded to ax.legend()
    """
    handles = [
        Patch(facecolor=REGIME_COLORS[c], edgecolor='#333333', linewidth=0.4,
              label=REGIME_NAMES[c])
        for c in sorted(present_codes)
    ]
    if ncol is None:
        ncol = len(handles)
    kw = dict(loc=loc, handles=handles, fontsize=7.5, framealpha=0.92,
              ncol=ncol, handlelength=1.2, handletextpad=0.4,
              columnspacing=1.0, edgecolor='none')
    if bbox_to_anchor is not None:
        kw['bbox_to_anchor'] = bbox_to_anchor
    kw.update(kwargs)
    return ax.legend(**kw)


def mark_point(ax, x, y, label=None, offset=(15, 15), fontsize=8):
    """
    Small open circle marker with optional offset text label (no arrow).

    Parameters
    ----------
    ax : matplotlib Axes
    x, y : data coordinates
    label : str or None
    offset : (dx, dy) in points for the text label
    fontsize : label font size
    """
    ax.plot(x, y, marker='o', markersize=5, markerfacecolor='white',
            markeredgecolor='black', markeredgewidth=0.8, zorder=10)
    if label is not None:
        ax.annotate(label, xy=(x, y), xytext=offset,
                    textcoords='offset points', fontsize=fontsize,
                    color='black', va='center', ha='left')
