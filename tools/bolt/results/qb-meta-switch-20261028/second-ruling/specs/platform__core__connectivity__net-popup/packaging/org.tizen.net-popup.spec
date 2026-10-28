Name:       org.tizen.net-popup
Summary:    Network Notification Popup application
Version:    0.3.2
Release:    1
Group:      App/Network
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  dotnet-build-tools
BuildRequires:  gettext
Requires:       capi-appfw-application
Requires:       notification
Requires:       vconf
Requires:       capi-network-stc
Requires:       capi-vpnsvc
BuildArch: noarch

%description
Network Notification Popup application
Handles network-related system popups
including WiFi notifications, VPN connect/disconnect, data usage warnings,
tethering, and roaming dialogs.

%prep
%setup -q

%define PKGNAME org.tizen.net-popup
%define APPDIR /usr/apps/%{PKGNAME}

%build
dotnet restore -s packaging/depends -s /nuget
dotnet publish -c Release --no-restore

# Compile .po translation files to .mo
for pofile in po/*.po; do
    lang=$(basename "$pofile" .po)
    mkdir -p po/build/${lang}
    msgfmt -o po/build/${lang}/net-popup.mo "$pofile"
done

%install
PUBLISH_DIR=%{buildroot}%{APPDIR}
mkdir -p $PUBLISH_DIR/bin
cp -rf bin/Release/net8.0-tizen/publish/* $PUBLISH_DIR/bin/ 2>/dev/null || cp -rf bin/Release/net8.0/publish/* $PUBLISH_DIR/bin/
if [ -f %{PKGNAME}.manifest ]; then
    cp -f %{PKGNAME}.manifest $PUBLISH_DIR/
fi
if [ -f tizen-manifest.xml ]; then
    cp -f tizen-manifest.xml $PUBLISH_DIR/
fi

# Install compiled .mo translation files
for pofile in po/*.po; do
    lang=$(basename "$pofile" .po)
    mkdir -p %{buildroot}/usr/share/locale/${lang}/LC_MESSAGES
    cp -f po/build/${lang}/net-popup.mo %{buildroot}/usr/share/locale/${lang}/LC_MESSAGES/
done

# Install app registration XML (required for Tizen to discover and launch the app)
mkdir -p %{buildroot}/usr/share/packages
cp -f resources/org.tizen.net-popup.xml %{buildroot}/usr/share/packages/

%files
%manifest %{PKGNAME}.manifest
%defattr(-,root,root,-)
%{APPDIR}/*
/usr/share/locale/*/LC_MESSAGES/net-popup.mo
%{_datadir}/packages/org.tizen.net-popup.xml
%license LICENSE
