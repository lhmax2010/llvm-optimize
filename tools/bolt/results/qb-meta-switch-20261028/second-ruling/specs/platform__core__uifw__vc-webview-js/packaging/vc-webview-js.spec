Name:       vc-webview-js
Summary:    Web voice touch javascript source
Version:    0.0.1
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  cmake

%description
Javascript source package to run web voice touch function on web application runtime

%prep
%setup -q
cp %{SOURCE1001} .

%build
export LDFLAGS+=" -Wl,--rpath=%{_libdir} -Wl,--hash-style=both -Wl,--as-needed,-lgcov"
rm -rf objdir
mkdir objdir

cd objdir
cmake .. -DVERSION=%{version} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_BUILD_TYPE=Debug \
    -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE

make %{?jobs:-j%jobs}

%install
(cd objdir &&
%make_install)

%clean
rm -rf %{buildroot}

%post

%files
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{TZ_SYS_RO_SHARE}/voice/vc-webview/res/js/*
%{TZ_SYS_RO_SHARE}/voice/vc-webview/res/js_custom/*
