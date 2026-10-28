%define __spec_check_pre exit 0

Name:           orc
Version:        0.4.40
Release:        0
Summary:        The Oil Runtime Compiler
License:        BSD-3-Clause
Group:          Multimedia/Libraries
URL:            https://gitlab.freedesktop.org/gstreamer/orc

Source:         https://gstreamer.freedesktop.org/src/orc/%{name}-%{version}.tar.xz
Source99:       baselibs.conf
Source1001:     orc.manifest

#BuildRequires:  gtk-doc >= 1.12
BuildRequires:  meson >= 0.47.0
#BuildRequires:  pkgconfig(glib-2.0)
Provides:       %{name}-devel = %{version}

%description
Orc is a library and set of tools for compiling and executing very simple
programs that operate on arrays of data.  The “language” is a generic
assembly language that represents many of the features available in SIMD
architectures, including saturated addition and subtraction, and many
arithmetic operations.

%package -n liborc
Summary:        The Oil Runtime Compiler Library
Group:          Multimedia/Libraries

%description -n liborc
Orc is a library and set of tools for compiling and executing very simple
programs that operate on arrays of data.  The “language” is a generic
assembly language that represents many of the features available in SIMD
architectures, including saturated addition and subtraction, and many
arithmetic operations.

%prep
%setup -q
cp %{SOURCE1001} .

%build
meson --prefix /usr --libdir %{_libdir} build \
	-Dorc-test=disabled \
	-Dexamples=disabled \
	-Dtests=disabled \
	-Dgtk_doc=disabled
ninja -C build all

%install
export DESTDIR=%{buildroot}
ninja -C build install

%post -n liborc -p /sbin/ldconfig
%postun -n liborc -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/orcc
%{_includedir}/orc-0.4/
%{_libdir}/*.so
%{_libdir}/pkgconfig/orc-0.4.pc

%files -n liborc
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/liborc-0.4.so.*
