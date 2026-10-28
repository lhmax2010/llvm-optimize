Name:       media-server
Summary:    A server for media content management
Version:    0.8.30
Release:    0
Group:      Multimedia/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    media-server.service
Source2:    media-server-user.service
Source3:    media-server-user.path
Source4:    media-server.socket
Source5:    99-media-server.rules
Source6:    media-server-user-ondemand.path
Source1001:     %{name}.manifest
Source1002:     libmedia-utils.manifest
Source1003:     libmedia-utils-devel.manifest
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-uid)
BuildRequires:  pkgconfig(capi-system-device)
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif
%if "%{tizen_profile_name}" == "tv"
BuildRequires:	pkgconfig(capi-system-resource)
BuildRequires:	pkgconfig(eventsystem)
BuildRequires:	pkgconfig(capi-system-info)
BuildRequires:	pkgconfig(vconf)
%define product_tv 1
%else
%define product_tv 0
%endif

%define upgrade_script_path /usr/share/upgrade/scripts/

%if ("%{sec_buildconf_optimized_memory}" == "1")
%define on_demand 1
%else
%define on_demand 0
%endif

%description
Description: A server for media content management.

%package -n libmedia-utils
Summary:   The media server runtime library
Group:     Multimedia/Libraries
Requires:  media-server = %{version}-%{release}

%description -n libmedia-utils
Description : The media server runtime library.

%package -n libmedia-utils-devel
Summary:   The media server runtime library (development)
Group:     Multimedia/Development
Requires:  libmedia-utils = %{version}-%{release}
Requires:  libtzplatform-config-devel

%description -n libmedia-utils-devel
Description: The media server runtime library. (Development files included)

%prep
%setup -q
cp %{SOURCE1001} %{SOURCE1002} %{SOURCE1003} .

%build
%if "%{asan}" == "1"
%restore_fcommon
%endif
export CFLAGS="$CFLAGS -D_GNU_SOURCE -D_FORTIFY_SOURCE=2 -DTIZEN_DEBUG_ENABLE"
export CFLAGS="$CFLAGS -DPATH_LIBDIR=\\\"%{_libdir}\\\""
%if 0%{?on_demand}
export CFLAGS="$CFLAGS -D_USE_ON_DEMAND"
%endif
%if 0%{?product_tv}
export CFLAGS="$CFLAGS -D_USE_TVPD_MODE"
%endif
rm -rf autom4te.cache
rm -f aclocal.m4 ltmain.sh
mkdir -p m4
%reconfigure --prefix=%{_prefix} \
%if 0%{?gtests:1}
	--enable-tests \
%endif
%if 0%{?on_demand}
	--enable-on-demand \
%endif
%if 0%{?product_tv}
	--enable-product-tv \
%else
	--disable-product-tv \
%endif
	--disable-static
%__make %{?jobs:-j%jobs}

%install

%make_install

mkdir -p %{buildroot}%{upgrade_script_path}
cp -f scripts/500.media_db_upgrade.sh %{buildroot}%{upgrade_script_path}

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/media-server.service
%if 0%{?on_demand}
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/media-server.socket
ln -s ../media-server.socket %{buildroot}%{_unitdir}/sockets.target.wants/media-server.socket
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/udev/rules.d/99-media-server.rules
%endif
%if !0%{?product_tv}
mkdir -p %{buildroot}%{_unitdir_user}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir_user}/media-server-user.service
%if 0%{?on_demand}
install -m 644 %{SOURCE6} %{buildroot}%{_unitdir_user}/media-server-user.path
%else
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir_user}/media-server-user.path
%endif
%endif

ln -s ../media-server.service %{buildroot}%{_unitdir}/multi-user.target.wants/media-server.service

#ini file
mkdir -p %{buildroot}/etc/multimedia
mkdir -p %{buildroot}/etc/gumd/useradd.d
cp -rf %{_builddir}/%{name}-%{version}/30_media-server-add.post %{buildroot}/etc/gumd/useradd.d/30_media-server-add.post
#dummy db file for reset media DB
cp -rf %{_builddir}/%{name}-%{version}/data/media.db %{buildroot}/etc/multimedia/.media.db

%post
# setup dbupdate in user session
mkdir -p %{_unitdir_user}/basic.target.wants/
ln -sf ../media-server-user.path  %{_unitdir_user}/basic.target.wants/

chmod 755 /etc/gumd/useradd.d/30_media-server-add.post

%post -n libmedia-utils -p /sbin/ldconfig

%postun -n libmedia-utils -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/media-server
%{_bindir}/mediadb-update
%if 0%{?gtests:1}
%{_bindir}/gtest*
%endif
%{_unitdir}/media-server.service
%{_unitdir}/multi-user.target.wants/media-server.service
%if 0%{?on_demand}
%{_unitdir}/media-server.socket
%{_unitdir}/sockets.target.wants/media-server.socket
%{_sysconfdir}/udev/rules.d/99-media-server.rules
%endif
%if !0%{?product_tv}
%{_unitdir_user}/media-server-user.service
%{_unitdir_user}/media-server-user.path
%endif
/etc/multimedia/.media.db
/etc/gumd/useradd.d/30_media-server-add.post
%license LICENSE.APLv2.0
%{upgrade_script_path}/500.media_db_upgrade.sh

%files -n libmedia-utils
%manifest libmedia-utils.manifest
%license LICENSE.APLv2.0
%defattr(-,root,root,-)
%{_libdir}/libmedia-utils.so.0
%{_libdir}/libmedia-utils.so.0.0.0

%files -n libmedia-utils-devel
%manifest libmedia-utils-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/libmedia-utils.so
%{_libdir}/pkgconfig/libmedia-utils.pc
%{_includedir}/media-utils/*.h
