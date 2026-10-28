%bcond_without wayland
%bcond_with x

%define enable_examples       0
%define enable_ephysics       0
%define enable_elua           0
%define enable_wayland_legacy 1

# this options are for reducing packaing time
##%%define _source_payload w1.gzdio
##%%define _binary_payload w1.gzdio

# this option is for debugging
##%%define _unpackaged_files_terminate_build 0

Name:           efl
Version:        1.25.1
Release:        0
License:        LGPL-2.1+
Summary:        Enlightenment Foundation Libraries - set of libraries used (not only) by E17
Url:            http://enlightenment.org/
Group:          Graphics & UI Framework/API
Source:         %{name}-%{version}.tar.bz2
Source100:      efl.conf
Source1001:     efl.manifest

BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  gettext-tools
BuildRequires:  hyphen-devel

BuildRequires:  meson >= 0.49.0

%if %{with wayland}
BuildRequires:  pkgconfig(gles20)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-egl-tizen)
BuildRequires:  pkgconfig(text-client)
BuildRequires:  pkgconfig(xdg-shell-client)
BuildRequires:  pkgconfig(wayland-tbm-client)
BuildRequires:  pkgconfig(wayland-tbm-server)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(tizen-launch-client)
BuildRequires:  pkgconfig(tizen-remote-surface-client)
BuildRequires:  pkgconfig(tizen-policy-ext-client)
BuildRequires:  pkgconfig(wtz-foreign-client)
BuildRequires:  pkgconfig(wtz-screen-client)
BuildRequires:  pkgconfig(wtz-shell-client)
BuildRequires:  pkgconfig(wtz-video-shell-client)
BuildRequires:  pkgconfig(relative-pointer-unstable-v1-client)
BuildRequires:  pkgconfig(pointer-constraints-unstable-v1-client)
BuildRequires:  pkgconfig(pointer-warp-v1-client)
BuildRequires:  pkgconfig(cursor-shape-v1-client)
BuildRequires:  wayland-protocols
Requires:       libwayland-extension-client
Requires:       libwayland-egl-tizen
%endif

%if %{with x}
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libdri2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(libXtst)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(ibus-1.0)
%endif

BuildRequires:  pkgconfig(thorvg)
BuildRequires:  pkgconfig(rlottie)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(ttrace)

#eldbus
BuildRequires:  pkgconfig(dbus-1)

#edje
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(libpulse)

#emotion
#BuildRequires:  pkgconfig(gstreamer-1.0)
#BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)

#evas
BuildRequires:  pkgconfig(libexif)
BuildRequires:  giflib-devel
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwebpdemux)

#eeze
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(dlog)

#ecore_buffer
%if %{with x}
BuildRequires:  pkgconfig(libdri2)
BuildRequires:  pkgconfig(xshmfence)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-sync)
BuildRequires:  pkgconfig(xcb-dri3)
%endif
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(libtdm)
BuildRequires:  pkgconfig(libtdm-client)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)

BuildRequires:  pkgconfig(tizen-core)

############ efl
Provides: efl-data
Obsoletes: efl-data

%define dbus_unavailable 1

%description
EFL is a library collection providing various functionality used (not only) by
Enlightenment, Terminology, Tizen and more.

############ efl-data

%package devel
Summary: Developer files for EFL package

%description devel
This package includes developer files common to all packages.

############ Eina
%package -n eina
Summary: Data type library
Requires: %{name}-data = %{version}-%{release}
License: LGPL-2.1+

%description -n eina
Eina is a data type library.

%package -n eina-tools
Summary: Eina Tools
Group:     Graphics & UI Framework/Utilities
Requires:  eina = %{version}-%{release}
Provides:  eina-bin

%description -n eina-tools
The eina tools package the eina binary utility.

%if %enable_examples
%package -n eina-examples
Summary:  Examples for the eina package
Group:    Graphics & UI Framework/Testing
Requires: eina = %{version}-%{release}
License: LGPL-2.1+

%description -n eina-examples
Example files for eina
%endif

%package -n eina-devel
Summary:  Development components for the eina package
Group:    Graphics & UI Framework/Development
Requires: eina = %{version}-%{release}
License: LGPL-2.1+

%description -n eina-devel
Development files for eina.

############ Emile
%package -n emile
Summary: EFL serialization, compression and crypto library
Requires: %{name}-data = %{version}-%{release}

%description -n emile
EFL serialization, compression and crypto library

%package -n emile-devel
Summary:  Development components for the emile package
Group:    Graphics & UI Framework/Development
Requires: emile = %{version}-%{release}

%description -n emile-devel
Development files for emile.

############ Eet
%package -n eet
Summary: Library for speedy data storage, retrieval, and compression
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause

%description -n eet
Eet is a tiny library designed to write an arbitrary set of chunks of
data to a file and optionally compress each chunk (very much like a
zip file) and allow fast random-access reading of the file later
on. It does not do zip as a zip itself has more complexity than is
needed, and it was much simpler to implement this once here.

It also can encode and decode data structures in memory, as well as
image data for saving to eet files or sending across the network to
other machines, or just writing to arbitrary files on the system. All
data is encoded in a platform independent way and can be written and
read by any architecture.

%package -n eet-tools
Summary:   Eet Tools
Group:     Graphics & UI Framework/Utilities
Requires:  eet = %{version}-%{release}
Provides:  eet-bin
License: BSD-2-Clause

%description -n eet-tools
The eet tools package the eet binary utility.

%if %enable_examples
%package -n eet-examples
Summary:  Examples for the eet package
Group:    Graphics & UI Framework/Testing
Requires: eet = %{version}-%{release}

%description -n eet-examples
Example files for eet
%endif

%package -n eet-devel
Summary:  Development components for the eet package
Group:    Graphics & UI Framework/Development
Requires: eet = %{version}-%{release}
License: BSD-2-Clause

%description -n eet-devel
Development files for eet

############ Eo
%package -n eo
Summary: EFL generic object system library
Requires: %{name}-data = %{version}-%{release}

%description -n eo
The Eo generic object system. It was designed to be the base object
system for the EFL.

%if %enable_examples
%package -n eo-examples
Summary:  Examples for the eo package
Group:    Graphics & UI Framework/Testing
Requires: eo = %{version}-%{release}

%description -n eo-examples
Example files for eo
%endif
%package -n eo-devel
Summary:  Development components for the eo package
Group:    Graphics & UI Framework/Development
Requires: eo = %{version}-%{release}
License: BSD-2-Clause

