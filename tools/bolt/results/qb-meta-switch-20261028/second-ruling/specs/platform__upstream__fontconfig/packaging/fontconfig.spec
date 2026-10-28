%global freetype_version 2.9.0

Name:           fontconfig
Summary:        Font configuration and customization library
Version:        2.14.2
Release:        1
Group:          Graphics & UI Framework/Fonts
License:        MIT
URL:            http://fontconfig.org
Source0:        http://fontconfig.org/release/fontconfig-%{version}.tar.gz
Source100:      fontconfig.conf
Source1001:     fontconfig.manifest
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  gawk
BuildRequires:  expat-devel
BuildRequires:  perl
BuildRequires:  gperf
BuildRequires:  python3
BuildRequires:  systemd-devel
BuildRequires:  gettext-tools
BuildRequires:  libuuid-devel
BuildRequires:  pkgconfig(libtzplatform-config)
Requires(pre):  %{TZ_SYS_BIN}/fc-cache, %{TZ_SYS_BIN}/mkdir %{TZ_SYS_BIN}/rm, %{TZ_SYS_BIN}/grep, %{TZ_SYS_BIN}/chsmack
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: security-config

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by
applications.

%package devel
Summary:        Font configuration and customization library
Group:          Graphics & UI Framework/Fonts
Requires:       %{name} = %{version}
Requires:       fontconfig = %{version}
Requires:       freetype-devel >= %{freetype_version}
Requires:       pkg-config

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which
will use fontconfig.

%prep
%setup -q
cp %{SOURCE1001} .

%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

%reconfigure --disable-static \
    --with-expat=%{_prefix} \
    --with-expat-include=%{_includedir} \
    --with-expat-lib=%{_libdir} \
    --with-freetype-config=%{TZ_SYS_BIN}/freetype-config \
    --with-add-fonts=%{TZ_SYS_RO_SHARE}/fonts,%{TZ_SYS_RO_SHARE}/app_fonts,%{TZ_SYS_RO_SHARE}/fallback_fonts,%{TZ_SYS_SHARE}/fonts \
    --with-cache-dir=%{TZ_SYS_VAR}/cache/fontconfig \
    --with-baseconfigdir=%{TZ_SYS_RO_ETC}/fonts \
    --with-configdir=%{TZ_SYS_RO_ETC}/fonts/conf.d \
    --with-templatedir=%{TZ_SYS_RO_ETC}/fonts/conf.avail \
    --with-xmldir=%{TZ_SYS_RO_ETC}/fonts \
    --disable-docs

make %{?jobs:-j%jobs}

#make check
%install
rm -rf %{buildroot}

%make_install

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE100 %{buildroot}%{_tmpfilesdir}/fontconfig.conf

# All font packages depend on this package, so we create
# and own /usr/share/fonts
mydir=$RPM_BUILD_ROOT%{TZ_SYS_RO_SHARE}/fonts
mkdir -p $RPM_BUILD_ROOT%{TZ_SYS_RO_SHARE}/fonts

# Remove unpackaged files. no need when configure --disable-static
#rm $RPM_BUILD_ROOT%{_libdir}/*.la
#rm $RPM_BUILD_ROOT%{_libdir}/*.a

%post
/sbin/ldconfig

umask 0022

mkdir -p %{TZ_SYS_RO_SHARE}/fonts
chmod 755 %{TZ_SYS_RO_SHARE}/fonts
chsmack -t %{TZ_SYS_RO_SHARE}/fonts
chsmack -a User::App::Shared %{TZ_SYS_RO_SHARE}/fonts

mkdir -p %{TZ_SYS_RO_SHARE}/fallback_fonts
chmod 755 %{TZ_SYS_RO_SHARE}/fallback_fonts
chsmack -t %{TZ_SYS_RO_SHARE}/fallback_fonts
chsmack -a User::App::Shared %{TZ_SYS_RO_SHARE}/fallback_fonts

mkdir -p %{TZ_SYS_RO_SHARE}/app_fonts
chmod 755 %{TZ_SYS_RO_SHARE}/app_fonts
chsmack -t %{TZ_SYS_RO_SHARE}/app_fonts
chsmack -a User::App::Shared %{TZ_SYS_RO_SHARE}/app_fonts

mkdir -p %{TZ_SYS_VAR}/cache/fontconfig
chown root:root %{TZ_SYS_VAR}/cache/fontconfig
chmod 755 %{TZ_SYS_VAR}/cache/fontconfig
chsmack -t %{TZ_SYS_VAR}/cache/fontconfig
chsmack -a User::App::Shared %{TZ_SYS_VAR}/cache/fontconfig

mkdir -p %{TZ_SYS_SHARE}/fonts
chown app_fw:users %{TZ_SYS_SHARE}/fonts
chmod 755 %{TZ_SYS_SHARE}/fonts
chsmack -t %{TZ_SYS_SHARE}/fonts
chsmack -a User::App::Shared %{TZ_SYS_SHARE}/fonts

# Skip making fontconfig cache folder for users. (/opt/home/app/.cache)
# The path will be changed according to a name of user.
#rm -rf %{TZ_USER_CACHE}/fontconfig
#mkdir -p %{TZ_USER_CACHE}/fontconfig
#chmod 755 %{TZ_USER_CACHE}
#chown app:app %{TZ_USER_CACHE}
#chsmack -t %{TZ_USER_CACHE}
#chsmack -a System::Shared %{TZ_USER_CACHE}
#chmod 755 %{TZ_USER_CACHE}/fontconfig
#chown app:app %{TZ_USER_CACHE}/fontconfig
#chsmack -t %{TZ_USER_CACHE}/fontconfig
#chsmack -a System::Shared %{TZ_USER_CACHE}/fontconfig

# remove 49-sansserif.conf to fix bmc #9024
#rm -rf /usr/%{_sysconfdir}/fonts/conf.d/49-sansserif.conf

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
#if [ -x %{TZ_SYS_BIN}/fc-cache ] && %{TZ_SYS_BIN}/fc-cache --version 2>&1 | grep -q %{version} ; then
#fc-cache -rf --system-only
#fi

%postun -p /sbin/ldconfig

%files
%manifest fontconfig.manifest
%defattr(-,root,root,-)
%defattr(-, root, root)
%doc README AUTHORS COPYING
%{_libdir}/libfontconfig.so.*
%{TZ_SYS_BIN}/fc-*
%{TZ_SYS_RO_ETC}/fonts/*
%dir %{TZ_SYS_RO_ETC}/fonts/conf.avail
%dir %{TZ_SYS_RO_SHARE}/fonts
%{TZ_SYS_RO_SHARE}/gettext/its/fontconfig*
%{TZ_SYS_RO_SHARE}/locale/*/*/fontconfig*
%doc %{TZ_SYS_RO_ETC}/fonts/conf.d/README
%config %{TZ_SYS_RO_ETC}/fonts/conf.avail/*.conf
%config(noreplace) %{TZ_SYS_RO_ETC}/fonts/conf.d/*.conf
%{_tmpfilesdir}/fontconfig.conf
%license COPYING

%files devel
%manifest fontconfig.manifest
%defattr(-,root,root,-)
%defattr(-, root, root)
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig

