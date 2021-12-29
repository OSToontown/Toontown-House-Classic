// Filename: bulletGenericConstraint.h
// Created by:  enn0x (02Mar10)
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

#ifndef __BULLET_GENERIC_CONSTRAINT_H__
#define __BULLET_GENERIC_CONSTRAINT_H__

#include "pandabase.h"

#include "bullet_includes.h"
#include "bullet_utils.h"
#include "bulletConstraint.h"

#include "transformState.h"
#include "luse.h"

class BulletRigidBodyNode;

////////////////////////////////////////////////////////////////////
//       Class : BulletGenericConstraint
// Description : 
////////////////////////////////////////////////////////////////////
class EXPCL_PANDABULLET BulletGenericConstraint : public BulletConstraint {

PUBLISHED:
  BulletGenericConstraint(const BulletRigidBodyNode *node_a, 
                          CPT(TransformState) frame_a,
                          bool use_frame_a);
  BulletGenericConstraint(const BulletRigidBodyNode *node_a,
                          const BulletRigidBodyNode *node_b,
                          CPT(TransformState) frame_a,
                          CPT(TransformState) frame_b,
                          bool use_frame_a);
  INLINE ~BulletGenericConstraint();

  void set_linear_limit(int axis, PN_stdfloat low, PN_stdfloat high);
  void set_angular_limit(int axis, PN_stdfloat low, PN_stdfloat high);

  LVector3 get_axis(int axis) const;
  PN_stdfloat get_pivot(int axis) const;
  PN_stdfloat get_angle(int axis) const;

public:
  virtual btTypedConstraint *ptr() const;

private:
  btGeneric6DofConstraint *_constraint;

////////////////////////////////////////////////////////////////////
public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    BulletConstraint::init_type();
    register_type(_type_handle, "BulletGenericConstraint", 
                  BulletConstraint::get_class_type());
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

#include "bulletGenericConstraint.I"

#endif // __BULLET_GENERIC_CONSTRAINT_H__
