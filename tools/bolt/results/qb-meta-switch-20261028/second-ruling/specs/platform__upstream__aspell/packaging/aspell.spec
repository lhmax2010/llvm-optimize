# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           aspell
Version:        0.60.8.1
Release:        0
License:        LGPL-2.1+
Summary:        A Free and Open Source Spell Checker
Url:            http://aspell.net/
Group:          System/Libraries
Source0:        ftp://ftp.gnu.org/gnu/aspell/%{name}-%{version}.tar.gz
Source1001: 	aspell.manifest
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  gettext-tools
BuildRequires:  libtool
BuildRequires:  ncurses-devel

%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

Its main feature is that it does a much better job of coming up with
possible suggestions than just about any other spell checker available
for the English language, including Ispell and Microsoft Word. It also
has many other technical enhancements over Ispell, such as using shared
memory for dictionaries and intelligently handling personal
dictionaries when more than one Aspell process is open at once.

%package devel
Summary:        Include Files and Libraries Mandatory for Development with aspell
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       libaspell = %{version}
Requires:       libpspell = %{version}

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require aspell.

%package ispell
Summary:        GNU Aspell - Ispell compatibility
Group:          System/Tools
Requires:       %{name} = %{version}

%description ispell
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

This package contains an ispell script for compatibility reasons so that
programs that expect the "ispell" command will work correctly.

%package spell
Summary:        GNU Aspell - Spell compatibility
Group:          System/Tools
Requires:       %{name} = %{version}

%description spell
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

This package contains a spell script for compatibility reasons so that programs
that expect the "spell" command will work correctly.

%package -n libaspell
Summary:        GNU Aspell Library
Group:          System/Libraries

%description -n libaspell
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

This package contains the aspell library.

%package -n libpspell
Summary:        GNU Aspell - Pspell Compatibility Library
Group:          System/Libraries

%description -n libpspell
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

This package contains the pspell compatibility library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
autoreconf -fiv
export CXXFLAGS="%{optflags} -fPIC `ncursesw6-config --cflags`"
export CFLAGS="%{optflags} -fPIC"
#this is an ugly kludge , don't look :-)
export LDFLAGS="-pie `ncursesw6-config --libs`"
%configure \
    --enable-curses="-lncursesw" \
 --disable-rpath

make %{?_smp_mflags}

%install
%make_install
# Links for compatibility reasons (ispell and spell)
ln -s %{_libdir}/aspell-0.60/ispell %{buildroot}%{_bindir}
ln -s %{_libdir}/aspell-0.60/spell %{buildroot}%{_bindir}
%fdupes -s %{buildroot}

%find_lang %{name}


%docs_package

%post -n libaspell -p /sbin/ldconfig

%postun -n libaspell -p /sbin/ldconfig

%post -n libpspell -p /sbin/ldconfig

%postun -n libpspell -p /sbin/ldconfig


%files -f %{name}.lang
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING 
%{_bindir}/aspell
%{_bindir}/aspell-import
%{_bindir}/pre*
%{_bindir}/run-with-aspell
%{_bindir}/word-list-compress

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc manual/aspell-dev.html/
%{_bindir}/pspell-config
%{_includedir}/pspell/
%{_includedir}/*.h
%{_libdir}/libaspell.so
%{_libdir}/libpspell.so
%doc %{_infodir}/%{name}-dev.info%{ext_info}
%doc %{_mandir}/man1/pspell-config.1%{ext_man}

%files ispell
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/ispell

%files spell
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/spell

%files -n libaspell
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/aspell-0.60/
%{_libdir}/libaspell.so.15*

%files -n libpspell
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libpspell.so.15*
