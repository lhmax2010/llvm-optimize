Name:       c-mock
Summary:    %{name}
Version:    0.4.0
Release:    0

# ==========================================================
License:    BSD-2-Clause
# ==========================================================
Url:        https://github.com/hjagodzinski/C-Mock
Group:      Definition/Libraries/C
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires: pkgconfig(gmock)

%description
C Mock is Google Mock's extension allowing a function mocking.
Only global (non-static) functions mocking is supported.

%package devel
Summary:  Google Mock Extension for function mocking (development)
Group:    System/Libraries
Requires: pkgconfig(gmock)

%description devel
Header and Configuration of C-Mock - Google Mock Extension for function mocking

%prep
%setup -q
cp %{SOURCE1001} .

%build
%{make_build}

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
%{__make} PREFIX=%{buildroot}%{_prefix} install

cat > c-mock.pc << EOF
includedir=%{_includedir}/cmock

Name: c-mock
Version: %{version}
Description: Google Mock Extension for Function Mocking
Libs:
Cflags: -I\${includedir}
EOF

install -D -m 644 c-mock.pc %{buildroot}/%{_libdir}/pkgconfig/c-mock.pc

%check
%{__make} test

%clean

%files devel
%license LICENSE.md
%manifest %{name}.manifest
%{_bindir}/cmock-config
%{_includedir}/cmock/cmock-function-class-mockers.h
%{_includedir}/cmock/cmock-function-mockers.h
%{_includedir}/cmock/cmock-internal.h
%{_includedir}/cmock/cmock-spec-builders.h
%{_includedir}/cmock/cmock.h
%{_libdir}/pkgconfig/c-mock.pc