%description -n eo-devel
Development files for eo

############ Ector
%package -n ector
Summary: vector graphics library
Requires: %{name}-data = %{version}-%{release}
License: FTL or GPL-2.0+

%description -n ector
vector graphics library.

%package -n ector-devel
Summary:  Development components for the ector package
Group:    Graphics & UI Framework/Development
Requires: ector = %{version}-%{release}
License: FTL or GPL-2.0+

%description -n ector-devel
Development files for ector

############ Evas
%package -n evas
Summary: Multi-platform canvas library
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and Zlib

%description -n evas
Evas is a clean display canvas API for several target display systems
that can draw anti-aliased text, smooth super and sub-sampled scaled
images, alpha-blend objects much and more.

%if %enable_examples
%package -n evas-examples
Summary:  Examples for the evas package
Group:    Graphics & UI Framework/Testing
Requires: evas = %{version}-%{release}
License: BSD-2-Clause and Zlib

%description -n evas-examples
Example files for evas
%endif

%package -n evas-devel
Summary:  Development components for the evas package
Group:    Graphics & UI Framework/Development
Requires: evas = %{version}-%{release}
License: BSD-2-Clause and Zlib

%description -n evas-devel
Development files for evas

############ Ecore
%package -n ecore
Summary: Enlightened Core X interface library
Requires: ecore-core
Requires: ecore-audio
Requires: ecore-buffer
Requires: ecore-con
Requires: ecore-evas
Requires: ecore-file
Requires: ecore-imf
Requires: ecore-imf-evas
Requires: ecore-input
Requires: ecore-input-evas
Requires: ecore-ipc
%if %{with wayland}
Requires: ecore-wl2
%if %enable_wayland_legacy
Requires: ecore-wayland
%endif
%endif
%if %{with x}
Requires: ecore-x
Requires: ecore-avahi
%endif
License: BSD-2-Clause and MIT

%description -n ecore
Ecore is the event/X abstraction layer that makes doing selections,
Xdnd, general X stuff, event loops, timeouts and idle handlers fast,
optimized, and convenient.

%package -n ecore-devel
Summary:  Development components for the ecore package
Group:    Graphics & UI Framework/Development
Requires: ecore-core-devel
Requires: ecore-audio-devel
Requires: ecore-buffer-devel
Requires: ecore-con-devel
Requires: ecore-evas-devel
Requires: ecore-file-devel
Requires: ecore-imf-devel
Requires: ecore-imf-evas-devel
Requires: ecore-input-devel
Requires: ecore-input-evas-devel
Requires: ecore-ipc-devel
%if %{with wayland}
Requires: ecore-wl2-devel
%if %enable_wayland_legacy
Requires: ecore-wayland-devel
%endif
%endif
%if %{with x}
Requires: ecore-x-devel
Requires: ecore-avahi-devel
%endif
License: BSD-2-Clause and MIT

%description -n ecore-devel
Development files for ecore

%package -n ecore-core
Summary:  Enlightened Core X interface library - core
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-core
This is the core main-loop, system events and execution layer. This
handles running the main loop, integrating with external data and
timing sources (the system clock, file descriptors, system signals),
and producing an event queue, walking that queue and dispatching
events to appropriate callbacks.

%package -n ecore-core-devel
Summary:  Development components for the ecore-core package
Group:    Graphics & UI Framework/Development
Requires: ecore-core = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-core-devel
Development files for ecore-core

%package -n ecore-audio
Summary: Enlightened Core X interface library - audio
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-audio
This library provides an API for audio playback and recording. It uses
pulse audio underneath to handle mixing and policies. The API for this
should not be considered stable right now because it relies on EO and
EO is not considered finalized yet.

%package -n ecore-audio-devel
Summary:  Development components for the ecore_audio package
Group:    Graphics & UI Framework/Development
Requires: ecore-audio = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-audio-devel
Development files for ecore_audio

%if %{with x}
%package -n ecore-avahi
Summary: Enlightened Core X interface library - avahi
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-avahi
Avahi main loop integration function.

%package -n ecore-avahi-devel
Summary:  Development components for the ecore_avahi package
Group:    Graphics & UI Framework/Development
Requires: ecore-avahi = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-avahi-devel
Development files for ecore_avahi
%endif

%package -n ecore-buffer
Summary: Enlightened Core X interface library - buffer
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-buffer
The Ecore Buffer is an abstraction of graphic buffer.
This library also provides simple mechanisms for sharing graphic buffer bet-
ween processes using wayland socket. Ecore Buffer Queue is for this
function, and it consists of two main object,
The Ecore_Buffer_Consumer and the Ecore_Buffer_Provider.

%package -n ecore-buffer-devel
Summary:  Development components for the ecore_buffer package
Group:    Graphics & UI Framework/Development
Requires: ecore-buffer = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-buffer-devel
Development files for ecore_buffer

%package -n ecore-con
Summary: Enlightened Core X interface library - con
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-con
This provides a completely event-based TCP/UDP and Unix domain socket
API that integrates with the main-loop. This means no blocking to send
or receive data, supporting "infinite send buffers" with storage and
spooling being done by Ecore Con. It also supports SSL encryption
transparently turned on or not on the same connection, certificate
verification, CURL wrapping for HTTP connection usage (GETs, POSTs
etc.), asynchronous DNS lookups and provides the ability to also be a
server, not just a client, with the same event-based API.

%package -n ecore-con-devel
Summary:  Development components for the ecore_con package
Group:    Graphics & UI Framework/Development
Requires: ecore-con = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-con-devel
Development files for ecore_con

%package -n ecore-evas
Summary: Enlightened Core X interface library - evas
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-evas
This acts as glue between the display target (X11, Wayland,
Frame buffer, Cocoa on OSX, Win32 etc.) and Evas. It creates/provides a
target for Evas to render to (a Window or Surface etc.) and feeds
input events (Keyboard, Mouse, Multi-touch) into Evas, which then
selects the target object and calls the callbacks. It also provides
wrappers/glue for manipulating the Window/Surface.

%package -n ecore-evas-devel
Summary:  Development components for the ecore_evas package
Group:    Graphics & UI Framework/Development
Requires: ecore-evas = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-evas-devel
Development files for ecore_evas


%package -n ecore-file
Summary: Enlightened Core X interface library - file
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-file
This provides file access convenience APIs for doing simple file
operations like renames, copies, listing directories and more. It also
supports file change monitoring and URL downloads.

