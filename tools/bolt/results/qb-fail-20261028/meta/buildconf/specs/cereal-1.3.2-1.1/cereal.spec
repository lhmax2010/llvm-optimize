%global debug_package %{nil}

Name:           cereal
VCS:            platform/upstream/cereal#28aedc95fdc600568c57babf28ff717e0b2bca7d
Version:        1.3.2
Release:        1.1
Summary:        A header-only C++11 serialization library
License:        BSD-3-Clause AND BSL-1.0 AND Zlib AND MIT AND (MIT OR BSL-1.0)
URL:            https://github.com/USCiLab/cereal
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake

%description
cereal is a header-only C++11 serialization library. cereal takes arbitrary
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast,
light-weight, and easy to extend - it has no external dependencies and can be
easily bundled with other code or used standalone.

%package devel
Summary:        Development headers and libraries for %{name}
Provides:       %{name}-static = %{version}-%{release}

%description devel
cereal is a header-only C++11 serialization library. cereal takes arbitrary
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast,
light-weight, and easy to extend - it has no external dependencies and can be
easily bundled with other code or used standalone.

This package contains development headers and libraries for the cereal library

%prep
%setup -q

%build
mkdir build
(cd build && cmake .. -DSKIP_PORTABILITY_TEST=ON -DWITH_WERROR=OFF -DCMAKE_INSTALL_PREFIX=%{_prefix} && %make_build)

%install
(cd build && %make_install)

%files devel
%license LICENSE
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
