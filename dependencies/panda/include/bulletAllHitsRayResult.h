// Filename: bulletAllHitsRayResult.h
// Created by:  enn0x (21Feb10)
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

#ifndef __BULLET_ALL_HITS_RAY_RESULT_H__
#define __BULLET_ALL_HITS_RAY_RESULT_H__

#include "pandabase.h"

#include "bullet_includes.h"
#include "bullet_utils.h"

#include "luse.h"
#include "pandaNode.h"
#include "collideMask.h"

////////////////////////////////////////////////////////////////////
//       Class : BulletRayHit
// Description : 
////////////////////////////////////////////////////////////////////
struct BulletRayHit {

PUBLISHED:
  INLINE static BulletRayHit empty();

  PandaNode *get_node() const;
  LPoint3 get_hit_pos() const;
  LVector3 get_hit_normal() const;
  PN_stdfloat get_hit_fraction() const;

private:
  btCollisionObject *_object; 
  btVector3 _normal;
  btVector3 _pos;
  btScalar _fraction;

  friend struct BulletAllHitsRayResult;
};

////////////////////////////////////////////////////////////////////
//       Class : BulletAllHitsRayResult
// Description : 
////////////////////////////////////////////////////////////////////
struct EXPCL_PANDABULLET BulletAllHitsRayResult : public btCollisionWorld::AllHitsRayResultCallback {

PUBLISHED:
  INLINE static BulletAllHitsRayResult empty();

  LPoint3 get_from_pos() const;
  LPoint3 get_to_pos() const;

  bool has_hits() const;
  PN_stdfloat get_closest_hit_fraction() const;

  int get_num_hits() const;
  const BulletRayHit get_hit(int idx) const;
  MAKE_SEQ(get_hits, get_num_hits, get_hit);

public:
  virtual bool needsCollision(btBroadphaseProxy* proxy0) const;

private:
  BulletAllHitsRayResult(const btVector3 &from_pos, const btVector3 &to_pos, const CollideMask &mask);

  CollideMask _mask;

  friend class BulletWorld;
};

#include "bulletAllHitsRayResult.I"

#endif // __BULLET_ALL_HITS_RAY_RESULT_H__
