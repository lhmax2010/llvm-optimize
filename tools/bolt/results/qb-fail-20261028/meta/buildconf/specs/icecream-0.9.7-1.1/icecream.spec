#
# spec file for package icecream
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild
# icecream 0


Name:           icecream
VCS:            platform/upstream/icecream#bf7fcfb8e0ca8783b877b3f88b8bafa74779e06d
BuildRequires:  gcc-c++
License:        GPLv2+ ; LGPLv2.1+
Group:          Development/Tools/Building
Summary:        For Distributed Compile in the Network
Requires:       /bin/tar /usr/bin/bzip2
%if 0%{?suse_version}
PreReq:         %fillup_prereq
PreReq:         %insserv_prereq
%endif
Requires(pre):  shadow-utils
Requires:       gcc-c++
Version:        0.9.7
Release:        1.1
Source:        ftp://ftp.suse.com/pub/projects/icecream/icecc-%{version}.tar.bz2

%description
icecream is the next generation distcc.

%package -n libicecream-devel
License:        GPLv2+ ; LGPLv2.1+
Summary:        For Distributed Compile in the Network
Group:          Development/Tools/Building
Summary:        For Distributed Compile in the Network
Requires:       libstdc++-devel

%description -n libicecream-devel
icecream is the next generation distcc.

%prep
%setup -q -n icecc-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
%configure
make %{?jobs:-j %jobs}

%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/opt/icecream/bin
for i in g++ gcc cc c++ clang clang++; do
  ln -s /usr/bin/icecc $RPM_BUILD_ROOT/opt/icecream/bin/$i
  rm -f $RPM_BUILD_ROOT/usr/bin/$i
done
%ifarch armv7l
ln -s /usr/bin/icecc $RPM_BUILD_ROOT/opt/icecream/bin/armv7l-tizen-linux-gnueabi-gcc
%endif
%ifarch aarch64
ln -s /usr/bin/icecc $RPM_BUILD_ROOT/opt/icecream/bin/aarch64-tizen-linux-gnueabi-gcc
%endif