%package -n ecore-file-devel
Summary:  Development components for the ecore_file package
Group:    Graphics & UI Framework/Development
Requires: ecore-file = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-file-devel
Development files for ecore_file

%package -n ecore-imf
Summary: Enlightened Core X interface library - imf
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-imf
This is an input method abstraction framework to allow EFL to talk to
things like SCIM, IBus, Wayland and XIM. This allows for complex text
entry in languages such as Chinese, Japanese and Korean.

%package -n ecore-imf-devel
Summary:  Development components for the ecore_imf package
Group:    Graphics & UI Framework/Development
Requires: ecore-imf = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-imf-devel
Development files for ecore_imf

%package -n ecore-imf-evas
Summary: Enlightened Core X interface library - imf_evas
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-imf-evas
This library glues Input method support from Ecore IMF and Evas
together.

%package -n ecore-imf-evas-devel
Summary:  Development components for the ecore_imf_evas package
Group:    Graphics & UI Framework/Development
Requires: ecore-imf-evas = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-imf-evas-devel
Development files for ecore_imf_evas

%package -n ecore-input
Summary: Enlightened Core X interface library - input
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-input
This acts as a generic input layer where multiple display systems can
post events in the same format to the event queue.

%package -n ecore-input-devel
Summary:  Development components for the ecore_input package
Group:    Graphics & UI Framework/Development
Requires: ecore-input = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-input-devel
Development files for ecore_input

%package -n ecore-input-evas
Summary: Enlightened Core X interface library - input_evas
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-input-evas
This Routes events from Ecore Input into a given Evas canvas which
will then route the event further to the destination object and
callbacks.

%package -n ecore-input-evas-devel
Summary:  Development components for the ecore_input_evas package
Group:    Graphics & UI Framework/Development
Requires: ecore-input-evas = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-input-evas-devel
Development files for ecore_input_evas

%package -n ecore-ipc
Summary: Enlightened Core X interface library - ipc
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-ipc
This acts as a layer on top of Ecore Con which handles entire IPC
message packets, dealing with header delta compression and
portability, as well as ensuring an entire message is received in one
go as a single IPC message, regardless of payload data size. The
entire API is event based almost exactly like Ecore Con and thus it
supports all the transport layers Ecore Con supports.

%package -n ecore-ipc-devel
Summary:  Development components for the ecore_ipc package
Group:    Graphics & UI Framework/Development
Requires: ecore-ipc = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-ipc-devel
Development files for ecore_ipc

%if %{with x}
%package -n ecore-x
Summary: Enlightened Core X interface library - x
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-x
This is a library to wrap/deal with Xlib as well as optionally XCB to
make dealing with X11 less painful and less footwork as well as being
glue to tie these into the Ecore main-loop and event queue.

%package -n ecore-x-devel
Summary:  Development components for the ecore_x package
Group:    Graphics & UI Framework/Development
Requires: ecore-x = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-x-devel
Development files for ecore_x
%endif

############ Eldbus
%package -n eldbus
Summary: D-Bus bindings for EFL
Requires: %{name}-data = %{version}-%{release}
License: LGPL-2.1+

%description -n eldbus
Eldbus allows connecting to both system and session buses acting as
both client and service roles.

This is a replacement for old library "edbus". Its main purpose is to
fix some core bugs and completely encapsulating D-Bus without exposing
libdbus to end-user. One day libdbus may be completely removed as a
dependency.

%if %enable_examples
%package -n eldbus-examples
Summary:  Examples for the eldbus package
Group:    Graphics & UI Framework/Testing
Requires: eldbus = %{version}-%{release}
License: LGPL-2.1+

%description -n eldbus-examples
Example files for eldbus
%endif

%package -n eldbus-devel
Summary:  Development components for the eldbus package
Group:    Graphics & UI Framework/Development
Requires: eldbus = %{version}-%{release}
License: LGPL-2.1+

%description -n eldbus-devel
Development files for eldbus

############ Embryo
%package -n embryo
Summary: A small virtual machine engine (in a library) and bytecode compiler
Requires: %{name}-data = %{version}-%{release}
Provides: embryo-bin
License: BSD-2-Clause

%description -n embryo
Embryo is a tiny library designed as a virtual machine to interpret a
limited set of small compiled programs.

%package -n embryo-devel
Summary:  Development components for the embryo package
Group:    Graphics & UI Framework/Development
Requires: embryo = %{version}-%{release}
License: BSD-2-Clause

%description -n embryo-devel
Development files for embryo

############ Eio
%package -n eio
Summary: Enlightenment Input/Output Library
Requires: %{name}-data = %{version}-%{release}
License: LGPL-2.1+

%description -n eio
Enlightenment Input/Output Library

%if %enable_examples
%package -n eio-examples
Summary:  Examples for the eio package
Group:    Graphics & UI Framework/Testing
Requires: eio = %{version}-%{release}
License: LGPL-2.1+

%description -n eio-examples
Example files for eio
%endif

%package -n eio-devel
Summary:  Development components for the eio package
Group:    Graphics & UI Framework/Development
Requires: eio = %{version}-%{release}
License: LGPL-2.1+

%description -n eio-devel
Development files for eio

############ Ephysics
%if %enable_ephysics
%package -n ephysics
Summary: EFL wrapper for the Bullet Physics library
License: BSD-2-Clause

%description -n ephysics
EPhysics is a library that makes it easy to use Ecore, Evas and Bullet
Physics together. It's a kind of wrapper, a glue, between these libraries.
It's not intended to be a physics library (we already have many out there).

Enlightenment Input/Output Library

%if %enable_examples
%package -n ephysics-examples
Summary:  Examples for the ephysics package
Group:    Graphics & UI Framework/Testing
Requires: ephysics = %{version}-%{release}
License: BSD-2-Clause

%description -n ephysics-examples
Example files for ephysics
%endif

%package -n ephysics-devel
Summary:  Development components for the ephysics package
Group:    Graphics & UI Framework/Development
Requires: ephysics = %{version}-%{release}
License: BSD-2-Clause

%description -n ephysics-devel
Development files for ephysics
%endif

############ Edje
%package -n edje
Summary: Complex Graphical Design/Layout Engine
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause

