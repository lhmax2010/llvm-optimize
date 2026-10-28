Name:           onnxruntime
Summary:        ONNX Runtime is a cross-platform inference and training machine-learning accelerator.
Version:        1.16.3
Release:        1
License:        MIT
Source0:        %{name}-%{version}.tar.gz
Source1001:     onnxruntime.manifest
Source1002:     libonnxruntime.pc.in
Source2001:     abseil-cpp.tar.gz
Source2002:     date.tar.gz
Source2003:     eigen-3.4.1.tar.gz
Source2004:     flatbuffers-1.12.0-Wno-implicit-fallthrough.tar.gz
Source2005:     google_nsync.tar.gz
Source2006:     microsoft_gsl.tar.gz
Source2007:     mimalloc.tar.gz
Source2008:     mp11.tar.gz
Source2009:     nlohmann_json.tar.gz
Source2010:     onnx.tar.gz
Source2011:     protobuf.tar.gz
Source2012:     pytorch_cpuinfo.tar.gz
Source2013:     re2.tar.gz
Source2014:     safeint.tar.gz

Source10001:    0001-change-external-source-path.patch
Source10002:    0002-change-cmakelists-patch.patch
Source10003:    0003-add-riscv-atomic-link-cmakelist.patch

BuildRequires: cmake
BuildRequires: ninja
BuildRequires:	python3
BuildRequires:	python3-devel

%define _toolchain_override gcc

%description
ONNX Runtime is a cross-platform inference and training machine-learning accelerator.
ONNX Runtime inference can enable faster customer experiences and lower costs, supporting models from deep learning frameworks such as PyTorch and TensorFlow/Keras as well as classical machine learning libraries such as scikit-learn, LightGBM, XGBoost, etc. ONNX Runtime is compatible with different hardware, drivers, and operating systems, and provides optimal performance by leveraging hardware accelerators where applicable alongside graph optimizations and transforms.
ONNX Runtime training can accelerate the model training time on multi-node NVIDIA GPUs for transformer models with a one-line addition for existing PyTorch training scripts.

%package devel
Summary: ONNX Runtime development headers and object file

%description devel
ONNX Runtime development headers and object file

%define MAX_N_PARALLEL 16
%define DISABLE_SPARSE_TENSORS "OFF"

%prep
%setup
cp %{SOURCE1001} .
patch -p1 < %{SOURCE10001}
patch -p1 < %{SOURCE10002}
patch -p1 < %{SOURCE10003}

mkdir -p cmake/external
pushd cmake/external
cp %{SOURCE2001} .
cp %{SOURCE2002} .
cp %{SOURCE2003} .
cp %{SOURCE2004} .
cp %{SOURCE2005} .
cp %{SOURCE2006} .
cp %{SOURCE2007} .
cp %{SOURCE2008} .
cp %{SOURCE2009} .
cp %{SOURCE2010} .
cp %{SOURCE2011} .
cp %{SOURCE2012} .
cp %{SOURCE2013} .
cp %{SOURCE2014} .
popd

pushd cmake
cp %{SOURCE1002} .
sed -i 's:@libdir@:%{_libdir}:g
    s:@includedir@:%{_includedir}/onnxruntime/:g' ./libonnxruntime.pc.in
popd

%build
mkdir -p build
pushd build

# To fix the buildbreak issue on gcc 11 or higher,
# '-Wno-error=stringop-overflow' option is added to CFLAGS and CXXFLAGS.
EXTRA_CFLAGS="${CFLAGS} -Wno-error=stringop-overflow"
EXTRA_CXXFLAGS="${CXXFLAGS} -Wno-error=stringop-overflow"

%ifarch %arm aarch64
EXTRA_CFLAGS="${EXTRA_CFLAGS} -Wno-error=attributes"
EXTRA_CXXFLAGS="${EXTRA_CXXFLAGS} -Wno-error=attributes"
  %ifarch %arm
    %define DISABLE_SPARSE_TENSORS "ON"
  %endif
%endif

EXTRA_CFLAGS="${EXTRA_CFLAGS} -Wno-template-id-cdtor -Wno-maybe-uninitialized"
EXTRA_CXXFLAGS="$(echo $EXTRA_CXXFLAGS | sed 's/-fno-inline-functions//g')"

cmake \
  -GNinja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_FLAGS="${EXTRA_CFLAGS}" \
  -DCMAKE_CXX_FLAGS="${EXTRA_CXXFLAGS}" \
  -DPython_ADDITIONAL_VERSIONS="$(python3 --version | sed -n 's/^Python[[:space:]]*\([0-9]*\.[0-9]*\)\..*/\1/p')" \
  -Donnxruntime_BUILD_SHARED_LIB=ON \
  -Donnxruntime_DISABLE_SPARSE_TENSORS="%{DISABLE_SPARSE_TENSORS}" \
  -Donnxruntime_BUILD_UNIT_TESTS=OFF \
  ../cmake

N_PARALLEL=$([ $(/usr/bin/getconf _NPROCESSORS_ONLN) -gt %{MAX_N_PARALLEL} ] && echo %{MAX_N_PARALLEL} || echo $(/usr/bin/getconf _NPROCESSORS_ONLN))
cmake --build . --parallel "${N_PARALLEL}"

popd

%install

pushd build
DESTDIR=%{buildroot} cmake --install . --prefix %{_prefix}
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%manifest onnxruntime.manifest
%license LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/onnxruntime/*
%{_libdir}/cmake/onnxruntime/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libonnxruntime.pc

%changelog
* Thu Jan 08 2024 Suyeon Kim <suyeon5.kim@samsung.com>
- Initial packaging of ONNX Runtime v1.16.3
