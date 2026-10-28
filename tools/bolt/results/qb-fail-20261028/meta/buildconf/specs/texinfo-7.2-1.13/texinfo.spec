Name:           texinfo
VCS:            platform/upstream/texinfo#e993512099ea63a196e5fa4d92949dde6d156e82
Version:        7.2
Release:        1.13
Summary:        Tools Needed to Create Documentation from Texinfo Sources
License:        GPL-3.0-or-later
Group:          Productivity/Publishing/Texinfo
Url:            https://www.gnu.org/software/texinfo/
Source:         %{name}-%{version}.tar.gz
Source10:       info-dir
Source1001:     texinfo.manifest

BuildRequires:  automake
BuildRequires:  help2man
BuildRequires:  bzip2-devel
BuildRequires:  libzio-devel
BuildRequires:  ncurses-devel
BuildRequires:  perl
BuildRequires:  perl-gettext
BuildRequires:  zlib-devel
BuildRequires:  gettext-tools
BuildRequires:  libsqlite


%description
Texinfo is a documentation system that uses a single source file to
produce both online information and printed output.  Using Texinfo, you
can create a printed document with the normal features of a book,
including chapters, sections, cross-references, and indices.  From the
same Texinfo source file, you can create a menu-driven, online info
file with nodes, menus, cross-references, and indices using the included
makeinfo tool.

%package -n info
Summary:        A Stand-Alone Terminal-Based Info Browser
License:       	GPL-3.0-or-later
Group:          Productivity/Publishing/Texinfo

%description -n info
Info is a terminal-based program for reading documentation of computer
programs in the Info format. The GNU Project distributes most of its
on-line manuals in the Info format, so you need a program called "Info
reader" to read the manuals.

%package -n makeinfo
Summary:        Translate Texinfo documents to info format
License:       	GPL-3.0-or-later
Group:          Productivity/Publishing/Texinfo
Provides:       texinfo:/usr/bin/makeinfo
Requires:       texinfo = %{version}

%description -n makeinfo
Makeinfo translates  Texinfo source documentation to various other
formats, by default Info files suitable for reading online with Emacs
or standalone GNU Info.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export HOST=%{_target_cpu}-tizen-linux
CFLAGS="$CFLAGS -pipe -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"
LDFLAGS="$LDFLAGS -pie"

AUTOPOINT=true autoreconf -fi
./configure --build=$HOST		        \
	        --prefix=%{_prefix}		    \
	        --mandir=%{_mandir}		    \
	        --datadir=%{_datadir}	    \
	        --infodir=%{_infodir}	    \
	        --without-included-gettext	\
	        --disable-perl-xs		    \
	        --enable-nls

export PATH=${PWD}/makeinfo:${PWD}/util:$PATH
make %{?_smp_mflags};

%install
export LD_AS_NEEDED=0

make DESTDIR=%{buildroot}       \
	 infodir=%{_infodir}	    \
	 htmldir=%{_defaultdocdir}/texi2html install

install -d -m 0755 %{buildroot}/sbin
mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin/
ln -sf ../../sbin/install-info %{buildroot}%{_bindir}/install-info

install -d -m 0755 %{buildroot}%{_infodir}
install -m 644 %{SOURCE10}  %{buildroot}%{_infodir}/dir

%find_lang %{name} %{name}.lang
%find_lang %{name}_document %{name}_document.lang

%remove_docs

%files -f %{name}_document.lang
%manifest %{name}.manifest
%license COPYING
%{_bindir}/pdftexi2dvi
%{_bindir}/pod2texi
%{_bindir}/texi2any
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/texindex
%{_datadir}/texinfo/*
%{_datadir}/texi2any/*

%files -n makeinfo -f %{name}.lang
%manifest %{name}.manifest
%license COPYING
%{_bindir}/makeinfo

%files -n info
%manifest %{name}.manifest
%license COPYING
/sbin/install-info
%{_bindir}/install-info
%{_bindir}/info