#
# Install icecream init script
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
install -m 755 suse/init.icecream $RPM_BUILD_ROOT/etc/init.d/icecream
ln -sf /etc/init.d/icecream $RPM_BUILD_ROOT%{_sbindir}/rcicecream
mkdir -p $RPM_BUILD_ROOT/var/adm/fillup-templates
install -m 644 suse/sysconfig.icecream $RPM_BUILD_ROOT/var/adm/fillup-templates/sysconfig.icecream
mkdir -p $RPM_BUILD_ROOT/var/cache/icecream
mkdir -p $RPM_BUILD_ROOT%_mandir/man{1,7}
for i in mans/*.1 mans/*.7; do
	install -m 644 $i $RPM_BUILD_ROOT%_mandir/man`echo $i | sed -e 's,.*\(.\)$,\1,'`/`basename $i`
done
install -m 644 -D suse/logrotate $RPM_BUILD_ROOT/etc/logrotate.d/icecream
%if 0%{?suse_version} > 1020
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/SuSEfirewall2.d/services
install -m 644 suse/SuSEfirewall.iceccd $RPM_BUILD_ROOT/etc/sysconfig/SuSEfirewall2.d/services/iceccd
install -m 644 suse/SuSEfirewall.scheduler $RPM_BUILD_ROOT/etc/sysconfig/SuSEfirewall2.d/services/icecream-scheduler
%endif

%preun
%stop_on_removal icecream

%pre
/usr/sbin/groupadd -r icecream 2> /dev/null || :
/usr/sbin/useradd -r -g icecream -s /bin/false -c "Icecream Daemon" -d /var/cache/icecream icecream 2> /dev/null || :
%if 0%{?suse_version}

%post
%{fillup_and_insserv -n icecream icecream}
%endif

%postun
%restart_on_update icecream
%{insserv_cleanup}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%config /etc/logrotate.d/icecream
%config /etc/init.d/icecream
%_bindir/icecc
%_bindir/icerun
%_sbindir/scheduler
%_libdir/icecc
%_sbindir/iceccd
%_sbindir/rcicecream
%_mandir/man*/*
/opt/icecream
%if 0%{?suse_version} > 1020
/etc/sysconfig/SuSEfirewall2.d/services/*
%endif
/var/adm/fillup-templates/sysconfig.icecream
%attr(-,icecream,icecream) /var/cache/icecream

%files -n libicecream-devel
%defattr(-,root,root)
%_includedir/icecc
%_libdir/libicecc.*
%_libdir/pkgconfig/icecc.pc

%changelog
* Thu May 19 2011 coolo@novell.com
- update to 0.9.7
  - bug fix for -MD and -MF
  - bug fix for gcc 4.6 plugins
* Tue Aug  3 2010 coolo@novell.com
- Update to 0.9.6
  - fix installation issues
  - add a value type of ticks in /proc - and make it long long
  - fix kFreeBSD build
  - fix run-failure with glibc 2.11
  - allow tgz as extension
  - support more local args (bnc#625621)
* Thu May 27 2010 dmueller@suse.de
- fix build against glibc 2.11
* Mon Feb  1 2010 coolo@novell.com
- Update to 0.9.5
  - fix: close the file descriptor (novell bug bnc#525799)
  - log PID even if no prefix is specified
  - allow get_msg() to fetch data from the kernel even if timeout is 0.
  - clean up event loop of gcc invocation
  - Install an "icerun" symlink that will serialize commands through
  icecream's local daemon
* Thu Apr 30 2009 coolo@suse.de
- Update to 0.9.4
  - don't leak file descriptor to create-env
  - don't use the shell to call simple commands
  - make a special exception for - in rest args (bnc#495786)
  - Fix way icecream changes permissions of /var/cache/icecream
* Sun Feb 15 2009 coolo@suse.de
- update to 0.9.3 to fix compilation with gcc 4.4
* Sun Nov  2 2008 coolo@suse.de
- update to 0.9.2 to include patches upstreamed
  - Add accessor for the hostname of the scheduler, so that we can
  show it in a tooltip in icemon in the future.
  - Only localize job if we find -Wa,.*-a[a-z]*= in an argument
  - also add accessor for network name
  - if called as "icecc" (i.e., not through a symlink) and the first
  argument starts with a slash, use that as the command to run.
* Mon Oct  6 2008 dmueller@suse.de
- correct service description (bnc#424431)
* Fri Aug 22 2008 aj@suse.de
- Fix init script.
* Thu Jun 19 2008 coolo@suse.de
- update to 0.9.1
  - trying to support gentoo x86_64
  - -mcpu=native has to compile locally (gentoo bug 183586#c13)
  - don't compile C files with C++ compile if ICECC_CXX is set
* Mon May 12 2008 coolo@suse.de
- update to 0.9.0 (no functionial change in suse package):
  * merged make-it-cool-branch
* Fri May  9 2008 dmueller@suse.de
- update make-it-cool-branch:
  * fix handling of pch's
  * ignore really small environments
  * small code cleanups and portability fixes
* Thu Apr 10 2008 coolo@suse.de
- fix compilation with glibc 2.8
* Tue Feb 12 2008 dmueller@suse.de
- more robustness fixes
* Fri Feb  8 2008 dmueller@suse.de
- fix scheduler "crash"
- fix scheduler to not bring down network of the machine during a
  DoS attack from a broken compile daemon
* Mon Jan 28 2008 dmueller@suse.de
- fix pid file generation in the daemon
* Tue Jan 15 2008 dmueller@suse.de
- update to current make-it-cool branch:
  * small bugfixes
* Thu Nov  8 2007 ro@suse.de
- install sysconfig fillup template also for <= 10.2
  (used unconditionally in rc-script)
* Thu Aug  2 2007 dmueller@suse.de
- update make-it-cool branch diff for the following changes:
  * fix handling of control channels, implement idle-timeout
  * make the protocol more rebust against integer overflows
    and other attacks
  * fix icecream update not restarting the daemon
  * clean up scheduler code to remove unnecessary dynamic_casts
  * improve error handling for protocol errors on daemon<->scheduler
    communication
  * daemon will no longer flood scheduler with connection requests
    when he got kicked
  * monitor connections are more bulky now and use much smaller
    messages to reduce network overhead
  * client will now try to fetch the error message from the compile
    server before claiming that the compile server unexpectedly ended
    connection.
  * Job statistics in the monitor were all broken. Fixed.
* Thu Jul 26 2007 dmueller@suse.de
- update make-it-cool branch diff to workaround scheduler hanging
  when icecream monitors are connected
- fix double deletion in the scheduler
- switch control connections to bulk mode
- remove errnous error in client when local daemon is offline
- implement host blocking
* Wed Jul 18 2007 dmueller@suse.de
- 0.8.0:
  - write a pid file. patch by Ismail Doenmez
  - precompiled header support, needed for compiling Qt 4.3
  - add support for --no-remote. patch by Matt Gruenke
  - update node name each time we login to the scheduler.
  - treat -combine and -fdump* as always local
  - Merged make-it-cool branch:
  * implement job preloading
  * asynchronous install of new environments
  * uses tcp keepalive for network connection tracking
- added make-it-cool branch diff:
  * implement local scheduling of arbitrary build commands
    (e.g. meinproc)
  * add non-blocking connect to the scheduler to improve latency
* Mon Apr 23 2007 coolo@suse.de
- provide SUSEfirewall descriptions (#247340)
* Wed Sep 13 2006 coolo@suse.de
- 0.7.14:
  - fix current_kids getting out of sync if send_scheduler
    failes in an unfortunate moment
  - fix reporting the error
  - add more to the internals dump
  - trying to make the scheduler kicks a little bit less frequent
  - if the compiler is supposed to keep temp files, then we
    have to do it locally
* Tue Sep 12 2006 coolo@suse.de
- 0.7.13:
  - use file -L to follow symlinks in create-env
  - fix an easy valgrind error
  - make handling of the return values consistent
  - if the client is in WAITCOMPILE then it's waiting for some
    other host to compile, not this one. So job == 0 -> crash
  - fix crash if the scheduler goes away while daemon transfers
    environment
  - apparently sometimes gcc can hang forever in some
    cases. By the time the client disconects, we know
    we don't have to wait any longer, because there is
    nobody left caring about the result.
  - update node name each time we login to the scheduler.
    Fixes tons of "linux" hosts appearing in the icecream
    monitor
* Wed Sep  6 2006 coolo@suse.de
- 0.7.12:
  - fixing error handling when scheduler restarts
  - do not waitpid before we're sure we read all of g++'s
    output otherwise g++ waits for us to read and we're
    waiting for g++ to finish -> deadlock
* Tue Sep  5 2006 coolo@suse.de
- 0.7.11:
  - fix a crash in the daemon when the scheduler was gone while
    local jobs were waiting for finishing
  - separate stat handling from ping handling
    to avoid excessive stat/ping loops
    (increases internal version number)
  - only reset scheduler ping time if the scheduler ping'ed us
  - even when we can't determine native environment, we
    can still use the daemon for inter-process locking
    instead of falling back to file locking.
  - quicker reap of dead daemons
  - improved load guessing
  - fix stupid logic bug in ping tracking
* Mon Sep  4 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Sep  4 2006 coolo@suse.de
- 0.7.10:
  - handle errors in installing environments correctly
  - block daemons that have full discs
  - add -pipe to the command line to reduce disk usage
  - fix cancelling of jobs awaiting a remote job (were hanging
    in scheduler forever)
  - if ICECC=no is set, don't try to be clever
  - adding two more flags for local compilation (profile
    feedback related)
  - flush debug files before every fork to avoid dups in
    log output
  - be stricter in what messages are required to keep the
    daemon<->scheduler communication intact (network drops
    again)
* Sun Sep  3 2006 coolo@suse.de
- 0.7.9:
  - scheduler will ping the daemon periodically,
    daemon will disconnect if not pinged from time
    to time (to avoid network drops being unnoticed)
  - removed some debug output
  - make logging more consistent
  - increased internal protocol version (still compatible)
  - try even harder to avoid races in daemon
  - rework how clients are catched
  - some random cleanup
  - remove the "this should be an exception" output to
    avoid failing configure checks for nothing
  - make sure the assembler is dead before we cleanup object
    files
-Sat Sep  2 19:01:02 CEST 2006 - ro@suse.de
- 0.7.8:
  - fd leak fix, which caused a deadlock under
    certain conditions
  - rework some FreeBSD patches that caused problems
  - fix race between select and SIGCHILD
* Tue Aug 29 2006 coolo@suse.de
- reverted part of the FreeBSD patch that broke x86_64 envs
* Fri Aug 25 2006 coolo@suse.de
- 0.7.7:
  - clear all internal maps
  - patches by Frerich to support FreeBSD
  - avoid busy loop in bizarre conditions
  - found another case of endless hanging jobs
  - some process fixes
* Wed Aug 23 2006 schwab@suse.de
- Avoid race condition with slow scheduler.
* Thu Jul 13 2006 coolo@suse.de
- 0.7.6:
  - report all daemon error message to the client
  - fix support for biarch machines that have only one
    environment installed with another environment with
    the same name and different architecture being around
  - work-around a bug in older libstdc++
  - ensure nobody uses -u root
* Wed Jul 12 2006 coolo@suse.de
- 0.7.5:
  - Don't block while looking for a scheduler over broadcast search.
  - Fix logrotate
  - immediately kick broken daemon connections
* Sat Jul  8 2006 coolo@suse.de
  0.7.4:
  - Add -fpreprocessed argument
  - Fix daemons getting stuck after a while with 100%% CPU
  - fix for kubuntu where libs are deeply nested
    such as /lib/tls/i686/cmov/libc.so.6
  - find the compiler even though icecc wasn't in the path
  - fix deletion of old environments
  - a lot more error handling
  - fix assertion failures in daemon upon sigchild delivery
  - use -fPIC also for C files
  - avoid race between local and remote daemon about who has
    the right exit status
  - rename the package to icecc
* Wed Jun 21 2006 coolo@suse.de
- fix build on 64 bit archs and older kernels
* Tue Jun 20 2006 coolo@suse.de
  0.7.3:
  - more work on error handling
  - corrected icecc --help output
  - handle local icecream load correctly
  - reduce the number of load updates from daemon to scheduler
  - early launch the compiler even before the whole preprocessed
    file has been received
  - handle low-latency networks better
  - builtin colorgcc
  - let the daemon schedule local load even without scheduler (important
    for multi processor machines)
* Mon Jun 12 2006 coolo@suse.de
- fix x86_64 build
* Fri Jun  9 2006 coolo@suse.de
  0.7.2:
  - split out libicecream-devel for the monitor
  - introducing ICECC_PREFERRED_HOST (=mybigfathost) to let
    the scheduler ignore all rules - this is meant to be a
    debugging aid
  - fix network performance between client and local daemon
  - replaced create-env with icecc --build-native (respecting
    the user's $PATH by default)
* Fri Jun  2 2006 mls@suse.de
  0.7.1:
  - Monitor is an extra package now
  - don't make non-existant cross compilers fatal, but just use
    the other environments in ICECC_VERSION
  - always handle aborted syscalls
  - update minilzo
  - never exit() or return from fork()'ed code paths,
* Thu Jun  1 2006 coolo@suse.de
  0.7.0:
  - WARNING: the protocol is not compatible with earlier
  versions, old clients will refuse to connect, so update
  the full farm
  - protocol reworked to no longer require a client->scheduler
  connection (the daemon will proxy it all)
  - all local jobs are now scheduled by the local daemon to
  make sure multiprocessor machines are handling as many jobs
  as they have jobs configured (# processors). They used to
    be "scheduled" by lock file
  - fixed grave bug that removed all daemon environments when
  the cache grew over limit
  - new telnet interface command: internals to output daemon
    states
  - stricter error handling to avoid suprises
  - SIGHUP to daemon and scheduler will reopen the log file
    to allow logrotate
  - a restart of the daemon and scheduler won't flush the log
    file, but append to it
  - create-env will create .tar.gz now - the client allows
    environments to be .tar, .tar.bz2 and .tar.gz
* Fri May 19 2006 coolo@suse.de
- update from SVN to adapt to the new location
- some fixes for catching out of memory situations better
- package man pages
* Fri Mar  3 2006 stbinner@suse.de
- make sure that log file exists and is writeable by icecream user
  (#141534)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 17 2006 coolo@suse.de
- 0.6.3: make sure the daemon does not erase environments too often
  (no client change)
* Fri Jan 13 2006 coolo@suse.de
- update to 0.6.2
* Mon Dec 19 2005 coolo@suse.de
- remove links
* Thu Oct 13 2005 coolo@suse.de
- update tarball to fix with gcc 4.1
* Fri Sep  2 2005 schwab@suse.de
- Require gcc-c++.
* Wed Apr 13 2005 coolo@suse.de
- some changes to the daemon to keep the cache size below 100MB
* Wed Apr 13 2005 coolo@suse.de
- update tarball
* Mon Feb 21 2005 schwab@suse.de
- create-env: try to find generic versions of libraries.  Remove
  LD_ASSUME_KERNEL hack.
* Sat Feb  5 2005 schwab@suse.de
- Don't set LD_ASSUME_KERNEL in BETA.
* Fri Jan 21 2005 coolo@suse.de
- some fixes from CVS
* Mon Jan 17 2005 schwab@suse.de
- create-env: Add specs only if it exists as file.
* Wed Nov 17 2004 coolo@suse.de
- fixing dead loop
* Sun Nov 14 2004 schwab@suse.de
- Don't use icecc during build.
* Tue Nov  2 2004 coolo@suse.de
- ignore duplicated platforms to avoid confusion between native
  compiler and cross compiler
* Wed Oct 13 2004 coolo@suse.de
- several improvements in the communication layer
- the daemon kills compiler jobs when the client exists before
  awaiting the result (gcc4 feature :)
* Tue Sep 28 2004 od@suse.de
- in create-env, use LD_ASSUME_KERNEL=2.4.21 on ppc64
* Fri Sep 10 2004 schwab@suse.de
- Workaround cfg bug in gcc.
* Mon Sep  6 2004 coolo@suse.de
- handle being called without _any_ environment variables correctly
  (blender's use of scons)
* Mon Sep  6 2004 coolo@suse.de
- correctly calculating output filename for -S jobs (grub's configure)
* Sun Sep  5 2004 coolo@suse.de
- several improvements in the network code to make things more
  robust on general network slowness
- speed up configure runs
* Tue Aug 31 2004 coolo@suse.de
- do calculate the load a bit more fair for those machines that got
  other niced jobs
- add time information to the log output
- track a bit more carefully the child pids
* Mon Aug 30 2004 coolo@suse.de
- do not crash when the network goes down (again)
- some cleanup
* Sun Aug 29 2004 coolo@suse.de
- finding quite some scheduler troubles while watching a network
  with half the computers using WLAN (KDE conference)
- run everything the daemon does with client data as specific user
- changed the spec file to create that user and move the cache
  dir to /var/cache/icecream
- more options for the sysconfig
* Wed Aug 18 2004 coolo@suse.de
- avoid crashes when the connection between client and daemon
  goes down (as happend at night)
* Tue Aug 17 2004 coolo@suse.de
- fix handling of unknown paramters (failed/gsl)
* Sun Aug 15 2004 coolo@suse.de
- bugfixes and more flag statistics
* Thu Aug 12 2004 coolo@suse.de
- transfer debug and optimization flags to the scheduler for better
  speed calculation
* Thu Aug 12 2004 coolo@suse.de
- fixing ugly regression in the daemon. Increased protocol version
  to avoid problems with these old daemons
* Wed Aug 11 2004 coolo@suse.de
- Fixing grave performance problem and several scheduler crashes
* Wed Aug  4 2004 coolo@suse.de
- update for new automake, let the daemon set a ulimit for memory usage
* Fri Jul 30 2004 coolo@suse.de
- don't stress the scheduler while compiling jobs three times
- also use icecream for .c files
- fix for the init script
* Tue Jun 29 2004 coolo@suse.de
- fixing bugs reported by prague office and ro
* Fri Jun 11 2004 coolo@suse.de
- major update (including fix for gcc build)
* Tue May 11 2004 coolo@suse.de
- really fixing build with several input files
* Tue May  4 2004 coolo@suse.de
- fix build with several input files (ltp package)
* Mon May  3 2004 coolo@suse.de
- support cross compiling
* Wed Apr 28 2004 coolo@suse.de
- support multiple architectures in the scheduler
* Mon Apr 26 2004 coolo@suse.de
- filter out more errors as info message trying to get binutils's
  testsuite to work
* Sun Apr 25 2004 coolo@suse.de
- adding -frandom-seed to the compilation for the jobs that compile
  thee times on several hosts
* Fri Apr 23 2004 coolo@suse.de
- fixing grave bug in the setup of the protocol version which caused
  lookups
* Thu Apr 22 2004 coolo@suse.de
- several fixes in the transport layer and the client now compiles
  every 5th job three times to test the farm
* Sat Apr 17 2004 coolo@suse.de
- splitting monitor into an extra source to simplify build
  requirements for the client
* Fri Apr 16 2004 coolo@suse.de
- new protocol version for fancier monitors
* Fri Apr 16 2004 coolo@suse.de
- new version with revised monitor and new init script name
* Tue Apr 13 2004 coolo@suse.de
- initial package
