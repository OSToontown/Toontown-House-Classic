// Filename: ffmpegVideo.h
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

#ifndef FFMPEGVIDEO_H
#define FFMPEGVIDEO_H

#include "pandabase.h"

#ifdef HAVE_FFMPEG

#include "movieVideo.h"

class FfmpegVideoCursor;
class FactoryParams;
class BamWriter;
class BamReader;

////////////////////////////////////////////////////////////////////
//       Class : FfmpegVideo
// Description : 
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA_MOVIES FfmpegVideo : public MovieVideo {

PUBLISHED:
  FfmpegVideo(const Filename &name);
  FfmpegVideo(const SubfileInfo &info);

  virtual ~FfmpegVideo();
  virtual PT(MovieVideoCursor) open();
  
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
    MovieVideo::init_type();
    register_type(_type_handle, "FfmpegVideo",
                  MovieVideo::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;

  friend class FfmpegVideoCursor;
};

#include "ffmpegVideo.I"

#endif // HAVE_FFMPEG
#endif // FFMPEGVIDEO_H
