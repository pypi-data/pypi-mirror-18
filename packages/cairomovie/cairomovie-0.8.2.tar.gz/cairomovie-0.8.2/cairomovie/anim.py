# -*- coding: utf-8 -*-
"""Makes animations from cairo frames, based on moviepy."""

import collections
import os.path
import argparse
import math

import moviepy.editor as mpy
import numpy as np
import abc
try:
    import cairo
except ImportError:
    import cairocffi as cairo

# -----------------------------------------------------------------------
# Animation Interface
# -----------------------------------------------------------------------

class Animation(metaclass=abc.ABCMeta):
    """Implement a class of this method to perform the animation."""

    @abc.abstractmethod
    def duration(self, config):
        """Return the total duration of the animation."""
        return 0

    @abc.abstractmethod
    def draw_frame(self, c, t, config):
        """Draw one animation frame to the cairo context."""
        return

    def get_cairo_frame(self, t, config):
        """Create a cairo image representing one frame, using draw_frame."""
        img = cairo.ImageSurface(cairo.FORMAT_RGB24, config.w, config.h)
        c = cairo.Context(img)
        c.save()
        self.draw_frame(c, t, config)
        c.restore()
        return img

# -----------------------------------------------------------------------
# Rendering support
# -----------------------------------------------------------------------

class AnimConfig(collections.namedtuple('AnimConfig', ('w','h','fps'))):
    pass

def render_animation(anim, filename, config, verbose=True):
    """Renders the animation to a file."""

    def render_frame(t):
        # Render as cairo img.
        img = anim.get_cairo_frame(t, config)
        # Convert to numpy array.
        im = np.frombuffer(img.get_data(), np.uint8)
        im.shape = (img.get_height(), img.get_width(), 4)
        return im[:,:,[2,1,0]] # RGB order

    duration = anim.duration(config)
    fps = config.fps
    frames = ceil(duration * fps) + 1
    duration = frames / fps

    clip = mpy.VideoClip(render_frame, duration=duration)

    # Save as the correct filetype
    _, ext = os.path.splitext(filename)
    if ext == '.gif':
        clip.write_gif(
            filename,
            fps=fps, opt="OptimizePlus", fuzz=10, verbose=verbose)
    else:
        clip.write_videofile(
            filename,
            fps=fps, verbose=verbose)

def render_one_frame(anim, filename, config, t=None, verbose=True):
    """Export one moment in the animation (for testing)."""
    t = anim.duration(config) if t is None else t
    img = anim.get_cairo_frame(t, config)
    img.write_to_png(filename)

def render(anim, filename, config, t=None, verbose=True):
    """Renders either a frame or an animation, depending on filename."""
    _, ext = os.path.splitext(filename)
    if ext == '.png':
        render_one_frame(anim, filename, config, t, verbose)
    else:
        render_animation(anim, filename, config, verbose)

# -----------------------------------------------------------------------
# Command line support.
# -----------------------------------------------------------------------

def add_anim_arguments(
        parser,
        default_filename='out.mp4',
        default_width=1280, default_height=720, default_fps=15
        ):
    """Adds argparse arguments."""
    parser.add_argument(
        '-o', '--out', type=str, default=default_filename, action='store',
        help="the output file (use .png for still frame)")
    parser.add_argument(
        '-x', '--width', type=int, default=default_width, action='store',
        help="the image width")
    parser.add_argument(
        '-y', '--height', type=int, default=default_height, action='store',
        help="the image height")
    parser.add_argument(
        '-f', '--fps', type=int, default=default_fps, action='store',
        help="the fps (ignoree with png filename)")
    parser.add_argument(
        '-t', '--time', type=float, default=None, action='store',
        help="the time for the still image (ignored without png filename)")
    parser.add_argument(
        '-q', '--quiet', default=False, action='store_true',
        help="reduces output")

def render_from_args(anim, args):
    """Processes arguments and calls the correct renderer."""
    config = AnimConfig(args.width, args.height, args.fps)
    if not args.quiet:
        duration = anim.duration(config)
        frames = math.ceil(duration * config.fps) + 1
        print("Full animation: {:.2f} s, {:d} frames".format(duration, frames))
    render(anim, args.out, config, t=args.time, verbose=not args.quiet)
