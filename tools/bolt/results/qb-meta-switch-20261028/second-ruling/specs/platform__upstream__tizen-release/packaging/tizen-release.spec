Name:           tizen-release
Version:        11.0.0
Release:        0
License:        Apache-2.0
Summary:        Tizen release files
Url:            http://www.tizen.org
Group:          System/Base
Provides:       system-release = %{version}
Provides:       tizen-release = %{version}
Provides:       product()
Provides:       product(Tizen) = %{version}
BuildRequires:  sed
Source1001:     LICENSE.APLv2

#HACK
Provides:       lsb = 4.1

%description
Tizen release files such as various /etc/ files that define the release.

%prep

%define release_type_default eng

%if z%{?tizen_build_devel_mode} == z && z%{?tizen_build_binary_release_type_eng} == z
	%define release_type %release_type_default
%else
	%if 0%{?tizen_build_devel_mode} == 1 || 0%{?tizen_build_devel_mode} == 1
		%define release_type %release_type_default
	%else
		%define release_type user
	%endif
%endif

%define build_variant_default NONE
%define build_variant %{?tizen_build_variant}%{?!tizen_build_variant:%{build_variant_default}}
cp %{SOURCE1001} .

%build

%install

%ifarch  %{ix86}
%define _tarch ia32
%else
%define _tarch %{_arch}
%endif

install -d %{buildroot}/etc
cat > %{buildroot}%{_sysconfdir}/tizen-release <<EOF
%{release_name} %{tizen_full_version} (%{_arch})
VERSION = %{tizen_full_version}
CODENAME = TELEVEN
EOF

ln -s tizen-release %{buildroot}%{_sysconfdir}/system-release

cat > %{buildroot}%{_sysconfdir}/os-release <<EOF
NAME=Tizen
VERSION="%{tizen_full_version} (%{release_name})"
ID=tizen
VERSION_ID=%{tizen_full_version}
PRETTY_NAME="Tizen %{tizen_full_version} (%{release_name})"
ANSI_COLOR="0;36"
CPE_NAME="cpe:/o:tizen:tizen:%{tizen_full_version}"
EOF

mkdir -p %{buildroot}%{_sysconfdir}/products.d
cat >%{buildroot}%{_sysconfdir}/products.d/tizen.prod.unified << EOF
<?xml version="1.0" encoding="UTF-8"?>
<product schemeversion="0">
  <vendor>Tizen.org</vendor>
  <name>Tizen</name>
  <version>%{tizen_full_version}</version>
  <release>%{release_name}</release>
  <arch>%{_target_cpu}</arch>
  <productline>Tizen</productline>
  <register>
    <target>tizen-%{tizen_full_version}-%{_target_cpu}</target>
    <release></release>
    <repositories>
    </repositories>
  </register>
  <updaterepokey>000000000</updaterepokey>
  <summary>Tizen</summary>
  <description>Tizen</description>
  <linguas>
    <language>cs</language>
    <language>da</language>
    <language>de</language>
    <language>en</language>
    <language>en_GB</language>
    <language>en_US</language>
    <language>es</language>
    <language>fi</language>
    <language>fr</language>
    <language>hu</language>
    <language>it</language>
    <language>ja</language>
    <language>nb</language>
    <language>nl</language>
    <language>pl</language>
    <language>pt</language>
    <language>pt_BR</language>
    <language>ru</language>
    <language>sv</language>
    <language>zh</language>
    <language>zh_CN</language>
    <language>zh_TW</language>
  </linguas>
  <urls>
    <url name="releasenotes">http://www.tizen.org</url>
    <url name="register">http://www.tizen.org/</url>
    <url name="repository">https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/latest/repos/%{_repository}/packages/%{_tarch}/</url>
  </urls>
  <buildconfig>
    <producttheme>Tizen</producttheme>
    <betaversion></betaversion>
  </buildconfig>
  <installconfig>
    <defaultlang>en_US</defaultlang>
    <releasepackage name="tizen-release" flag="EQ" version="%{tizen_full_version}" release="%{release}" />
    <distribution>Tizen</distribution>
  </installconfig>
  <runtimeconfig />
</product>

EOF

# this is a base product, create symlink
ln -s tizen.prod %{buildroot}%{_sysconfdir}/products.d/baseproduct


# generate tizen-build.conf


cat > %{buildroot}%{_sysconfdir}/tizen-build.conf.unified <<'EOF'
TZ_BUILD_RELEASE_NAME="%{release_name}"
TZ_BUILD_VERSION=%{tizen_version}
TZ_BUILD_FULLVER=%{tizen_full_version}
TZ_BUILD_RELEASE_TYPE=%{release_type}
TZ_BUILD_VARIANT=%{build_variant}

TZ_BUILD_PROFILE=common
TZ_BUILD_PROJECT=%{_project}
%{?asan:TZ_BUILD_REF_PROJECT=%{_ref_project}}
TZ_BUILD_VENDOR=%{vendor}
TZ_BUILD_REPO=%{_repository}
TZ_BUILD_ARCH=%{_arch}

TZ_BUILD_ID=@BUILD_ID@
TZ_BUILD_DATE=@BUILD_DATE@
TZ_BUILD_TIME=@BUILD_TIME@
TZ_BUILD_TS=@BUILD_TS@

TZ_BUILD_URL=http://download.tizen.org
TZ_BUILD_SNAPSHOT_URL=${TZ_BUILD_URL}/snapshots/TIZEN/Tizen/Tizen-Unified/
TZ_BUILD_DAILY_URL=${TZ_BUILD_URL}/releases/daily/TIZEN/Tizen/Tizen-Unified/
TZ_BUILD_WEEKLY_URL=${TZ_BUILD_URL}/releases/weekly/TIZEN/Tizen/Tizen-Unified/
TZ_BUILD_MILESTONE_URL=${TZ_BUILD_URL}/releases/milestone/TIZEN/Tizen/Tizen-Unified/

TZ_BUILD_WITH_MESA=%{?_with_mesa}
TZ_BUILD_WITH_WAYLAND=%{?_with_wayland}
TZ_BUILD_WITH_RDP=%{?_with_rdp}
TZ_BUILD_WITH_X=%{?_with_x}

EOF

%post
ln -sf tizen.prod.unified %{_sysconfdir}/products.d/tizen.prod
ln -sf tizen-build.conf.unified %{_sysconfdir}/tizen-build.conf
%preun
rm %{_sysconfdir}/products.d/tizen.prod
rm %{_sysconfdir}/tizen-build.conf


%files
%config %attr(0644,root,root) %{_sysconfdir}/tizen-release
%config %attr(0644,root,root) %{_sysconfdir}/os-release
%license LICENSE.APLv2
%{_sysconfdir}/system-release
%{_sysconfdir}/products.d/baseproduct
%{_sysconfdir}/products.d/tizen.prod.unified
%config %attr(0444,root,root) %{_sysconfdir}/tizen-build.conf.unified
