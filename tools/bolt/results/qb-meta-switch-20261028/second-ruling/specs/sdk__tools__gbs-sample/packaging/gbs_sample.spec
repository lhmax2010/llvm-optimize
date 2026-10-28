Name:     org.example.gbs-sample
Version:  1.0.0
Release:  1
License:  Samsung Electronics. Co., Ltd.
Summary:  Tizen
Group:    Applications/Native Applciation
Source0:  %{name}-%{version}.tar.gz

BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: prebuilt-tizensdk
#BuildRequires: native-dev-rootstrap
#BuildRequires: hash-signer

%global debug_package %{nil}
%global __debug_install_post %{nil}

%ifarch %arm
%define SDK_PLATFORM tizen-10.0-device.core.public
%endif

%ifarch aarch64
%define SDK_PLATFORM tizen-10.0-device64.core.public
%endif

%ifarch x86_64
%define SDK_PLATFORM tizen-10.0-emulator64.core.public
%endif

%ifarch riscv64
%define SDK_PLATFORM tizen-10.0-riscv64.core.public
%endif

%define APP_PACKAGE %{name}-%{version}-%{_arch}.tpk
%define preload_ro_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk
%define preload_rw_tpk_path %{TZ_SYS_RO_APP}/.preload-rw-tpk
%define configuration Release
%define exec_name gbs-sample
%define nonstrip_bin nonstrip/bin
%define nonstrip_lib nonstrip/lib



%description
%{summary}

%package nonstrip
Summary: nonstrip package
 
%description nonstrip
nonstrip package

%package rw-version
Summary: %{summary}
Requires(post): pkgmgr-tool

%description rw-version
Application package for rw area.

%package rw-version-nonstrip
Summary: nonstrip package for rw-version

%description rw-version-nonstrip
nonstrip package for rw-version

%prep
%setup -q

%clean
rm -fr %{buildroot}

%build
pwd
tizen build-native -a %{_arch} -c gcc -C %{configuration} %{?jobs:-j %jobs} -r %{SDK_PLATFORM}
#tizen build-native -a %{_arch} -c gcc -r %{SDK_PLATFORM}

# copy nonstrip
if [ -e "./lib/" ]; then
    /usr/bin/mkdir -p ./%{nonstrip_lib}
    /usr/bin/cp -f ./lib/*.so ./%{nonstrip_lib}/
    /usr/bin/strip -v -s ./lib/*.so
fi

/usr/bin/mkdir -p ./%{nonstrip_bin}
/usr/bin/cp -f ./%{configuration}/%{exec_name} ./%{nonstrip_bin}/
/usr/bin/strip -v -s ./%{configuration}/%{exec_name}

if [ -e "./%{configuration}/res/locale" ]; then
cp -rf %{configuration}/res/locale shared/res
cp -rf %{configuration}/res/locale shared/res
fi

tizen cli-config "profiles.path=/usr/tizen-studio-data/profile/profiles.xml"
tizen package -- ./%{configuration}/ -t tpk -s tizen-certificates

%install
mkdir -p %{buildroot}%{preload_ro_tpk_path}
mkdir -p %{buildroot}%{preload_rw_tpk_path}
install ./%{configuration}/%{APP_PACKAGE} %{buildroot}%{preload_ro_tpk_path}
install ./%{configuration}/%{APP_PACKAGE} %{buildroot}%{preload_rw_tpk_path}

# install nonstrip
install -d %{buildroot}/%{TZ_SYS_RO_APP}/%{name}
install -d %{buildroot}/%{TZ_SYS_RW_APP}/%{name}
mkdir -p %{buildroot}/usr/apps/%{name}/shared/res
mkdir -p %{buildroot}/opt/usr/globalapps/%{name}/shared/res
if [ -e "./%{nonstrip_bin}" ]; then
    cp -rf ./%{nonstrip_bin} %{buildroot}/usr/apps/%{name}
    cp -rf ./%{nonstrip_bin} %{buildroot}/opt/usr/globalapps/%{name}
fi
if [ -e "./%{configuration}/res" ]; then
    cp -rf %{configuration}/res %{buildroot}/usr/apps/%{name}
    cp -rf %{configuration}/res %{buildroot}/opt/usr/globalapps/%{name}
    cp -rf %{configuration}/res/locale %{buildroot}/usr/apps/%{name}/shared/res
    cp -rf %{configuration}/res/locale %{buildroot}/opt/usr/globalapps/%{name}/shared/res
fi
if [ -e "./%{nonstrip_lib}" ]; then
    cp -rfP ./%{nonstrip_lib} %{buildroot}/usr/apps/%{name}
    cp -rfP ./%{nonstrip_lib} %{buildroot}/opt/usr/globalapps/%{name}
fi

%files
%defattr(-,root,root,-)
%{preload_ro_tpk_path}/%{APP_PACKAGE}

%files rw-version
%defattr(-,root,root,-)
%{preload_rw_tpk_path}/%{APP_PACKAGE}

%files nonstrip
%{TZ_SYS_RO_APP}/%{name}

%files rw-version-nonstrip
%{TZ_SYS_RW_APP}/%{name}
