# efl is enabled by default; disable with: gbs build --define "efl 0"
%{!?efl:%define efl 1}

Name:       libmm-display
Summary:    Multimedia framework display library
Version:    1.1.5
Release:    1
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  pkgconfig(dali2-toolkit)
%if 0%{?efl}
BuildRequires:  pkgconfig(evas)
BuildRequires:  pkgconfig(ecore-evas)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(mm-evas-renderer)
%endif
%if "%{gtests}" == "1"
BuildRequires:  pkgconfig(gmock)
%endif

%description
Multimedia framework display library.


%package interface
Summary:    Multimedia framework display interface library
Group:      Multimedia/Libraries
Version:    %{version}

%description interface
Multimedia framework display interface library.


%package interface-devel
Summary:    Multimedia framework display interface library for development
Group:      libdevel
Version:    %{version}
Requires:   %{name}-interface = %{version}-%{release}

%description interface-devel
Multimedia framework display library for develpment.


%prep
%setup -q


%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
export CFLAGS+=" -D_LARGEFILE64_SOURCE -DMM_DISPLAY_LIBDIR=\\\"%{_libdir}\\\" -DEFL_BETA_API_SUPPORT"
./autogen.sh
%configure \
%if !0%{?efl}
	--disable-efl-backend \
%endif
%if "%{gtests}" == "1"
	--enable-gtests \
%endif
	--disable-static
make %{?jobs:-j%jobs}

%install
%make_install


%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest libmm-display.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_libdir}/libmmfdisplay.so*
%if "%{gtests}" == "1"
%{_bindir}/gtests-libmm-display
%endif

%files interface
%manifest libmm-display-interface.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_libdir}/libmmfdisplay_interface.so.*

%files interface-devel
%defattr(-,root,root,-)
%{_includedir}/mmf/mm_display_interface.h
%{_libdir}/pkgconfig/mm-display-interface.pc
%{_libdir}/libmmfdisplay_interface.so
