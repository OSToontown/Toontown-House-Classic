// Filename: bulletConvexHullShape.h
// Created by:  enn0x (26Jan10)
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

#ifndef __BULLET_CONVEX_HULL_SHAPE_H__
#define __BULLET_CONVEX_HULL_SHAPE_H__

#include "pandabase.h"

#include "bullet_includes.h"
#include "bulletShape.h"

#include "luse.h"
#include "geom.h"
#include "pta_LVecBase3.h"

////////////////////////////////////////////////////////////////////
//       Class : BulletConvexHullShape
// Description : 
////////////////////////////////////////////////////////////////////
class EXPCL_PANDABULLET BulletConvexHullShape : public BulletShape {

PUBLISHED:
  BulletConvexHullShape();
  INLINE BulletConvexHullShape(const BulletConvexHullShape &copy);
  INLINE void operator = (const BulletConvexHullShape &copy);
  INLINE ~BulletConvexHullShape();

  void add_point(const LPoint3 &p);
  void add_array(const PTA_LVecBase3 &points);
  void add_geom(const Geom *geom);

public:
  virtual btCollisionShape *ptr() const;

private:
  btConvexHullShape *_shape;

////////////////////////////////////////////////////////////////////
public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    BulletShape::init_type();
    register_type(_type_handle, "BulletConvexHullShape", 
                  BulletShape::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {
    init_type();
    return get_class_type();
  }

private:
  static TypeHandle _type_handle;
};

#include "bulletConvexHullShape.I"

#endif // __BULLET_CONVEX_HULL_SHAPE_H__
