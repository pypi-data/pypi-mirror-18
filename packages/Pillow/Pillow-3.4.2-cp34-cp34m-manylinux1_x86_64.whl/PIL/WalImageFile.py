# encoding: utf-8
#
# The Python Imaging Library.
# $Id$
#
# WAL file handling
#
# History:
# 2003-04-23 fl   created
#
# Copyright (c) 2003 by Fredrik Lundh.
#
# See the README file for information on usage and redistribution.
#

# NOTE: This format cannot be automatically recognized, so the reader
# is not registered for use with Image.open().  To open a WAL file, use
# the WalImageFile.open() function instead.

# This reader is based on the specification available from:
#    http://www.flipcode.com/archives/Quake_2_BSP_File_Format.shtml
# and has been tested with a few sample files found using google.

from __future__ import print_function

from PIL import Image, _binary

try:
    import builtins
except ImportError:
    import __builtin__
    builtins = __builtin__

i32 = _binary.i32le


def open(filename):
    """
    Load texture from a Quake2 WAL texture file.

    By default, a Quake2 standard palette is attached to the texture.
    To override the palette, use the <b>putpalette</b> method.

    :param filename: WAL file name, or an opened file handle.
    :returns: An image instance.
    """
    # FIXME: modify to return a WalImageFile instance instead of
    # plain Image object ?

    if hasattr(filename, "read"):
        fp = filename
    else:
        fp = builtins.open(filename, "rb")

    # read header fields
    header = fp.read(32+24+32+12)
    size = i32(header, 32), i32(header, 36)
    offset = i32(header, 40)

    # load pixel data
    fp.seek(offset)

    im = Image.frombytes("P", size, fp.read(size[0] * size[1]))
    im.putpalette(quake2palette)

    im.format = "WAL"
    im.format_description = "Quake2 Texture"

    # strings are null-terminated
    im.info["name"] = header[:32].split(b"\0", 1)[0]
    next_name = header[56:56+32].split(b"\0", 1)[0]
    if next_name:
        im.info["next_name"] = next_name

    return im


