Name:           ctags
Version:        6.2.20251026.0
Release:        1
Summary:        Universal Ctags - A maintained implementation of ctags
License:        GPL-2.0+
URL:            https://ctags.io/
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest

%description
Universal Ctags (abbreviated as u-ctags) is a maintained implementation of ctags.
ctags generates an index (or tag) file of language objects found in source files
for programming languages. This index makes it easy for text editors and other
tools to locate the indexed items.

Universal Ctags has the objective of continuing the development of Exuberant
Ctags with more numbers of improved language support, fully extended optlib,
and interactive mode.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .

%build
# Disable features that depend on unavailable libraries
export CFLAGS="$CFLAGS -fPIC "
export CXXFLAGS="$CXXFLAGS -fPIC "
export LDFLAGS="$LDFLAGS -pie "

./autogen.sh

%configure \
    --disable-json \
    --disable-seccomp \
    --disable-xml \
    --disable-yaml \
    --disable-pcre2

%{__make} %{?_smp_mflags}

%install
%make_install

# Remove documentation to follow Tizen guidelines
%remove_docs

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/ctags
%{_bindir}/readtags
%{_bindir}/optscript

%changelog
