%bcond_with x
%bcond_with wayland

%define gst_branch 1.0
%define _lib_gstreamer_dir %{_libdir}/gstreamer-%{gst_branch}
%define _lib_girepository %{_libdir}/girepository-%{gst_branch}
%define _enable_v4l2h264enc 0
%define _enable_v4l2jpegdec 0
%define _enable_introspection 0

#######################################################################
## how to build each plugin :
## add define option at gbs build cmd like [ --define "plugin bad" ]
## if not, all the source code in subprojects will be built
#######################################################################

%if 0%{?plugin:1}
  %if "%{plugin}" == "core"
    %define _name gstreamer
    %define _core_opt ""
  %endif
  %if "%{plugin}" == "base" || "%{plugin}" == "good" || "%{plugin}" == "bad" || "%{plugin}" == "ugly"
    %define _name gst-plugins-%{plugin}
    %define _base_opt ""
    %define _good_opt ""
    %define _bad_opt ""
    %define _ugly_opt ""
  %endif
  %if "%{plugin}" == "libav"
    %define _name gst-%{plugin}
    %define _libav_opt ""
  %endif
  %if "%{plugin}" == "rs"
    %define _name gst-rtsp-server
    %define _rs_opt ""
  %endif
  %if "%{plugin}" == "es"
    %define _name gst-editing-services
    %define _es_opt ""
  %endif

  %define _source_path subprojects/%{_name}

%else

  %define plugin all
  %define _name gstreamer
  %define _source_path .

  # plugin option prefix
  %define _core_opt gstreamer:
  %define _base_opt gst-plugins-base:
  %define _good_opt gst-plugins-good:
  %define _bad_opt gst-plugins-bad:
  %define _ugly_opt gst-plugins-ugly:
  %define _libav_opt gst-libav:
  %define _rs_opt gst-rtsp-server:
  %define _es_opt gst-editing-services:

%endif

Name:           %{_name}
Version:        1.24.11
Release:        42
Summary:        Streaming-Media Framework Runtime
License:        LGPL-2.0+
Group:          Multimedia/Framework
Url:            http://gstreamer.freedesktop.org/
Source0:        gstreamer-%{version}.tar.gz
Source1001:     gstreamer.manifest
BuildRequires:  meson >= 0.62.0
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(glib-2.0) >= 2.32.0


%if "%{plugin}" == "all" || "%{plugin}" == "core"

BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  libtool
BuildRequires:  pkgconfig(dlog)
%if "%{_enable_introspection}" == "1"
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 1.31.1
%endif
BuildRequires:  pkgconfig(libxml-2.0)

%description -n gstreamer
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related.  Its plug-in-based architecture
means that new data types or processing capabilities can be added by
installing new plug-ins.

%package -n gstreamer-utils
Summary:        Streaming-Media Framework Runtime
Group:          Multimedia/Framework
Provides:       gstreamer:%{_bindir}/gst-launch-%{gst_branch} = %{version}
# Symbol for unversioned wrappers:
Provides:       gstreamer-utils_versioned = %{version}

%description -n gstreamer-utils
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related.  Its plug-in-based architecture
means that new data types or processing capabilities can be added by
installing new plug-ins.

%package -n gstreamer-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
# gstreamer-utils is required for the gstreamer-provides rpm magic.
Requires:       gstreamer-utils = %{version}
Requires:       gstreamer = %{version}

%description -n gstreamer-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%else

BuildRequires:  pkgconfig(gstreamer-1.0)

%if "%{plugin}" != "base"
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
%endif

%endif

#######################################################
## Package info of Base Plugin
#######################################################

%if "%{plugin}" == "all"
%package -n gst-plugins-base
Summary:        GStreamer Streaming-Media Framework Plug-Ins
Group:          Multimedia/Framework
%endif

%if "%{plugin}" == "all" || "%{plugin}" == "base"

BuildRequires:  orc >= 0.4.16
BuildRequires:  python
BuildRequires:  pkgconfig(alsa) >= 0.9.1
BuildRequires:  pkgconfig(freetype2) >= 2.0.9
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(ogg) >= 1.0
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(theoradec) >= 1.1
BuildRequires:  pkgconfig(theoraenc) >= 1.1
BuildRequires:  pkgconfig(vorbis) >= 1.0
BuildRequires:  pkgconfig(vorbisenc) >= 1.0
BuildRequires:  pkgconfig(zlib)
%if "%{_enable_introspection}" == "1"
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 1.31.1
%endif
%if "%{tizen_profile_name}" != "tv"
BuildRequires:  update-desktop-files
%endif
%if %{with wayland}
%if 0%{?enable_gl:1}
BuildRequires:  pkgconfig(gles20)
BuildRequires:  pkgconfig(wayland-egl) >= 9.0
%endif # wayland
%endif # gl
%if %{with x}
BuildRequires:  pkgconfig(dri2proto)
BuildRequires:  pkgconfig(libdri2)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(xfixes)
%endif
# gstreamer-utils is required for the gstreamer-provides rpm magic.
Requires:       gstreamer >= 1.0.0
Requires:       opus
Supplements:    gstreamer

%description -n gst-plugins-base
GStreamer is a streaming media framework based on graphs of filters
that operate on media data. Applications using this library can do
anything media-related, from real-time sound processing to playing
videos. Its plug-in-based architecture means that new data types or
processing capabilities can be added simply by installing new plug-ins.

%if "%{tizen_profile_name}" != "tv"
%package -n gst-plugins-base-extension-adder
Summary:        libgstadder.so for gst-plugins-base
Requires:       gst-plugins-base = %{version}-%{release}
Provides:       gst-plugins-base-profile_mobile = %{version}-%{release}

%description -n gst-plugins-base-extension-adder
Libgstadder.so for gst-plugin-base. Supplicant for gst-plugin-base.
This is for Tizen mobile profile.
%endif

%package -n gst-plugins-base-devel
Summary:        Include files and Libraries
Requires:       gst-plugins-base = %{version}

%description -n gst-plugins-base-devel
This package contains all necessary include files and libraries needed
to compile and link applications that use gstreamer-plugins-base.

%endif

#######################################################
## Package info of Good Plugin
#######################################################

%if "%{plugin}" == "all"
%package -n gst-plugins-good
Summary:        GStreamer Streaming-Media Framework Plug-Ins
Group:          Multimedia/Framework
%endif

%if "%{plugin}" == "all" || "%{plugin}" == "good"

