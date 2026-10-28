Name:           cmake
VCS:            platform/upstream/cmake#5ef35065c26ad12c0e5599aafc5f0bfa768d753f
Version:        3.31.2
Release:        1.9
License:        BSD-3-Clause
Summary:        Cross-platform make system
Url:            http://www.cmake.org
Group:          Platfrom Development/Tools
Source0:        %{name}-%{version}.tar.gz
Source1:        macros.cmake
Source2:        TizenCommon.cmake
Source1001:     cmake.manifest

BuildRequires:  fdupes
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(jsoncpp)

%description
CMake is used to control the software compilation process using simple platform
and compiler independent configuration files. CMake generates native makefiles
and workspaces that can be used in the compiler environment of your choice.
CMake is quite sophisticated: it is possible to support complex environments
requiring system configuration, pre-processor generation, code generation, and
template instantiation.


%prep
%setup -q -n cmake-%{version}
cp %{SOURCE1001} .

%build
export CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
export CFLAGS="$CXXFLAGS"
./configure \
    --prefix=%{_prefix} \
    --datadir=/share/%{name} \
    --docdir=/share/doc/packages/%{name} \
    --mandir=/share/man \
    --system-libs \
    --parallel=0%jobs \
    --no-qt-gui \
    --no-system-curl \
    --no-system-librhash \
    --no-system-nghttp2 \
	--no-system-cppdap \
    --no-system-jsoncpp \
    --no-system-libuv
%__make VERBOSE=1 %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_libdir}/%{name}
find %{buildroot}%{_datadir}/%{name} -type f -print0 | xargs -0 chmod 644
cp %{SOURCE2} %{buildroot}%{_datadir}/%{name}/Modules

# Install cmake rpm macros
install -D -p -m 0644 %{S:1} \
  %{buildroot}%{_sysconfdir}/rpm/macros.cmake

fdupes %{buildroot}%{_datadir}/%{name}

rm -rf %{buildroot}%{_datadir}/bash-completion
rm -rf %{buildroot}%{_datadir}/emacs
rm -rf %{buildroot}%{_datadir}/vim
%docs_package

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rpm/macros.cmake
%doc %{_datadir}/doc/packages/%{name}
%{_datadir}/aclocal/cmake.m4
%{_bindir}/cmake
%{_bindir}/ccmake
%{_bindir}/cpack
%{_bindir}/ctest
%{_datadir}/%{name}
