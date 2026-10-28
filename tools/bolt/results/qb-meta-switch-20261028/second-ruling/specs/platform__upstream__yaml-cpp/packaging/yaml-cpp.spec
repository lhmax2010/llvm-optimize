Name:       yaml-cpp
Summary:    YAML parser and emitter in C++
Version:    0.8.0
Release:    0

# ==========================================================
License:    MIT
# ==========================================================

Group:      Development/Libraries/C and C++
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires:  cmake

%description
A YAML parser and emitter in C++ matching the YAML Spec

%package -n lib%{name}
Summary:        YAML parser and emitter in C++
Group:          Development/Libraries/C and C++

%description -n lib%{name}
A YAML parser and emitter in C++ matching the YAML 1.2 spec.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries/C and C++
Requires:       lib%{name} = %{version}

%description devel
Development files for %{name} library.

%prep
%setup -q
cp %{SOURCE1001} .

# ==========================================================
# build section
# how to actually build the software we are packaging
# ==========================================================
%build
export CXXFLAGS="$CXXFLAGS -fPIC"
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if "%{?_lib}" == "lib64"
        %{?_cmake_lib_suffix64} \
%endif
         -DYAML_BUILD_SHARED_LIBS=ON \
         -DYAML_CPP_BUILD_TESTS=OFF
%{__make} %{?_smp_mflags}
cd -


# ==========================================================
# install section
# how to actually build the software we are packaging
# ==========================================================
%install
cd build
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
cd -

%post -n lib%{name} -p /sbin/ldconfig

%postun -n lib%{name} -p /sbin/ldconfig

# ==========================================================
# files section
# The list of files that will be installed in the end
# user’s system.
# ==========================================================

%files -n lib%{name}
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libyaml-cpp.so.*

%files devel
%manifest %{name}.manifest
%license LICENSE
%{_includedir}/yaml-cpp/
%{_libdir}/libyaml-cpp.so
%{_libdir}/pkgconfig/yaml-cpp.pc
%{_libdir}/cmake/%{name}/
