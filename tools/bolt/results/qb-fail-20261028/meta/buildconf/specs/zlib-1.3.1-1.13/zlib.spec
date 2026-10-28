
%if "%{run_tests}" == "1" 
	%define check %%check
%endif

%define keepstatic 1
Name:           zlib
VCS:            platform/upstream/zlib#76eff23cff0a4dfd320fea8ee5884e758c8c74f4
Provides:       libz
Obsoletes:      libz
Version:        1.3.1
Release:        1.13
Summary:        Data Compression Library
License:        Zlib
Group:          Base/Libraries
Url:            http://www.zlib.net/
#X-Vcs-Url:     https://github.com/madler/zlib.git
Source:         http://zlib.net/zlib-%{version}.tar.bz2
Source1:        LICENSE
Source2:        baselibs.conf
Source1001:     zlib.manifest
Source1002:     0001-Remove-the-definition-of-NOUNCRYPT.patch
BuildRequires:  pkgconfig

%description
ftp://ds.internic.net/rfc/rfc1950.txt (zlib format), rfc1951.txt
(deflate format) and rfc1952.txt (gzip format). These documents are
also available in other formats from
ftp://ftp.uu.net/graphics/png/documents/zlib/zdoc-index.html.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       zlib = %{version}
Provides:       libz:/usr/include/zlib.h

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require the provided includes and
libraries.

%package devel-static
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}
Provides:       %{name}-devel:%{_libdir}/libz.a

%description devel-static
This package contains all necessary include files and libraries needed
to develop applications that require the provided includes and
libraries.

%package -n minizip
Summary:    Manipulates files from a .zip archive
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}

%description -n minizip
Minizip is a tool to manipulates files from a .zip archive.

%package -n minizip-devel
Summary:    Development files for the minizip library
Group:      Development/Libraries
Requires:   minizip = %{version}-%{release}

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

%prep
%setup -q
cp %{SOURCE1} .
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
export LDFLAGS="-Wl,-z,relro,-z,now"

export CFLAGS="%{optflags}"
./configure --shared --prefix=%{_prefix} --libdir=/%{_lib}
%__make %{?_smp_mflags}

cd contrib/minizip
%reconfigure
%__make %{?_smp_mflags}

%check
rm -f /tmp/%{name}_test
%__make check | tee -i /tmp/%{name}_log

%install
#mkdir -p %%{buildroot}%%{_mandir}/man3
mkdir -p %{buildroot}%{_libdir}
%make_install
( cd %{buildroot}%{_libdir} && ln -sf -v ../../%{_lib}/$(readlink %{buildroot}/%{_lib}/libz.so) %{buildroot}%{_libdir}/libz.so )
rm -v %{buildroot}/%{_lib}/libz.so
# static lib
mv %{buildroot}/%{_lib}/libz.a %{buildroot}%{_libdir}
# Move .pc file to %%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
# manpage
install -m 644 zlib.3 %{buildroot}%{_mandir}/man3
install -m 644 zutil.h %{buildroot}%{_includedir}

(
  cd contrib/minizip
  %make_install
  rm -rf %{buildroot}%{_libdir}/libminizip.a
  rm -rf %{buildroot}%{_libdir}/libminizip.la
)

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
/%{_lib}/libz.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%doc README
%license LICENSE
%{_mandir}/man3/zlib.3.gz
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_includedir}/zutil.h
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc

%files devel-static
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libz.a

%files -n minizip
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libminizip.so.*

%files -n minizip-devel
%manifest %{name}.manifest
%license LICENSE
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc
%changelog
* Fri Mar 22 2013 Anas Nashif <anas.nashif@intel.com> submit/trunk/20121229.053403@09b3b82
- Fixed package groups
* Fri Dec 28 2012 Anas Nashif <anas.nashif@intel.com> submit/trunk/20121229.021410@1254f4c
- fix minizip dependencies
* Fri Dec 28 2012 Anas Nashif <anas.nashif@intel.com> upstream/1.2.7@897cf16
- add minizip package
