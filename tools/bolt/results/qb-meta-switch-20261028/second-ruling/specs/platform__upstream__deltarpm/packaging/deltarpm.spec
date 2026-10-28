Name:           deltarpm
Version:        3.5.git
Release:        0
Summary:        Tools to Create and Apply deltarpms
License:        BSD-3-Clause
Group:          System/Packages
Url:            ftp://ftp.suse.com/pub/projects/deltarpm
Source:         deltarpm-3.5.git.tar.bz2
Source1001: 	deltarpm.manifest
BuildRequires:  bzip2-devel
BuildRequires:  python-devel
BuildRequires:  rpm-devel
BuildRequires:  xz-devel
# we need to build against recent rpm, so avoid the new payload
%define _binary_payload w9.bzdio

%description
This package contains tools to create and apply deltarpms. A deltarpm
contains the difference between an old and a new version of an RPM,
which makes it possible to recreate the new RPM from the deltarpm and
the old one. You do not need to have a copy of the old RPM, because
deltarpms can also work with installed RPMs.

%package -n python-deltarpm
Summary:        Tools to Create and Apply deltarpms
Group:          Development/Languages/Python
Requires:       %{name} = %{version}

%description -n python-deltarpm
Python bindings for deltarpm

%prep
%setup -q
cp %{SOURCE1001} .

%build
make CC="%__cc" CFLAGS="%{optflags}" rpmdumpheader="/usr/lib/rpm/rpmdumpheader" %{?_smp_mflags}
make CC="%__cc" CFLAGS="%{optflags}" rpmdumpheader="/usr/lib/rpm/rpmdumpheader" %{?_smp_mflags} python

%install
mkdir -p %{buildroot}%{_prefix}/lib/rpm
make DESTDIR=%{buildroot} prefix="%{_prefix}" libdir="%{_libdir}" mandir="%{_mandir}" rpmdumpheader="/usr/lib/rpm/rpmdumpheader" install
rm -rf %{buildroot}%{_libdir}/python/site-packages/{_deltarpmmodule.so,deltarpm.py} # Remove wrongly installed Python module
mv %{buildroot}%{python_sitearch}/_deltarpm{module,}.so # Fix binary Python module name

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%doc README LICENSE.BSD
%{_bindir}/*
%{_mandir}/man8/*
%{_prefix}/lib/rpm/rpmdumpheader

%files -n python-deltarpm
%manifest %{name}.manifest
%defattr(-,root,root)
%{python_sitearch}/deltarpm.py
%{python_sitearch}/_deltarpm.so

%changelog