%description -n edje
Edje is a complex graphical design and layout engine. It provides a
mechanism for allowing configuration data to define visual elements in
terms of layout, behavior, and appearance.  Edje allows for multiple
collections of layouts in one file, allowing a complete set of images,
animations, and controls to exist as a unified whole.

Edje separates the arrangement, appearance, and behavior logic into
distinct independent entities.  This allows visual objects to share
image data and configuration information without requiring them to do
so.  This separation and simplistic event driven style of programming
can produce almost any look and feel one could want for basic visual
elements. Anything more complex is likely the domain of an application
or widget set that may use Edje as a conveneient way of being able to
configure parts of the display.

%package -n edje-tools
Summary:   Edje tools
Group:     Graphics & UI Framework/Utilities
Requires:  edje = %{version}-%{release}
Provides:  edje-bin
License: BSD-2-Clause and GPL-2.0+

%description -n edje-tools
The edje tools package include the compiler, decompiler, visualizer, code
generator and more.

%if %enable_examples
%package -n edje-examples
Summary:  Examples for the edje package
Group:    Graphics & UI Framework/Testing
Requires: edje = %{version}-%{release}
License: BSD-2-Clause and GPL-2.0+

%description -n edje-examples
Example files for edje
%endif

%package -n edje-devel
Summary:  Development components for the edje package
Group:    Graphics & UI Framework/Development
Requires: edje = %{version}-%{release}
Requires: edje-tools = %{version}-%{release}
License: BSD-2-Clause and GPL-2.0+

%description -n edje-devel
Development files for edje

############ Eeze
%package -n eeze
Summary: Device convenience library
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause

%description -n eeze
Eeze is a library for manipulating devices through udev with a simple
and fast api. It interfaces directly with libudev, avoiding such
middleman daemons as udisks/upower or hal, to immediately gather
device information the instant it becomes known to the system.  This
can be used to determine such things as:
  * If a cdrom has a disk inserted
  * The temperature of a cpu core
  * The remaining power left in a battery
  * The current power consumption of various parts
  * Monitor in realtime the status of peripheral devices

Each of the above examples can be performed by using only a single
eeze function, as one of the primary focuses of the library is to
reduce the complexity of managing devices.

%package -n eeze-devel
Summary:  Development components for the eeze package
Group:    Graphics & UI Framework/Development
Requires: eeze = %{version}-%{release}
License: BSD-2-Clause

%description -n eeze-devel
Development files for eeze

############ Efreet
%package -n efreet
Summary: FreeDesktop.Org standards implementation
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause

%description -n efreet
Efreet implements the FreeDesktop.Org application and MIME-handling
standards.

%package -n efreet-devel
Summary:  Development components for the efreet package
Group:    Graphics & UI Framework/Development
Requires: efreet = %{version}-%{release}
License: BSD-2-Clause

%description -n efreet-devel
Development files for efreet

############ Emotion
%package -n emotion
Summary: EFL Media Library
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause

%description -n emotion
Emotion is a media library with support for different backends as plug-ins.

%if %enable_examples
%package -n emotion-examples
Summary:  Examples for the emotion package
Group:    Graphics & UI Framework/Testing
Requires: emotion = %{version}-%{release}

%description -n emotion-examples
Example files for emotion
%endif

%package -n emotion-devel
Summary:  Development components for the emotion package
Group:    Graphics & UI Framework/Development
Requires: emotion = %{version}-%{release}
License: BSD-2-Clause

%description -n emotion-devel
Development files for emotion

############ Ethumb
%package -n ethumb
Summary: EFL thumbnail generator library
Requires: %{name}-data = %{version}-%{release}
License: LGPL-2.1+

%description -n ethumb
Enlightenment thumbnailing library

%if %enable_examples
%package -n ethumb-examples
Summary:  Examples for the ethumb package
Group:    Graphics & UI Framework/Testing
Requires: ethumb = %{version}-%{release}
License: LGPL-2.1+

%description -n ethumb-examples
Example files for ethumb
%endif

%package -n ethumb-devel
Summary:  Development components for the ethumb package
Group:    Graphics & UI Framework/Development
Requires: ethumb = %{version}-%{release}
License: LGPL-2.1+

%description -n ethumb-devel
Development files for emotion

############ Eolian
%package -n eolian
Summary: EO object parser and C code generator
Group:    Graphics & UI Framework/Development
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause

%description -n eolian
Tool that parses Enlightenment's meta-data (.eo) filesg
and can then generate C code along with header files.

%package -n eolian-devel
Summary: Development components for the eolian package
Group:    Graphics & UI Framework/Development
Requires: eolian = %{version}-%{release}
License: BSD-2-Clause

%description -n eolian-devel
Development files for eolian

%if %enable_examples
%package -n eolian-examples
Summary:  Examples for the eolian package
Group:    Graphics & UI Framework/Testing
Requires: eolian = %{version}-%{release}
License: BSD-2-Clause

%description -n eolian-examples
Example files for eolian
%endif
############ End of Eolian

############ Elua
%if %enable_elua
%package -n elua
Summary: EFL lua binding library
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause

%description -n elua
The Elua library was created to ease integration of EFL Lua into other EFL
libraries or applications. Using the Elua library you can easily create a
Lua state that is fully set up for running EFL Lua bindings.

%package -n elua-devel
Summary: Development components for the elua package
Group:    Graphics & UI Framework/Development
Requires: elua = %{version}-%{release}
License: BSD-2-Clause

%description -n elua-devel
Development files for elua
%endif

%package -n elementary
Summary: EFL toolkit for small touchscreens
Group:    Graphics & UI Framework/Development
License:        LGPL-2.1+ and CC-BY-SA-3.0

%description -n elementary
Elementary is a widget set. It is a new-style of widget set much more canvas
object based than anything else. Why not ETK? Why not EWL? Well they both
tend to veer away from the core of Evas, Ecore and Edje a lot to build their
own worlds. Also I wanted something focused on embedded devices -
specifically small touchscreens. Unlike GTK+ and Qt, 75% of the "widget set"
is already embodied in a common core - Ecore, Edje, Evas etc. So this
fine-grained library splitting means all of this is shared, just a new
widget "personality" is on top. And that is... Elementary, my dear watson
Elementary

%package -n elementary-tizen
Summary:        EFL toolkit for small touchscreens for Tizen devices
Requires:       elementary

