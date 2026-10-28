Name:           python-cairo
Version:        1.17.1
Release:        0
Summary:        Python Bindings for Cairo
License:        LGPL-2.1+ or MPL-1.1
Group:          Development/Libraries/Python
# FIXME: on update, check if we still need to manually compile the byte-code in %%install
Url:            http://www.cairographics.org/
Source:         py2cairo-%{version}.tar.bz2
Source1001: 	python-cairo.manifest
BuildRequires:  cairo-devel
BuildRequires:  fdupes
BuildRequires:  python-devel

%description
Python bindings for cairo.

%package devel
Summary:        Headers for python-cairo
Group:          Development/Libraries/C and C++
Requires:       %name = %{version}
Requires:       cairo-devel
Requires:       python-devel

%description devel
Headers for python-cairo

%prep
%setup -n py2cairo-%{version}
cp %{SOURCE1001} .

%build
export CFLAGS='%{optflags}'
%{__python} setup.py build

%install
mkdir -p %{buildroot}/%{python_sitearch}/cairo
%{__python} setup.py install --skip-build \
        --install-base=%{buildroot} \
        --install-lib=%{buildroot}%{python_sitearch} \
        --install-purelib=%{buildroot}%{_libdir} \
        --install-scripts=%{buildroot}%{_bindir} \
        --install-headers=%{buildroot}%{_includedir} \
        --install-data=%{buildroot}%{_usr}
rm -f %{buildroot}/%{python_sitearch}/*.egg-info
rm -rf %{buildroot}/%{python_sitearch}/cairo/include
rm -f %{buildroot}/%{python_sitearch}/cairo/*.pyi
rm -f %{buildroot}/%{python_sitearch}/cairo/*.typed

%py_compile %{buildroot}/%{python_sitearch}
%py_compile -O %{buildroot}/%{python_sitearch}
%fdupes %{buildroot}/%{python_sitearch}

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%doc COPYING COPYING-*
%{python_sitearch}/cairo/

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/pycairo/
%{_libdir}/pkgconfig/pycairo.pc

%changelog
