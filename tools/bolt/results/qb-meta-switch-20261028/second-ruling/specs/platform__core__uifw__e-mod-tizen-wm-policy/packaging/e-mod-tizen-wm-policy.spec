%bcond_with x
%bcond_with wayland

Name:       e-mod-tizen-wm-policy
Summary:    The Enlightenment WM Policy Module for Tizen
Version:    0.6.14
Release:    1
Group:      Graphics & UI Framework/Other
License:    BSD-2-Clause and Flora-1.1
Source0:    %{name}-%{version}.tar.bz2
BuildRequires: pkgconfig(enlightenment)
BuildRequires: pkgconfig(ttrace)
BuildRequires: pkgconfig(sensor)
BuildRequires: pkgconfig(vconf)
%if %{with x}
BuildRequires: pkgconfig(x11)
%endif
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(tizen-policy-ext-server)

%if 0%{?TZ_SYS_RO_SHARE:1}
# TZ_SYS_RO_SHARE is defined
%else
%global TZ_SYS_RO_SHARE /usr/share
%endif

%description
The Enlightenment WM Policy Module for Tizen

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS+=" -DE_LOGGING=2 -Werror-implicit-function-declaration"
%if %{with wayland}
%reconfigure \
      --enable-wayland-only \
      --enable-auto-rotation
#      --enable-zoom-viewer
%else
%reconfigure
%endif
make %{?_smp_mflags}

%install
# install
%make_install

%files
%defattr(-,root,root,-)
%{_libdir}/enlightenment/modules/e-mod-tizen-wm-policy
%license COPYING COPYING.Flora

%define _unpackaged_files_terminate_build 0
