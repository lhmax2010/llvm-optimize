Name:           wdiff
Version:        1.2.2
Release:        1
License:        GPL-3.0+
Summary:        Display Word Differences Between Text Files
Url:            https://ftp.gnu.org/gnu/wdiff/
Group:          Productivity/Text/Utilities
Source:         %{name}-%{version}.tar.bz2
Source2:        0001-CVE-2018-17942-vasnprintf-Fix-heap-memory-overrun-bu.patch
Source3:        0002-CVE-2009-5155-Diagnose-ERE-1.patch
Source1001: 	wdiff.manifest

BuildRequires:  ncurses-devel
BuildRequires:  makeinfo
BuildRequires:  gettext-tools

%description
wdiff compares two files and finds which words have been deleted or
added to old_file to get new_file. A word is considered to be anything
between whitespace.

Xwdiff is a handy X Window System front-end, based on Tcl/Tk.

%package lang
Summary:        Translations for Wdiff
Group:          Productivity/Text/Utilities
Requires:       %{name} = %{version}

%description lang
Contains language specific files for of wdiff.

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE2}
%{__patch} -p1 < %{SOURCE3}

%build
LIBS=-lncurses \
CFLAGS="%{optflags} -pipe -DPROTOTYPES" \
GETOPT="" \
%configure
make

%install
make "DESTDIR=%{buildroot}" install
%find_lang %{name}-gnulib
%find_lang %{name}

%files
%manifest %{name}.manifest
%license COPYING
%{_infodir}/wdiff.info*
/usr/bin/*
%{_mandir}/man1/*

%files lang -f %{name}-gnulib.lang -f %{name}.lang
%license COPYING
%manifest %{name}.manifest

