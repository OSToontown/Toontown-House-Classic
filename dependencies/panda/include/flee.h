////////////////////////////////////////////////////////////////////////
// Filename    : flee.h
// Created by  : Deepak, John, Navin
// Date        :  24 Oct 09
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

#ifndef _FLEE_H
#define _FLEE_H

#include "aiGlobals.h"
#include "aiCharacter.h"

class AICharacter;

class EXPCL_PANDAAI Flee {

public:
  AICharacter *_ai_char;

  LVecBase3f _flee_position;
  float _flee_weight;
  LVecBase3f _flee_direction;
  double _flee_distance;
  double _flee_relax_distance;
  LVecBase3f _flee_present_pos;
  bool _flee_done;
  bool _flee_activate_done;

  Flee(AICharacter *ai_ch, NodePath target_object, double panic_distance = 10.0,
                              double relax_distance = 10.0, float flee_wt = 1.0);

  Flee(AICharacter *ai_ch, LVecBase3f pos, double panic_distance = 10.0,
                              double relax_distance = 10.0, float flee_wt = 1.0);

  ~Flee();
  LVecBase3f do_flee();
  void flee_activate();
};

#endif
