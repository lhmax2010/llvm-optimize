Name: toybox
Version: 0.8.14
Release: 5%{?dist}
Summary: Single binary providing simplified versions of system commands
Group: Base/Utilities
License: 0BSD
URL: http://www.landley.net/toybox/
Source: %{name}-%{version}.tar.bz2
Source1: config
Source2: toybox-prefixed.list
Source1001: toybox.manifest
# tizen_macros' %%make_install (.la/.a cleanup) and %%remove_docs (man page
# cleanup) use `find -regex ... | xargs rm -f --`. Once toybox owns
# /usr/bin/find, those macros need -regex/-iregex, which upstream toybox's
# find does not implement. Affects packages that use %%make_install or
# %%remove_docs, not every package.
Source1002: 0001-find-add-regex-iregex.patch
# Upstream toybox's "ls -l" always prints long-iso timestamps. Autotools
# helper scripts bundled by many GNU packages (automake's/make's/grep's
# mdate-sh) parse the classic "Mon DD HH:MM"/"Mon DD  YYYY" format out of
# plain "ls -l" to timestamp generated docs; failing to find a month
# abbreviation makes mdate-sh error out (or, in older copies lacking a
# bounds check, loop forever) and can corrupt the generated Texinfo files.
Source1003: 0002-ls-classic-time-format.patch
# Autoconf's AC_PROG_MKDIR_P only trusts "mkdir -p" to be race-free if
# "mkdir --version" claims to be GNU coreutils (or old fileutils). Failing
# that check makes autotools packages fall back to their bundled install-sh,
# whose "-d" mode silently drops every directory but the first when given
# several at once (e.g. automake's $(MKDIR_P) dir1 dir2 dir3), so later
# install steps targeting the dropped directories fail.
Source1004: 0003-mkdir-gnu-coreutils-version.patch
# "cp -p SYMLINK DEST" (no -r/-a/-d), where SYMLINK resolves to a directory,
# dereferences it via a plain openat() and then unconditionally creates DEST
# as an empty regular file instead of refusing like a literal directory
# source would. GBS's icecream integration hits this: icecc-create-env's
# multilib special case does "cp -p /lib $tempdir/lib" to preserve the
# /lib -> usr/lib symlink on merged-usr rootfs, which leaves a bogus empty
# file at $tempdir/lib; every later "mkdir/cp" into $tempdir/lib for libc,
# ld-linux.so, etc. then fails and aborts the icecream env tarball.
Source1005: 0004-cp-reject-symlinked-dir.patch
# RPM %%post scripts in Tizen packages use GNU coreutils long options
# (mkdir --mode=MODE, date --date=DATE) that toybox's optparser did not
# recognise, producing "Unknown option" at image build time. The (mode) and
# (date) aliases in the NEWTOY option strings add the missing long-option
# mappings without changing any behaviour for the short forms.
Source1006: 0005-mkdir-date-add-gnu-long-option-aliases.patch
Source1007: 0006-scripts-make-force-serial-on-bash-without-wait-n.patch

BuildRequires : smack-devel
BuildRequires : libattr-devel
# Older findutils/which own /usr/bin/find, xargs and which as real files and
# conflict with this package; the new ones must be published first.
BuildRequires: findutils >= 4.3.8-11
BuildRequires: which >= 2.17-11

# toybox owns the standard coreutils command names on Tizen.
# It is installed alongside the coreutils package, which carries only
# the commands toybox does not implement (join, pr, ...).  The GNU
# implementations remain available as gnu_* from coreutils-gnu.
#
# toybox also owns find/xargs (findutils) and which. findutils and
# which are installed alongside it, carrying only the commands toybox
# does not implement (locate/updatedb, ...).
Provides: mktemp
Provides: /bin/basename /bin/cat /bin/chmod /bin/chown /bin/cp /bin/env /bin/ln
Provides: /bin/ls /bin/mkdir /bin/mv /bin/pwd /bin/rm /bin/sort /bin/touch
Conflicts: findutils < 4.3.8-11
Conflicts: which < 2.17-11
Obsoletes: toybox-full < %{version}-%{release}
Obsoletes: toybox-symlinks-nslookup < %{version}-%{release}

