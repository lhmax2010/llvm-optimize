Name:           swig
Version:        4.0.2
Release:        0
License:        GPL-3.0+ and BSD-3-Clause
Summary:        Simplified Wrapper and Interface Generator
Url:            http://www.swig.org/
Group:          Development/Languages/C and C++
Source:         http://sourceforge.net/projects/swig/files/swig/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.rpmlintrc
Source1001: 	swig.manifest
Source1002: 	Fix_make_check_error.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  boost-devel
%define docpath %{_docdir}/%{name}
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pcre-devel
BuildRequires:  perl
BuildRequires:  pkg-config
BuildRequires:  python-devel
BuildRequires:  bison

%description
SWIG is a compiler that attempts to make it easy to integrate C, C++,
or Objective-C code with scripting languages including Perl, Tcl, and
Python.  In a nutshell, you give it a bunch of ANSI C/C++ declarations
and it generates an interface between C and your favorite scripting
language.  However, this is only scratching the surface of what SWIG
can do--some of its more advanced features include automatic
documentation generation, module and library management, extensive
customization options, and more.

%package doc
License:        BSD-3-Clause
Summary:        SWIG Manual
Group:          Documentation/Man
Requires:       swig
BuildArch:      noarch

%description doc
SWIG is a compiler that attempts to make it easy to integrate C, C++,
or Objective-C code with scripting languages including Perl, Tcl, and
Python.  In a nutshell, you give it a bunch of ANSI C/C++ declarations
and it generates an interface between C and your favorite scripting
language.  However, this is only scratching the surface of what SWIG
can do--some of its more advanced features include automatic
documentation generation, module and library management, extensive
customization options, and more.

This package contains the SWIG manual.

%package examples
License:        BSD-3-Clause
Summary:        SWIG example files
Group:          Documentation/Howto
Requires:       swig

%description examples
SWIG is a compiler that attempts to make it easy to integrate C, C++,
or Objective-C code with scripting languages including Perl, Tcl, and
Python.  In a nutshell, you give it a bunch of ANSI C/C++ declarations
and it generates an interface between C and your favorite scripting
language.  However, this is only scratching the surface of what SWIG
can do--some of its more advanced features include automatic
documentation generation, module and library management, extensive
customization options, and more.

This package contains SWIG examples, useful both for testing and
understandig SWIG usage.

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
sh autogen.sh
%configure --disable-ccache CFLAGS="-fPIC" CPPFLAGS="-fPIC"

make %{?_smp_mflags}

%check
%if 0%{?run_unit_test:1}
# Segfaults
rm -f Examples/test-suite/python/li_std_containers_int_runme.py
rm -f Examples/test-suite/python/li_boost_shared_ptr_runme.py
make check
%endif

%install
%make_install

install -d %{buildroot}%{docpath}
cp -a TODO ANNOUNCE CHANGES* LICENSE README Doc/Devel Doc/Manual \
	%{buildroot}%{docpath}
install -d %{buildroot}%{_libdir}/swig
cp -a Examples %{buildroot}%{_libdir}/swig/examples
rm -rf %{buildroot}%{_libdir}/swig/examples/test-suite

# rm files that are not needed for running or rebuilding the examples
find %{buildroot}%{_libdir}/swig \
	-name '*.dsp' -o -name '*.vcproj' -o -name '*.sln' -o \
	-name '*.o' -o -name '*_wrap.c' | xargs rm

# fix perms
chmod -x %{buildroot}%{docpath}/Manual/*
find %{buildroot}%{_libdir}/swig -name '*.h' -perm +111 | \
	xargs --no-run-if-empty chmod -x
ln -s %{_libdir}/swig/examples %{buildroot}%{docpath}/Examples

%fdupes %{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(644,root,root,755)
%dir %{docpath}
%{docpath}/[A-Z][A-Z]*
%{_datadir}/swig
%attr(755,root,root) %{_bindir}/swig

%files doc
%manifest %{name}.manifest
%defattr(-,root,root)
%{docpath}/Devel
%{docpath}/Manual

%files examples
%manifest %{name}.manifest
%defattr(-,root,root)
%{docpath}/Examples
%{_libdir}/swig

%changelog
