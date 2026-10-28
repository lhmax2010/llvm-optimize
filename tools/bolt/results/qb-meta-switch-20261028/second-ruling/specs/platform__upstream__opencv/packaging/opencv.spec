%if 0%{?_with_da_profile}%{?CV_VIDEOIO_BACKEND_GSTREAMER}
%define support_gstreamer 1
%else
%define support_gstreamer 0
%endif

Name: opencv
Summary: OpenCV library
Version: 4.7.0
Release: 8
Group: Development/Libraries
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source100: opencv-contrib-%{version}.tar.gz
# In cmake/OpenCVDetectPython.cmake, python packages are installed
# in lib/ regardless of i586, armv7l, x86_64, aarch64, riscv64
# So, this patch installs the python packages in:
# lib64/ if x86_64 or aarch64
# lib/ if i586 or armv7l
Source1001: 1001-TIZEN-OPENCV-PYTHON3-LIB64-PATH.patch
#`numpy.distutils` is removed in numpy 1.26 on Python 3.12.
Source1002: 1002-numpy.distutils-is-removed-in-numpy-1.26-on-Python-3.patch

BuildRequires:  cmake
BuildRequires:  pkg-config
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  libavutil-devel
BuildRequires:  libavcodec-devel
BuildRequires:  libavformat-devel
BuildRequires:  libswscale-devel
BuildRequires:  pkgconfig(libwebp)
#support python3
%if "%{?profile}" != "tv"
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-numpy-devel
%endif

Requires(post):  /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
The Open Computer Vision Library includes various algorithms for computer vision problems.

%package devel
Summary:    OpenCV Library (Dev)
Group:      Development/Libraries
Requires:    %{name} = %{version}-%{release}

%description devel
The Open Computer Vision Library (Dev) includes various algorithms for computer vision problems.

%if "%{?profile}" != "tv"
%package -n python3-opencv
Summary:    OpenCV Python3 Library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description -n python3-opencv
The Open Computer Vision Library (Python3) includes various algorithms for computre vision problems.
%endif

%prep
%setup -q
%setup -q -T -D -a 100

cp %{SOURCE1001} .
cp %{SOURCE1002} .
patch -p1 < %{SOURCE1001}
patch -p1 < %{SOURCE1002}

%build
%ifarch aarch64
ARCH=aarch64
%endif
%ifarch %arm
ARCH=arm
%endif
%ifarch x86_64
ARCH=x86_64
%endif
%ifarch %ix86
ARCH=i386
%endif
%ifarch riscv64
ARCH=riscv64
%endif

# compatibility to opencv3
sed -i 's/opencv4.pc/opencv.pc/g' cmake/OpenCVGenPkgconfig.cmake

# FFMPEG's TIZEN_FEATURE_LIBAV feature.
export CFLAGS+=" -DTIZEN_FEATURE_LIBAV"
export CXXFLAGS+=" -DTIZEN_FEATURE_LIBAV"

mkdir -p build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr \
	-DARCH=${ARCH} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CONFIGURATION_TYPES=Release \
	-DOPENCV_ENABLE_NONFREE=OFF \
	-DOPENCV_GENERATE_PKGCONFIG=YES \
	-DOPENCV_GENERATE_SETUPVARS=OFF \
	-DBUILD_PROTOBUF=ON \
	-DPROTOBUF_UPDATE_FILES=OFF \
	-DBUILD_opencv_calib3d=ON \
	-DBUILD_opencv_core=ON \
	-DBUILD_opencv_dnn=ON \
	-DBUILD_opencv_features2d=ON \
	-DBUILD_opencv_flann=ON \
	-DBUILD_opencv_highgui=ON \
	-DBUILD_opencv_imgcodecs=ON \
	-DBUILD_opencv_imgproc=ON \
	-DBUILD_opencv_ml=ON \
	-DBUILD_opencv_objdetect=ON \
	-DBUILD_opencv_photo=ON \
	-DBUILD_opencv_python2=OFF \
%if "%{?profile}" != "tv"
	-DBUILD_opencv_python3=ON \
%else
	-DBUILD_opencv_python3=OFF \
	-DPARALLEL_ENABLE_PLUGINS=OFF \
