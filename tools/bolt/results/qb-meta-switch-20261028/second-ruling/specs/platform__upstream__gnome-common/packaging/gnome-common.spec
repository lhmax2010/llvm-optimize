Name:           gnome-common
Version:        3.12.0
BuildRequires:  pkg-config
Summary:        Common Files to Build GNOME
License:        GPL-2.0+
Group:          Platform Development/Utilities
Release:        0
Source:         http://download.gnome.org/sources/gnome-common/3.12/%{name}-%{version}.tar.xz
#X-Vcs-Url:     git://git.gnome.org/gnome-common
Source1001:     gnome-common.manifest
Url:            http://www.gnome.org/
BuildArch:      noarch
Requires:       autoconf
Requires:       automake
Requires:       gettext-tools
Requires:       glib2-devel
Requires:       intltool
Requires:       libtool
Requires:       pkg-config

%description
Gnome-common includes files used by to build GNOME and GNOME applications.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%autogen
%configure
%__make %{?_smp_mflags}

%install
%make_install

%files
%manifest %{name}.manifest
%defattr (-, root, root)
%license COPYING
%{_bindir}/gnome-autogen.sh
%{_bindir}/gnome-doc-common
%dir %{_datadir}/aclocal
%{_datadir}/aclocal/gnome-common.m4
%{_datadir}/aclocal/gnome-compiler-flags.m4
%{_datadir}/aclocal/gnome-code-coverage.m4
%{_datadir}/gnome-common/
