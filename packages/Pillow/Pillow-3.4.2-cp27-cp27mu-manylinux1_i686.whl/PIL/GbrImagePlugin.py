#
# The Python Imaging Library
#
# load a GIMP brush file
#
# History:
#       96-03-14 fl     Created
#       16-01-08 es     Version 2
#
# Copyright (c) Secret Labs AB 1997.
# Copyright (c) Fredrik Lundh 1996.
# Copyright (c) Eric Soroos 2016.
#
# See the README file for information on usage and redistribution.
#
#
# See https://github.com/GNOME/gimp/blob/master/devel-docs/gbr.txt for
# format documentation.
#
# This code Interprets version 1 and 2 .gbr files.
# Version 1 files are obsolete, and should not be used for new
#   brushes.
# Version 2 files are saved by GIMP v2.8 (at least)
# Version 3 files have a format specifier of 18 for 16bit floats in
#   the color depth field. This is currently unsupported by Pillow.

from PIL import Image, ImageFile, _binary

i32 = _binary.i32be


def _accept(prefix):
    return len(prefix) >= 8 and i32(prefix[:4]) >= 20 and i32(prefix[4:8]) in (1, 2)


##
# Image plugin for the GIMP brush format.

class GbrImageFile(ImageFile.ImageFile):

    format = "GBR"
    format_description = "GIMP brush file"

    def _open(self):
        header_size = i32(self.fp.read(4))
        version = i32(self.fp.read(4))
        if header_size < 20:
            raise SyntaxError("not a GIMP brush")
        if version not in (1, 2):
            raise SyntaxError("Unsupported GIMP brush version: %s" % version)

        width = i32(self.fp.read(4))
        height = i32(self.fp.read(4))
        color_depth = i32(self.fp.read(4))
        if width <= 0 or height <= 0:
            raise SyntaxError("not a GIMP brush")
        if color_depth not in (1, 4):
            raise SyntaxError("Unsupported GIMP brush color depth: %s" % color_depth)

        if version == 1:
            comment_length = header_size-20
        else:
            comment_length = header_size-28
            magic_number = self.fp.read(4)
            if magic_number != b'GIMP':
                raise SyntaxError("not a GIMP brush, bad magic number")
            self.info['spacing'] = i32(self.fp.read(4))

        comment = self.fp.read(comment_length)[:-1]

        if color_depth == 1:
            self.mode = "L"
        else:
            self.mode = 'RGBA'

        self.size = width, height

        self.info["comment"] = comment

        # Image might not be small
        Image._decompression_bomb_check(self.size)

        # Data is an uncompressed block of w * h * bytes/pixel
        self._data_size = width * height * color_depth

    def load(self):
        self.im = Image.core.new(self.mode, self.size)
        self.frombytes(self.fp.read(self._data_size))

#
# registry

Image.register_open(GbrImageFile.format, GbrImageFile, _accept)
Image.register_extension(GbrImageFile.format, ".gbr")
