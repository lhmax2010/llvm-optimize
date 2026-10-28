Name:           shared-mime-info
Version:        1.7
Release:        0
License:        GPL-2.0+
Summary:        Shared MIME Database
Url:            http://freedesktop.org/wiki/Software/shared-mime-info
Group:          Base/Configuration
Source:         http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.xz
Source1:        mime-info-to-mime
Source2:        macros.shared-mime-info
Source1001: 	shared-mime-info.manifest
BuildRequires:  intltool
BuildRequires:  libxml2-tools
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
Requires:       /usr/bin/fgrep
Requires:       /usr/bin/mkdir
Requires:       /usr/bin/rm
#!BuildIgnore:  shared-mime-info
# needed by update-mime-database
Provides:       %{name}-devel = %{version}

%description
This package contains:

- The freedesktop.org shared MIME database spec.

- The merged GNOME and KDE databases, in the new format.

- The update-mime-database command, used to install new MIME data.

%package tools
Summary:    Tools supporting shared-mime-info 
Requires:   shared-mime-info

%description tools
Tools to support packages %{name}

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS=`echo $RPM_OPT_FLAGS |sed -e 's/atom/i686/g'`
autoreconf -ivf
%configure \
	CFLAGS="$CFLAGS -fPIE" \
	LDFLAGS="$LDFLAGS -pie"
make V=1

%install
%make_install
install %{SOURCE1} %{buildroot}%{_bindir}/
%find_lang %{name} %{?no_lang_C}
# Install rpm macros
install -D -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.shared-mime-info


%post
%{_bindir}/update-mime-database %{_datadir}/mime || true

%lang_package

%docs_package

%files
%manifest %{name}.manifest
%defattr (-, root, root)
%license COPYING
%{_bindir}/update-mime-database
%{_datadir}/mime/packages/*.xml
%{_datadir}/pkgconfig/*.pc
%ghost %{_datadir}/mime/[a-ms-vxX]*
%{_sysconfdir}/rpm/macros.shared-mime-info


%files tools
%manifest %{name}.manifest
%{_bindir}/mime-info-to-mime

%changelog