BuildRequires:  libjpeg-devel
BuildRequires:  orc >= 0.4.16
BuildRequires:  python
BuildRequires:  xsltproc
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libpulse) >= 1.0
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(libxml-2.0) >= 2.4.9
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(opencore-amrwb)
%if "%{tizen_profile_name}" != "tv"
BuildRequires:  pkgconfig(opencore-amrnb)
BuildRequires:  pkgconfig(libpng) >= 1.2
%endif
%if %{with x}
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xfixes)
# used by libgstvideo4linux2.so
BuildRequires:  pkgconfig(xv)
%endif
Requires:       gstreamer >= %{version}
Requires:       gst-plugins-base >= %{version}
Requires:       libsoup

%description -n gst-plugins-good
GStreamer is a streaming media framework based on graphs of filters
that operate on media data. Applications using this library can do
anything media-related, from real-time sound processing to playing
videos. Its plug-in-based architecture means that new data types or
processing capabilities can be added simply by installing new plug-ins.

%package -n gst-plugins-good-extra
Summary:        Complementary plugins for gst-plugins-good
Group:          Productivity/Multimedia/Other
Requires:       gst-plugins-good = %{version}
Enhances:       gst-plugins-good

%description -n gst-plugins-good-extra
This package provides complementary plugins for gst-plugins-good and
plugins not included in official Tizen images, which may be used for development / experimental purposes.

%if "%{tizen_profile_name}" != "tv"
%package -n gst-plugins-good-cairo
Summary:        Cairo plugin for gst-plugins-good
Group:          Multimedia/Framework
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-gobject)
Requires:       gst-plugins-good = %{version}
Enhances:       gst-plugins-good

%description -n gst-plugins-good-cairo
This package provides cairo plugin for gst-plugins-good and
this is not included in Tizen headless image.

%package -n gst-plugins-good-v4l2
Summary:        Video4Linux2 plugin for gst-plugins-good
Group:          Multimedia/Framework
BuildRequires:  pkgconfig(libv4l2)
Requires:       gst-plugins-good = %{version}
Enhances:       gst-plugins-good

%description -n gst-plugins-good-v4l2
This package provides Video4Linux2 plugin for gst-plugins-good.
%endif

%endif

#######################################################
## Package info of Bad Plugin
#######################################################

%if "%{plugin}" == "all"
%package -n gst-plugins-bad
Summary:        GStreamer Streaming-Media Framework Plug-Ins
Group:          Multimedia/Framework
%endif

%if "%{plugin}" == "all" || "%{plugin}" == "bad"

BuildRequires:  python
BuildRequires:  xsltproc
BuildRequires:  pkgconfig(gio-2.0) >= 2.25.0
BuildRequires:  pkgconfig(libcurl) >= 7.21.0
BuildRequires:  pkgconfig(libexif) >= 0.6.16
BuildRequires:  pkgconfig(libsrtp2) >= 2.1.0
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(nice)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(orc-0.4) >= 0.4.11
BuildRequires:  pkgconfig(sndfile) >= 1.0.16
BuildRequires:  pkgconfig(soundtouch) > 1.4
%if "%{tizen_profile_name}" != "tv"
BuildRequires:  pkgconfig(srt)
%endif
%if %{with wayland}
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(wayland-client) >= 1.0.0
BuildRequires:  pkgconfig(wayland-cursor) >= 1.0.0
BuildRequires:  pkgconfig(wayland-protocols)
%endif
%if %{with x}
BuildRequires:  pkgconfig(x11)
%endif
Requires:       gstreamer >= %{version}

%description -n gst-plugins-bad
GStreamer is a streaming media framework based on graphs of filters
that operate on media data. Applications using this library can do
anything media-related,from real-time sound processing to playing
videos. Its plug-in-based architecture means that new data types or
processing capabilities can be added simply by installing new plug-ins.

%package -n gst-plugins-bad-devel
Summary:        GStreamer Streaming-Media Framework Plug-Ins
Requires:       gst-plugins-bad = %{version}-%{release}
Requires:       gst-plugins-base-devel

%description -n gst-plugins-bad-devel
GStreamer is a streaming media framework based on graphs of filters
that operate on media data. Applications using this library can do
anything media-related,from real-time sound processing to playing
videos. Its plug-in-based architecture means that new data types or
processing capabilities can be added simply by installing new plug-ins.

%endif

#######################################################
## Package info of Ugly Plugin
#######################################################

%if "%{plugin}" == "all"
%package -n gst-plugins-ugly
Summary:        GStreamer plugins from the "ugly" set
Group:          Multimedia/Framework
%endif

%if "%{plugin}" == "all" || "%{plugin}" == "ugly"

BuildRequires:  which

%description -n gst-plugins-ugly
 GStreamer is a streaming media framework, based on graphs of filters
 which operate on media data.  Applications using this library can do
 anything from real-time sound processing to playing videos, and just
 about anything else media-related.  Its plugin-based architecture means
 that new data types or processing capabilities can be added simply by
 installing new plug-ins.
 .
 This packages contains plugins from the "ugly" set, a set of
 good-quality plug-ins that might pose distribution problems.

%endif

#######################################################
## Package info of libav Plugin
#######################################################

%if "%{plugin}" == "all"
%package -n gst-libav
Summary:        Libav plugin for GStreamer
Group:          Multimedia/Framework
%endif

%if "%{plugin}" == "all" || "%{plugin}" == "libav"

BuildRequires:  bzip2-devel
BuildRequires:  gettext
BuildRequires:  which
BuildRequires:  yasm
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(orc-0.4)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(zlib)

%description -n gst-libav
This GStreamer plugin supports a large number of audio and video compression
formats through the use of the libav library.  The plugin contains GStreamer
elements for decoding 90+ formats (AVI, MPEG, OGG, Matroska, ASF, ...),
demuxing 30+ formats and colorspace conversion.

%endif

#######################################################
## Package info of rtsp-server Plugin
#######################################################

%if "%{plugin}" == "all"
%package -n gst-rtsp-server
Summary:        Multimedia Framework Library
Group:          System/Libraries
%endif

%if "%{plugin}" == "all" || "%{plugin}" == "rs"

Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description -n gst-rtsp-server
This GStreamer plugin supports a large number of audio and video compression
formats through the use of the libav library.  The plugin contains GStreamer
elements for decoding 90+ formats (AVI, MPEG, OGG, Matroska, ASF, ...),
demuxing 30+ formats and colorspace conversion.

