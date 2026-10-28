Name:           kbd
Version:        2.2.0
Release:        0
Summary:        Tools for configuring the console (keyboard, virtual terminals, etc

License:        GPL-2.0+
Url:            http://ftp.altlinux.org/pub/people/legion/kbd
Group:          Base/Utilities
Source0:        %{name}-%{version}.tar.bz2
Source2:        kbd-latsun-fonts.tar.bz2
Source3:        kbd-latarcyrheb-16-fixed.tar.bz2
Source4:        fr-dvorak.tar.bz2
Source5:        kbd-latarcyrheb-32.tar.bz2
Source6:        Add_pie_compile_option.patch
Source7:        fix_no-error-incompatible-pointer-types.patch
Source1001:     kbd.manifest

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gettext
BuildRequires:  pkgconfig(check)
BuildRequires:  pam-devel
BuildRequires:  fdupes
Requires:       %{name}-misc = %{version}

%description
The %{name} package contains tools for managing a Linux
system's console's behavior, including the keyboard, the screen
fonts, the virtual terminals and font files.

%package misc
Summary:        Data for kbd package
BuildArch:      noarch

%description misc
The %{name}-misc package contains data for kbd package - console fonts,
keymaps etc. Please note that %{name}-misc is not helpful without kbd.

%prep
%setup -q -a 2 -a 3 -a 4 -a 5
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE6}
%{__patch} -p1 < %{SOURCE7}

# 7-bit maps are obsolete; so are non-euro maps
cd data/keymaps/i386
mv qwerty/fi.map qwerty/fi-old.map
#cp qwerty/fi-latin9.map qwerty/fi.map
cp qwerty/pt-latin9.map qwerty/pt.map
cp qwerty/sv-latin1.map qwerty/se-latin1.map

mv azerty/fr.map azerty/fr-old.map
cp azerty/fr-latin9.map azerty/fr.map

cp azerty/fr-latin9.map azerty/fr-latin0.map # legacy alias

# Rename conflicting keymaps
mv fgGIod/trf.map fgGIod/trf-fgGIod.map
mv olpc/es.map olpc/es-olpc.map
mv olpc/pt.map olpc/pt-olpc.map
mv qwerty/cz.map qwerty/cz-qwerty.map
cd -

# remove obsolete "gr" translation
cd po
rm -f gr.po gr.gmo
cd -

%build
%if "%{asan}" == "1"
%restore_fcommon
%endif

autoreconf -fi
%configure --prefix=%{_prefix} \
           --datadir=%{_prefix}/lib/kbd \
           --mandir=%{_mandir} \
           --localedir=%{_datadir}/locale \
           --disable-nls

%__make %{?_smp_mflags}

%install
%make_install

# ro_win.map.gz is useless
rm -f %{buildroot}/%{_prefix}/lib/kbd/keymaps/i386/qwerty/ro_win.map.gz

# Create additional name for Serbian latin keyboard
ln -sf sr-cy.map.gz %{buildroot}/%{_prefix}/lib/kbd/keymaps/i386/qwerty/sr-latin.map.gz

# The rhpl keyboard layout table is indexed by kbd layout names, so we need a
# Korean keyboard
ln -sf us.map.gz %{buildroot}/%{_prefix}/lib/kbd/keymaps/i386/qwerty/ko.map.gz

# Some microoptimization
sed -i -e 's,\<kbd_mode\>,/usr/bin/kbd_mode,g;s,\<setfont\>,/usr/bin/setfont,g' \
        %{buildroot}/%{_bindir}/unicode_start

# Link open to openvt
ln -sf openvt %{buildroot}%{_bindir}/open

## Move locale files to correct place
#cp -r %%{buildroot}/lib/kbd/locale/ %%{buildroot}%%{_datadir}/locale
#rm -rf %%{buildroot}/lib/kbd/locale

%fdupes %{buildroot}%{_prefix}/lib/kbd

%docs_package

%check
# %__make check || exit 0


%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/*

%files misc
%manifest %{name}.manifest
%{_prefix}/lib/kbd
