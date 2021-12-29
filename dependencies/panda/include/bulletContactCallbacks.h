// Filename: bulletContactCallbacks.h
// Created by:  enn0x (10Apr10)
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

#ifndef __BULLET_CONTACT_CALLBACKS_H__
#define __BULLET_CONTACT_CALLBACKS_H__

#include "pandabase.h"

#include "bullet_includes.h"

#include "config_bullet.h" // required for: bullet_cat.debug()

#include "event.h"
#include "eventQueue.h"
#include "eventParameter.h"
#include "eventStorePandaNode.h"
#include "pandaNode.h"

struct UserPersitentData {
  PT(PandaNode) node0;
  PT(PandaNode) node1;
};

////////////////////////////////////////////////////////////////////
//     Function: contact_added_callback
//  Description: 
////////////////////////////////////////////////////////////////////
static bool
contact_added_callback(btManifoldPoint &cp,
                       const btCollisionObject *obj0,
                       int id0,
                       int index0,
                       const btCollisionObject *obj1,
                       int id1,
                       int index1) {

  if (cp.m_userPersistentData == NULL) {
    PT(PandaNode) node0 = (PandaNode *)obj0->getUserPointer();
    PT(PandaNode) node1 = (PandaNode *)obj1->getUserPointer();

    bullet_cat.debug() << "contact added: " << cp.m_userPersistentData << endl;

    // Gather persistent data
    UserPersitentData *data = new UserPersitentData();
    data->node0 = node0;
    data->node1 = node1;

    cp.m_userPersistentData = (void *)data;

    // Send event
    if (bullet_enable_contact_events) {

      Event *event = new Event("bullet-contact-added");
      event->add_parameter(EventParameter(new EventStorePandaNode(node0)));
      event->add_parameter(EventParameter(new EventStorePandaNode(node1)));

      EventQueue::get_global_event_queue()->queue_event(event);
    }
  }

  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: contact_processed_callback
//  Description: 
////////////////////////////////////////////////////////////////////
static bool
contact_processed_callback(btManifoldPoint &cp,
                           void *body0,
                           void *body1) {

/*
  btCollisionObject *obj0 = (btCollisionObject *)body0;
  btCollisionObject *colobj1Obj1 = (btCollisionObject *)body1;

  int flags0 = obj0->getCollisionFlags();
  int flags1 = obj1->getCollisionFlags();

  if ((flags0 & btCollisionObject::CF_CUSTOM_MATERIAL_CALLBACK)
   || (flags1 & btCollisionObject::CF_CUSTOM_MATERIAL_CALLBACK)) {

    // do something...
  }
*/

  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: contact_destroyed_callback
//  Description: 
////////////////////////////////////////////////////////////////////
static bool
contact_destroyed_callback(void *userPersistentData) {

  bullet_cat.debug() << "contact removed: " << userPersistentData << endl;

  UserPersitentData *data = (UserPersitentData *)userPersistentData;

  // Send event
  if (bullet_enable_contact_events) {

    Event *event = new Event("bullet-contact-destroyed");
    event->add_parameter(EventParameter(new EventStorePandaNode(data->node0)));
    event->add_parameter(EventParameter(new EventStorePandaNode(data->node1)));

    EventQueue::get_global_event_queue()->queue_event(event);
  }

  // Delete persitent data
  delete data;

  return false;
}

#endif // __BULLET_CONTACT_CALLBACKS_H__
