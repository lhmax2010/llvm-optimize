Name:       hal-api-ml
Summary:    hal-api-ml interface
# Synchronize the version information.
# 1. CMake : ./CMakeLists.txt
# 2. Tizen : ./packaging/hal-api-ml.spec
Version:    0.1.0
Release:    0
Group:      Machine Learning/ML Framework
License:    Apache-2.0
Source0:    hal-api-ml-%{version}.tar.gz
Source1:    hal-api-ml.manifest
Source2:    hal-api-ml-manifest.xml
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(hal-api-common)
BuildRequires: pkgconfig(gtest)

%description
hal-api-ml interface


### devel package #########
%package    devel
Summary:    hal-api-ml interface
Group:      Machine Learning/ML Framework
Requires:   hal-api-ml = %{version}-%{release}

%description devel
hal-api-ml interface development package

### hal test package #########
%package    haltests
Summary:    hal-api-ml tests
Requires:   hal-api-ml = %{version}-%{release}

%description haltests
hal-api-ml tests package


### build and install #########
%prep
%setup -q

%cmake . -DCMAKE_C_COMPILER=%__cc -DCMAKE_CXX_COMPILER=%__cxx -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_LIBDIR_PREFIX=%{_libdir} -DENABLE_HALTESTS=ON

%build
cp %{SOURCE1} .
make %{?jobs:-j%jobs}

%check
LD_LIBRARY_PATH=./ ./ml-haltests

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/hal
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/hal/
%make_install

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

%postun
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

%files
%manifest hal-api-ml.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/hal/*.so*
%{_sysconfdir}/hal/hal-api-ml-manifest.xml

%files devel
%defattr(-,root,root,-)
%{_includedir}/hal/*.*
%{_libdir}/pkgconfig/*.pc

%files haltests
%defattr(-,root,root,-)
%manifest hal-api-ml.manifest
%{_bindir}/hal/ml-haltests

%changelog
* Wed Aug 27 2025 Yongjoo Ahn <yongjoo1.ahn@samsung.com>
- Release of 0.1.0 (Tizen 10.0 M2)
