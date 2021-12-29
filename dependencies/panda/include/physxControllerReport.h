// Filename: physxControllerReport.h
// Created by:  enn0x (24Sep09)
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

#ifndef PHYSXCONTROLLERREPORT_H
#define PHYSXCONTROLLERREPORT_H

#include "pandabase.h"
#include "pStatCollector.h"

#include "physx_includes.h"

////////////////////////////////////////////////////////////////////
//       Class : PhysxControllerReport
// Description : Implementation of the NxUserControllerHitReport
//               interface.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDAPHYSX PhysxControllerReport : public NxUserControllerHitReport {

public:
  INLINE PhysxControllerReport();
  INLINE ~PhysxControllerReport();

  void enable();
  void disable();
  bool is_enabled() const;

  virtual NxControllerAction onShapeHit(const NxControllerShapeHit& hit);
  virtual NxControllerAction onControllerHit(const NxControllersHit& hit);

private:
  bool _enabled;
  static PStatCollector _pcollector;
};

#include "physxControllerReport.I"

#endif // PHYSXCONTROLLERREPORT_H
