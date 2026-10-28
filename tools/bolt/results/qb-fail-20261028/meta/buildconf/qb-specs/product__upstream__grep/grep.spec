%if "%{run_tests}" == "1"
    %define __spec_check_pre %___build_pre
    %define check %%check
%endif

Name:           grep
BuildRequires:  automake
BuildRequires:  pcre-devel
Url:            http://www.gnu.org/software/grep/
Version:        2.5.2
Release:        0
Summary:        Print lines matching a pattern
License:        GPL-2.0-or-later
Group:          Base/Utilities
Source0:        grep-%{version}.tar.xz
Source1001: 	grep.manifest
Provides:       base:/usr/bin/grep
Provides:       /bin/grep
BuildRequires:  makeinfo
BuildRequires:  gettext-tools

%description
The grep command searches one or more input files for lines
containing a match to a specified pattern.  By default, grep prints
the matching lines.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -fPIE -Wno-error=implicit-function-declaration"
export LDFLAGS="$LDFLAGS -pie"

%configure  --disable-silent-rules \
			--without-included-regex

%{__make} %{?_smp_mflags}

#make check VERBOSE=1 || exit 0

%check
make check VERBOSE=1 || exit 0

%install
%make_install
%find_lang %name

%remove_docs

%lang_package


%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