%description -n elementary-tizen
Elementary is a widget set. It is a new-style of widget set much more canvas
object based than anything else. Why not ETK? Why not EWL? Well they both
tend to veer away from the core of Evas, Ecore and Edje a lot to build their
own worlds. Also I wanted something focused on embedded devices -
specifically small touchscreens. Unlike GTK+ and Qt, 75% of the "widget set"
is already embodied in a common core - Ecore, Edje, Evas etc. So this
fine-grained library splitting means all of this is shared, just a new
widget "personality" is on top. And that is... Elementary, my dear watson.
Elementary. This is an alternative package for Tizen devices that uses different
set of source code.

%if %enable_examples
%package -n elementary-examples
Summary:   EFL elementary examples

%description -n elementary-examples
EFL elementary examples
%endif

%package -n elementary-tools
Summary:   EFL elementary configuration and test apps

%description -n elementary-tools
EFL elementary configuration and test apps package

%package -n elementary-devel
Summary:        Development files for elementary
Group:          Development/Libraries
Requires:       elementary = %{version}-%{release}

%description -n elementary-devel
Development components for the elementary package

%package -n elementary-theme
Summary:        Default theme for elementary

%description -n elementary-theme
Default theme which provides various styles for elementary.

%package -n efl-locale
Summary:        Translations and Locale for package %{name}
Group: Translations
AutoReqProv: 0

%description -n efl-locale
This package provides translations for package %{name}.

%if %enable_wayland_legacy
%package -n ecore-wayland
Summary: Enlightened Core X interface library - wayland
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-wayland
This is a glue/wrapper library to interface EFL to Wayland libraries
to tie them into the Ecore main-loop and event queue.

%package -n ecore-wayland-devel
Summary:  Development components for the ecore_wayland package
Group:    Graphics & UI Framework/Development
Requires: ecore-wayland = %{version}-%{release}
License: BSD-2-Clause and MIT

%description -n ecore-wayland-devel
Development files for ecore_wayland
%endif

%package -n ecore-wl2
Summary: Ecore_Wl2 provides a wrapper and convenience functions for using the Wayland protocol in implementing a window system.
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause
# i am not sure that the license is correct

%description -n ecore-wl2
Ecore_Wl2 provides a wrapper and convenience functions for using the Wayland protocol in implementing a window system.

%package -n ecore-wl2-devel
Summary: Development files for ecore-wl2
Group: Graphics & UI Framework/Development
Requires: ecore-wl2 = %{version}-%{release}
License: BSD-2-Clause

%description -n ecore-wl2-devel
Development files for ecore-wl2

%package -n efl-canvas-wl
Summary: EFL Wayland compositor widget
Requires: %{name}-data = %{version}-%{release}
License: BSD-2-Clause
# i am not sure that the license is correct

%description -n efl-canvas-wl
EFL Wayland compositor widget

%package -n efl-canvas-wl-devel
Summary: Development components for the efl-canvas-wl package
Group: Graphics & UI Framework/Development
Requires: efl-canvas-wl = %{version}-%{release}
License: BSD-2-Clause
# i am not sure that the license is correct

%description -n efl-canvas-wl-devel
Development files for efl-canvas-wl

##%%package -n elput
##%Summary: Elput provides a wrapper and functions for using libinput
##%Requires: %{name}-data = %{version}-%{release}
##%License: BSD-2-Clause
##%# i am not sure that the license is correct
##%
##%%description -n elput
##%Elput provides a wrapper and functions for using libinput
##%
##%%package -n elput-devel
##%Summary: Development components for the elput package
##%Group: Graphics & UI Framework/Development
##%Requires: elput = %{version}-%{release}
##%License: BSD-2-Clause
##%# i am not sure that the license is correct
##%
##%%description -n elput-devel
##%Development files for elput


%prep
echo "%{_buildsystem}"
%setup -q
cp %{SOURCE1001} .


%build
%if "%{tizen_profile_name}" == "tv"
        export CFLAGS="$CFLAGS -DTIZEN_PROFILE_TV"
%endif

%if ! %{with x}
CFLAGS="$CFLAGS -DMESA_EGL_NO_X11_HEADERS "
%endif

CFLAGS="$CFLAGS -DLIBDIR=\\\"%{_libdir}\\\""

%if "%{asan}" == "1"
%restore_fcommon
%endif

export CFLAGS="$CFLAGS -Wno-int-conversion -Wno-incompatible-pointer-types -Wno-implicit-function-declaration"
%if %{defined _toolchain}
%if %{toolchain_is clang}
%ifarch armv7l armv7hl
CFLAGS="$CFLAGS -fno-integrated-as"
CXXFLAGS="$CXXFLAGS -fno-integrated-as"
%endif
%endif
%endif
export XDG_RUNTIME_DIR="/tmp/"

export DESTDIR=%{buildroot}
meson setup \
    -Dtizen=true -Dtbm=true \
    -Davahi=false -Dx11=false -Dfb=true -Dwl=true -Dbuffer=true -Dphysics=false -Dopengl=es-egl \
    -Dbuild-examples=false -Dbuild-tests=false -Dgstreamer=false -Dsystemd=false -Dpulseaudio=false \
    -Dtslib=false -Dhyphen=true -Delua=false -Dwl-deprecated=true -Dbindings=[] -Dinstall-eo-files=true \
    -Dglib=true -Dexactness=false \
    -Decore-imf-loaders-disabler="xim, ibus, scim" -Dlua-interpreter=lua \
    -Demotion-loaders-disabler="gstreamer1, libvlc, xine" \
    -Devas-loaders-disabler="gst, pdf, ps, raw, rsvg, jp2k, avif" \
    -Delementary-base-dir='share/.elementary' \
    -Dtrace=none \
    --buildtype plain \
    --prefix /usr \
    --libdir %{_libdir} \
    -Dcpp_std=gnu++17 \
    -Dtizen-core=false \
    builddir 2>&1

sed -i.bak -e "s/soname,libelementary_t/soname,libelementary/g" builddir/build.ninja

ninja \
                -C builddir \
                -j %(echo "`/usr/bin/getconf _NPROCESSORS_ONLN`") \
                all

%install
export DESTDIR=%{buildroot}
ninja \
                -C builddir \
                -j %(echo "`/usr/bin/getconf _NPROCESSORS_ONLN`") \
                install

mv %{buildroot}%{_libdir}/libelementary_t.so.1.25.100 %{buildroot}%{_libdir}/libelementary.so.1.25.100
rm %{buildroot}%{_libdir}/libelementary_t.*

