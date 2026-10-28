Name:       dfs-opencv
Summary:    OpenCV based Depth-from-Stereo implementation
Version:    1.0.12
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(dfs-adaptation)
BuildRequires: pkgconfig(opencv)
BuildRequires: pkgconfig(libtzplatform-config)

%description
OpenCV based Depth-from-Stereo implementation


%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

export CXXFLAGS+=" -DDFS_CALIB_FILE_PATH=\\\"%{TZ_SYS_RO_SHARE}/%{name}/\\\""

%cmake .

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/capi-media-vision
cp res/*.yaml %{buildroot}%{_datadir}/capi-media-vision
cp res/*.json %{buildroot}%{_datadir}/capi-media-vision

%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_datadir}/capi-media-vision/*.yaml
%{_datadir}/capi-media-vision/*.json
