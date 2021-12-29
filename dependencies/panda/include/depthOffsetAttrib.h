// Filename: depthOffsetAttrib.h
// Created by:  drose (14Mar02)
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

#ifndef DEPTHOFFSETATTRIB_H
#define DEPTHOFFSETATTRIB_H

#include "pandabase.h"

#include "renderAttrib.h"
#include "luse.h"

class FactoryParams;

////////////////////////////////////////////////////////////////////
//       Class : DepthOffsetAttrib
// Description : This is a special kind of attribute that instructs
//               the graphics driver to apply an offset or bias to the
//               generated depth values for rendered polygons, before
//               they are written to the depth buffer.
//
//               This can be used to shift polygons forward slightly,
//               to resolve depth conflicts.  The cull traverser may
//               optionally use this, for instance, to implement
//               decals.  However, driver support for this feature
//               seems to be spotty, so use with caution.
//
//               The bias is always an integer number, and each
//               integer increment represents the smallest possible
//               increment in Z that is sufficient to completely
//               resolve two coplanar polygons.  Positive numbers are
//               closer towards the camera.
//
//               Nested DepthOffsetAttrib values accumulate; that is,
//               a DepthOffsetAttrib with a value of 1 beneath another
//               DepthOffsetAttrib with a value of 2 presents a net
//               offset of 3.  (A DepthOffsetAttrib will not, however,
//               combine with any other DepthOffsetAttribs with a
//               lower override parameter.)  The net value should
//               probably not exceed 16 or drop below 0 for maximum
//               portability.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA_PGRAPH DepthOffsetAttrib : public RenderAttrib {
private:
  INLINE DepthOffsetAttrib(int offset);

PUBLISHED:
  static CPT(RenderAttrib) make(int offset = 1);
  static CPT(RenderAttrib) make_default();

  INLINE int get_offset() const;

public:
  virtual void output(ostream &out) const;

protected:
  virtual int compare_to_impl(const RenderAttrib *other) const;
  virtual size_t get_hash_impl() const;
  virtual CPT(RenderAttrib) compose_impl(const RenderAttrib *other) const;
  virtual CPT(RenderAttrib) invert_compose_impl(const RenderAttrib *other) const;

private:
  int _offset;

PUBLISHED:
  static int get_class_slot() {
    return _attrib_slot;
  }
  virtual int get_slot() const {
    return get_class_slot();
  }

public:
  static void register_with_read_factory();
  virtual void write_datagram(BamWriter *manager, Datagram &dg);

protected:
  static TypedWritable *make_from_bam(const FactoryParams &params);
  void fillin(DatagramIterator &scan, BamReader *manager);
  
public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    RenderAttrib::init_type();
    register_type(_type_handle, "DepthOffsetAttrib",
                  RenderAttrib::get_class_type());
    _attrib_slot = register_slot(_type_handle, 100, make_default);
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
  static int _attrib_slot;
};

#include "depthOffsetAttrib.I"

#endif