%endif
	-DBUILD_opencv_shape=OFF \
	-DBUILD_opencv_stitching=OFF \
	-DBUILD_opencv_superres=OFF \
	-DBUILD_opencv_ts=OFF \
	-DBUILD_opencv_video=ON \
	-DBUILD_opencv_videoio=ON \
	-DBUILD_opencv_videostab=OFF \
	-DBUILD_opencv_world=OFF \
	-DBUILD_opencv_viz=OFF \
	-DOPENCV_EXTRA_MODULES_PATH=../opencv-contrib/modules \
	-DBUILD_opencv_aruco=OFF \
	-DBUILD_opencv_bgsegm=OFF \
	-DBUILD_opencv_bioinspired=OFF \
	-DBUILD_opencv_ccalib=OFF \
	-DBUILD_opencv_cnn_3dobj=OFF \
	-DBUILD_opencv_cvv=OFF \
	-DBUILD_opencv_datasets=OFF \
	-DBUILD_opencv_dnn_objdetect=OFF \
	-DBUILD_opencv_dnns_easily_fooled=OFF \
	-DBUILD_opencv_dnn_superres=OFF \
	-DBUILD_opencv_dpm=OFF \
	-DBUILD_opencv_face=ON \
	-DBUILD_opencv_freetype=OFF \
	-DBUILD_opencv_fuzzy=OFF \
	-DBUILD_opencv_hdf=OFF \
	-DBUILD_opencv_hfs=OFF \
	-DBUILD_opencv_img_hash=OFF \
	-DBUILD_opencv_line_descriptor=OFF \
	-DBUILD_opencv_matlab=OFF \
	-DBUILD_opencv_optflow=ON \
	-DBUILD_opencv_ovis=OFF \
	-DBUILD_opencv_phase_unwrapping=OFF \
	-DBUILD_opencv_plot=ON \
	-DBUILD_opencv_quality=OFF \
	-DBUILD_opencv_reg=OFF \
	-DBUILD_opencv_rgbd=OFF \
	-DBUILD_opencv_saliency=OFF \
	-DBUILD_opencv_sfm=OFF \
	-DBUILD_opencv_shape=OFF \
	-DBUILD_opencv_stereo=OFF \
	-DBUILD_opencv_structured_light=OFF \
	-DBUILD_opencv_superres=OFF \
	-DBUILD_opencv_surface_matching=OFF \
	-DBUILD_opencv_text=OFF \
	-DBUILD_opencv_tracking=ON \
	-DBUILD_opencv_videostab=OFF \
	-DBUILD_opencv_viz=OFF \
	-DBUILD_opencv_xfeatures2d=ON \
	-DBUILD_opencv_ximgproc=ON \
	-DBUILD_opencv_xobjdetect=OFF \
	-DBUILD_opencv_xphoto=OFF \
	-DBUILD_opencv_wechat_qrcode=OFF \
	-DBUILD_opencv_barcode=OFF \
	-DBUILD_opencv_intensity_transform=OFF \
	-DBUILD_opencv_mcc=OFF \
	-DBUILD_opencv_rapid=OFF \
	-DOPENCV_FORCE_3RDPARTY_BUILD=OFF \
	-DBUILD_ZLIB=OFF \
	-DBUILD_TIFF=OFF \
	-DBUILD_JASPER=OFF \
	-DBUILD_JPEG=OFF \
	-DBUILD_PNG=OFF \
	-DBUILD_WEBP=OFF \
	-DBUILD_OPENEXR=OFF \
	-DBUILD_TBB=OFF \
	-DBUILD_OPENJPEG=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_opencv_apps=OFF \
	-DBUILD_opencv_js=OFF \
	-DBUILD_DOCS=OFF \
	-DBUILD_EXAMPLES=OFF \
	-DBUILD_PACKAGE=OFF \
	-DBUILD_PERF_TESTS=OFF \
	-DBUILD_TESTS=OFF \
	-DBUILD_WITH_DEBUG_INFO=ON \
	-DBUILD_WITH_DYNAMIC_IPP=OFF \
	-DBUILD_ANDROID_SERVICE=OFF \
	-DBUILD_IPP_IW=OFF \
	-DBUILD_ITT=OFF \
	-DBUILD_WITH_STATIC_CRT=OFF \
	-DBUILD_JAVA=OFF \
	-DBUILD_opencv_java=OFF \
	-DBUILD_FAT_JAVA_LIB=OFF \
	-DBUILD_CUDA_STUBS=OFF \
	-DWITH_CUDA=OFF \
	-DWITH_CAROTENE=OFF \
	-DWITH_CPUFEATURES=OFF \
	-DWITH_1394=OFF \
	-DWITH_CSTRIPES=OFF \
	-DWITH_CUBLAS=OFF \
	-DWITH_CUFFT=OFF \
	-DWITH_NVCUVID=OFF \
	-DWITH_DSHOW=OFF \
	-DWITH_EIGEN=OFF \
	-DWITH_FFMPEG=ON \
	-DWITH_GIGEAPI=OFF \
	-DWITH_INTELPERC=OFF \
	-DWITH_IPP=OFF \
	-DWITH_JASPER=OFF \
	-DWITH_OPENJPEG=OFF \
	-DWITH_WEBP=ON \
	-DWITH_MSMF=OFF \
	-DWITH_NVCUVID=OFF \
	-DWITH_OPENCL=OFF \
	-DWITH_OPENCLAMDBLAS=OFF \
	-DWITH_OPENCLAMDFFT=OFF \
	-DWITH_OPENEXR=OFF \
	-DWITH_OPENGL=OFF \
	-DWITH_OPENMP=OFF \
	-DWITH_OPENNI=OFF \
	-DWITH_JPEG=ON \
	-DWITH_PNG=ON \
	-DWITH_PVAPI=OFF \
	-DWITH_QT=OFF \
	-DWITH_TBB=OFF \
	-DWITH_TIFF=ON \
	-DWITH_VFW=OFF \
	-DWITH_VTK=OFF \
	-DWITH_WIN32UI=OFF \
	-DWITH_XIMEA=OFF \
	-DWITH_QUIRC=OFF \
