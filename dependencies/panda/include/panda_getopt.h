/* Filename: panda_getopt.h
 * Created by:  drose (19Jul11)
 *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#ifndef PANDA_GETOPT_H
#define PANDA_GETOPT_H

#include "dtoolbase.h"

/* Include this file to get a definition of getopt(). */

#ifndef HAVE_GETOPT
  /* If the system doesn't provide a getopt(), use our own implementation. */
  #include "panda_getopt_impl.h"
#else
  /* We prefer to use the system version if it is available. */
  #ifdef PHAVE_GETOPT_H
    #include <getopt.h>
  #endif
#endif

#endif

