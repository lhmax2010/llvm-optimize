%bcond_with x

Name:           xkeyboard-config
Version:        2.13
Release:        0
License:        MIT
Summary:        The X Keyboard Extension
Url:            http://www.freedesktop.org/Software/XKeyboardConfig
Group:          System/Utilities
Source:         http://xorg.freedesktop.org/releases/individual/data/%{name}-%{version}.tar.bz2
Source1001:     xkeyboard-config.manifest
BuildRequires:  fdupes
BuildRequires:  intltool
BuildRequires:  perl-XML-Parser
BuildRequires:  pkg-config
%if %{with x}
BuildRequires:  xkbcomp
Requires:       xkbcomp
%endif
BuildRequires:  pkgconfig(xorg-macros) >= 1.12
Provides:       XFree86:/etc/X11/xkb/symbols/us
Provides:       xorg-x11:/etc/X11/xkb/symbols/us
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(pre):  /usr/bin/ln
Requires(pre):  /usr/bin/rm
# This is for backword compatibility only. Tizen 4.0 Configurability gets no damage from this.
Requires:  xkb-tizen-data
BuildRequires:  pkgconfig(xkbcommon)
# The post script executes "make_keycodes.sh", which requires awk
Requires(post): awk

%{!?TZ_SYS_RO_SHARE: %global TZ_SYS_RO_SHARE /usr/share}
%{!?TZ_SYS_VAR: %global TZ_SYS_VAR /opt/var}
%global KEYMAP_FILE_PATH "%{TZ_SYS_RO_SHARE}/X11/xkb/tizen_key_layout.txt"

%description
The X Keyboard Extension essentially replaces the core protocol
definition of keyboard. The extension makes possible to clearly and
explicitly specify most aspects of keyboard behaviour on per-key basis
and to more closely track the logical and physical state of the
keyboard. It also includes a number of keyboard controls designed to
make keyboards more accessible to people with physical impairments.

%package i18n
Summary:        Translation files for xkeyboard-config
Group:          System/Utilities
Requires:       %{name} = %{version}-%{release}

%description i18n
Translation files for xkeyboard-config package.

%prep
%setup -q
cp %{SOURCE1001} .

%if %{with x}
export TIZEN_WINDOW_SYSTEM="x11"
%else
export TIZEN_WINDOW_SYSTEM="wayland"
%endif

export TZ_SYS_RO_SHARE="%{TZ_SYS_RO_SHARE}"
export KEYMAP_FILE_PATH="%{KEYMAP_FILE_PATH}"

%build
%autogen --with-xkb-rules-symlink=xfree86,xorg \
            --with-xkb-base=%{TZ_SYS_RO_SHARE}/X11/xkb \
            --enable-compat_rules \
            --disable-runtime-deps \
            --disable-xkbcomp-symlink
rm -f */*.dir
%__make

%install
%make_install
mkdir -p %{buildroot}%{_localstatedir}/lib/xkb
ln -snf %{_bindir}/xkbcomp %{buildroot}%{_datadir}/X11/xkb/xkbcomp
# Bug 335553
mkdir -p %{buildroot}%{_localstatedir}/lib/xkb/compiled/
ln -snf %{TZ_SYS_VAR}/lib/xkb/compiled/ %{buildroot}%{_datadir}/X11/xkb/compiled
%find_lang %{name}
%fdupes -s %{buildroot}%{_datadir}/X11/xkb

cp -af %{buildroot}/%{TZ_SYS_RO_SHARE}/X11/xkb/rules/evdev %{buildroot}/%{TZ_SYS_RO_SHARE}/X11/xkb/rules/tizen
mv -f %{buildroot}/%{TZ_SYS_RO_SHARE}/X11/xkb/rules/evdev %{buildroot}/%{TZ_SYS_RO_SHARE}/X11/xkb/rules/evdev.org
sed -i 's/evdev/tizen/g' %{buildroot}/%{TZ_SYS_RO_SHARE}/X11/xkb/rules/tizen
ln -sf tizen %{buildroot}/%{TZ_SYS_RO_SHARE}/X11/xkb/rules/evdev
export LOCAL_KEYMAP_PATH=%{buildroot}/%{TZ_SYS_RO_SHARE}/X11/xkb
export RULE_FILE_PATH=%{TZ_SYS_RO_SHARE}/X11/xkb/xkb.rule
export KEYMAP_FILE_PATH="%{KEYMAP_FILE_PATH}"
./remove_unused_files.sh

install -m 0700 make_symbols.sh %{buildroot}%{_bindir}/
install -m 0700 make_keycodes.sh %{buildroot}%{_bindir}/
install -m 0700 remove_symbols.sh %{buildroot}%{_bindir}/

# DO the optimization at RPM install, not at build
%post
mkdir -p /tmp/xkeyboard-config-install
%if %{with x}
export TIZEN_WINDOW_SYSTEM="x11"
%else
export TIZEN_WINDOW_SYSTEM="wayland"
%endif
export TZ_SYS_RO_SHARE="%{TZ_SYS_RO_SHARE}"
export LOCAL_KEYMAP_PATH=%{TZ_SYS_RO_SHARE}/X11/xkb
export RULE_FILE_PATH=%{TZ_SYS_RO_SHARE}/X11/xkb/xkb.rule
export KEYMAP_FILE_PATH=%{KEYMAP_FILE_PATH}
cd %{TZ_SYS_RO_SHARE}/X11/xkb || exit 0
%{_bindir}/make_keycodes.sh
%{_bindir}/make_symbols.sh
%{_bindir}/remove_symbols.sh
rm -f %{_bindir}/make_keycodes.sh
rm -f %{_bindir}/make_symbols.sh
rm -f %{_bindir}/remove_symbols.sh
cd /tmp/xkeyboard-config-install || exit 0
ln -sf %{_bindir}/remove_symbols.sh remove_symbols.sh
rm -f %{_bindir}/remove_symbols.sh
rm remove_symbols.sh
%{_bindir}/cache
rm -f %{_bindir}/cache
mkdir -p /%{TZ_SYS_VAR}/lib/xkb/
touch /%{TZ_SYS_VAR}/lib/xkb/dummy.xkb
cp *.xkb /%{TZ_SYS_RO_SHARE}/X11/xkb/

%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%doc AUTHORS README docs/HOWTO.* docs/README.*
%dir %{_localstatedir}/lib/xkb/compiled
%{_datadir}/pkgconfig/*.pc
%{_datadir}/X11/xkb/
%{_bindir}/cache
%{_bindir}/make_keycodes.sh
%{_bindir}/make_symbols.sh
%{_bindir}/remove_symbols.sh

%files i18n -f %{name}.lang