sed -i 's/, openssl3//g' %{buildroot}%{_libdir}/pkgconfig/*.pc

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE100 %{buildroot}%{_tmpfilesdir}/efl.conf

%find_lang %{name}

%post -n eina -p /sbin/ldconfig
%postun -n eina -p /sbin/ldconfig

%post -n emile -p /sbin/ldconfig
%postun -n emile -p /sbin/ldconfig

%post -n eet -p /sbin/ldconfig
%postun -n eet -p /sbin/ldconfig

%post -n eo -p /sbin/ldconfig
%postun -n eo -p /sbin/ldconfig

%post -n ector -p /sbin/ldconfig
%postun -n ector -p /sbin/ldconfig

%post -n evas -p /sbin/ldconfig
%postun -n evas -p /sbin/ldconfig

%post -n ecore -p /sbin/ldconfig
%postun -n ecore -p /sbin/ldconfig

%post -n eldbus -p /sbin/ldconfig
%postun -n eldbus -p /sbin/ldconfig

%post -n embryo -p /sbin/ldconfig
%postun -n embryo -p /sbin/ldconfig

%post -n eio -p /sbin/ldconfig
%postun -n eio -p /sbin/ldconfig

%post -n edje -p /sbin/ldconfig
%postun -n edje -p /sbin/ldconfig

%post -n eeze -p /sbin/ldconfig
%postun -n eeze -p /sbin/ldconfig

%post -n efreet -p /sbin/ldconfig
%postun -n efreet -p /sbin/ldconfig

%post -n emotion -p /sbin/ldconfig
%postun -n emotion -p /sbin/ldconfig

%post -n ethumb -p /sbin/ldconfig
%postun -n ethumb -p /sbin/ldconfig

%if %enable_ephysics
%post -n ephysics -p /sbin/ldconfig
%postun -n ephysics -p /sbin/ldconfig
%endif

%post -n eolian -p /sbin/ldconfig
%postun -n eolian -p /sbin/ldconfig

%post -n ecore-wl2 -p /sbin/ldconfig
%postun -n  ecore-wl2 -p /sbin/ldconfig

%post -n ecore-wayland -p /sbin/ldconfig
%postun -n  ecore-wayland -p /sbin/ldconfig

##%%post -n elput -p /sbin/ldconfig
##%%postun -n elput -p /sbin/ldconfig

%post -n efl-canvas-wl -p /sbin/ldconfig
%postun -n efl-canvas-wl -p /sbin/ldconfig

%post -n elementary
ldconfig -l %{_libdir}/libelementary.so.1.25.1

%postun -n elementary -p /sbin/ldconfig

%post -n elementary-tizen
ldconfig -l %{_libdir}/libelementary.so.1.25.100

%preun -n elementary-tizen
ldconfig -l %{_libdir}/libelementary.so.1.25.1

%postun -n elementary-tizen -p /sbin/ldconfig

%files -n %{name}
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.LGPL
%{_libdir}/libefl.so.*
%{_bindir}/efl_debug
%{_bindir}/efl_debugd
%exclude %dir /usr/lib*/debug/.build-id/*
%exclude %dir /usr/lib*/debug/*
#avahi
%if %{with x}
%exclude %{_libdir}/libecore_avahi.so.*
%exclude %{_includedir}/ecore-avahi*/
%exclude %{_libdir}/libecore_avahi.so
%exclude %{_libdir}/pkgconfig/ecore-avahi*.pc
%endif

%files -n %{name}-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/efl-*1/
%{_libdir}/cmake/Efl*/
%{_libdir}/libefl.so
%{_libdir}/pkgconfig/efl*.pc
%{_datadir}/eolian/include/efl-*1/

%files -n eina
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.LGPL
%{_libdir}/libeina.so.*

%files -n eina-tools
%manifest %{name}.manifest
%{_bindir}/eina_btlog
%exclude %{_bindir}/eina_modinfo

%if %enable_examples
%files -n eina-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/eina*/examples/
%{_libdir}/eina/examples/
%endif

%files -n eina-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/eina-*1/
%{_libdir}/libeina.so
%{_libdir}/pkgconfig/eina*.pc
%{_libdir}/cmake/Eina*/*.cmake

%files -n emile
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.LGPL
%{_libdir}/libemile.so.*

%files -n emile-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/emile-*1/
%{_libdir}/libemile.so
%{_libdir}/pkgconfig/emile*.pc
%{_libdir}/cmake/Emile*/*.cmake

%files -n eet
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libeet.so.*

%files -n eet-tools
%manifest %{name}.manifest
%{_bindir}/eet
%{_bindir}/vieet
%{_bindir}/diffeet
%{_bindir}/eetpack

%if %enable_examples
%files -n eet-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/eet/examples/
%{_libdir}/eet/examples/
%endif

%files -n eet-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libeet.so
%{_includedir}/eet-*1/
%{_libdir}/pkgconfig/eet*.pc
%{_libdir}/cmake/Eet*/*.cmake

%files -n eo
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libeo.so.*
%exclude %{_libdir}/libeo_dbg.so.*

%if %enable_examples
%files -n eo-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/eo/examples/
%{_libdir}/eo/examples/
%endif

%files -n eo-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/eo-*1/
%{_libdir}/libeo.so
%{_libdir}/pkgconfig/eo*.pc
%{_datadir}/eo/gdb/eo_gdb.py
%{_datadir}/gdb/auto-load/usr/lib*/
%{_libdir}/cmake/Eo/*.cmake
%{_libdir}/cmake/EoCxx/*.cmake
%exclude %{_libdir}/libeo_dbg.so
%exclude %{_bindir}/eo_debug

%files -n ector
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.FTL licenses/COPYING.GPL
%{_libdir}/libector.so.*

%files -n ector-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
#%{_includedir}/ector-*1/
%{_libdir}/libector.so
%{_libdir}/pkgconfig/ector*.pc
#%{_datadir}/eolian/include/ector-*1/

%files -n evas
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_bindir}/ecore_evas_*
%{_libdir}/evas/modules/
%{_libdir}/libevas.so.*
%{_datadir}/evas/checkme
%{_datadir}/evas/filters/lua/*.lua
%exclude %{_libdir}/evas/utils/

%if %enable_examples
%files -n evas-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/evas/examples/
%{_libdir}/evas/examples/
%endif

%files -n evas-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/evas-*1/
%{_libdir}/libevas.so
%{_libdir}/pkgconfig/evas*.pc
%{_datadir}/eolian/include/evas-*1/
%{_libdir}/cmake/Evas*/*.cmake

