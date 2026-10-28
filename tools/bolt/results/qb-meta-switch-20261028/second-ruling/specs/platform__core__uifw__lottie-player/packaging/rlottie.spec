Name:       lottie-player
Summary:    Platform independent standalone library that plays Lottie Animation
Version:    0.2.5
Release:    1
Group:      UI Framework/Services
License:    MIT and BSD and MPL-2.0
URL:        http://www.tizen.org/
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  pkgconfig(dlog)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
rlottie is a platform independent standalone c++ library for rendering vector
based animations and art in realtime.

Lottie loads and renders animations and vectors exported in the bodymovin JSON
format. Bodymovin JSON can be created and exported from After Effects with
bodymovin, Sketch with Lottie Sketch Export, and from Haiku.

For the first time, designers can create and ship beautiful animations without
an engineer painstakingly recreating it by hand. Since the animation is backed
by JSON they are extremely small in size but can be large in complexity!


%package devel
Summary:    Development libraries for rlottie
Group:      UI Frameork/Services
Requires:   %{name} = %{version}-%{release}


%description devel
rlottie is a platform independent standalone c++ library for rendering vector
based animations and art in realtime.

Lottie loads and renders animations and vectors exported in the bodymovin JSON
format. Bodymovin JSON can be created and exported from After Effects with
bodymovin, Sketch with Lottie Sketch Export, and from Haiku.

For the first time, designers can create and ship beautiful animations without
an engineer painstakingly recreating it by hand. Since the animation is backed
by JSON they are extremely small in size but can be large in complexity!


%prep
%setup -q


%build

export DESTDIR=%{buildroot}

export CXXFLAGS+=" -std=gnu++14"

%{?_toolchain:
%ifarch %arm
%if %{toolchain_is clang}
CXXFLAGS+=" -fno-integrated-as"
%endif
%endif
}

meson setup \
                --prefix /usr \
                --libdir %{_libdir} \
                builddir 2>&1
ninja \
      -C builddir \
      -j %(echo "`/usr/bin/getconf _NPROCESSORS_ONLN`")

%install

export DESTDIR=%{buildroot}

ninja -C builddir install

%files
%defattr(-,root,root,-)
%{_libdir}/librlottie.so.*
%{_libdir}/librlottie-image-loader.so*
%manifest packaging/rlottie.manifest
%license COPYING licenses/COPYING*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/librlottie.so
%{_libdir}/librlottie-image-loader.so

%{_libdir}/pkgconfig/rlottie.pc
