%bcond_with wayland
%bcond_with x
%define disable_docs_package 1
%define debug_package %{nil}

Name:           filesystem
VCS:            platform/upstream/filesystem#266eca3b74d423c76f00bd21e8b62664991c0f49
Version:        3.1
Release:        1.1
License:        PD
Summary:        The basic directory layout for a Linux system
Url:            https://fedorahosted.org/filesystem
Group:          Base/Configuration
Requires(pre): setup
Source2:        languages
Source3:        languages.man
Source4:        200.filesystem-platform-extension-migration.sh
Source1001:     %{name}.manifest

%description
The filesystem package is one of the basic packages that is installed
on a Linux system. Filesystem contains the basic directory layout
for a Linux operating system, including the correct permissions for
the directories.

%prep
rm -f $RPM_BUILD_DIR/filelist

%build
cp %{SOURCE1001} .

%install
create_dir () {
    local MODE=$1
    case "$MODE" in
     \#*) return ;;
    esac
    local OWNR=$2
    local GRUP=$3
    local NAME=$4
    local XTRA=$5
    local BDIR=`dirname $NAME`
    test -d "$RPM_BUILD_ROOT/$NAME" && { echo "dir $NAME does already exist" ; echo "input out of sequence ?" ; exit 1 ; }
    test -n "$BDIR" -a ! -d $RPM_BUILD_ROOT$BDIR && create_dir 0755 root root $BDIR
    mkdir -m $MODE $RPM_BUILD_ROOT/$NAME
    echo "$XTRA%%dir %%attr($MODE,$OWNR,$GRUP) $NAME" >> $RPM_BUILD_DIR/filelist
}

cd %{buildroot}

mkdir -p boot dev \
%if %{with x}
        etc/X11/applnk etc/X11/fontpath.d \
	usr/share/xsessions usr/share/X11 \
%endif
	etc/xdg/autostart etc/ld.so.conf.d etc/opt etc/pm/config.d etc/pm/power.d etc/pm/sleep.d etc/xinetd.d etc/sysconfig etc/pki \
        home mnt root run/lock srv tmp \
        opt/home opt/media opt/usr opt/share opt/dbspace opt/data opt/etc/skel opt/var \
        usr/bin usr/etc usr/games usr/include usr/%{_lib}/pkgconfig usr/%{_lib}/games usr/%{_lib}/sse2 usr/%{_lib}/tls usr/%{_lib}/X11 usr/%{_lib}/pm-utils/module.d usr/%{_lib}/pm-utils/power.d usr/%{_lib}/pm-utils/sleep.d usr/lib/games usr/lib/locale usr/lib/modules usr/lib/sse2 usr/libexec usr/local/bin usr/local/etc usr/local/games usr/local/lib usr/local/%{_lib} usr/local/sbin usr/local/src usr/local/share/applications usr/local/share/man/man1 usr/local/share/man/man2 usr/local/share/man/man3 usr/local/share/man/man4 usr/local/share/man/man5 usr/local/share/man/man6 usr/local/share/man/man7 usr/local/share/man/man8 usr/local/share/man/man9 usr/local/share/man/mann usr/local/share/man/man1x usr/local/share/man/man2x usr/local/share/man/man3x usr/local/share/man/man4x usr/local/share/man/man5x usr/local/share/man/man6x usr/local/share/man/man7x usr/local/share/man/man8x usr/local/share/man/man9x usr/local/share/info usr/local/libexec usr/local/include usr/sbin usr/share/help/C usr/share/aclocal usr/share/applications usr/share/augeas/lenses usr/share/backgrounds usr/share/desktop-directories usr/share/dict usr/share/doc usr/share/empty usr/share/games usr/share/ghostscript/conf.d usr/share/gnome usr/share/idl usr/share/info usr/share/man/man1 usr/share/man/man2 usr/share/man/man3 usr/share/man/man4 usr/share/man/man5 usr/share/man/man6 usr/share/man/man7 usr/share/man/man8 usr/share/man/man9 usr/share/man/mann usr/share/man/man1x usr/share/man/man2x usr/share/man/man3x usr/share/man/man4x usr/share/man/man5x usr/share/man/man6x usr/share/man/man7x usr/share/man/man8x usr/share/man/man9x usr/share/man/man0p usr/share/man/man1p usr/share/man/man3p usr/share/mime-info usr/share/misc usr/share/omf usr/share/pixmaps usr/share/sounds usr/share/themes usr/share/upgrade/data usr/share/upgrade/scripts usr/share/platform-extension usr/src usr/src/kernels usr/src/debug \
        var/lib/empty var/lib/misc var/local var/lock/subsys var/log var/nis var/preserve var/run var/spool/mail var/spool/lpd var/tmp var/db var/cache var/opt var/games \
        vendor apps product

cp %{SOURCE4} %{buildroot}/usr/share/platform-extension/

ln -snf opt/media media
ln -snf ../var/tmp usr/tmp
ln -snf spool/mail var/mail
ln -snf usr/bin bin
ln -snf usr/sbin sbin
ln -snf usr/lib lib
ln -snf usr/%{_lib} %{_lib}
ln -snf /opt/etc/skel etc/skel

# Create the locale directories:
while read LANG ; do
  echo "%lang(${LANG}) %ghost %config(missingok) /usr/share/locale/${LANG}" >>$RPM_BUILD_DIR/filelist
  create_dir 0755 root root /usr/share/locale/$LANG/LC_MESSAGES
  create_dir 0755 root root /usr/share/help/$LANG