%package -n gst-rtsp-server-devel
Summary:        Multimedia Framework RTSP server library (DEV)
Group:          Development/Libraries
Requires:       gst-rtsp-server = %{version}-%{release}

%description -n gst-rtsp-server-devel

%endif

#######################################################
## Package info of editing-services Plugin
#######################################################

%if "%{tizen_profile_name}" != "tv"

%if "%{plugin}" == "all"
%package -n gst-editing-services
Summary:        GStreamer Editing Service Plug-Ins
Group:          Multimedia/Framework
%endif

%if "%{plugin}" == "all" || "%{plugin}" == "es"

BuildRequires:  flex
BuildRequires:  gtk-doc
BuildRequires:  pkgconfig(libxml-2.0)
Requires:       gstreamer >= 1.0.0
Supplements:    gstreamer

%description -n gst-editing-services
This is a high-level library for facilitating the creation of audio/video
non-linear editors.

%package -n gst-editing-services-devel
Summary:        Development files for gst-editing-services
Requires:       gst-editing-services = %{version}-%{release}

%description -n gst-editing-services-devel
This package contains libraries and header files for
developing applications that use %{name}

%endif # plugin

%endif # profile

#######################################################
## Prep
#######################################################

%prep
%setup -q -n gstreamer-%{version}
cp %{SOURCE1001} ./gstreamer.manifest
cp %{SOURCE1001} ./gst-plugins-base.manifest
cp %{SOURCE1001} ./gst-plugins-good.manifest
cp %{SOURCE1001} ./gst-plugins-bad.manifest
cp %{SOURCE1001} ./gst-plugins-ugly.manifest
cp %{SOURCE1001} ./gst-libav.manifest
cp %{SOURCE1001} ./gst-rtsp-server.manifest
%if "%{tizen_profile_name}" != "tv"
cp %{SOURCE1001} ./gst-editing-services.manifest
%endif

#######################################################
## Build
#######################################################

%build

%if "%{plugin}" != "all"
_gst_saved_dir=$(pwd)
cd %{_source_path}
%endif

mkdir -p build
export CFLAGS="%{optflags} \
  -fno-strict-aliasing\
  -fstack-protector-strong\
  -Wl,-z,relro\
%if "%{tizen_profile_name}" == "tv"
  -Wno-declaration-after-statement\
%endif
  -D_FORTIFY_SOURCE=2"
export CXXFLAGS="$CXXFLAGS -Wno-error"
export LDFLAGS="$LDFLAGS -pthread"

meson --auto-features=disabled --prefix=/usr --libdir=%{_libdir} --datadir=%{_datadir} --sysconfdir=%{_hal_sysconfdir} \
%if "%{plugin}" == "all"
  %if "%{tizen_profile_name}" == "tv"
    -D ges=disabled \
  %endif # profile
  -D webrtc=enabled \
%endif # plugin
%if "%{plugin}" == "all" || "%{plugin}" == "core"
  -D %{_core_opt}check=enabled \
  -D %{_core_opt}coretracers=enabled \
  -D %{_core_opt}extra-checks=enabled \
  -D %{_core_opt}tools=enabled \
  %if "%{tizen_profile_name}" == "tv"
    -D %{_core_opt}tv-profile=true \
  %endif # profile
  %if "%{_enable_introspection}" == "1"
    -D %{_core_opt}introspection=enabled \
  %endif # introspection
%endif # plugin
%if "%{plugin}" == "all" || "%{plugin}" == "base"
  -D %{_base_opt}alsa=enabled \
  -D %{_base_opt}app=enabled \
  -D %{_base_opt}audioconvert=enabled \
  -D %{_base_opt}audiomixer=enabled \
  -D %{_base_opt}audiorate=enabled \
  -D %{_base_opt}audioresample=enabled \
  -D %{_base_opt}audiotestsrc=enabled \
  -D %{_base_opt}compositor=enabled \
  -D %{_base_opt}gio=enabled \
  -D %{_base_opt}gio-typefinder=enabled \
  -D %{_base_opt}ogg=enabled \
  -D %{_base_opt}opus=enabled \
  -D %{_base_opt}overlaycomposition=enabled \
  -D %{_base_opt}pbtypes=enabled \
  -D %{_base_opt}playback=enabled \
  -D %{_base_opt}rawparse=enabled \
  -D %{_base_opt}subparse=enabled \
  -D %{_base_opt}tbm=true \
  -D %{_base_opt}tcp=enabled \
  -D %{_base_opt}tools=disabled \
  -D %{_base_opt}theora=enabled \
  -D %{_base_opt}typefind=enabled \
  -D %{_base_opt}videoconvertscale=enabled \
  -D %{_base_opt}videorate=enabled \
  -D %{_base_opt}videotestsrc=enabled \
  -D %{_base_opt}volume=enabled \
  -D %{_base_opt}vorbis=enabled \
  %if "%{tizen_profile_name}" == "tv"
    -D %{_base_opt}tv-profile=true \
  %else
    -D %{_base_opt}adder=enabled \
    -D %{_base_opt}encoding=enabled \
    %if 0%{?enable_gl:1}
      -D %{_base_opt}gl=enabled \
    %endif # gl
  %endif # profile
  %if "%{_enable_introspection}" == "1"
    -D %{_base_opt}introspection=enabled \
  %endif # introspection
