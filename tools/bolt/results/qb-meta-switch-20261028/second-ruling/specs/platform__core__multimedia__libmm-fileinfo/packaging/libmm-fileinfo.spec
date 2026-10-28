Name:	    libmm-fileinfo
Summary:    Media Fileinfo
Version:    1.1.29
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:    libmm-fileinfo.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(vconf)
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%description
Multimedia Framework FileInfo Library

%package tool
Summary:    Media Fileinfo Tools
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description tool
Multimedia Framework FileInfo Tools

%package devel
Summary:    Media Fileinfo
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Multimedia Framework FileInfo Library (development files)

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -DUSE_CODEC_VPX"
export CFLAGS="$CFLAGS -Wextra -Wno-array-bounds"
export CFLAGS="$CFLAGS -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow"
export CFLAGS="$CFLAGS -Wwrite-strings -Wswitch-default -Werror"
export CFLAGS="$CFLAGS -Wno-int-to-pointer-cast -Wno-pointer-to-int-cast -fgnu89-inline -fstack-protector-strong -D_FORTIFY_SOURCE=2"
./autogen.sh

%reconfigure \
CFLAGS="${CFLAGS} -DEXPORT_API=\"__attribute__((visibility(\\\"default\\\")))\" " LDFLAGS="${LDFLAGS}" \
./configure --disable-testmode --disable-dump --enable-dyn \
%if 0%{?gtests:1}
	--enable-tests \
%endif
	--prefix=/usr

%__make

%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/multimedia
cp -rf %{_builddir}/%{name}-%{version}/mm_file_config.ini %{buildroot}%{_sysconfdir}/multimedia/mm_file_config.ini
%if 0%{?gtests:1}
mkdir -p %{buildroot}%{_bindir}
cp -rf %{_builddir}/%{name}-%{version}/unittest/*.mp4 %{buildroot}%{_bindir}/
cp -rf %{_builddir}/%{name}-%{version}/unittest/*.mp3 %{buildroot}%{_bindir}/
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/libmmffile.so.*
%{_libdir}/libmmfile_formats.so.*
%{_libdir}/libmmfile_utils.so.*
%{_libdir}/libmmffile.so
%{_libdir}/libmmfile_formats.so
%{_libdir}/libmmfile_utils.so
%{_sysconfdir}/multimedia/mm_file_config.ini
%if 0%{?gtests:1}
%{_bindir}/gtest*
%{_bindir}/libmm-fileinfo-unittest*
%endif
%license LICENSE.APLv2.0

%files tool
%manifest %{name}.manifest
%{_bindir}/mm_file_test

%files devel
%manifest %{name}.manifest
%{_includedir}/mmf/mm_file.h
%{_includedir}/mmf/mm_file_error.h
%{_libdir}/pkgconfig/mm-fileinfo.pc
