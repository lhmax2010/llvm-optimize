Name:       default-fonts-sdk
Summary:    free fonts for Tizen SDK
Version:    1.2.1.0
Release:    10
Group:      TO_BE/FILLED_IN
License:    Apache-2.0 and GPL-2.0-with-font-exception
Source0:    %{name}-%{version}.tar.gz
Source1001: packaging/default-fonts-sdk.manifest
BuildRequires: pkgconfig(libtzplatform-config)
Requires(post): fontconfig

%description
free fonts for Tizen SDK
This package is maintained by SDK team

%prep
%setup -q

%build
cp %{SOURCE1001} .

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/fonts && cp -a common/fonts %{buildroot}%{_datadir}
#cp -a $TARGET/fonts %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_datadir}/fallback_fonts && cp -a common/fallback_fonts %{buildroot}%{_datadir}
#cp -a $TARGET/fallback_fonts %{buildroot}%{_datadir}

%post
if [ -x /usr/bin/fc-cache ] ; then
  /usr/bin/fc-cache -f
  chsmack -a User::App::Shared %{TZ_SYS_VAR}/cache/fontconfig/*
fi

%files
%manifest default-fonts-sdk.manifest
%defattr(-,root,root,-)
%{_datadir}/fonts/*
%{_datadir}/fallback_fonts/*
%license LICENSE
