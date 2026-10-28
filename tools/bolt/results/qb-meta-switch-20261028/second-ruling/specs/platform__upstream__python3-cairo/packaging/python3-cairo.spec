Name:           python3-cairo
Version:        1.19.1
Release:        0
Summary:        Python Bindings for Cairo
License:        LGPL-2.1+ or MPL-1.1
Group:          Development/Libraries/Python
Url:            http://www.cairographics.org/
Source:         py3cairo-%{version}.tar.bz2
Source11:       change_python_install_path.patch
Source1001: 	python3-cairo.manifest
BuildRequires:  cairo-devel
BuildRequires:  python3-devel
BuildRequires:  meson

%description
Python3 bindings for cairo.

%package devel
Summary:        Headers for python3-cairo
Group:          Development/Libraries/C and C++
Requires:       %name = %{version}
Requires:       cairo-devel
Requires:       python3-devel

%description devel
Headers for python3-cairo

%prep
%setup -n py3cairo-%{version}
%{__patch} -p1 < %{SOURCE11}
cp %{SOURCE1001} .

%build
export CFLAGS='%{optflags}'
%{meson}
%{meson_build}

%install
%{meson_install}

%files
%manifest %{name}.manifest
%license COPYING COPYING-*
%{python3_sitearch}/cairo/
%{python3_sitearch}/*.egg-info

%files devel
%manifest %{name}.manifest
%{_includedir}/pycairo/
%{_libdir}/pkgconfig/py3cairo.pc

%changelog
