%define keepstatic yes
Name:           capi-system-info
Version:        0.5.2
Release:        1
License:        Apache-2.0
Summary:        A System Information library in Core API
Group:          System/API
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  model-config-default
BuildRequires:  python3
BuildRequires:  glibc-devel-static
Requires: security-config
Requires:  model-config-default

%description

%package devel
Summary:  A System Information library in Core API (Development)
Group:    Development/System
Requires: %{name} = %{version}-%{release}

%description devel

%package devel-static
Summary:  A System Information static library in Core API (Development)
Group:    Development/System
Requires: %{name} = %{version}-%{release}

%description devel-static

%package test
Summary:  System-info test package
Group:    Development/System
Requires: %{name}

%description test
A System Information test tool

%package tool
Summary:  System-info command line tool package
Group:    Development/System
Requires: %{name}

%description tool
A System Information command line tool

%if 0%{?gcov:1}
%package -n system-info-gcov
Summary:  A System Information gcov test file
%description -n system-info-gcov
gcno files for System-info line coverage test
%endif


%prep
%setup -q
cp %{SOURCE1001} .

%define info_file_path /etc/info.ini
%define hal_info_file_path %{_hal_sysconfdir}/hal-info.ini
%define product_info_file_path %{_product_sysconfdir}/product-info.ini

%define sysinfo_shared_path %{TZ_SYS_ETC}/sysinfo
%define tizen_id_path %{sysinfo_shared_path}/tizenid

%define model_config_ro_path %{_sysconfdir}/config/model-config.xml
%define hal_model_config_ro_path %{_hal_sysconfdir}/config/model-config.xml
%define product_model_config_ro_path %{_product_sysconfdir}/config/model-config.xml

%define db_ro_path %{TZ_SYS_RO_ETC}/system_info_db
%define hal_db_ro_path %{_hal_prefix}/etc/system_info_db
%define product_db_ro_path %{_product_prefix}/etc/system_info_db

%define model_config_rw_dir /opt/system/model-config
%define db_rw_path %{model_config_rw_dir}/system_info_db

%define plugin_dir %{_libdir}

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . -DMODEL_CONFIG_RO_PATH=%{model_config_ro_path} \
	     -DHAL_MODEL_CONFIG_RO_PATH=%{hal_model_config_ro_path} \
	     -DPRODUCT_MODEL_CONFIG_RO_PATH=%{product_model_config_ro_path} \
	     -DINFO_FILE_PATH=%{info_file_path} \
	     -DHAL_INFO_FILE_PATH=%{hal_info_file_path} \
	     -DPRODUCT_INFO_FILE_PATH=%{product_info_file_path} \
	     -DMAJORVER=${MAJORVER} \
	     -DFULLVER=%{version} \
	     -DTIZEN_ID_PATH=%{tizen_id_path} \
	     -DDB_RO_PATH=%{db_ro_path} \
	     -DDB_RW_PATH=%{db_rw_path}	\
	     -DHAL_DB_RO_PATH=%{hal_db_ro_path} \
	     -DPRODUCT_DB_RO_PATH=%{product_db_ro_path} \
	     -DPLUGIN_DIR=%{plugin_dir} \
	     -DGCOV=%{?gcov:1}%{!?gcov:0}

%__make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}/etc

%install_service sysinit.target.wants tizenid.service

mkdir -p %{buildroot}/%{sysinfo_shared_path}
mkdir -p %{buildroot}/%{model_config_rw_dir}

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif


%posttrans
/usr/bin/chsmack -a "System::Shared" -t %{sysinfo_shared_path}
/usr/bin/chsmack -a "System::Shared" -t %{model_config_rw_dir}
/usr/bin/system_info_init_db
/sbin/ldconfig

%if 0%{?gcov:1}
# A gcda file is created when binary system_info_init_db is executed.
# At this time, the home directory is not created yet,
# so the home directory is created and the gcda file is created under it.
# But home directory with wrong permissions due to umask set to 0222 in the binary
# So, when build with gcov, set the home directory to the correct permissions
[ -d /home/abuild ] && chmod 755 /home/abuild
%endif

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libcapi-system-info.so.*
%attr(0744,root,-) /etc/make_info_file.sh
%attr(0744,root,-) /etc/update_info_file.sh
%{_bindir}/system_info_init_db

%attr(0775,root,system_share) %dir %{model_config_rw_dir}
#tizenid
%attr(0775,root,system_share) %dir %{sysinfo_shared_path}
%{_bindir}/tizen_id

%{_unitdir}/tizenid.service
%{_unitdir}/sysinit.target.wants/tizenid.service

%files devel
%manifest %{name}.manifest
%{_includedir}/system/system_info.h
%{_includedir}/system/system_info_generated.h
%{_includedir}/system/system_info_type.h
%{_includedir}/plugin/system_info_intf.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-system-info.so

%files devel-static
%{_libdir}/libcapi-system-info.a

%files test
# Init DB test
%{_bindir}/system_info_init_db_test
# Plugin test
%attr(0755,root,-) %{_bindir}/system_info_external_plugin_test.sh
%{_libdir}/libsystem_info_plugins/libsystem_info_test_plugin.so
%{_libdir}/libsystem_info_plugins/libsystem_info_test_plugin2.so

%if 0%{?gcov:1}
%files -n system-info-gcov
%{_datadir}/gcov/obj/*
%endif

%files tool
%{_bindir}/system-info-tool
