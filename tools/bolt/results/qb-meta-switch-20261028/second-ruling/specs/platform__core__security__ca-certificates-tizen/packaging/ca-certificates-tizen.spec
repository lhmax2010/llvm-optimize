Name:          ca-certificates-tizen
Summary:       Tizen-specific CA certificate installation
Version:       1.1.5
Release:       0
Group:         Security/Certificate Management
URL:           http://www.tizen.org
License:       Apache-2.0
Source:        %{name}-%{version}.tar.gz
Source1001:    %{name}.manifest
BuildRequires: cmake
BuildRequires: openssl3
BuildRequires: pkgconfig(libtzplatform-config)

%description
Used for the installation of Tizen-specific CA certificates.

%package devel
Summary:  Devel package of %{name} which contains RPM macros
Group:    Development/Libraries
License:  Apache-2.0
Requires: %name = %version-%release

%description devel
%{name} devel package which contains RPM macros for runtime revoked certs fingerprint

%define ro_data_dir     %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:%_datadir}
%define rw_data_dir     %{?TZ_SYS_SHARE:%TZ_SYS_SHARE}%{!?TZ_SYS_SHARE:/opt/share}
%define tizen_dir       %{ro_data_dir}/ca-certificates/tizen
%define fingerprint_dir %{ro_data_dir}/ca-certificates/fingerprint
%define fingerprint_rw_dir %{rw_data_dir}/ca-certificates/fingerprint
%define ro_etc_dir %{?TZ_SYS_RO_ETC:%TZ_SYS_RO_ETC}%{!?TZ_SYS_RO_ETC:%_sysconfdir}

%define macro_ca_certificates_tizen %{ro_etc_dir}/rpm/macros.ca-certificates-tizen

%prep
%setup -q

%build

# define build architecture
%ifarch %{ix86}
    echo "release emulator mode"
    %define ARCH i586
    %define REL_MODE emul
%else
    %define ARCH arm
    %if 0%{?tizen_build_devel_mode}
        echo "release engineering mode"
        %define REL_MODE eng
    %else
        echo "release user mode"
        %define REL_MODE usr
    %endif
%endif

%cmake . -DRELMODE=%{REL_MODE} \
         -DTIZEN_DIR=%{tizen_dir} \
         -DFINGERPRINT_DIR=%{fingerprint_dir} \
         -DFINGERPRINT_RW_DIR=%{fingerprint_rw_dir}

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{ro_etc_dir}/rpm
touch %{buildroot}%{macro_ca_certificates_tizen}
echo "%TZ_SYS_REVOKED_CERTS_FINGERPRINTS_RUNTIME %{fingerprint_rw_dir}/fingerprint_list_runtime.xml" >> %{buildroot}%{macro_ca_certificates_tizen}

cp %{SOURCE1001} %{buildroot}%{_datadir}/

%files
%defattr(-,root,root,-)
%manifest %{_datadir}/%{name}.manifest
%license LICENSE
%{tizen_dir}/*
%{fingerprint_dir}/*
%{fingerprint_rw_dir}/fingerprint_list_runtime.xml

%files devel
%config %{macro_ca_certificates_tizen}
