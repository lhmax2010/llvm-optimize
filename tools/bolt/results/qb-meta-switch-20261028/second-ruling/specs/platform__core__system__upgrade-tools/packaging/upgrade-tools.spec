%define install_path /%{name}
%define mk_delta_install_path %{install_path}/mk_delta
%define bin_install_path %{mk_delta_install_path}/common/bin

Name:		upgrade-tools
Version:	0.1.0
Release:	0
License:	Apache-2.0
Summary:	Tools for upgrade
Group:		System/Tools
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libbrotlienc)
%if "%{tizen_profile_name}" != "tv" && "%{mv_prj}" != "1"
BuildRequires:	pkgconfig(libdivsufsort)
%endif

%description
Tools for upgrade

%prep
%setup -q
%cmake . \
	-DCMAKE_C_COMPILER=%__cc \
	-DCMAKE_CXX_COMPILER=%__cxx \
	-DINSTALL_PATH=%{bin_install_path} \
%if "%{tizen_profile_name}" == "tv" || "%{mv_prj}" == "1"
	-DDISABLE_LIBDIVSUFSORT=1
%else
	-DDISABLE_LIBDIVSUFSORT=0
%endif

%build
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{bin_install_path}
cp -r ./scripts %{buildroot}/%{install_path}
cp -r ./mk_delta/common %{buildroot}/%{mk_delta_install_path}/.
%make_install

%files
%{install_path}/*
