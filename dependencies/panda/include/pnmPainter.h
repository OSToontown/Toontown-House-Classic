// Filename: pnmPainter.h
// Created by:  drose (02Feb07)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

#ifndef PNMPAINTER_H
#define PNMPAINTER_H

#include "pandabase.h"

class PNMImage;

////////////////////////////////////////////////////////////////////
//       Class : PNMPainter
// Description : This class provides a number of convenient methods
//               for painting drawings directly into a PNMImage.
//
//               It stores a pointer to the PNMImage you pass it, but
//               it does not take ownership of the object; you are
//               responsible for ensuring that the PNMImage does not
//               destruct during the lifetime of the PNMPainter
//               object.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA_PNMIMAGE PNMPainter {
PUBLISHED:
  PNMPainter(PNMImage &image, int xo = 0, int yo = 0);
  INLINE ~PNMPainter();

  INLINE void set_pen(PNMBrush *pen);
  INLINE PNMBrush *get_pen() const;
  INLINE void set_fill(PNMBrush *fill);
  INLINE PNMBrush *get_fill() const;

  INLINE void draw_point(double x, double y);
  void draw_line(double xa, double ya, double xb, double yb);
  void draw_rectangle(double xa, double ya, double xb, double yb);

private:
  INLINE void draw_hline_point(int x, double xa, double ya, 
                               double xd, double yd,
                               double pixel_scale);
  INLINE void draw_vline_point(int y, double xa, double ya, 
                               double xd, double yd,
                               double pixel_scale);

private:
  PNMImage &_image;
  int _xo, _yo;

  PT(PNMBrush) _pen;
  PT(PNMBrush) _fill;
};

#include "pnmPainter.I"

#endif
