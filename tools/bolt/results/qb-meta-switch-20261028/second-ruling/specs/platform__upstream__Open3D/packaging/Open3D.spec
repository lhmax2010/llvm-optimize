Name: Open3D
Summary: Open3D library
Version: 0.17
Release: 2
Group: Development/Libraries
License: MIT
Source0: %{name}-%{version}.tar.gz
Source100: 3rdparty_downloads.tar.bz2
Source1001: 1001-TIZEN-OPEN3D-BUILD.patch
ExclusiveArch: aarch64

BuildRequires: cmake
BuildRequires: nasm
BuildRequires: gcc-fortran
BuildRequires: minizip-devel
BuildRequires: pkg-config
BuildRequires: openblas-devel
BuildRequires: jsoncpp-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: python3-devel
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(openssl3)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Open3D: A Modern Library for 3D Data Processing.

%package devel
Summary:    Open3D Library (Dev)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Open3D: A Modern Library (Dev) for 3D Data Processing.

%prep
%setup -q
%setup -q -T -D -a 100

cp %{SOURCE1001} .
patch -p1 < %{SOURCE1001}

%build
mkdir -p build
cd build
cmake .. \
	-DTIZEN=TRUE \
	-DLINUX_AARCH64=TRUE \
	-DBUILD_AZURE_KINECT=OFF \
	-DBUILD_BENCHMARKS=ON \
	-DBUILD_CACHED_CUDA_MANAGER=OFF \
	-DBUILD_COMMON_CUDA_ARCHS=OFF \
	-DBUILD_COMMON_ISPC_ISAS=OFF \
	-DBUILD_CUDA_MODULE=OFF \
	-DBUILD_EXAMPLES=ON \
	-DBUILD_FILAMENT_FROM_SOURCE=ON \
	-DBUILD_GUI=OFF \
	-DBUILD_ISPC_MODULE=OFF \
	-DBUILD_JUPYTER_EXTENSION=OFF \
	-DBUILD_LIBREALSENSE=OFF \
	-DBUILD_PYTHON_MODULE=OFF \
	-DBUILD_PYTORCH_OPS=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_TENSORFLOW_OPS=OFF \
	-DBUILD_UNIT_TESTS=ON \
	-DBUILD_VTK_FROM_SOURCE=ON \
	-DBUILD_WEBRTC=OFF \
	-DBUNDLE_OPEN3D_ML=OFF \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=/usr \
	-DDEVELOPER_BUILD=ON \
	-DENABLE_CACHED_CUDA_MANAGER=OFF \
	-DENABLE_HEADLESS_RENDERING=OFF \
	-DFETCHCONTENT_FULLY_DISCONNECTED=OFF \
	-DFETCHCONTENT_QUIET=ON \
	-DFETCHCONTENT_UPDATES_DISCONNECTED=OFF \
	-DFETCHCONTENT_UPDATES_DISCONNECTED_EXT_OPEN3D_SPHINX_THEME=OFF \
	-DGLFW_USE_MIR=OFF \
	-DGLFW_USE_WAYLAND=OFF \
	-DGLFW_VULKAN_STATIC=OFF \
	-DGLIBCXX_USE_CXX11_ABI=ON \
	-DLIB_SUFFIX:STRING= \
	-DPREFER_OSX_HOMEBREW=OFF \
	-DSTATIC_WINDOWS_RUNTIME=OFF \
	-DUSE_BLAS=ON \
	-DUSE_LINUX_MKL_FROM_CONDA_REPO=OFF \
	-DUSE_SYSTEM_BLAS=ON \
	-DUSE_SYSTEM_EIGEN3=OFF \
	-DUSE_SYSTEM_FMT=OFF \
	-DUSE_SYSTEM_GLEW=OFF \
	-DUSE_SYSTEM_GLFW=OFF \
	-DUSE_SYSTEM_IMGUI=OFF \
	-DUSE_SYSTEM_JPEG=ON \
	-DUSE_SYSTEM_LIBLZF=OFF \
	-DUSE_SYSTEM_LIBREALSENSE=OFF \
	-DUSE_SYSTEM_PNG=ON \
	-DUSE_SYSTEM_PYBIND11=OFF \
	-DUSE_SYSTEM_QHULLCPP=OFF \
	-DUSE_SYSTEM_TINYGLTF=OFF \
	-DUSE_SYSTEM_TINYOBJLOADER=OFF \
	-DWITH_FAISS=OFF \
	-DWITH_IPPICV=OFF \
	-DWITH_OPENMP=ON \
	-DUSE_SYSTEM_CURL=ON \
	-DUSE_SYSTEM_OPENSSL=ON \
	-DUSE_SYSTEM_JSONCPP=ON

make %{?jobs:-j%jobs}

%install
cd build
rm -rf %{buildroot}
%make_install
strip %{buildroot}%{_libdir}/libOpen3D.so

%clean
rm -rf %{buildroot}

%pre

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest Open3D.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/*.so

%files devel
/usr/include/open3d
%{_libdir}/pkgconfig/Open3D.pc
%{_libdir}/cmake/Open3D/*.cmake

