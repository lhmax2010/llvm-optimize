Summary: 	The xdelta3
Name: 		xdelta3
Version: 	3.0.11
Release: 	1
License: 	GPL-2.0+
Group: 		System/Libraries
Source:		%{name}-%{version}.tar.gz
SOURCE1:	xdelta3.manifest
URL:		http://xdelta.org/

%description
Xdelta3 is a set of tools designed to compute changes between
binary files.  These changes (delta files) are similar to the output of the
"diff" program, in that they may be used to store and transmit only the
changes between files.  The "delta files" that Xdelta3 manages are
stored in RFC3284 (VCDIFF) format.

%package devel
Summary:	Development files for xdelta3
Group:		Development/Libraries
Requires:		%{name} = %{version}-%{release}

%description devel
This package contains the header files, libraries and documentation needed to
develop applications that use xdelta3.

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -fPIE"
export CXXFLAGS="$CXXFLAGS -fPIE"
export LDFLAGS
cp %{SOURCE1} .
libtoolize -c -f
aclocal
autoheader
autoconf
automake -a -c
%configure \
	--prefix="/usr" \
	--disable-dependency-tracking \
	LDFLAGS="$LDFLAGS -pie"

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%manifest xdelta3.manifest
%defattr(-, root, root)
%doc README.md COPYING
%doc %{_mandir}/man1/xdelta3.1.gz
%license COPYING
%{_bindir}/%{name}