done < %{SOURCE2}
# Create the locale directories for man:
while read LANG ; do
  create_dir 0755 root root /usr/share/man/$LANG
  for sec in 1 2 3 4 5 6 7 8 9 n; do
    create_dir 0755 root root /usr/share/man/$LANG/man$sec
##"%lang(${LANG}) %ghost %config(missingok)"
  done
done < %{SOURCE3}


%pretrans -p <lua>
--#
--# If we are running in pretrans in a fresh root, there is no /usr and symlinks.
--# We cannot be sure, to be the very first rpm in the transaction list,
--# so, let's create the toplevel symlinks here and the directories they point to.
--# When our rpm is unpacked by cpio, it will set all permissions and modes later.
--#

if posix.stat("/usr") == nil then
    posix.mkdir("/usr")
end

for i,dir in ipairs({"/lib", "/%{_lib}", "/sbin", "/bin"}) do
    if posix.stat("/usr"..dir) == nil then
        if posix.stat(dir, "mode") == nil then
            posix.mkdir("/usr"..dir)
	else
	    os.rename(dir,"/usr"..dir)
	end

        posix.symlink("usr"..dir, dir)
    end
end

return 0

%post -p <lua>
posix.symlink("/run", "/var/run")
posix.symlink("/run/lock", "/var/lock")

%files -f filelist
%manifest %{name}.manifest
%defattr(0755,root,root,-)
%dir %attr(555,root,root)
/bin
%attr(555,root,root) /boot
/dev
%dir /etc
%if %{with x}
%{_sysconfdir}/X11
%endif
%{_sysconfdir}/xdg
%{_sysconfdir}/opt
%{_sysconfdir}/pm
%{_sysconfdir}/xinetd.d
%{_sysconfdir}/skel
%{_sysconfdir}/sysconfig
%{_sysconfdir}/pki
/opt/usr
/opt/share
/opt/dbspace
/opt/data
/opt/etc
/home
/opt/home
/lib
#%ifarch x86_64 ppc ppc64 sparc sparc64 s390 s390x
/%{_lib}
#%endif
/media
/opt/media
%dir /mnt
%attr(550,root,root) /root
/run
/sbin
/srv
%attr(1777,root,root) /tmp
%dir /usr
%attr(555,root,root) /usr/bin
/usr/etc
/usr/games
/usr/include
%attr(555,root,root) /usr/lib
#%ifarch x86_64 ppc ppc64 sparc sparc64 s390 s390x
%attr(555,root,root) /usr/%{_lib}
#%endif
/usr/libexec
/usr/local
%attr(555,root,root) /usr/sbin
%dir /usr/share
/usr/share/aclocal
/usr/share/applications
/usr/share/help/C
/usr/share/augeas
/usr/share/backgrounds
/usr/share/desktop-directories
/usr/share/dict
/usr/share/doc
%attr(555,root,root) %dir /usr/share/empty
/usr/share/games
/usr/share/ghostscript
/usr/share/gnome
/usr/share/idl
/usr/share/info
%dir /usr/share/locale
%dir /usr/share/man
/usr/share/mime-info
/usr/share/misc
/usr/share/omf
/usr/share/pixmaps
/usr/share/sounds
/usr/share/themes
%if %{with x}
/usr/share/xsessions
/usr/share/X11
%endif
%attr(700,root,root) /usr/share/upgrade
%attr(755,root,root) /usr/share/platform-extension
%attr(755,root,root) /usr/share/platform-extension/200.filesystem-platform-extension-migration.sh
/usr/src
/usr/tmp
/opt/var
%dir /var
%dir /vendor
%dir /apps
%dir /product
%{_localstatedir}/cache
%{_localstatedir}/db
%{_localstatedir}/games
%{_localstatedir}/lib
%{_localstatedir}/local
%ghost %dir %attr(755,root,root) %{_localstatedir}/lock
%ghost %{_localstatedir}/lock/subsys
%{_localstatedir}/log
%{_localstatedir}/mail
%{_localstatedir}/nis
%{_localstatedir}/opt
%{_localstatedir}/preserve
%ghost %attr(755,root,root) %{_localstatedir}/run
%dir %{_localstatedir}/spool
%attr(755,root,root) %{_localstatedir}/spool/lpd
%attr(775,root,mail) %{_localstatedir}/spool/mail
%attr(1777,root,root) %{_localstatedir}/tmp

%changelog
* Wed Dec  4 2013 Łukasz Stelmach <l.stelmach@samsung.com> accepted/tizen/20131126.190119@88643ce
- Add directory for Tizen applications: /usr/apps
* Tue Nov 26 2013 Rusty Lynch <rusty.lynch@intel.com> accepted/tizen_ivi_stable/20131116.085010@725b1e0
- TIVI-2017: create media and share directories
- TIVI-2052: Create tizen dbspace directories
- Add the creation of the app user home directory and soft link Add the developer home directory
* Fri Jun 14 2013 Anas Nashif <anas.nashif@intel.com> submit/tizen/20130614.193514@280f99a
- add pkgconfig
* Wed May 29 2013 Anas Nashif <anas.nashif@intel.com> submit/tizen/20130529.081016@11e5401
- add /etc/ld.so.conf.d to default file system
* Fri Mar 22 2013 Anas Nashif <anas.nashif@intel.com> submit/trunk/20130306.090327@6d1f77e
- Fixed package groups
