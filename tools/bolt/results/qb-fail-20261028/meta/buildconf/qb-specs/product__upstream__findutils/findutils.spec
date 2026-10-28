Name:           findutils
Url:            http://www.gnu.org/software/findutils/
Version:        4.3.8
Release:        11
Summary:        The GNU versions of find utilities (find and xargs)
License:        GPL-2.0
Group:          Base/Tools
# retrieved from http://alpha.gnu.org/pub/gnu/findutils/findutils-4.5.10.tar.gz
Source:         findutils-%{version}.tar.bz2
Source1:        sysconfig.locate
Source1001: 	findutils.manifest
Requires:       toybox

%description
find and xargs are provided by toybox; /usr/bin/find and /usr/bin/xargs
here are symlinks to it. The complete GNU implementations remain
available under the gnu_ name prefix (/usr/bin/gnu_find,
/usr/bin/gnu_xargs).

%package locate
Summary:        Tool for Locating Files (findutils subpackage)
Group:          Base/Tools
Provides:       findutils:/usr/bin/locate
Requires:       findutils = %{version}

%description locate
This package contains the locate program which is part of the GNU
findutils software suite. The complete GNU implementations of locate
and updatedb remain available under the gnu_ name prefix
(/usr/bin/gnu_locate, /usr/bin/gnu_updatedb).

You can find files fast using locate.  On installing findutils-locate
an additional daily cron job will be added to the cron system. This
job will update the files database every night or shortly after
switching on the computer.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if "%{asan}" == "1"
%restore_fcommon
%endif
%if "%{hwasan}" == "1"
%restore_fcommon
%endif

%ifarch %arm armv5tel armv7l armv7el armv5el
# this is a workaround for a qemu-user bug, we hit. A qemu patch is being discussed, but for now ...
export DEFAULT_ARG_SIZE="(31u * 1024u)"
%endif

CFLAGS="$CFLAGS -fPIE -fcommon"
LDFLAGS="$LDFLAGS -pie"
%configure \
  --program-prefix=gnu_ \
  --libexecdir=%{_libdir}/find \
  --localstatedir=/var/lib
%{__make} %{?_smp_mflags}

%check
make check

%install
%make_install

install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/locate
rm -f $RPM_BUILD_ROOT%{_bindir}/gnu_oldfind
rm -f $RPM_BUILD_ROOT%{_bindir}/gnu_ftsfind
rm -f $RPM_BUILD_ROOT%{_infodir}/find-maint*
%find_lang %{name}

%remove_docs

# standard names for commands toybox does not implement, shipped as
# real binaries alongside the gnu_ prefixed ones
for c in locate updatedb; do
    cp -p %{buildroot}%{_bindir}/gnu_$c %{buildroot}%{_bindir}/$c
done

# identical to the symlinks toybox owns, so rpm treats them as shared
# rather than conflicting; keeps find usable with any toybox version
for c in find xargs; do
    ln -s toybox %{buildroot}%{_bindir}/$c
done

%lang_package

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/find
%{_bindir}/xargs
%{_bindir}/gnu_find
%{_bindir}/gnu_xargs

%files locate
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/locate
%{_bindir}/updatedb
%{_bindir}/gnu_locate
%{_bindir}/gnu_updatedb
%{_libdir}/find
%config(noreplace) %{_sysconfdir}/sysconfig/locate

%changelog
