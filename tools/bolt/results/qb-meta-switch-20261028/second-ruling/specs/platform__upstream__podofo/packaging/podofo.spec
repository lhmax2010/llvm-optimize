Name:		podofo
Summary:	Editing tool for PDF format
Version:	0.9.7
Release:	0
Group:		Multimedia/Libraries
Url:		http://podofo.sourceforge.net/
License:	LGPL-2.0
Source0:	%{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(zlib)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A PDF parsing, modification and creation library.

%package devel
Summary: Libraries and header files for podofo app development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
A PDF parsing, modification and creation library.

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
CXXFLAGS="$CXXFLAGS -std=c++14 -Wno-shadow -Wno-format-truncation -Wno-deprecated-copy -Wno-ignored-qualifiers -Wno-array-bounds -Werror"
%if %{defined _toolchain}
%if %{toolchain_is gcc}
    CXXFLAGS="$CXXFLAGS -Wno-stringop-truncation -Wno-stringop-overflow -Wno-clobbered -Wno-error=alloc-size-larger-than="
%endif
%if %{toolchain_is clang}
    CXXFLAGS="$CXXFLAGS -Wno-error=unused-private-field"
%endif
%else
CXXFLAGS="$CXXFLAGS -Wno-stringop-truncation -Wno-stringop-overflow -Wno-clobbered -Wno-error=alloc-size-larger-than="
%endif
%cmake . -DPODOFO_BUILD_SHARED=TRUE -DPODOFO_BUILD_LIB_ONLY=TRUE

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING.LIB
%{_libdir}/libpodofo.so.*

%files devel
%{_includedir}/podofo/*.h
%{_includedir}/podofo/base/*.h
%{_includedir}/podofo/base/util/*.h
%{_includedir}/podofo/doc/*.h
%{_libdir}/libpodofo.so
%{_libdir}/pkgconfig/libpodofo.pc
