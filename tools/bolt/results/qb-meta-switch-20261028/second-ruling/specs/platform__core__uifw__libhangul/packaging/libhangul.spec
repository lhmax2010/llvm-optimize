Name:           libhangul
Version:        0.2.0
Release:        0
License:        LGPL-2.1+
Group:          System/Utilities
AutoReqProv:    on
Url:            http://code.google.com/p/libhangul
Source0:        %{name}-%{version}.tar.gz
Source1001:     libhangul.manifest
Summary:        Hangul input library used by scim-hangul and ibus-hangul
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig


%description
"Hangul input library used by scim-hangul and ibus-hangul


Authors:
--------
    Choe Hwanjin <choe.hwanjin@gmail.com>
    Joon-cheol Park <jooncheol@gmail.com>

Hangul input library used by scim-hangul and ibus-hangul
"

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          System/Utilities
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%package test
Summary:        Test utilities for libhangul
Group:          System/Utilities
Requires:       %{name} = %{version}-%{release}

%description test
This package contains test utilities for libhangul.

%prep
%setup -q
cp %{SOURCE1001} .

%build
[ ! -x autogen.sh ] ||  rm -f configure
touch ChangeLog
%reconfigure --disable-static --with-pic
%__make %{?_smp_mflags}

%install
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f %{buildroot}%{_libdir}/*.la
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files -f %{name}.lang
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/lib*.so.*
%dir %{_datadir}/libhangul/hanja/
%{_datadir}/libhangul/hanja/*.txt

%files test
%manifest %{name}.manifest
%defattr(-, root, root)
%{_bindir}/hangul

%files devel
%manifest %{name}.manifest
%defattr(-, root, root)
%{_includedir}/hangul-1.0/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libhangul.pc