%endif # base plugin
%if "%{plugin}" == "all" || "%{plugin}" == "good"
  %if 0%{?ENABLE_AALIB}
    -D %{_good_opt}aalib=enabled \
  %endif
  -D %{_good_opt}adaptivedemux2=enabled \
  -D %{_good_opt}amrwbdec=enabled \
  -D %{_good_opt}apetag=enabled \
  -D %{_good_opt}audiofx=enabled \
  -D %{_good_opt}audioparsers=enabled \
  -D %{_good_opt}autodetect=enabled \
  -D %{_good_opt}avi=enabled \
  -D %{_good_opt}debugutils=enabled \
  -D %{_good_opt}deinterlace=enabled \
  -D %{_good_opt}icydemux=enabled \
  -D %{_good_opt}id3demux=enabled \
  -D %{_good_opt}interleave=enabled \
  -D %{_good_opt}isomp4=enabled \
  -D %{_good_opt}jpeg=enabled \
  -D %{_good_opt}law=enabled \
  -D %{_good_opt}pulse=enabled \
  -D %{_good_opt}replaygain=enabled \
  -D %{_good_opt}rtp=enabled \
  -D %{_good_opt}rtpmanager=enabled \
  -D %{_good_opt}rtsp=enabled \
  -D %{_good_opt}soup=enabled \
  -D %{_good_opt}tbm=true \
  -D %{_good_opt}udp=enabled \
  -D %{_good_opt}videocrop=enabled \
  -D %{_good_opt}videofilter=enabled \
  -D %{_good_opt}vpx=enabled \
  -D %{_good_opt}wavenc=enabled \
  -D %{_good_opt}wavparse=enabled \
  %if "%{_enable_v4l2h264enc}" == "1"
    -D %{_good_opt}v4l2h264enc=enabled \
  %endif
  %if "%{_enable_v4l2jpegdec}" == "1"
    -D %{_good_opt}v4l2jpegdec=enabled \
  %endif
  %if "%{tizen_profile_name}" == "tv"
    -D %{_good_opt}tv-profile=true \
    %ifnarch %{arm} aarch64
      -D %{_good_opt}v4l2=enabled \
    %endif
  %else
    -D %{_good_opt}amrnb=enabled \
    -D %{_good_opt}cairo=enabled \
    -D %{_good_opt}effectv=enabled \
    -D %{_good_opt}flv=enabled \
    -D %{_good_opt}imagefreeze=enabled \
    -D %{_good_opt}matroska=enabled \
    -D %{_good_opt}multifile=enabled \
    -D %{_good_opt}png=enabled \
    -D %{_good_opt}smpte=enabled \
    -D %{_good_opt}v4l2=enabled \
    -D %{_good_opt}v4l2-libv4l2=enabled \
    -D %{_good_opt}v4l2-probe=true \
    -D %{_good_opt}videobox=enabled \
    -D %{_good_opt}videomixer=enabled \
  %endif # profile
%endif # plugin
%if "%{plugin}" == "all" || "%{plugin}" == "bad"
  -D %{_bad_opt}aes=enabled \
  -D %{_bad_opt}audiobuffersplit=enabled \
  -D %{_bad_opt}audiolatency=enabled \
  -D %{_bad_opt}audiomixmatrix=enabled \
  -D %{_bad_opt}debugutils=enabled \
  -D %{_bad_opt}dtls=enabled \
  -D %{_bad_opt}gst_play_tests=false\
  -D %{_bad_opt}introspection=disabled \
  -D %{_bad_opt}ipcpipeline=enabled \
  -D %{_bad_opt}midi=enabled \
  -D %{_bad_opt}mpegtsdemux=enabled \
  -D %{_bad_opt}mpegtsmux=enabled \
  -D %{_bad_opt}netsim=enabled \
  -D %{_bad_opt}openal=enabled \
  -D %{_bad_opt}opus=enabled \
  -D %{_bad_opt}proxy=enabled \
  -D %{_bad_opt}sctp=enabled \
  -D %{_bad_opt}sdp=enabled \
  -D %{_bad_opt}shm=enabled \
  -D %{_bad_opt}soundtouch=enabled \
  -D %{_bad_opt}srtp=enabled \
  -D %{_bad_opt}timecode=enabled \
  -D %{_bad_opt}videoframe_audiolevel=enabled \
  -D %{_bad_opt}videoparsers=enabled \
  -D %{_bad_opt}webrtc=enabled \
  %if %{with wayland}
    -D %{_bad_opt}wayland=enabled \
  %endif
  %if "%{tizen_profile_name}" == "tv"
    -D %{_bad_opt}tv-profile=true \
  %else
    -D %{_bad_opt}autoconvert=enabled \
    -D %{_bad_opt}camerabin2=enabled \
    -D %{_bad_opt}coloreffects=enabled \
    -D %{_bad_opt}dash=enabled \
    -D %{_bad_opt}gaudieffects=enabled \
    -D %{_bad_opt}gdp=enabled \
    -D %{_bad_opt}hls=enabled \
    -D %{_bad_opt}id3tag=enabled \
    -D %{_bad_opt}jpegformat=enabled \
    -D %{_bad_opt}mpegdemux=enabled \
    -D %{_bad_opt}rist=enabled \
    -D %{_bad_opt}rtp=enabled \
    -D %{_bad_opt}srt=enabled \
    -D %{_bad_opt}smoothstreaming=enabled \
    %if 0%{?enable_gl:1}
      -D %{_bad_opt}gl=enabled \
    %endif # gl
  %endif # profile
%endif # plugin
%if "%{plugin}" == "all" || "%{plugin}" == "ugly"
  %if "%{tizen_profile_name}" == "tv"
    -D %{_ugly_opt}tv-profile=true \
  %else
    -D %{_ugly_opt}asfdemux=enabled \
  %endif # profile
%endif # plugin
%if "%{plugin}" == "all" || "%{plugin}" == "libav"
  %if "%{tizen_profile_name}" == "tv"
    -D %{_libav_opt}tv-profile=true \
  %endif # profile
%endif # plugin
%if "%{plugin}" == "all" || "%{plugin}" == "rs"
  %if "%{tizen_profile_name}" == "tv"
    -D %{_rs_opt}tv-profile=true \
  %endif # profile
  -D %{_rs_opt}introspection=disabled \
  -D %{_rs_opt}rtspclientsink=enabled \
%endif
%if "%{tizen_profile_name}" != "tv"
  %if "%{plugin}" == "all" || "%{plugin}" == "es"
    -D %{_es_opt}introspection=disabled \
    -D %{_es_opt}tools=enabled \
    -D %{_es_opt}xptv=enabled \
    -D %{_es_opt}python=enabled \
  %endif # plugin
%endif # profile
  build

ninja -C build all %{?_smp_mflags}

%if "%{plugin}" != "all"
cd "$_gst_saved_dir"
%endif

#######################################################
## Install
#######################################################

%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
ninja -C %{_source_path}/build install
mkdir -p %{buildroot}%{_datadir}/gstreamer-%{gst_branch}/presets
rm -rf %{buildroot}%{_datadir}/gstreamer-%{gst_branch}/encoding-profiles
rm -rf %{buildroot}%{_datadir}/locale

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

#######################################################
## Packaging rpms
#######################################################

###################### gstreamer ######################

%if "%{plugin}" == "all" || "%{plugin}" == "core"

