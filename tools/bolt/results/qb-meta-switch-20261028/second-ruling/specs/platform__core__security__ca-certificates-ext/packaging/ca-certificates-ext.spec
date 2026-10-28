Summary:        System wide CA certificates resource for a specific product
Name:           ca-certificates-ext
Version:        0.0.1
Release:        0
License:        Apache-2.0
Group:          Security/Certificate Management
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  ca-certificates-devel
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  findutils
Requires: filesystem
Requires: security-config
Requires: ca-certificates

%description
Utilities for system wide CA certificate installation or deinstallation for a specific product


%define user_name security_fw
%define group_name security_fw
%define smack_domain_name System::Shared


%define ro_data_dir %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:%_datadir}
%define certs_ext_dir %{ro_data_dir}/%{name}
%define certs_ext_add %{certs_ext_dir}/certs_add
%define certs_ext_del %{certs_ext_dir}/certs_del


%prep
%setup -q

%build
%cmake . -DVERSION=%version \
         -DCERTS_EXT_DIR=%{certs_ext_dir} \
         -DCERTS_EXT_ADD=%{certs_ext_add} \
         -DCERTS_EXT_DEL=%{certs_ext_del}

%install
%make_install

%post
# remove README file before processing
rm %{certs_ext_add}/README
rm %{certs_ext_del}/README

# add certificates for a specific product
find %{certs_ext_add} -type f -exec cp  {} %{TZ_SYS_RO_CA_CERTS_ORIG} \;
# delete certificates not to be used in a specific product
DEL_LIST=`find %{certs_ext_del} -type f -printf "%f "`
for cert in ${DEL_LIST}
do
	rm -f %{TZ_SYS_RO_CA_CERTS_ORIG}/${cert}
done

# regenerate symbolic files and bundle files
%{TZ_SYS_RO_CA_CERTS_SCRIPT}/concat-cacerts.sh \
    %{TZ_SYS_RO_CA_CERTS_ORIG} \
    %{TZ_SYS_CA_BUNDLE}

%{TZ_SYS_RO_CA_CERTS_SCRIPT}/gen-symlinks.sh \
    "" \
    %{TZ_SYS_CA_CERTS} \
    %{TZ_SYS_RO_CA_CERTS} \
    %{TZ_SYS_RO_CA_CERTS_ORIG} \
    %{TZ_SYS_CA_BUNDLE} \
	%{TZ_SYS_RO_CA_BUNDLE}

# remove all files
rm -rf %{certs_ext_dir}

%files
%manifest %{name}.manifest
%license LICENSE
%dir %{certs_ext_add}
%attr(444, root, root) %{certs_ext_add}/*
%dir %{certs_ext_del}
%attr(444, root, root) %{certs_ext_del}/*

