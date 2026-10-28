Name:       openusd
Summary:    OpenUSD libraries
Version:    24.03
Release:    0
Group:      Development/Libraries
License:    Modified Apache 2.0 License
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

ExcludeArch: riscv64
BuildRequires:  pkgconfig(libtbb)
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  gawk
BuildRequires:  boost-devel

%description
Universal Scene Description (USD) is an efficient, scalable system for
authoring, reading, and streaming time-sampled scene description for
interchange between graphics applications.

%package devel
License: Modified Apache 2.0 License
Summary: Development package to use OpenUSD
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libtbb-devel
Requires: boost-devel

%description devel
This package provides headers and other miscellaneous files required to use OpenUSD.

%prep
%setup -q
cp %{SOURCE1} .

%build
CXXFLAGS=$(echo $CXXFLAGS -Wno-psabi \
           -Wno-error=shadow \
           -Wno-error=format \
           -Wno-error=unused-result \
           -Wno-error=return-type \
           -Wno-error=deprecated-copy \
           -Wno-error=missing-field-initializers)
cmake -DPXR_ENABLE_PYTHON_SUPPORT=OFF \
      -DPXR_ENABLE_PTEX_SUPPORT=OFF \
      -DPXR_ENABLE_OPENVDB_SUPPORT=OFF \
      -DPXR_ENABLE_HDF5_SUPPORT=OFF \
      -DPXR_ENABLE_MATERIALX_SUPPORT=OFF \
      -DPXR_BUILD_IMAGING=OFF \
      -DPXR_BUILD_USD_IMAGING=OFF \
      -DPXR_BUILD_USDVIEW=OFF \
      -DPXR_BUILD_DOCUMENTATION=OFF \
      -DPXR_BUILD_HTML_DOCUMENTATION=OFF \
      -DPXR_BUILD_PYTHON_DOCUMENTATION=OFF \
      -DPXR_BUILD_TESTS=OFF \
      -DPXR_BUILD_EXAMPLES=OFF \
      -DPXR_BUILD_TUTORIALS=OFF \
      -DPXR_BUILD_USD_TOOLS=OFF \
      -DPXR_BUILD_MAYAPY_TESTS=OFF \
      -DPXR_BUILD_ANIMX_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} .
%{__make} %{?jobs:-j%jobs}

%install
pushd %{_builddir}/%{name}-%{version}
%make_install

%post
%{_sbindir}/ldconfig

%postun
%{_sbindir}/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.txt
/usr/lib/lib*.so*
/usr/lib/usd/ar/resources/plugInfo.json
/usr/lib/usd/ndr/resources/plugInfo.json
/usr/lib/usd/plugInfo.json
/usr/lib/usd/sdf/resources/plugInfo.json
/usr/lib/usd/usd/resources/codegenTemplates/plugInfo.json
/usr/lib/usd/usd/resources/codegenTemplates/schemaClass.cpp
/usr/lib/usd/usd/resources/codegenTemplates/tokens.cpp
/usr/lib/usd/usd/resources/codegenTemplates/wrapSchemaClass.cpp
/usr/lib/usd/usd/resources/codegenTemplates/wrapTokens.cpp
/usr/lib/usd/usd/resources/generatedSchema.usda
/usr/lib/usd/usd/resources/plugInfo.json
/usr/lib/usd/usd/resources/usd/schema.usda
/usr/lib/usd/usdGeom/resources/generatedSchema.usda
/usr/lib/usd/usdGeom/resources/plugInfo.json
/usr/lib/usd/usdGeom/resources/usdGeom/schema.usda
/usr/lib/usd/usdShade/resources/generatedSchema.usda
/usr/lib/usd/usdShade/resources/plugInfo.json
/usr/lib/usd/usdShade/resources/usdShade/schema.usda
/usr/lib/usd/usdSkel/resources/generatedSchema.usda
/usr/lib/usd/usdSkel/resources/plugInfo.json
/usr/lib/usd/usdSkel/resources/usdSkel/schema.usda

%files devel
%manifest %{name}.manifest
%license LICENSE.txt
%{_includedir}/*
/usr/lib/usd/usd/resources/codegenTemplates/api.h
/usr/lib/usd/usd/resources/codegenTemplates/schemaClass.h
/usr/lib/usd/usd/resources/codegenTemplates/tokens.h
/usr/cmake/pxrTargets-release.cmake
/usr/cmake/pxrTargets.cmake
/usr/plugin/usd/plugInfo.json
/usr/pxrConfig.cmake