%files -n ecore
%license licenses/COPYING.BSD

%files -n ecore-devel
%{_libdir}/pkgconfig/ecore.pc

%files -n ecore-core
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore.so.*
%{_datadir}/ecore/checkme
%exclude %{_libdir}/ecore/system/upower/

%files -n ecore-core-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-*1/
%{_libdir}/libecore.so
%{_libdir}/pkgconfig/ecore-core.pc
%{_libdir}/cmake/Ecore*/*.cmake
%{_datadir}/eolian/include/ecore-*1/

%files -n ecore-audio
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_audio.so.*

%files -n ecore-audio-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-audio*/
%{_libdir}/libecore_audio.so
%{_libdir}/pkgconfig/ecore-audio*.pc

%if %{with x}
%files -n ecore-avahi
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_avahi.so.*

%files -n ecore-avahi-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-avahi*/
%{_libdir}/libecore_avahi.so
%{_libdir}/pkgconfig/ecore-avahi*.pc
%endif

%files -n ecore-buffer
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_buffer.so.*
%{_libdir}/ecore_buffer/modules/
%exclude %{_libdir}/ecore_buffer/bin/

%files -n ecore-buffer-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-buffer*/
%{_libdir}/libecore_buffer.so
%{_libdir}/pkgconfig/ecore-buffer*.pc

%files -n ecore-con
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_con.so.*
%{_tmpfilesdir}/efl.conf
%{_datadir}/ecore_con/checkme
%exclude %{_libdir}/ecore_con/utils/

%files -n ecore-con-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-con*/
%{_libdir}/libecore_con.so
%{_libdir}/pkgconfig/ecore-con*.pc

%files -n ecore-evas
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_evas.so.*
%{_libdir}/ecore_evas/engines/*/*/module.so

%files -n ecore-evas-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-evas*/
%{_libdir}/libecore_evas.so
%{_libdir}/pkgconfig/ecore-evas*.pc


%files -n ecore-file
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_file.so.*

%files -n ecore-file-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-file*/*.h
%{_libdir}/libecore_file.so
%{_libdir}/pkgconfig/ecore-file*.pc

%files -n ecore-imf
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_imf.so.*
%{_datadir}/ecore_imf/checkme
%exclude %{_libdir}/ecore_imf/modules/

%files -n ecore-imf-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-imf-*1/
%{_libdir}/libecore_imf.so
%{_libdir}/pkgconfig/ecore-imf.pc

%files -n ecore-imf-evas
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_imf_evas.so.*

%files -n ecore-imf-evas-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-imf-evas*/
%{_libdir}/libecore_imf_evas.so
%{_libdir}/pkgconfig/ecore-imf-evas.pc

%files -n ecore-input
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_input.so.*

%files -n ecore-input-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-input-*1/
%{_libdir}/libecore_input.so
%{_libdir}/pkgconfig/ecore-input.pc

%files -n ecore-input-evas
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_input_evas.so.*

%files -n ecore-input-evas-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-input-evas*/
%{_libdir}/libecore_input_evas.so
%{_libdir}/pkgconfig/ecore-input-evas.pc

%files -n ecore-ipc
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_ipc.so.*

%files -n ecore-ipc-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-ipc-*1/
%{_libdir}/libecore_ipc.so
%{_libdir}/pkgconfig/ecore-ipc.pc

%if %{with wayland}
%if %enable_wayland_legacy
%files -n ecore-wayland
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_wayland.so.*

%files -n ecore-wayland-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-wayland-*1/
%{_libdir}/libecore_wayland.so
%{_libdir}/pkgconfig/ecore-wayland.pc
%endif

%files -n ecore-wl2
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_wl2.so.*
%{_libdir}/ecore_wl2/engines/*/*/module.so

%files -n ecore-wl2-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-wl2-*1/
%{_libdir}/libecore_wl2.so
%{_libdir}/pkgconfig/ecore-wl2.pc
%endif

%exclude %{_libdir}/libecore_fb.so
%exclude %{_libdir}/libecore_fb.so.*
%exclude %{_libdir}/pkgconfig/ecore-fb.pc

%if %{with x}
%files -n ecore-x
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libecore_x.so.*
%{_libdir}/ecore_x/*/*/*
%{_datadir}/ecore_x/checkme

%files -n ecore-x-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ecore-x-*1/
%{_libdir}/libecore_x.so
%{_libdir}/pkgconfig/ecore-x.pc
%endif

%files -n eldbus
%manifest %{name}.manifest
%license licenses/COPYING.LGPL
%defattr(-,root,root,-)
%{_libdir}/libeldbus.so.*
%{_bindir}/eldbus*


%if %enable_examples
%files -n eldbus-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/eldbus/examples/*
%{_libdir}/eldbus/examples/*
%endif

%files -n eldbus-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libeldbus.so
%{_includedir}/eldbus*/
%{_libdir}/pkgconfig/eldbus*.pc
%{_libdir}/cmake/Eldbus/*.cmake
#%{_datadir}/eolian/include/eldbus-*1/

%files -n embryo
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.SMALL
%{_bindir}/embryo_cc
%{_libdir}/libembryo.so.*
%{_datadir}/embryo/include/default.inc

%files -n embryo-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/embryo-*1/
%{_libdir}/libembryo.so
%{_libdir}/pkgconfig/embryo*.pc

%files -n eio
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.LGPL
%{_libdir}/libeio.so.*

%if %enable_examples
%files -n eio-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/eio/examples/
%{_libdir}/eio/examples/
%endif

%files -n eio-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/eio-*1/
%{_libdir}/libeio.so
%{_libdir}/pkgconfig/eio*.pc
%{_libdir}/cmake/Eio*/*.cmake

%files -n edje
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libedje.so.*
%{_libdir}/edje/utils/
%{_datadir}/edje/include/edje.inc
%{_datadir}/edje/images/
%{_datadir}/mime/packages/edje.xml

%files -n edje-tools
%manifest %{name}.manifest
%{_bindir}/edje*

%if %enable_examples
%files -n edje-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/edje/examples/
%{_libdir}/edje/examples/
%endif

