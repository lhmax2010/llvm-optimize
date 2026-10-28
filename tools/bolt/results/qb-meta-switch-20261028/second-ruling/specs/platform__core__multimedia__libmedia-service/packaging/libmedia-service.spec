Name:       libmedia-service
Summary:    Media information service library for multimedia applications
Version:    0.8.27
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: libmedia-service.manifest

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(mmutil-magick)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(mm-fileinfo)
BuildRequires:  pkgconfig(libmedia-utils)
BuildRequires:  pkgconfig(media-thumbnail)
BuildRequires:  pkgconfig(libpodofo)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(vconf)
%if "%{tizen_profile_name}" == "tv"
BuildRequires:  pkgconfig(pvr-service-api)
%define _vd_product_type %_vd_cfg_product_type
%define product_tv 1
%else
%define product_tv 0
%endif

%description
This package is a library that provides the media information service for the multimedia applications.

%package devel
Summary:    Media information service library for multimedia applications. (development)
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description devel
This package is a library that provides the media information service for the multimedia applications. (Development files included)

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -DSYSCONFDIR=\\\"%{_sysconfdir}\\\" -DPATH_LIBDIR=\\\"%{_libdir}\\\""
%if 0%{?product_tv}
export CFLAGS="$CFLAGS -D_USE_TVPD_MODE"
%cmake . -DVD_PRODUCT_TYPE=%{_vd_product_type} -DTIZEN_PRODUCT_TV=YES
#make %{?jobs:-j%jobs}
make 2>&1 %{?jobs:-j%jobs} | sed -e 's%^.*: error: .*$%\x1b[37;41m&\x1b[m%' -e  's%^.*: warning: .*$%\x1b[30;43m&\x1b[m%'
%else
%{?asan:
export CXXFLAGS="$CXXFLAGS -Wno-maybe-uninitialized"
}
%cmake . -DTIZEN_PRODUCT_TV=NO
make %{?jobs:-j%jobs}
%endif

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libmedia-service.so.*
%{_libdir}/libmedia-content-plugin.so
%{_libdir}/libmedia-content-plugin.so.*
%{_libdir}/libmedia-ebook-plugin.so
#License
%license LICENSE.APLv2.0

%files devel
%manifest %{name}.manifest
%{_libdir}/libmedia-service.so
%{_libdir}/pkgconfig/libmedia-service.pc
%{_includedir}/media-service/*.h
