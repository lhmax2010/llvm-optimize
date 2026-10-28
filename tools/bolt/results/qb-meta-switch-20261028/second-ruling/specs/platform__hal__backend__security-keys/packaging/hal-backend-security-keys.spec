Name: hal-backend-security-keys
Summary: Security Keys backend library
Version: 1.1.0
Release: 0
Group: Security/Development
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(hal-rootstrap)

%description
Security Keys backend library

%prep
%setup -q
cp -a %{SOURCE1001} .

%{?_toolchain:
%if %{toolchain_is clang}
export LDFLAGS=" %{build_ldflags}"
%endif
}

%cmake . -DCMAKE_C_COMPILER=%__cc \
         -DCMAKE_CXX_COMPILER=%__cxx \
         -DHAL_LIB_DIR=%{_hal_libdir} \
         -DHAL_LICENSE_DIR=%{_hal_licensedir} \
         -DCMAKE_BUILD_TYPE=%{?build_type:%build_type}%{!?build_type:Release}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%files
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.Apache-2.0
%{_hal_libdir}/lib%{name}.so
