%define name	app-rootstrap-csharp-data-common
%define desc    App Rootstrap Csharp for Common Profile

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

Name:		%{name}
Summary:	%{desc}
Version:	11.0.0
Release:	1
#Group:
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
AutoReqProv:	no

Requires:	csapi-tizenfx-nuget
BuildRequires:	csapi-tizenfx-nuget
Requires:	pkgconfig(libtzplatform-config)
BuildRequires:	pkgconfig(libtzplatform-config)

%description
%{desc}

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir %{buildroot}
mkdir -p %{buildroot}/tmp
ls -al
cp -R ./rs_resource %{buildroot}/tmp

%files
/tmp/*
