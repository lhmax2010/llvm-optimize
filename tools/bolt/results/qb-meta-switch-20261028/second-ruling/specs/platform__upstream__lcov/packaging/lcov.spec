Summary: A graphical GCOV front-end
Name: lcov
Version: 2.4
Release: 1
License: GPL-2.0+
Group: Development/Tools
URL: http://ltp.sourceforge.net/coverage/lcov.php
Source0: http://downloads.sourceforge.net/ltp/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: perl >= 5.8.8
Requires: perl-PerlIO-gzip
Requires: perl-json
Requires: perl-Capture-Tiny
Requires: perl-DateTime
Requires: perl-TimeDate
Requires: perl-namespace-autoclean
Requires: perl-B-Hooks-EndOfScope
Requires: perl-Module-Implementation
Requires: perl-Module-Runtime
Requires: perl-Try-Tiny
Requires: perl-Variable-Magic
Requires: perl-Sub-Exporter-Progressive
Requires: perl-namespace-clean
Requires: perl-Package-Stash
Requires: perl-Sub-Identify
Requires: perl-Specio
Requires: perl-MRO-Compat
Requires: perl-Role-Tiny
Requires: perl-Eval-Closure
Requires: perl-Devel-StackTrace
Requires: perl-Params-ValidationCompiler
Requires: perl-Exception-Class
Requires: perl-Class-Data-Inheritable
Requires: perl-DateTime-Locale
Requires: perl-DateTime-TimeZone
Requires: perl-File-ShareDir-Install
Requires: perl-File-ShareDir
Requires: perl-Class-Inspector
Requires: perl-Class-Singleton
Requires: perl-TimeDate

%description
LCOV is a graphical front-end for GCC's coverage testing tool gcov. It collects
gcov data for multiple source files and creates HTML pages containing the
source code annotated with coverage information. It also adds overview pages
for easy navigation within the file structure.

%prep
%setup -q -n %{name}-%{version}

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr CFG_DIR=/etc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/*
/usr/share/man/man*/*
%config /etc/*
%{_prefix}/lib/lcov/lcovutil.pm
%{_datadir}/lcov/*
