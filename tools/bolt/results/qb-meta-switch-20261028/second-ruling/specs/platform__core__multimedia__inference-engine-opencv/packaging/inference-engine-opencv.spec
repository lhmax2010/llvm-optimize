Name:       inference-engine-opencv
Summary:    OpenCV based implementation of inference-engine-interface
Version:    0.0.2
Release:    7
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(opencv)
BuildRequires: pkgconfig(inference-engine-interface-common)

%description
OpenCV based implementation of inference-engine-interface


%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

#MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
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
