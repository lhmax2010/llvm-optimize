Summary:        System wide CA certificates resource
Name:           ca-certificates
Version:        0.0.4
Release:        0
License:        Apache-2.0
Group:          Security/Certificate Management
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  openssl3
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  findutils
Requires: filesystem
Requires: security-config
Requires: openssl3

%description
Utilities for system wide CA certificate installation

%package devel
Summary:  Devel package of ca-certificates which contains RPM macros
Group:    Development/Libraries
License:  Apache-2.0
Requires: %name = %version-%release

%description devel
ca-certificates devel package which contains RPM macros
for ca-bundle and ssl certs directory

%define user_name security_fw
%define group_name security_fw
%define smack_domain_name System::Shared

# prefix macro
%define var_dir              %{?TZ_SYS_VAR:%TZ_SYS_VAR}%{!?TZ_SYS_VAR:/opt/var}
%define etc_dir              %{?TZ_SYS_ETC:%TZ_SYS_ETC}%{!?TZ_SYS_ETC:/opt/etc}
%define ro_etc_dir           %{?TZ_SYS_RO_ETC:%TZ_SYS_RO_ETC}%{!?TZ_SYS_RO_ETC:%_sysconfdir}
%define ssl_dir              %{etc_dir}/ssl
%define ro_ssl_dir           %{ro_etc_dir}/ssl
%define ro_data_dir          %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:%_datadir}
%define ro_ca_certs_root_dir %{ro_data_dir}/ca-certificates

# CA certs macro
%define ro_ca_certs_orig_dir   %{ro_ca_certs_root_dir}/certs
%define ro_ca_certs_script_dir %{ro_ca_certs_root_dir}/scripts
%define ro_ca_certs_dir        %{ro_ssl_dir}/certs
%define ca_certs_dir           %{ssl_dir}/certs

# CA bundle macro
%define ca_bundle_dir     %{var_dir}/lib/ca-certificates
%define ca_bundle         %{ca_bundle_dir}/ca-bundle.pem
%define ro_ca_bundle      %{ro_ssl_dir}/ca-bundle.pem
%define old_ca_bundle_dir /opt/share/ca-certificates

# define system macro
%define macro_ca_certificates %{ro_etc_dir}/rpm/macros.ca-certificates

%prep
%setup -q

%build
%cmake . -DVERSION=%version \
         -DUSER_NAME=%user_name \
         -DGROUP_NAME=%group_name \
         -DSMACK_DOMAIN_NAME=%smack_domain_name \
         -DTZ_SYS_CA_CERTS=%ca_certs_dir \
         -DTZ_SYS_CA_BUNDLE=%ca_bundle \
         -DTZ_SYS_RO_CA_BUNDLE=%ro_ca_bundle \
         -DTZ_SYS_CA_BUNDLE_DIR=%ca_bundle_dir \
         -DTZ_SYS_RO_CA_CERTS_ORIG=%ro_ca_certs_orig_dir \
         -DTZ_SYS_RO_CA_CERTS_SCRIPT=%ro_ca_certs_script_dir \
         -DRO_CA_CERTS_ROOT_DIR=%ro_ca_certs_root_dir \
         -DOLD_CA_BUNDLE_DIR=%old_ca_bundle_dir

%install

# devel macro
mkdir -p %{buildroot}%{ro_etc_dir}/rpm
touch %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_RO_CA_CERTS_ORIG   %{ro_ca_certs_orig_dir}"   >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_RO_CA_CERTS_SCRIPT %{ro_ca_certs_script_dir}" >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_RO_CA_CERTS        %{ro_ca_certs_dir}"        >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_CERTS           %{ca_certs_dir}"           >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_RO_CA_BUNDLE       %{ro_ca_bundle}"           >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_BUNDLE          %{ca_bundle}"              >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_RO_CA_DIR          %{ro_ca_certs_root_dir}"   >> %{buildroot}%{macro_ca_certificates}

%make_install

# generate directories
mkdir -p %{buildroot}%{ca_bundle_dir}
mkdir -p %{buildroot}%{ro_ssl_dir}
mkdir -p %{buildroot}%{ca_certs_dir}

# generate original CA bundle
%{buildroot}%{ro_ca_certs_script_dir}/concat-cacerts.sh \
    %{buildroot}%{ro_ca_certs_orig_dir} \
    %{buildroot}%{ca_bundle}

# link files and directory
%{buildroot}%{ro_ca_certs_script_dir}/gen-symlinks.sh \
	%{buildroot} \
	%{ca_certs_dir} \
	%{ro_ca_certs_dir} \
	%{ro_ca_certs_orig_dir} \
	%{ca_bundle} \
	%{ro_ca_bundle}


%files
%manifest %{name}.manifest
%license LICENSE
# original CA Certificates
%dir %{ro_ca_certs_orig_dir}
%attr(444, root, root) %{ro_ca_certs_orig_dir}/*
# symbol Certificates : R0 area
%{ro_ssl_dir}
# symbol Certificates : RW area
%dir %attr(775, %{user_name}, %{group_name}) %{ca_certs_dir}
%{ca_certs_dir}/*
# original CA bundle
%dir %{ca_bundle_dir}
%attr(664, root, %{group_name}) %{ca_bundle}
# symbol CA bundle
%{ro_ca_bundle}
# scripts for managing certificates
%dir %{ro_ca_certs_script_dir}
%attr(744, root, root) %{ro_ca_certs_script_dir}/*
# update script for CA bundle re-creation
%attr(755,root,root) /usr/share/upgrade/scripts/500.ca-certificates_upgrade.sh

%files devel
%config %{macro_ca_certificates}