quake2palette = (
    # default palette taken from piffo 0.93 by Hans Häggström
    b"\x01\x01\x01\x0b\x0b\x0b\x12\x12\x12\x17\x17\x17\x1b\x1b\x1b\x1e"
    b"\x1e\x1e\x22\x22\x22\x26\x26\x26\x29\x29\x29\x2c\x2c\x2c\x2f\x2f"
    b"\x2f\x32\x32\x32\x35\x35\x35\x37\x37\x37\x3a\x3a\x3a\x3c\x3c\x3c"
    b"\x24\x1e\x13\x22\x1c\x12\x20\x1b\x12\x1f\x1a\x10\x1d\x19\x10\x1b"
    b"\x17\x0f\x1a\x16\x0f\x18\x14\x0d\x17\x13\x0d\x16\x12\x0d\x14\x10"
    b"\x0b\x13\x0f\x0b\x10\x0d\x0a\x0f\x0b\x0a\x0d\x0b\x07\x0b\x0a\x07"
    b"\x23\x23\x26\x22\x22\x25\x22\x20\x23\x21\x1f\x22\x20\x1e\x20\x1f"
    b"\x1d\x1e\x1d\x1b\x1c\x1b\x1a\x1a\x1a\x19\x19\x18\x17\x17\x17\x16"
    b"\x16\x14\x14\x14\x13\x13\x13\x10\x10\x10\x0f\x0f\x0f\x0d\x0d\x0d"
    b"\x2d\x28\x20\x29\x24\x1c\x27\x22\x1a\x25\x1f\x17\x38\x2e\x1e\x31"
    b"\x29\x1a\x2c\x25\x17\x26\x20\x14\x3c\x30\x14\x37\x2c\x13\x33\x28"
    b"\x12\x2d\x24\x10\x28\x1f\x0f\x22\x1a\x0b\x1b\x14\x0a\x13\x0f\x07"
    b"\x31\x1a\x16\x30\x17\x13\x2e\x16\x10\x2c\x14\x0d\x2a\x12\x0b\x27"
    b"\x0f\x0a\x25\x0f\x07\x21\x0d\x01\x1e\x0b\x01\x1c\x0b\x01\x1a\x0b"
    b"\x01\x18\x0a\x01\x16\x0a\x01\x13\x0a\x01\x10\x07\x01\x0d\x07\x01"
    b"\x29\x23\x1e\x27\x21\x1c\x26\x20\x1b\x25\x1f\x1a\x23\x1d\x19\x21"
    b"\x1c\x18\x20\x1b\x17\x1e\x19\x16\x1c\x18\x14\x1b\x17\x13\x19\x14"
    b"\x10\x17\x13\x0f\x14\x10\x0d\x12\x0f\x0b\x0f\x0b\x0a\x0b\x0a\x07"
    b"\x26\x1a\x0f\x23\x19\x0f\x20\x17\x0f\x1c\x16\x0f\x19\x13\x0d\x14"
    b"\x10\x0b\x10\x0d\x0a\x0b\x0a\x07\x33\x22\x1f\x35\x29\x26\x37\x2f"
    b"\x2d\x39\x35\x34\x37\x39\x3a\x33\x37\x39\x30\x34\x36\x2b\x31\x34"
    b"\x27\x2e\x31\x22\x2b\x2f\x1d\x28\x2c\x17\x25\x2a\x0f\x20\x26\x0d"
    b"\x1e\x25\x0b\x1c\x22\x0a\x1b\x20\x07\x19\x1e\x07\x17\x1b\x07\x14"
    b"\x18\x01\x12\x16\x01\x0f\x12\x01\x0b\x0d\x01\x07\x0a\x01\x01\x01"
    b"\x2c\x21\x21\x2a\x1f\x1f\x29\x1d\x1d\x27\x1c\x1c\x26\x1a\x1a\x24"
    b"\x18\x18\x22\x17\x17\x21\x16\x16\x1e\x13\x13\x1b\x12\x12\x18\x10"
    b"\x10\x16\x0d\x0d\x12\x0b\x0b\x0d\x0a\x0a\x0a\x07\x07\x01\x01\x01"
    b"\x2e\x30\x29\x2d\x2e\x27\x2b\x2c\x26\x2a\x2a\x24\x28\x29\x23\x27"
    b"\x27\x21\x26\x26\x1f\x24\x24\x1d\x22\x22\x1c\x1f\x1f\x1a\x1c\x1c"
    b"\x18\x19\x19\x16\x17\x17\x13\x13\x13\x10\x0f\x0f\x0d\x0b\x0b\x0a"
    b"\x30\x1e\x1b\x2d\x1c\x19\x2c\x1a\x17\x2a\x19\x14\x28\x17\x13\x26"
    b"\x16\x10\x24\x13\x0f\x21\x12\x0d\x1f\x10\x0b\x1c\x0f\x0a\x19\x0d"
    b"\x0a\x16\x0b\x07\x12\x0a\x07\x0f\x07\x01\x0a\x01\x01\x01\x01\x01"
    b"\x28\x29\x38\x26\x27\x36\x25\x26\x34\x24\x24\x31\x22\x22\x2f\x20"
    b"\x21\x2d\x1e\x1f\x2a\x1d\x1d\x27\x1b\x1b\x25\x19\x19\x21\x17\x17"
    b"\x1e\x14\x14\x1b\x13\x12\x17\x10\x0f\x13\x0d\x0b\x0f\x0a\x07\x07"
    b"\x2f\x32\x29\x2d\x30\x26\x2b\x2e\x24\x29\x2c\x21\x27\x2a\x1e\x25"
    b"\x28\x1c\x23\x26\x1a\x21\x25\x18\x1e\x22\x14\x1b\x1f\x10\x19\x1c"
    b"\x0d\x17\x1a\x0a\x13\x17\x07\x10\x13\x01\x0d\x0f\x01\x0a\x0b\x01"
    b"\x01\x3f\x01\x13\x3c\x0b\x1b\x39\x10\x20\x35\x14\x23\x31\x17\x23"
    b"\x2d\x18\x23\x29\x18\x3f\x3f\x3f\x3f\x3f\x39\x3f\x3f\x31\x3f\x3f"
    b"\x2a\x3f\x3f\x20\x3f\x3f\x14\x3f\x3c\x12\x3f\x39\x0f\x3f\x35\x0b"
    b"\x3f\x32\x07\x3f\x2d\x01\x3d\x2a\x01\x3b\x26\x01\x39\x21\x01\x37"
    b"\x1d\x01\x34\x1a\x01\x32\x16\x01\x2f\x12\x01\x2d\x0f\x01\x2a\x0b"
    b"\x01\x27\x07\x01\x23\x01\x01\x1d\x01\x01\x17\x01\x01\x10\x01\x01"
    b"\x3d\x01\x01\x19\x19\x3f\x3f\x01\x01\x01\x01\x3f\x16\x16\x13\x10"
    b"\x10\x0f\x0d\x0d\x0b\x3c\x2e\x2a\x36\x27\x20\x30\x21\x18\x29\x1b"
    b"\x10\x3c\x39\x37\x37\x32\x2f\x31\x2c\x28\x2b\x26\x21\x30\x22\x20"
)
