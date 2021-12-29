// Filename: lpoint4_src.h
// Created by:  drose (08Mar00)
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

////////////////////////////////////////////////////////////////////
//       Class : LPoint4
// Description : This is a four-component point in space.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA_LINMATH FLOATNAME(LPoint4) : public FLOATNAME(LVecBase4) {
PUBLISHED:
  INLINE_LINMATH FLOATNAME(LPoint4)();
  INLINE_LINMATH FLOATNAME(LPoint4)(const FLOATNAME(LVecBase4) &copy);
  INLINE_LINMATH FLOATNAME(LPoint4) &operator = (const FLOATNAME(LVecBase4) &copy);
  INLINE_LINMATH FLOATNAME(LPoint4) &operator = (FLOATTYPE fill_value);
  INLINE_LINMATH FLOATNAME(LPoint4)(FLOATTYPE fill_value);
  INLINE_LINMATH FLOATNAME(LPoint4)(FLOATTYPE x, FLOATTYPE y, FLOATTYPE z, FLOATTYPE w);

  EXTENSION(PyObject *__getattr__(const string &attr_name) const);
  EXTENSION(int __setattr__(PyObject *self, const string &attr_name, PyObject *assign));

  INLINE_LINMATH static const FLOATNAME(LPoint4) &zero();
  INLINE_LINMATH static const FLOATNAME(LPoint4) &unit_x();
  INLINE_LINMATH static const FLOATNAME(LPoint4) &unit_y();
  INLINE_LINMATH static const FLOATNAME(LPoint4) &unit_z();
  INLINE_LINMATH static const FLOATNAME(LPoint4) &unit_w();

  INLINE_LINMATH FLOATNAME(LPoint4) operator - () const;

  INLINE_LINMATH FLOATNAME(LVecBase4)
  operator + (const FLOATNAME(LVecBase4) &other) const;
  INLINE_LINMATH FLOATNAME(LPoint4)
  operator + (const FLOATNAME(LVector4) &other) const;

  INLINE_LINMATH FLOATNAME(LVecBase4)
  operator - (const FLOATNAME(LVecBase4) &other) const;
  INLINE_LINMATH FLOATNAME(LVector4)
  operator - (const FLOATNAME(LPoint4) &other) const;
  INLINE_LINMATH FLOATNAME(LPoint4)
  operator - (const FLOATNAME(LVector4) &other) const;

  INLINE_LINMATH FLOATNAME(LPoint4) operator * (FLOATTYPE scalar) const;
  INLINE_LINMATH FLOATNAME(LPoint4) operator / (FLOATTYPE scalar) const;
  INLINE_LINMATH FLOATNAME(LPoint4) project(const FLOATNAME(LVecBase4) &onto) const;

  EXTENSION(INLINE_LINMATH void python_repr(ostream &out, const string &class_name) const);

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type();

private:
  static TypeHandle _type_handle;
};

#include "lpoint4_src.I"
