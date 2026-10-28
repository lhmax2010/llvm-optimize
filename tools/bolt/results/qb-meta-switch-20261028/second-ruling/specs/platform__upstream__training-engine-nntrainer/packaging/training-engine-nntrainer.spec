Name:       training-engine-nntrainer
Summary:    Training engine NNTrainer backend
Version:    0.1.5
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(training-engine-interface-common)
BuildRequires: pkgconfig(nntrainer)
BuildRequires: pkgconfig(capi-ml-training)
BuildRequires: pkgconfig(capi-ml-common)
BuildRequires: pkgconfig(capi-ml-inference)

%description
Training Engine NNTrainer backend of training-engine-interface

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

%cmake %{build_options} .

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
