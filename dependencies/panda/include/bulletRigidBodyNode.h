// Filename: bulletRigidBodyNode.h
// Created by:  enn0x (19Nov10)
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

#ifndef __BULLET_RIGID_BODY_NODE_H__
#define __BULLET_RIGID_BODY_NODE_H__

#include "pandabase.h"

#include "bullet_includes.h"
#include "bullet_utils.h"
#include "bulletBodyNode.h"

#include "pandaNode.h"
#include "collideMask.h"

class BulletShape;

////////////////////////////////////////////////////////////////////
//       Class : BulletRigidBodyNode
// Description : 
////////////////////////////////////////////////////////////////////
class EXPCL_PANDABULLET BulletRigidBodyNode : public BulletBodyNode {

PUBLISHED:
  BulletRigidBodyNode(const char *name="rigid");
  INLINE ~BulletRigidBodyNode();

  // Mass & inertia
  void set_mass(PN_stdfloat mass);
  PN_stdfloat get_mass() const;
  void set_inertia(const LVecBase3 &inertia);
  LVector3 get_inertia() const;

  // Velocity
  LVector3 get_linear_velocity() const;
  LVector3 get_angular_velocity() const;
  void set_linear_velocity(const LVector3 &velocity);
  void set_angular_velocity(const LVector3 &velocity);

  // Damping
  INLINE PN_stdfloat get_linear_damping() const;
  INLINE PN_stdfloat get_angular_damping() const;
  INLINE void set_linear_damping(PN_stdfloat value);
  INLINE void set_angular_damping(PN_stdfloat value);

  // Forces
  void clear_forces();
  void apply_force(const LVector3 &force, const LPoint3 &pos);
  void apply_central_force(const LVector3 &force);
  void apply_impulse(const LVector3 &impulse, const LPoint3 &pos);
  void apply_central_impulse(const LVector3 &impulse);
  void apply_torque(const LVector3 &torque);
  void apply_torque_impulse(const LVector3 &torque);

  // Deactivation thresholds
  PN_stdfloat get_linear_sleep_threshold() const;
  PN_stdfloat get_angular_sleep_threshold() const;
  void set_linear_sleep_threshold(PN_stdfloat threshold);
  void set_angular_sleep_threshold(PN_stdfloat threshold);

  // Gravity
  void set_gravity(const LVector3 &gravity);
  LVector3 get_gravity() const;

  // Restrict movement
  void set_linear_factor(const LVector3 &factor);
  void set_angular_factor(const LVector3 &factor);

public:
  virtual btCollisionObject *get_object() const;

  virtual void output(ostream &out) const;

  void sync_p2b();
  void sync_b2p();

protected:
  virtual void transform_changed();

private:
  virtual void shape_changed();

  // The motion state is required only for kinematic bodies.
  // For kinematic nodies getWorldTransform is called each frame, and
  // should return the current world transform of the node.
  class MotionState : public btMotionState {

  public:
    MotionState(CPT(TransformState) & sync) : _sync(sync) {};
    ~MotionState() {};

    virtual void getWorldTransform(btTransform &trans) const;
    virtual void setWorldTransform(const btTransform &trans);

  private:
    CPT(TransformState) &_sync;
  };

  CPT(TransformState) _sync;
  bool _sync_disable;

  btRigidBody *_rigid;

////////////////////////////////////////////////////////////////////
public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    BulletBodyNode::init_type();
    register_type(_type_handle, "BulletRigidBodyNode", 
                  BulletBodyNode::get_class_type());
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

#include "bulletRigidBodyNode.I"

#endif // __BULLET_RIGID_BODY_NODE_H__

