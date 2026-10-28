%define app_rootstrap_install_path	/opt/data/app-rootstrap
%define app_rootstrap_nuget_path	/nuget
%define app_rootstrap_sbi_plugin_path	/opt/usr/data/tools/smart-build-interface/plugins

%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

%if "%{tizen_profile_name}" == "tv"
%define WITH_VD 1
%else
%define WITH_VD 0
%endif

%if "%{mv_prj}" == "1"
%define WITH_VD_MV 1
%else
%define WITH_VD_MV 0
%endif

%if "%{WITH_VD}" == "1" || "%{WITH_VD_MV}" == "1"
%define INCLUDE_INTERNAL 1
%else
%define INCLUDE_INTERNAL 0
%endif

Name:		app-rootstrap
Summary:	Package for rootstrap of app
Version:	11.0.1
Release:	1
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
AutoReqProv:    no

BuildRequires:	cmake
BuildRequires:	xmlstarlet
BuildRequires:	python3
BuildRequires:	pkgconfig

Requires: edje-bin
Requires: gettext-tools
Requires: jdk

# Public Tizen provides Native public API
BuildRequires:	app-rootstrap-native-data-public
# Public Tizen provides Native internal API
BuildRequires:	app-rootstrap-native-data-internal
# Public Tizen provides CSharp public and internal API
BuildRequires:	app-rootstrap-csharp-data-common

%if "%{WITH_DA}" == "1"
# DA provides Native Internal API
BuildRequires:	app-rootstrap-native-data-da
# DA provides CSharp Internal API
BuildRequires:	app-rootstrap-csharp-data-da
%endif

### app-rootstrap
%description
Package that creates rootstrap by app type

### app-rootstrap-devel
%package devel
Summary:	Development files for app-rootstrap
Group:		Development/Libraries
AutoReqProv: no
Provides:	pkgconfig(app-rootstrap)
Requires:	pkgconfig(libtzplatform-config)

%description devel
Development files for app-rootstrap including native rootstrap and csharp nuget packages

%prep
%setup -q

%build
%cmake . -DCMAKE_LIBDIR_PREFIX=%{_libdir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir %{buildroot}
mkdir -p %{buildroot}%{_bindir}

./generate_rootstrap.sh "%{_arch}" "%{buildroot}%{app_rootstrap_install_path}" "%{INCLUDE_INTERNAL}"
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
cp packaging/app-rootstrap.pc %{buildroot}%{_libdir}/pkgconfig/
# Copy nuget packages
cp -r %{buildroot}%{app_rootstrap_install_path}%{app_rootstrap_nuget_path} %{buildroot}%{app_rootstrap_nuget_path}
# Copy tizen macro under /etc for build environment
cp -r %{buildroot}%{app_rootstrap_install_path}/etc %{buildroot}/etc

rm -f "%{buildroot}%{app_rootstrap_install_path}/%{_libdir}/pkgconfig/libtzplatform-config.pc"

./modify_pc.py "%{buildroot}%{_libdir}/pkgconfig/app-rootstrap.pc" "%{buildroot}%{app_rootstrap_install_path}/%{_libdir}/pkgconfig"
rm -f "%{buildroot}%{app_rootstrap_install_path}/%{_libdir}/pkgconfig/*.pc"
rm -rf "%{buildroot}%{app_rootstrap_install_path}%{app_rootstrap_nuget_path}"

find %{buildroot} -name "app-rootstrap.pc" -exec sed -i 's/ -Wl,--wrap=[^ ]*//g' {} +
find %{buildroot} -name "app-rootstrap.pc" -exec sed -i 's/ -Dmain=SDL_main//g' {} +

# Inject -B<libdir>/ into Libs: so consumers can find *.o startup file automatically
find %{buildroot} -name "app-rootstrap.pc" -exec sed -i 's|^Libs:|Libs: -B%{app_rootstrap_install_path}%{_libdir}/|' {} +

mkdir -p %{buildroot}%{app_rootstrap_sbi_plugin_path}
DEV_XML_FILE=
case "%{_arch}" in
    arm|armv7l|armv7hl)
        DEV_XML_FILE=tizen-11.0-device.core.public.dev.xml
        ;;
    aarch64)
        DEV_XML_FILE=tizen-11.0-device64.core.public.dev.xml
        ;;
esac

if [ -n "${DEV_XML_FILE}" ]; then
    PKG_CONFIG_LIBDIR=%{buildroot}%{_libdir}/pkgconfig \
    PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig \
        ./script/generate_dev_xml.sh \
            %{buildroot}%{app_rootstrap_sbi_plugin_path}/${DEV_XML_FILE}
fi

# Remove /etc files from buildroot - not packaged by app-rootstrap
rm -rf %{buildroot}/etc

%files

%files devel
%{app_rootstrap_install_path}
%exclude %dir %{app_rootstrap_install_path}/%{_includedir}
%{app_rootstrap_install_path}/%{_includedir}
%{_libdir}/pkgconfig/app-rootstrap.pc
%{app_rootstrap_nuget_path}
%{app_rootstrap_sbi_plugin_path}
