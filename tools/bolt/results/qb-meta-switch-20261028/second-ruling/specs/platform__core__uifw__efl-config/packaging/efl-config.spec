%define alias efl-config
Name:       efl-config
Summary:    EFL Config daemon
Version:    0.1
Release:    0
Provides:   efl-config = %{version}-%{release}
Group:      System/Libraries
License:    Apache-2.0
Source:     %{name}-%{version}.tar.gz
Source2: %{alias}.manifest
BuildRequires: automake
BuildRequires: libtool
BuildRequires: pkgconfig(elementary)
BuildRequires: pkgconfig(ecore-wl2)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(capi-system-info)

%description
EFL config daemon

%prep
%setup -q
cp %{SOURCE2} .

%build
export CFLAGS+=" -DEFL_BETA_API_SUPPORT -Wno-int-conversion"

./autogen.sh
TZ_SYS_BIN=%{TZ_SYS_BIN} ./configure --prefix %{_prefix}/

export TZ_SYS_RO_SHARE="%{TZ_SYS_RO_SHARE}"
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_unitdir_user}/basic.target.wants
mkdir -p %{buildroot}%{_unitdir_user}/delayed.target.wants
mkdir -p %{buildroot}%{_unitdir_user}/sockets.target.wants

install -m 0644 %{_builddir}/%{name}-%{version}/packaging/%{alias}.service %{buildroot}%{_unitdir_user}/%{alias}.service
install -m 0644 %{_builddir}/%{name}-%{version}/packaging/%{alias}-post.service %{buildroot}%{_unitdir_user}/%{alias}-post.service
install -m 0644 %{_builddir}/%{name}-%{version}/packaging/%{alias}-ondemand.service %{buildroot}%{_unitdir_user}/%{alias}-ondemand.service
install -m 0644 %{_builddir}/%{name}-%{version}/packaging/%{alias}.socket %{buildroot}%{_unitdir_user}/%{alias}.socket

ln -s ../%{alias}.service %{buildroot}%{_unitdir_user}/basic.target.wants/%{alias}.service
ln -s ../%{alias}-post.service %{buildroot}%{_unitdir_user}/delayed.target.wants/%{alias}-post.service
ln -s ../%{alias}.socket %{buildroot}%{_unitdir_user}/sockets.target.wants/%{alias}.socket

%post
/sbin/ldconfig
mkdir -p /opt/share/.elementary
chmod -R 775 /opt/share/.elementary
chown -R :users /opt/share/.elementary
chsmack -a 'User::App::Shared' /opt/share/.elementary
chsmack -t /opt/share/.elementary

%postun
/sbin/ldconfig
rm -f %{buildroot}%{_unitdir_user}/basic.target.wants/%{alias}.service
rm -f %{buildroot}%{_unitdir_user}/delayed.target.wants/%{alias}-post.service

%files
%defattr(-,root,root,-)
%{TZ_SYS_BIN}/efl_config
%{_unitdir_user}/%{alias}.service
%{_unitdir_user}/%{alias}-post.service
%{_unitdir_user}/%{alias}-ondemand.service
%{_unitdir_user}/basic.target.wants/%{alias}.service
%{_unitdir_user}/delayed.target.wants/%{alias}-post.service
%{_unitdir_user}/sockets.target.wants/%{alias}.socket
%{_unitdir_user}/%{alias}.socket
%manifest %{alias}.manifest
