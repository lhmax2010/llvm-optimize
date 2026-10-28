Name:           harfbuzz
Version:        8.2.2
Release:        0
License:        MIT and ISC
Summary:        An OpenType text shaping engine
Url:            http://www.freedesktop.org/wiki/Software/HarfBuzz
Group:          Graphics/Font Management
Source:         %{name}-%{version}.tar.xz
Source99:       baselibs.conf
Source1001: 	harfbuzz.manifest
BuildRequires:  gcc-c++
#BuildRequires:  pkgconfig(cairo) >= 1.8.0
#BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(freetype2) >= 2.3.8
BuildRequires:  pkgconfig(glib-2.0) >= 2.16
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(icu-uc)

%description
HarfBuzz is an OpenType text shaping engine.

%package -n libharfbuzz
Summary:        An OpenType text shaping engine
Group:          Graphics/Font Management

%description -n libharfbuzz
HarfBuzz is an OpenType text shaping engine.

%package tools
Summary:        An OpenType text shaping engine -- Tools
Group:          Graphics/Font Management

%description tools
HarfBuzz is an OpenType text shaping engine.

%package devel
Summary:        An OpenType text shaping engine -- Development Files
Group:          Development/Libraries
Requires:       libharfbuzz = %{version}

%description devel
HarfBuzz is an OpenType text shaping engine.

%prep
%setup -q
cp %{SOURCE1001} .
patch -p1 < %{_builddir}/%{name}-%{version}/patch/remove-icu-header-dependencies-from-harfbuzz-header.patch

%build
%configure \
        --disable-static
make %{?_smp_mflags}

%install
%make_install
rm -rf %{buildroot}/%{_datadir}/gtk-doc

%post -n libharfbuzz -p /sbin/ldconfig

%postun -n libharfbuzz -p /sbin/ldconfig

%files -n libharfbuzz
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.0*

%files tools
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/hb-ot-shape-closure
%{_bindir}/hb-shape
%{_bindir}/hb-subset
%{_bindir}/hb-info
#%{_bindir}/hb-view

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/harfbuzz/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake
#%{_libdir}/debug/usr/bin/hb-info.debug