%files -n gstreamer
%manifest gstreamer.manifest
%defattr(-, root, root)
%license subprojects/gstreamer/COPYING
%dir %{_datadir}/gstreamer-%{gst_branch}
%dir %{_datadir}/gstreamer-%{gst_branch}/presets
%dir %{_lib_gstreamer_dir}
%{_lib_gstreamer_dir}/libgstcoreelements.so
%{_lib_gstreamer_dir}/libgstcoretracers.so
%dir %{_libexecdir}/gstreamer-%{gst_branch}
%{_libexecdir}/gstreamer-%{gst_branch}/gst-hotdoc-plugins-scanner
%{_libexecdir}/gstreamer-%{gst_branch}/gst-plugin-scanner
%{_libexecdir}/gstreamer-%{gst_branch}/gst-completion-helper
%exclude %{_libexecdir}/gstreamer-%{gst_branch}/gst-plugins-doc-cache-generator
%{_libdir}/libgstbase-%{gst_branch}.so.*
%{_libdir}/libgstcontroller-%{gst_branch}.so.*
%{_libdir}/libgstnet-%{gst_branch}.so.*
%{_libdir}/libgstcheck-%{gst_branch}.so.*
%{_libdir}/libgstreamer-%{gst_branch}.so.*
%if "%{_enable_introspection}" == "1"
%{_lib_girepository}/Gst-%{gst_branch}.typelib
%{_lib_girepository}/GstBase-%{gst_branch}.typelib
%{_lib_girepository}/GstController-%{gst_branch}.typelib
%{_lib_girepository}/GstNet-%{gst_branch}.typelib
%{_lib_girepository}/GstCheck-%{gst_branch}.typelib
%endif #introspection
%{_datadir}/gdb/auto-load/usr/%{_lib}/libgstreamer-%{gst_branch}*-gdb.py
%{_datadir}/gstreamer-%{gst_branch}/gdb/glib_gobject_helper.py
%{_datadir}/gstreamer-%{gst_branch}/gdb/gst_gdb.py

