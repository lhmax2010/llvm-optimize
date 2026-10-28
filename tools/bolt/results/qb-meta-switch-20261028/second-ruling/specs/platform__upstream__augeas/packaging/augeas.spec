%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}

Name:           augeas
Version:        1.14.1
Release:        0
Summary:        A library for changing configuration files
License:        LGPL-2.1+
Group:          System/Libraries
Url:            http://augeas.net/
Source0:        http://augeas.net/download/augeas-%{version}.tar.gz
Source1:        baselibs.conf
Source2:        gnulib.tar.gz
Source3:        Fix_bootstrap_for_build.patch
Source4:        Add_parser.h_to_Makefile.patch
Source1001: 	augeas.manifest

BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  readline-devel
BuildRequires:  flex
BuildRequires:  bison

%description
A library for programmatically editing configuration files. Augeas parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

The transformation works very hard to preserve comments and formatting
details. It is controlled by ``lens'' definitions that describe the file
format and the transformation into a tree.

%package        devel
Summary:        A library for changing configuration files
Group:          System/Development
Requires:       %{name}-libs = %{version}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        libs
Summary:        Libraries for %{name}
Group:          System/Libraries

%description    libs
The libraries for %{name}.

Augeas is a library for programmatically editing configuration files. It parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

%prep
%setup -q
cp %{SOURCE1001} .
tar -zxvf %{SOURCE2}
%{__patch} -p1 < %{SOURCE3}
%{__patch} -p1 < %{SOURCE4}

%build
./autogen.sh  --gnulib-srcdir=%{_builddir}/%{?buildsubdir}/gnulib --prefix=%{_prefix} --disable-static --libdir=%{_libdir}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# The tests/ subdirectory contains lenses used only for testing, and
# so it shouldn't be packaged.
rm -r $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/dist/tests

%remove_docs

%check
#pushd ./gnulib/tests/
#chmod +x *.sh
#popd
#%{__make} check || exit 0

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_bindir}/augtool
%{_bindir}/augparse
%{_bindir}/fadot
%{_datadir}/vim/vimfiles/syntax/augeas.vim
%{_datadir}/vim/vimfiles/ftdetect/augeas.vim

%files libs
%manifest %{name}.manifest
# %{_datadir}/augeas and %{_datadir}/augeas/lenses are owned
# by filesystem.
%{_datadir}/augeas/lenses/dist
%{_libdir}/*.so.*
%license COPYING

%files devel
%manifest %{name}.manifest
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/augeas.pc
