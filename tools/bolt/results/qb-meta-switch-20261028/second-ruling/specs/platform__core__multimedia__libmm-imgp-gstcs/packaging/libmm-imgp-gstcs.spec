Name:       libmm-imgp-gstcs
Summary:    Multimedia Framework Utility Library
Version:    1.0.2
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	libmm-imgp-gstcs.manifest
Requires:	gst-plugins-base
Requires:	gst-plugins-good
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%description
Multimedia Framework Utility Library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
./autogen.sh

export CFLAGS="$CFLAGS -Wextra -Wno-array-bounds -D_FORTIFY_SOURCE=2"
export CFLAGS="$CFLAGS -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow"
export CFLAGS="$CFLAGS -Wwrite-strings -Wswitch-default"
CFLAGS="$CFLAGS -DEXPORT_API=\"__attribute__((visibility(\\\"default\\\")))\" -D_MM_PROJECT_FLOATER" \
LDFLAGS="$LDFLAGS -Wl,--rpath=%{_libdir} -Wl,--hash-style=both -Wl,--as-needed" \
%if 0%{?gtests:1}
%configure --enable-tests
%else
%configure
%endif
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.APLv2.0
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so*
%if 0%{?gtests:1}
%{_bindir}/gtest*
%endif