%if 0%{?support_gstreamer}
	-DWITH_GSTREAMER=ON \
%else
	-DWITH_GSTREAMER=OFF \
%endif
	-DWITH_V4L=ON \
	-DWITH_GTK=OFF \
	-DWITH_MATLAB=OFF \
	-DWITH_ITT=OFF \
	-DWITH_GPHOTO2=OFF \
	-DWITH_PTHREADS_PF=OFF \
	-DWITH_LAPACK=OFF \
	-DWITH_OPENVX=OFF \
	-DWITH_PROTOBUF=ON \
	-DWITH_ADE=OFF \
	-DINSTALL_C_EXAMPLES=OFF \
	-DINSTALL_PYTHON_EXAMPLES=OFF \
	-DINSTALL_TESTS=OFF \
	-DINTALL_ANDROID_EXAMPLES=OFF \
	-DENABLE_PRECOMPILED_HEADERS=OFF \
	-DENABLE_DYNAMIC_CUDA=OFF \
	-DENABLE_SOLUTION_FOLDERS=OFF \
	-DENABLE_PROFILLING=OFF \
	-DENABLE_COVERAGE=OFF \
%ifarch %arm aarch64
	-DCPU_BASELINE="" \
	-DCPU_DISPATCH=NEON \
%endif
	-DCV_TRACE=OFF

make %{?jobs:-j%jobs}

%install
cd build
rm -rf %{buildroot}
%make_install

# To support backward compatibility with OpenCV3
# Header files
ln -sf %{_includedir}/opencv4/opencv2 %{buildroot}%{_includedir}/opencv2
# pkgconfig
ln -sf %{_libdir}/pkgconfig/opencv.pc %{buildroot}%{_libdir}/pkgconfig/%{name}4.pc
# cascades files
mkdir -p %{buildroot}%{_datadir}/OpenCV
ln -sf %{_datadir}/opencv4/haarcascades %{buildroot}%{_datadir}/OpenCV/haarcascades
ln -sf %{_datadir}/opencv4/lbpcascades %{buildroot}%{_datadir}/OpenCV/lbpcascades

ln -sf %{_libdir}/cmake/opencv4/OpenCVConfig-version.cmake %{buildroot}%{_datadir}/OpenCV/OpenCVConfig-version.cmake
ln -sf %{_libdir}/cmake/opencv4/OpenCVConfig.cmake %{buildroot}%{_datadir}/OpenCV/OpenCVConfig.cmake
ln -sf %{_libdir}/cmake/opencv4/OpenCVModules-release.cmake %{buildroot}%{_datadir}/OpenCV/OpenCVModules-release.cmake
ln -sf %{_libdir}/cmake/opencv4/OpenCVModules.cmake %{buildroot}%{_datadir}/OpenCV/OpenCVModules.cmake

%clean
rm -rf %{buildroot}

%pre
if [ -d %{_datadir}/OpenCV ];then
 rm -r %{_datadir}/OpenCV
fi

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest opencv.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/*.so*

/usr/share/licenses/opencv4/*
/usr/share/opencv4/haarcascades/*frontalface_alt*
/usr/share/opencv4/haarcascades/*smile*
/usr/share/opencv4/lbpcascades/*frontalface*
/usr/share/OpenCV/OpenCV*
/usr/share/OpenCV/haarcascades
/usr/share/OpenCV/lbpcascades

%exclude /usr/share/opencv4/haarcascades/*eye*
%exclude /usr/share/opencv4/haarcascades/*catface*
%exclude /usr/share/opencv4/haarcascades/*default*
%exclude /usr/share/opencv4/haarcascades/*plate*
%exclude /usr/share/opencv4/haarcascades/*body*
%exclude /usr/share/opencv4/haarcascades/*profile*
%exclude /usr/share/opencv4/haarcascades/*2splits*

%exclude /usr/share/opencv4/lbpcascades/*catface*
%exclude /usr/share/opencv4/lbpcascades/*profile*
%exclude /usr/share/opencv4/lbpcascades/*silverware*
%exclude /usr/share/opencv4/*.supp

%if "%{?profile}" != "tv"
%files -n python3-opencv
%{python3_sitearch}/cv2/*.py
%{python3_sitearch}/cv2/*/*.py
%{python3_sitearch}/cv2/*/*.so
%endif

%files devel
/usr/include/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/opencv4/*.cmake
%doc
