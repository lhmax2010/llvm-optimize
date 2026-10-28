Name:           desktop-file-utils
Version:        0.28
Release:        1
Summary:        Utilities for Manipulating Desktop Files
License:        GPL-2.0-or-later
URL:            http://www.freedesktop.org/wiki/Software/desktop-file-utils
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     macros.desktop-file-utils

BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  meson
BuildRequires:  ninja

%description
This packages contains a couple of command line utilities for
working with desktop files.

More information about desktop files can be found at:
http://freedesktop.org/wiki/Specifications/desktop-entry-spec

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
# Add user-requested compilation flags
export CFLAGS="$CFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"

mkdir -p builddir
meson setup \
          --prefix=%{_prefix} \
          --libdir=%{_libdir} \
          --buildtype=release \
          --wrap-mode=nodownload \
          builddir

ninja -C builddir

%install
DESTDIR=%{buildroot} ninja -C builddir install

# Install rpm macros
install -D -m644 %{SOURCE1002} %{buildroot}%{_sysconfdir}/rpm/macros.desktop-file-utils

# Create ghosts based on default /usr/share/gnome:/usr/local/share:/usr/share:/var/lib/snapd/desktop:
mkdir -p %{buildroot}%{_datadir}/applications
touch %{buildroot}%{_datadir}/applications/mimeinfo.cache

# Remove documentation and manual pages as per Tizen policy
%remove_docs

%post
%{_bindir}/update-desktop-database --quiet %{_datadir}/applications || true

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/desktop-file-edit
%{_bindir}/desktop-file-install
%{_bindir}/desktop-file-validate
%{_bindir}/update-desktop-database
%ghost %{_datadir}/applications/mimeinfo.cache
%{_datadir}/emacs/site-lisp/*.el*
%{_sysconfdir}/rpm/macros.desktop-file-utils