%files -n edje-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/edje-*1/
%{_libdir}/libedje.so
%{_libdir}/pkgconfig/edje*.pc
%{_libdir}/cmake/Edje/*.cmake
%{_datadir}/eolian/include/edje-*1/

%files -n eeze
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libeeze.so.*
%{_datadir}/eeze/checkme
%{_bindir}/eeze_disk_ls
%{_bindir}/eeze_mount
%{_bindir}/eeze_umount
%{_libdir}/eeze/modules/sensor/
%exclude %{_bindir}/eeze_scanner
%exclude %{_bindir}/eeze_scanner_monitor

%files -n eeze-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/eeze-*1/
%{_libdir}/libeeze.so
%{_libdir}/pkgconfig/eeze*.pc
%{_libdir}/cmake/Eeze/*.cmake

%files -n efreet
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libefreet.so.*
%{_libdir}/libefreet_mime.so.*
%{_libdir}/libefreet_trash.so.*
%{_libdir}/efreet/*/efreet_desktop_cache_create
%{_libdir}/efreet/*/efreet_icon_cache_create
%{_datadir}/efreet/
%exclude %{_bindir}/efreetd
%exclude %{_libdir}/efreet/*/efreet_mime_cache_create

%files -n efreet-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/efreet-*1/
%{_libdir}/libefreet.so
%{_libdir}/libefreet_mime.so
%{_libdir}/libefreet_trash.so
%{_libdir}/pkgconfig/efreet*.pc
%{_libdir}/cmake/Efreet/*.cmake

%files -n emotion
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libemotion.so.*
%{_libdir}/edje/modules/emotion/
%{_datadir}/emotion/
%{_libdir}/emotion/modules/

%if %enable_examples
%files -n emotion-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/emotion/examples/
%{_libdir}/emotion/examples/
%endif

%files -n emotion-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/emotion-*1/
%{_libdir}/libemotion.so
%{_libdir}/pkgconfig/emotion*.pc
%{_libdir}/cmake/Emotion/*.cmake

%files -n ethumb
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libethumb.so.*
%{_libdir}/libethumb_client.so.*
%{_datadir}/ethumb_client/
%{_datadir}/ethumb/
%{_libdir}/ethumb/modules/
%exclude %{_datadir}/dbus-1/services/org.enlightenment.Ethumb.service
%exclude %{_libdir}/ethumb_client/utils/*/ethumbd_slave
%exclude %{_bindir}/ethumb
%exclude %{_bindir}/ethumbd
%exclude %{_bindir}/ethumbd_client

%if %enable_examples
%files -n ethumb-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/ethumb_client/examples/
%{_libdir}/ethumb_client/examples/
%endif

%files -n ethumb-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ethumb-*1/
%{_libdir}/libethumb.so
%{_libdir}/libethumb_client.so
%{_libdir}/pkgconfig/ethumb*.pc
%{_libdir}/cmake/Ethumb/*.cmake
%{_libdir}/cmake/EthumbClient/*.cmake

%if %enable_ephysics
%files -n ephysics
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_libdir}/libephysics.so.*

%files -n ephysics-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libephysics.so
%{_libdir}/pkgconfig/ephysics.pc
%{_includedir}/ephysics-*1/

%if %enable_examples
%files -n ephysics-examples
%{_datadir}/ephysics/examples/
%endif
%endif

%files -n eolian
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license licenses/COPYING.BSD
%{_bindir}/eolian*
%{_libdir}/libeolian.so.*

%files -n eolian-devel
%{_includedir}/eolian-*1/
%{_datadir}/eolian/include/
%{_libdir}/libeolian.so
%{_libdir}/cmake/Eolian*/*.cmake

%if %enable_examples
%files -n eolian-examples
%{_datadir}/eolian_*/examples/
%endif

%if %enable_elua
%files -n elua
%manifest %{name}.manifest
%license licenses/COPYING.BSD
%defattr(-,root,root,-)
%{_datadir}/elua/checkme

%files -n elua-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/cmake/Elua*/*.cmake
%endif

%files -n efl-canvas-wl
%manifest %{name}.manifest
%license licenses/COPYING.BSD
%defattr(-,root,root,-)
%{_libdir}/libefl_canvas_wl.so.*
%exclude %{_bindir}/efl_canvas_wl_test
%exclude %{_bindir}/efl_canvas_wl_test_stack

%files -n efl-canvas-wl-devel
%manifest %{name}.manifest
%license licenses/COPYING.BSD
%defattr(-,root,root,-)
%{_libdir}/libefl_canvas_wl.so
%{_includedir}/efl-canvas-wl-*1/
%{_libdir}/pkgconfig/efl-canvas-wl.pc

##%%files -n elput
##%%manifest %{name}.manifest
##%%license licenses/COPYING.BSD
##%%defattr(-,root,root,-)
##%%{_libdir}/libelput.so.*
##%
##%%files -n elput-devel
##%%manifest %{name}.manifest
##%%license licenses/COPYING.BSD
##%%defattr(-,root,root,-)
##%%{_libdir}/libelput.so
##%%{_libdir}/pkgconfig/elput.pc
##%%{_includedir}/elput-*1/

%files -n elementary
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/elementary_quicklaunch
%{_bindir}/elementary_run
%{_libdir}/edje/modules/elm/
%{_libdir}/libelementary.so.1
%{_libdir}/libelementary.so.1.25.1
%{_datadir}/elementary/edje_externals/
%{_datadir}/icons/hicolor/128x128/apps/elementary.png
%{_libdir}/elementary/modules/
%exclude %{_datadir}/elementary/config/

%files -n elementary-tizen
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libelementary.so.1.25.100

%if ! %dbus_unavailable
%if %enable_examples
%files -n elementary-examples
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/elementary/examples/
%endif
%endif

%files -n elementary-tools
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/applications/
%{_datadir}/elementary/images/
%{_datadir}/elementary/objects/
%{_bindir}/elementary_*
%exclude %{_bindir}/elm_prefs_cc
%exclude %{_bindir}/elementary_perf

%files -n elementary-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/elementary-*1/
%{_libdir}/libelementary.so
%{_libdir}/pkgconfig/elementary.pc
%{_libdir}/cmake/Elementary/ElementaryConfig.cmake
%{_libdir}/cmake/Elementary/ElementaryConfigVersion.cmake
%{_datadir}/eolian/include/elementary-*1/

%files -n elementary-theme
%manifest %{name}.manifest
%{_datadir}/elementary/themes/
%exclude %{_datadir}/elementary/test*

%files -n efl-locale -f %{name}.lang
%license COPYING
%defattr(-,root,root,-)

