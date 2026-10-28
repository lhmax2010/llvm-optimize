Name:       inference-engine-tflite
Summary:    Tensorflow-Lite based implementation of inference-engine-interface
Version:    0.0.9
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: python
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(inference-engine-interface-common)
BuildRequires: coregl-devel
BuildRequires: flatbuffers-devel
BuildRequires: tensorflow2-lite-devel

%description
Tensorflow-Lite based implementation of inference-engine-interface


%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

%cmake .

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_libdir}/*.so
