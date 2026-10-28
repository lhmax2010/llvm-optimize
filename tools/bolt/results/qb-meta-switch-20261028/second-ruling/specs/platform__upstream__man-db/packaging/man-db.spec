Name:           man-db
Version:        2.9.4
Release:        1
License:        GPL-2.0+
Summary:        A set of documentation tools: man, apropos and whatis
Url:            http://man-db.nongnu.org/
Group:          System/Base
Source:         %{name}-%{version}.tar.gz
Source2:        gnulib.tar.gz
Source1001: 	man-db.manifest

BuildRequires:  flex
BuildRequires:  db4-devel
BuildRequires:  gettext
BuildRequires:  groff
BuildRequires:  pkgconfig(libpipeline)

Requires:       bzip2
Requires:       coreutils
Requires:       groff >= 1.18
Requires:       gzip
Requires:       less
Requires:       lzma
Provides:       man

%description
The man package includes three tools for finding information and/or
documentation about your Linux system: man, apropos, and whatis. The
man system formats and displays on-line manual pages about commands or
functions on your system. Apropos searches the whatis database
(containing short descriptions of system commands) for a string.
Whatis searches its own database for a complete word.

The man package should be installed on your system because it is the
primary way to find documentation on a Linux system.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"

tar -xf %{SOURCE2}
./bootstrap --no-git --gnulib-srcdir=gnulib
chmod +x ./configure
%configure --libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--with-db=db4 \
	--disable-setuid \
	--enable-mandirs=GNU \
	--enable-mb-groff \
	--with-sections="1 n l 8 3 0 2 5 4 9 6 7"

make %{?_smp_mflags}

%install
%make_install

# remove service files
rm -f %{buildroot}/lib/systemd/system/man-db.*
rm -f %{buildroot}/usr/lib/tmpfiles.d/man-db.conf

# remove manual files
rm -f %{buildroot}/%{_datadir}/doc/%{name}/%{name}-manual.*

%find_lang %{name} --with-man --all-name
%lang_package

%docs_package

%files
%manifest %{name}.manifest
%license docs/COPYING
%config(noreplace) %{_sysconfdir}/man_db.conf
%{_bindir}/apropos
%{_bindir}/catman
%{_bindir}/lexgrog
%{_bindir}/man
%{_bindir}/mandb
%{_bindir}/manpath
%{_bindir}/man-recode
%{_bindir}/whatis
%{_sbindir}/accessdb
%{_libdir}/man-db/libman-*.so
%{_libdir}/man-db/libman.so
%{_libdir}/man-db/libmandb-*.so
%{_libdir}/man-db/libmandb.so
%{_libdir}/man-db/globbing
%{_libdir}/man-db/manconv
%{_libdir}/man-db/zsoelim