%files -n gstreamer-utils
%manifest gstreamer.manifest
%defattr(-, root, root)
%license subprojects/gstreamer/COPYING
%{_bindir}/gst-inspect-%{gst_branch}
%{_bindir}/gst-launch-%{gst_branch}
%{_bindir}/gst-stats-%{gst_branch}
%{_bindir}/gst-typefind-%{gst_branch}
%exclude %doc %{_mandir}/man?/*-%{gst_branch}.*

%files -n gstreamer-devel
%manifest gstreamer.manifest
%defattr(-, root, root)
%{_datadir}/aclocal/gst-element-check-%{gst_branch}.m4
%{_includedir}/gstreamer-%{gst_branch}/gst/*.h
%{_includedir}/gstreamer-%{gst_branch}/gst/base/*
%{_includedir}/gstreamer-%{gst_branch}/gst/controller/*
%{_includedir}/gstreamer-%{gst_branch}/gst/net/*
%{_includedir}/gstreamer-%{gst_branch}/gst/check/*
%{_libdir}/libgstbase-%{gst_branch}.so
%{_libdir}/libgstcontroller-%{gst_branch}.so
%{_libdir}/libgstnet-%{gst_branch}.so
%{_libdir}/libgstcheck-%{gst_branch}.so
%{_libdir}/libgstreamer-%{gst_branch}.so
%{_libdir}/pkgconfig/gstreamer-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{gst_branch}.pc
%if "%{_enable_introspection}" == "1"
%{_datadir}/gir-%{gst_branch}/Gst-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstBase-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstController-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstNet-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstCheck-%{gst_branch}.gir
%endif #introspection

%changelog

%endif

###################### gst-plugins-base ######################

%if "%{plugin}" == "all" || "%{plugin}" == "base"

%files -n gst-plugins-base
%manifest gst-plugins-base.manifest
%defattr(-, root, root)
%license subprojects/gst-plugins-base/COPYING
%{_lib_gstreamer_dir}/libgstalsa.so
%{_lib_gstreamer_dir}/libgstapp.so
%{_lib_gstreamer_dir}/libgstaudioconvert.so
%{_lib_gstreamer_dir}/libgstaudiomixer.so
%{_lib_gstreamer_dir}/libgstaudiorate.so
%{_lib_gstreamer_dir}/libgstaudioresample.so
%{_lib_gstreamer_dir}/libgstaudiotestsrc.so
%{_lib_gstreamer_dir}/libgstcompositor.so
%{_lib_gstreamer_dir}/libgstgio.so
%{_lib_gstreamer_dir}/libgstogg.so
%{_lib_gstreamer_dir}/libgstopus.so
%{_lib_gstreamer_dir}/libgstoverlaycomposition.so
%{_lib_gstreamer_dir}/libgstpbtypes.so
%{_lib_gstreamer_dir}/libgstplayback.so
%{_lib_gstreamer_dir}/libgstrawparse.so
%{_lib_gstreamer_dir}/libgstsubparse.so
%{_lib_gstreamer_dir}/libgsttcp.so
%{_lib_gstreamer_dir}/libgsttheora.so
%{_lib_gstreamer_dir}/libgsttypefindfunctions.so
%{_lib_gstreamer_dir}/libgstvideoconvertscale.so
%{_lib_gstreamer_dir}/libgstvideorate.so
%{_lib_gstreamer_dir}/libgstvideotestsrc.so
%{_lib_gstreamer_dir}/libgstvolume.so
%{_lib_gstreamer_dir}/libgstvorbis.so
%if %{with x}
%{_lib_gstreamer_dir}/libgstximagesink.so
%{_lib_gstreamer_dir}/libgstxvimagesink.so
%endif
%{_libdir}/libgstallocators-%{gst_branch}.so.*
%{_libdir}/libgstapp-%{gst_branch}.so.*
%{_libdir}/libgstaudio-%{gst_branch}.so.*
%{_libdir}/libgstfft-%{gst_branch}.so.*
%{_libdir}/libgstpbutils-%{gst_branch}.so.*
%{_libdir}/libgstriff-%{gst_branch}.so.*
%{_libdir}/libgstrtp-%{gst_branch}.so.*
%{_libdir}/libgstrtsp-%{gst_branch}.so.*
%{_libdir}/libgstsdp-%{gst_branch}.so.*
%{_libdir}/libgsttag-%{gst_branch}.so.*
%{_libdir}/libgstvideo-%{gst_branch}.so.*
%if "%{tizen_profile_name}" != "tv"
%{_lib_gstreamer_dir}/libgstencoding.so
%endif #profile
%if "%{_enable_introspection}" == "1"
%{_lib_girepository}/GstAllocators-%{gst_branch}.typelib
%{_lib_girepository}/GstApp-%{gst_branch}.typelib
%{_lib_girepository}/GstAudio-%{gst_branch}.typelib
%{_lib_girepository}/GstPbutils-%{gst_branch}.typelib
%{_lib_girepository}/GstRtp-%{gst_branch}.typelib
%{_lib_girepository}/GstRtsp-%{gst_branch}.typelib
%{_lib_girepository}/GstSdp-%{gst_branch}.typelib
%{_lib_girepository}/GstTag-%{gst_branch}.typelib
%{_lib_girepository}/GstVideo-%{gst_branch}.typelib
%endif #introspection
%if 0%{?enable_gl:1}
%{_lib_gstreamer_dir}/libgstopengl.so
%{_libdir}/libgstgl-%{gst_branch}.so*
%endif # gl
%dir %{_datadir}/gst-plugins-base/
%dir %{_datadir}/gst-plugins-base/%{gst_branch}/
%{_datadir}/gst-plugins-base/%{gst_branch}/license-translations.dict

%if "%{tizen_profile_name}" != "tv"
%files -n gst-plugins-base-extension-adder
%{_lib_gstreamer_dir}/libgstadder.so
%license subprojects/gst-plugins-base/COPYING
%endif # profile

%files -n gst-plugins-base-devel
%manifest gst-plugins-base.manifest
%defattr(-, root, root)
%{_includedir}/gstreamer-%{gst_branch}/gst/allocators/*
%{_includedir}/gstreamer-%{gst_branch}/gst/app/*
%{_includedir}/gstreamer-%{gst_branch}/gst/audio/*
%{_includedir}/gstreamer-%{gst_branch}/gst/fft/*
%if 0%{?enable_gl:1}
%{_includedir}/gstreamer-%{gst_branch}/gst/gl/*
%{_libdir}/gstreamer-%{gst_branch}/include/gst/gl/*
%endif # gl
%{_includedir}/gstreamer-%{gst_branch}/gst/pbutils/*
%{_includedir}/gstreamer-%{gst_branch}/gst/riff/*
%{_includedir}/gstreamer-%{gst_branch}/gst/rtp/*
%{_includedir}/gstreamer-%{gst_branch}/gst/rtsp/*
%{_includedir}/gstreamer-%{gst_branch}/gst/sdp/*
%{_includedir}/gstreamer-%{gst_branch}/gst/tag/*
%{_includedir}/gstreamer-%{gst_branch}/gst/video/*
%if "%{plugin}" == "all" && "%{tizen_profile_name}" != "tv"
%exclude %{_includedir}/gstreamer-%{gst_branch}/gst/audio/audio-bad-prelude.h
%exclude %{_includedir}/gstreamer-%{gst_branch}/gst/audio/gstnonstreamaudiodecoder.h
%exclude %{_includedir}/gstreamer-%{gst_branch}/gst/audio/gstplanaraudioadapter.h
%endif
%{_libdir}/libgstallocators-%{gst_branch}.so
%{_libdir}/libgstapp-%{gst_branch}.so
%{_libdir}/libgstaudio-%{gst_branch}.so
%{_libdir}/libgstfft-%{gst_branch}.so
%{_libdir}/libgstpbutils-%{gst_branch}.so
%{_libdir}/libgstriff-%{gst_branch}.so
%{_libdir}/libgstrtp-%{gst_branch}.so
%{_libdir}/libgstrtsp-%{gst_branch}*.so
%{_libdir}/libgstsdp-%{gst_branch}.so
%{_libdir}/libgsttag-%{gst_branch}.so
%{_libdir}/libgstvideo-%{gst_branch}.so
%{_libdir}/pkgconfig/gstreamer-allocators-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-app-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-audio-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-fft-%{gst_branch}.pc
%if 0%{?enable_gl:1}
%{_libdir}/pkgconfig/gstreamer-gl-*.pc
%endif # gl
%{_libdir}/pkgconfig/gstreamer-pbutils-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-plugins-base-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-riff-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-rtp-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-rtsp-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-sdp-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-tag-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-video-%{gst_branch}.pc
%if "%{_enable_introspection}" == "1"
%{_datadir}/gir-%{gst_branch}/GstAllocators-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstApp-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstAudio-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstPbutils-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstRtp-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstRtsp-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstSdp-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstTag-%{gst_branch}.gir
%{_datadir}/gir-%{gst_branch}/GstVideo-%{gst_branch}.gir
%endif # introspection

%endif # plugin

###################### gst-plugins-good ######################

%if "%{plugin}" == "all" || "%{plugin}" == "good"

%files -n gst-plugins-good
%manifest gst-plugins-good.manifest
%defattr(-, root, root)
%license subprojects/gst-plugins-good/COPYING
%{_lib_gstreamer_dir}/libgstadaptivedemux2.so
%{_lib_gstreamer_dir}/libgstalaw.so
%{_lib_gstreamer_dir}/libgstamrwbdec.so
%{_lib_gstreamer_dir}/libgstapetag.so
%{_lib_gstreamer_dir}/libgstaudiofx.so
%{_lib_gstreamer_dir}/libgstaudioparsers.so
%{_lib_gstreamer_dir}/libgstautodetect.so
%{_lib_gstreamer_dir}/libgstavi.so
%{_lib_gstreamer_dir}/libgstdebug.so
%{_lib_gstreamer_dir}/libgstdeinterlace.so
%{_lib_gstreamer_dir}/libgsticydemux.so
%{_lib_gstreamer_dir}/libgstid3demux.so
%{_lib_gstreamer_dir}/libgstinterleave.so
%{_lib_gstreamer_dir}/libgstisomp4.so
%{_lib_gstreamer_dir}/libgstjpeg.so
%{_lib_gstreamer_dir}/libgstmulaw.so
%{_lib_gstreamer_dir}/libgstnavigationtest.so
%{_lib_gstreamer_dir}/libgstpulseaudio.so
%{_lib_gstreamer_dir}/libgstreplaygain.so
%{_lib_gstreamer_dir}/libgstrtp.so
%{_lib_gstreamer_dir}/libgstrtpmanager.so
%{_lib_gstreamer_dir}/libgstrtsp.so
%{_lib_gstreamer_dir}/libgstsoup.so
%{_lib_gstreamer_dir}/libgstudp.so
%{_lib_gstreamer_dir}/libgstvideocrop.so
%{_lib_gstreamer_dir}/libgstvideofilter.so
%{_lib_gstreamer_dir}/libgstvpx.so
%{_lib_gstreamer_dir}/libgstwavenc.so
%{_lib_gstreamer_dir}/libgstwavparse.so
%if %{with x}
%{_lib_gstreamer_dir}/libgstximagesrc.so
%endif # x
%if "%{tizen_profile_name}" != "tv"
%{_lib_gstreamer_dir}/libgstamrnb.so
%{_lib_gstreamer_dir}/libgsteffectv.so
%{_lib_gstreamer_dir}/libgstflv.so
%{_lib_gstreamer_dir}/libgstimagefreeze.so
%{_lib_gstreamer_dir}/libgstmatroska.so
%{_lib_gstreamer_dir}/libgstmultifile.so
%{_lib_gstreamer_dir}/libgstsmpte.so
%{_lib_gstreamer_dir}/libgstvideobox.so
%{_lib_gstreamer_dir}/libgstvideomixer.so
%exclude %{_datadir}/gstreamer-%{gst_branch}/presets/GstAmrnbEnc.prs
%else # profile
%ifnarch %{arm} aarch64
%{_lib_gstreamer_dir}/libgstvideo4linux2.so
%endif # arch
%endif # profile
%{_datadir}/gstreamer-%{gst_branch}/presets/GstQTMux.prs
%{_datadir}/gstreamer-%{gst_branch}/presets/GstVP8Enc.prs

%files -n gst-plugins-good-extra
%manifest gst-plugins-good.manifest
%defattr(-, root, root)
%license subprojects/gst-plugins-good/COPYING
%if 0%{?ENABLE_AALIB}
%{_lib_gstreamer_dir}/libgstaasink.so
%endif
%if "%{tizen_profile_name}" != "tv"
%{_lib_gstreamer_dir}/libgstpng.so
%endif

%if "%{tizen_profile_name}" != "tv"
%files -n gst-plugins-good-cairo
%manifest gst-plugins-good.manifest
%defattr(-, root, root)
%license subprojects/gst-plugins-good/COPYING
%{_lib_gstreamer_dir}/libgstcairo.so

%files -n gst-plugins-good-v4l2
%manifest gst-plugins-good.manifest
%defattr(-, root, root)
%license subprojects/gst-plugins-good/COPYING
%{_lib_gstreamer_dir}/libgstvideo4linux2.so
%endif

%endif

###################### gst-plugins-bad ######################

%if "%{plugin}" == "all" || "%{plugin}" == "bad"

%files -n gst-plugins-bad
%manifest gst-plugins-bad.manifest
%defattr(-, root, root)
%license subprojects/gst-plugins-bad/COPYING
%if "%{tizen_profile_name}" != "tv"
%{_lib_gstreamer_dir}/libgstautoconvert.so
%{_lib_gstreamer_dir}/libgstcamerabin.so
%{_lib_gstreamer_dir}/libgstcoloreffects.so
%{_lib_gstreamer_dir}/libgstdash.so
%{_lib_gstreamer_dir}/libgstgaudieffects.so
%{_lib_gstreamer_dir}/libgstgdp.so
%{_lib_gstreamer_dir}/libgsthls.so
%{_lib_gstreamer_dir}/libgstid3tag.so
%{_lib_gstreamer_dir}/libgstjpegformat.so
%{_lib_gstreamer_dir}/libgstmpegpsdemux.so
%{_lib_gstreamer_dir}/libgstrist.so
%{_lib_gstreamer_dir}/libgstsmoothstreaming.so
%{_lib_gstreamer_dir}/libgstsrt.so
%{_libdir}/libgstadaptivedemux-%{gst_branch}.so.0*
%{_libdir}/libgstbadaudio-%{gst_branch}.so.0*
%{_libdir}/libgstbasecamerabinsrc-%{gst_branch}.so.0*
%{_libdir}/libgstcuda-%{gst_branch}.so.0*
%{_libdir}/libgstinsertbin-%{gst_branch}.so.0*
%{_libdir}/libgstisoff-%{gst_branch}.so.0*
%{_libdir}/libgstphotography-%{gst_branch}.so.0*
%{_libdir}/libgstplay-%{gst_branch}.so.0*
%{_libdir}/libgstplayer-%{gst_branch}.so.0*
%{_libdir}/libgsturidownloader-%{gst_branch}.so.0*
%endif # profile
%{_lib_gstreamer_dir}/libgstaes.so
%{_lib_gstreamer_dir}/libgstaudiobuffersplit.so
%{_lib_gstreamer_dir}/libgstaudiolatency.so
%{_lib_gstreamer_dir}/libgstaudiomixmatrix.so
%{_lib_gstreamer_dir}/libgstdebugutilsbad.so
%{_lib_gstreamer_dir}/libgstdtls.so
%{_lib_gstreamer_dir}/libgstipcpipeline.so
%{_lib_gstreamer_dir}/libgstmidi.so
%{_lib_gstreamer_dir}/libgstmpegtsdemux.so
%{_lib_gstreamer_dir}/libgstmpegtsmux.so
%{_lib_gstreamer_dir}/libgstnetsim.so
%{_lib_gstreamer_dir}/libgstnice.so
%{_lib_gstreamer_dir}/libgstopenal.so
%{_lib_gstreamer_dir}/libgstopusparse.so
%{_lib_gstreamer_dir}/libgstproxy.so
%if "%{tizen_profile_name}" != "tv"
%{_lib_gstreamer_dir}/libgstrtpmanagerbad.so
%endif
%{_lib_gstreamer_dir}/libgstsctp.so
%{_lib_gstreamer_dir}/libgstsdpelem.so
%{_lib_gstreamer_dir}/libgstshm.so
%{_lib_gstreamer_dir}/libgstsoundtouch.so
%{_lib_gstreamer_dir}/libgstsrtp.so
%{_lib_gstreamer_dir}/libgsttimecode.so
%{_lib_gstreamer_dir}/libgstvideoframe_audiolevel.so
%{_lib_gstreamer_dir}/libgstvideoparsersbad.so
%if %{with wayland}
%{_lib_gstreamer_dir}/libgstwaylandsink.so
%endif
%{_lib_gstreamer_dir}/libgstwebrtc.so
%{_libdir}/libgstcodecparsers-%{gst_branch}.so.0*
%{_libdir}/libgstcodecs-%{gst_branch}.so.0*
%{_libdir}/libgstmpegts-%{gst_branch}.so.0*
%{_libdir}/libgstsctp-%{gst_branch}.so.0*
%{_libdir}/libgsttranscoder-%{gst_branch}.so.0*
%if %{with wayland}
%{_libdir}/libgstwayland-%{gst_branch}.so.0*
%endif
%{_libdir}/libgstwebrtc-%{gst_branch}.so.0*
%{_libdir}/libgstwebrtcnice-%{gst_branch}.so.0*
%exclude %{_bindir}/gst-transcoder-%{gst_branch}

%files -n gst-plugins-bad-devel
%manifest gst-plugins-bad.manifest
%defattr(-, root, root)
%if "%{tizen_profile_name}" != "tv"
%{_includedir}/gstreamer-%{gst_branch}/gst/audio/audio-bad-prelude.h
%{_includedir}/gstreamer-%{gst_branch}/gst/audio/gstnonstreamaudiodecoder.h
%{_includedir}/gstreamer-%{gst_branch}/gst/audio/gstplanaraudioadapter.h
%{_includedir}/gstreamer-%{gst_branch}/gst/basecamerabinsrc/*
%{_includedir}/gstreamer-%{gst_branch}/gst/cuda/*
%{_includedir}/gstreamer-%{gst_branch}/gst/insertbin/*
%{_includedir}/gstreamer-%{gst_branch}/gst/interfaces/*
%{_includedir}/gstreamer-%{gst_branch}/gst/isoff/*
%{_includedir}/gstreamer-%{gst_branch}/gst/play/*
%{_includedir}/gstreamer-%{gst_branch}/gst/player/*
%{_includedir}/gstreamer-%{gst_branch}/gst/uridownloader/*
%endif
%{_includedir}/gstreamer-%{gst_branch}/gst/codecparsers/*
%{_includedir}/gstreamer-%{gst_branch}/gst/mpegts/*
%{_includedir}/gstreamer-%{gst_branch}/gst/sctp/*
%{_includedir}/gstreamer-%{gst_branch}/gst/transcoder/*
%if %{with wayland}
%{_includedir}/gstreamer-%{gst_branch}/gst/wayland/*
%endif
%{_includedir}/gstreamer-%{gst_branch}/gst/webrtc/*
%if "%{tizen_profile_name}" != "tv"
%{_libdir}/libgstadaptivedemux*.so
%{_libdir}/libgstbadaudio*.so
%{_libdir}/libgstbasecamerabinsrc*.so
%{_libdir}/libgstcuda*.so
%{_libdir}/libgstinsertbin*.so
%{_libdir}/libgstisoff*.so
%{_libdir}/libgstphotography*.so
%{_libdir}/libgstplay*.so
%{_libdir}/libgsturidownloader*.so
%endif # profile

%{_libdir}/libgstcodecparsers*.so
%{_libdir}/libgstcodecs*.so
%{_libdir}/libgstmpegts*.so
%{_libdir}/libgstsctp*.so
%{_libdir}/libgsttranscoder*.so
%if %{with wayland}
%{_libdir}/libgstwayland*.so
%endif
%{_libdir}/libgstwebrtc*.so
%{_libdir}/pkgconfig/gstreamer-codecparsers-%{gst_branch}.pc
%if "%{tizen_profile_name}" != "tv"
%{_libdir}/pkgconfig/gstreamer-bad-audio-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-cuda-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-insertbin-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-photography-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-play-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-player-%{gst_branch}.pc
%endif # profile
%{_libdir}/pkgconfig/gstreamer-mpegts-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-plugins-bad-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-sctp-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-transcoder-%{gst_branch}.pc
%if %{with wayland}
%{_libdir}/pkgconfig/gstreamer-wayland-%{gst_branch}.pc
%endif
%{_libdir}/pkgconfig/gstreamer-webrtc-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-webrtc-nice-%{gst_branch}.pc

%endif # plugin

###################### gst-plugins-ugly ######################

%if "%{plugin}" == "all" || "%{plugin}" == "ugly"

%files -n gst-plugins-ugly
%manifest gst-plugins-ugly.manifest
%defattr(-,root,root,-)
%license subprojects/gst-plugins-ugly/COPYING
%if "%{tizen_profile_name}" != "tv"
%{_lib_gstreamer_dir}/libgstasf.so
%endif # profile

%endif # plugin

######################## gst-libav ###########################

%if "%{plugin}" == "all" || "%{plugin}" == "libav"

%files -n gst-libav
%manifest gst-libav.manifest
%defattr(-,root,root,-)
%license subprojects/gst-libav/COPYING
%{_lib_gstreamer_dir}/libgstlibav.so

%endif

###################### gst-rtsp-server #######################

%if "%{plugin}" == "all" || "%{plugin}" == "rs"

%files -n gst-rtsp-server
%manifest gst-rtsp-server.manifest
%defattr(-,root,root,-)
%license subprojects/gst-rtsp-server/COPYING
%{_libdir}/libgstrtspserver*.so.*
%{_lib_gstreamer_dir}/libgstrtspclientsink.so

%files -n gst-rtsp-server-devel
%defattr(-,root,root,-)
%{_libdir}/libgstrtspserver*.so
%{_includedir}/gstreamer-%{gst_branch}/gst/rtsp-server/rtsp-*.h
%{_includedir}/gstreamer-%{gst_branch}/gst/rtsp-server/gstwfd*.h
%{_libdir}/pkgconfig/gstreamer-rtsp-server-%{gst_branch}.pc

%endif

%if "%{tizen_profile_name}" != "tv"

###################### gst-editing-services #######################

%if "%{plugin}" == "all" || "%{plugin}" == "es"

%files -n gst-editing-services
%manifest gst-editing-services.manifest
%defattr(-,root,root,-)
%license subprojects/gst-editing-services/COPYING
%{_libdir}/libges-%{gst_branch}.so.*
%{_lib_gstreamer_dir}/libgstges.so
%{_lib_gstreamer_dir}/libgstnle.so
%{_bindir}/ges-launch-%{gst_branch}

%files -n gst-editing-services-devel
%{_libdir}/libges-%{gst_branch}.so
%{_includedir}/gstreamer-%{gst_branch}/ges/*
%{_libdir}/pkgconfig/gst-editing-services-%{gst_branch}.pc

%endif # plugin

%endif # profile
