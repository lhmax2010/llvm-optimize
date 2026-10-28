Name:           tcl
VCS:            platform/upstream/tcl#43d1e55d2810128599aad73f04b26c4cf680cf9a
Version:        8.6.17
Release:        1.1
License:        TCL
Summary:        The Tcl Programming Language
Url:            http://www.tcl.tk
Group:          Development/Languages
Source0:        %{name}%{version}-src.tar.gz
Source1:        tcl-rpmlintrc
Source2:        baselibs.conf
Source3:        macros.tcl
Source10:       add_pie_compile_option.patch
Source1001: 	tcl.manifest

BuildRequires:  autoconf
Requires(pre):  /usr/bin/rm
Provides:       tclsh
%define TCL_MINOR %(echo %{version} | cut -c1-3)
Provides:       tclsh%{TCL_MINOR}

%description
Tcl (Tool Command Language) is a very powerful but easy to learn
dynamic programming language, suitable for a very wide range of uses,
including web and desktop applications, networking, administration,
testing and many more. Open source and business-friendly, Tcl is a
mature yet evolving language that is truly cross platform, easily
deployed and highly extensible.

For more information on Tcl see http://www.tcl.tk and
http://wiki.tcl.tk .

%package devel
Summary:        Header Files and C API Documentation for Tcl
Requires:       tcl = %{version}-%{release}

%description devel
This package contains header files and documentation needed for writing
Tcl extensions in compiled languages like C, C++, etc., or for
embedding the Tcl interpreter in programs written in such languages.

This package is not needed for writing extensions or applications in
the Tcl language itself.

%prep
%setup -q -n %{name}%{version}
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE10}

%build

cd unix
autoconf
%configure \
    --enable-man-symlinks \
    --enable-man-compression=gzip
%define scriptdir %{_libdir}/tcl
make %{?_smp_mflags} \
        PACKAGE_DIR=%_libdir/tcl \
        TCL_LIBRARY="%scriptdir/tcl%TCL_MINOR" \
        TCL_PACKAGE_PATH="%_libdir/tcl %_datadir/tcl"

%install
make -C unix install install-private-headers \
    INSTALL_ROOT=%{buildroot} \
    TCL_LIBRARY="%scriptdir/tcl%TCL_MINOR"
rm -f %{buildroot}%scriptdir/tcl%TCL_MINOR/ldAix
ln -sf tclsh%TCL_MINOR %{buildroot}%{_bindir}/tclsh
mkdir -p %{buildroot}%{_datadir}/tcl
install -D %{SOURCE3} -m 644 %{buildroot}%{_sysconfdir}/rpm/macros.tcl
%remove_docs


%files
%manifest %{name}.manifest
%license license.terms
%{_bindir}/*
%{_libdir}/lib*.so
%{_datadir}/tcl
%scriptdir
%exclude %scriptdir/*/tclAppInit.c
%config %{_sysconfdir}/rpm/macros.tcl

%files devel
%manifest %{name}.manifest
%{_includedir}/*
%scriptdir/*/tclAppInit.c
%{_libdir}/*.a
%{_libdir}/tclConfig.sh
%{_libdir}/pkgconfig/tcl.pc
%{_libdir}/tclooConfig.sh