%description
Toybox is a single binary which includes versions of a large number
of system commands, including a shell.  On Tizen it provides the
standard command names previously owned by GNU coreutils, as well as
find, xargs and which.  Command names owned by other packages are
installed with a toybox- prefix (see the symlinks-compat subpackage).

%package symlinks-compat
Group: Base/Utilities
Summary: ToyBox symlinks with toybox- prefix for commands owned by other packages
Requires: %{name} = %{version}-%{release}
Obsoletes: toybox-symlinks-full < %{version}-%{release}

%description symlinks-compat
toybox- prefixed symlinks for the applets whose standard names are owned
by other packages (util-linux, procps-ng, grep, sed, ...).

%package symlinks-dhcp
Group: Base/Utilities
Summary: ToyBox symlinks to provide 'dhcp'
Requires: %{name} = %{version}-%{release}

%description symlinks-dhcp
ToyBox symlinks for utilities corresponding to 'dhcp' package.

%package symlinks-dhcpd
Group: Base/Utilities
Summary: ToyBox symlinks to provide 'dhcpd'
Requires: %{name} = %{version}-%{release}

%description symlinks-dhcpd
ToyBox symlinks for utilities corresponding to 'dhcpd' package.

%package symlinks-ping
Group: Base/Utilities
Summary: ToyBox symlinks to provide 'ping'
Requires: %{name} = %{version}-%{release}

%description symlinks-ping
ToyBox symlinks for utilities corresponding to 'ping' package.

%package symlinks-ping6
Group: Base/Utilities
Summary: ToyBox symlinks to provide 'ping6'
Requires: %{name} = %{version}-%{release}

%description symlinks-ping6
ToyBox symlinks for utilities corresponding to 'ping6' package.

%prep
%setup -q
%{__patch} -p1 < %{SOURCE1002}
%{__patch} -p1 < %{SOURCE1003}
%{__patch} -p1 < %{SOURCE1004}
%{__patch} -p1 < %{SOURCE1005}
%{__patch} -p1 < %{SOURCE1006}
%{__patch} -p1 < %{SOURCE1007}

%build
cp %{SOURCE1001} .

%{?!_toolchain:
export CC="gcc"
}
KCONFIG_ALLCONFIG=%{SOURCE1} scripts/genconfig.sh -n
make %{?_smp_mflags} CFLAGS=" $CFLAGS -fPIE -Wno-nonnull -Wno-incompatible-pointer-types" LDOPTIMIZE=" -Wl,--gc-sections -pie"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
install -m 755 toybox %{buildroot}%{_bindir}/toybox

./toybox | tr ' ' '\n' | sed '/^$/d' | sort -u > applets.all

: > files.main
: > files.compat
while read -r a; do
    case "$a" in
        toybox|dhcp|dhcpd|dumpleases|ping|ping6|\[) continue ;;
    esac
    if grep -qxF "$a" %{SOURCE2}; then
        ln -s toybox "%{buildroot}%{_bindir}/toybox-$a"
        printf '%%s\n' "%{_bindir}/toybox-$a" >> files.compat
    elif [ "$a" = telnetd ]; then
        ln -s ../bin/toybox "%{buildroot}%{_sbindir}/$a"
        printf '%%s\n' "%{_sbindir}/$a" >> files.main
    else
        ln -s toybox "%{buildroot}%{_bindir}/$a"
        printf '%%s\n' "%{_bindir}/$a" >> files.main
    fi
done < applets.all

# unprefixed by design, packaged in dedicated symlinks subpackages
ln -s toybox %{buildroot}%{_bindir}/dhcp
ln -s toybox %{buildroot}%{_bindir}/dumpleases
ln -s ../bin/toybox %{buildroot}%{_sbindir}/dhcpd
ln -s toybox %{buildroot}%{_bindir}/ping
ln -s toybox %{buildroot}%{_bindir}/ping6

%files -f files.main
%manifest toybox.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_bindir}/toybox

%files symlinks-compat -f files.compat
%manifest toybox.manifest
%license LICENSE
%defattr(-,root,root,-)

%files symlinks-dhcp
%manifest toybox.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_bindir}/dhcp

%files symlinks-dhcpd
%manifest toybox.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_bindir}/dumpleases
%{_sbindir}/dhcpd

%files symlinks-ping
%manifest toybox.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_bindir}/ping

%files symlinks-ping6
%manifest toybox.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_bindir}/ping6
