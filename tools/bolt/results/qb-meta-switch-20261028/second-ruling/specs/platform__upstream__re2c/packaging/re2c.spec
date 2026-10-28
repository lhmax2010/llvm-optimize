Name:           re2c
Version:        4.3
Release:        1
License:        PD
Summary:        Tool for generating C-based recognizers from regular expressions
URL:            https://re2c.org/
Source0:        %{name}-%{version}.tar.bz2
Source1001:     %{name}.manifest

BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  python3

%description
re2c is a tool for writing fast and flexible lexers. Unlike other such
tools, it concentrates solely on generating efficient code for matching
regular expressions. This makes it suitable for a wide variety of
applications. The generated scanners approach hand-crafted ones in
terms of size and speed.

%prep
%setup -q
cp %{SOURCE1001} .
find -type d -name .svn -print0 | xargs -r0 rm -rf
find CHANGELOG lessons examples -type f -print0 \
    | xargs -r0 chmod -v a-x

%build
export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"
mkdir -p m4
autoreconf -i -W all

%configure
%{__make} %{?_smp_mflags}

%install
%make_install
%remove_docs

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/re2c
%{_bindir}/re2d
%{_bindir}/re2go
%{_bindir}/re2hs
%{_bindir}/re2js
%{_bindir}/re2ocaml
%{_bindir}/re2py
%{_bindir}/re2rust
%{_bindir}/re2swift
%{_bindir}/re2v
%{_bindir}/re2zig
%{_datadir}/re2c/stdlib/unicode_categories.re
%{_datadir}/re2c/stdlib/c
%{_datadir}/re2c/stdlib/d
%{_datadir}/re2c/stdlib/go
%{_datadir}/re2c/stdlib/haskell
%{_datadir}/re2c/stdlib/java
%{_datadir}/re2c/stdlib/js
%{_datadir}/re2c/stdlib/ocaml
%{_datadir}/re2c/stdlib/python
%{_datadir}/re2c/stdlib/rust
%{_datadir}/re2c/stdlib/swift
%{_datadir}/re2c/stdlib/v
%{_datadir}/re2c/stdlib/zig
