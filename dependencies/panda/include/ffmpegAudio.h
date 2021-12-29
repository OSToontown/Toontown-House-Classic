// Filename: ffmpegAudio.h
// Created by: jyelon (01Aug2007)
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

#ifndef FFMPEGAUDIO_H
#define FFMPEGAUDIO_H

#include "pandabase.h"

#ifdef HAVE_FFMPEG

#include "movieAudio.h"

class FfmpegAudioCursor;

////////////////////////////////////////////////////////////////////
//       Class : FfmpegAudio
// Description : A stream that generates a sequence of audio samples.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA_MOVIES FfmpegAudio : public MovieAudio {

PUBLISHED:
  FfmpegAudio(const Filename &name);
  virtual ~FfmpegAudio();
  virtual PT(MovieAudioCursor) open();

 private:
  friend class FfmpegAudioCursor;
  
public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedWritableReferenceCount::init_type();
    register_type(_type_handle, "FfmpegAudio",
                  MovieAudio::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "ffmpegAudio.I"

#endif // HAVE_FFMPEG
#endif // FFMPEG_AUDIO.H
