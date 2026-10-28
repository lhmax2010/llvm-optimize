%define name				hal-rootstrap
%define devel_name			hal-rootstrap-devel
%define hal_rootstrap_install_path	/opt/data/hal-rootstrap

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

%if "%{WITH_VD}" == "1" || "%{WITH_VD_MV}" == "1" || "%{WITH_DA}" == "1"
%define INCLUDE_INTERNAL 1
%else
%define INCLUDE_INTERNAL 0
%endif

Name:		hal-rootstrap
Summary:	Package for rootstrap of hal
Version:	10.0.0
Release:	1
#Group: 
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
AutoReqProv:    no

BuildRequires:	cmake
BuildRequires:	xmlstarlet
BuildRequires:	python3

BuildRequires:	hal-rootstrap-data-common
%if "%{WITH_DA}" == "1"
BuildRequires:	hal-rootstrap-data-da
%endif

### hal-rootstrap
%description
Package for rootstrap of hal

### hal-rootstrap-devel
%package -n	%{devel_name}
Summary:	%{name} interface
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n	%{devel_name}
%{name} Interface for product vendor developer

%prep
%setup -q

%build
%cmake . -DCMAKE_LIBDIR_PREFIX=%{_libdir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir %{buildroot}
mkdir -p %{buildroot}%{_libdir}/pkgconfig/

# hal-rootstrap
./generate_rootstrap.sh "%{_arch}" "%{buildroot}%{hal_rootstrap_install_path}" "%{INCLUDE_INTERNAL}"
cp packaging/hal-rootstrap.pc %{buildroot}%{_libdir}/pkgconfig/
./modify_pc.py "%{buildroot}%{_libdir}/pkgconfig/hal-rootstrap.pc" "%{buildroot}%{hal_rootstrap_install_path}/%{_libdir}/pkgconfig"
rm -f "%{buildroot}%{hal_rootstrap_install_path}/%{_libdir}/pkgconfig/*.pc"

%files
%{hal_rootstrap_install_path}
%exclude %dir %{hal_rootstrap_install_path}/%{_includedir}

%files	-n %{devel_name}
%defattr(-,root,root,-)
%{hal_rootstrap_install_path}/%{_includedir}
%{_libdir}/pkgconfig/hal-rootstrap.pc
