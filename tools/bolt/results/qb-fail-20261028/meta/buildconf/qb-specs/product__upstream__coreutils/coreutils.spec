%define _unpackaged_files_terminate_build 0

%define run_tests 0
%if %{run_tests}
    # check is defined off at .rpmmacros file.
    %undefine check
%endif

Summary: 	Core utilities complementing toybox
Name:		coreutils
Version:	6.9
Release:	16
License:	GPL-2.0-or-later
Group:		System Environment/Base
Url:		http://www.gnu.org/software/coreutils/
Source0:	coreutils-%{version}.tar.bz2
Source1001:	%{name}.manifest

BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1.10
BuildRequires:	gettext findutils

Requires:	toybox >= 0.8.14
Provides:	/bin/basename /bin/cat /bin/chmod /bin/chown /bin/cp /bin/env /bin/ln
Provides:	/bin/ls /bin/mkdir /bin/mv /bin/pwd /bin/rm /bin/sort /bin/touch
Provides:	mktemp
Obsoletes:	coreutils-su < 7

%description
The standard command names (cp, ls, cat, ...) are provided by toybox;
this package is installed alongside toybox and carries only the GNU
coreutils commands that toybox does not implement: dir dircolors join
pathchk pinky pr ptx sum unexpand users vdir. This source package also
ships the complete GNU implementations under the gnu_ name prefix
(coreutils-gnu subpackage) for build environments that need GNU behavior.

%package -n coreutils-gnu
Summary:        GNU core utilities installed as gnu_* (build environment only)
Group:          System Environment/Base

%description -n coreutils-gnu
GNU coreutils binaries renamed with the gnu_ prefix (/usr/bin/gnu_cp,
/usr/bin/gnu_ls, ...).  Unprefixed names are available under
%{_libdir}/coreutils-gnu/bin so a package that needs GNU behavior can
opt in with a single line:
  export PATH=%{_libdir}/coreutils-gnu/bin:$PATH

%prep
%setup -q

%build
cp %{SOURCE1001} .

export CFLAGS="${CFLAGS} -fPIC -fvisibility=hidden -flto"
export LDFLAGS="${LDFLAGS} -Wl,-z,relro -pie -fvisibility=hidden -flto"

%configure --program-prefix=gnu_
# doc/ only regenerates texinfo files this package never ships (docs are
# stripped post-install below); skip the subdir so its stamp-vti/version.texi
# rule can't fire, and close stdin so any cp/mv "overwrite read-only file?"
# prompt fails fast instead of blocking the build on a tty read.
make SUBDIRS="lib src man po tests" < /dev/null

%check
%if %{run_tests}
    %__make check || exit 0
    chmod 755 ./run_test.sh
    ./run_test.sh %{name} %{version}
%endif

%install
make SUBDIRS="lib src man po tests" install DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p" < /dev/null

# su needs setuid to work; Tizen uses util-linux-su instead
rm -f %{buildroot}%{_bindir}/gnu_su

# Use hard links instead of symbolic links for LC_TIME files (bug #246729).
find %{buildroot}%{_datadir}/locale -type l | \
(while read link
 do
   target=$(readlink "$link")
   rm -f "$link"
   ln "$(dirname "$link")/$target" "$link"
 done)

# PATH shim: unprefixed GNU names, opt-in via PATH
mkdir -p %{buildroot}%{_libdir}/coreutils-gnu/bin
for f in %{buildroot}%{_bindir}/gnu_*; do
    c=$(basename "$f" | sed 's/^gnu_//')
    ln -s %{_bindir}/gnu_$c %{buildroot}%{_libdir}/coreutils-gnu/bin/$c
done

# standard names for commands toybox does not implement, shipped in the
# main package as real binaries so they never depend on coreutils-gnu
for c in dir dircolors join pathchk pinky pr ptx sum unexpand users vdir; do
    cp -p %{buildroot}%{_bindir}/gnu_$c %{buildroot}%{_bindir}/$c
done

%clean
rm -rf $RPM_BUILD_ROOT

%{remove_docs}

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/dir
%{_bindir}/dircolors
%{_bindir}/join
%{_bindir}/pathchk
%{_bindir}/pinky
%{_bindir}/pr
%{_bindir}/ptx
%{_bindir}/sum
%{_bindir}/unexpand
%{_bindir}/users
%{_bindir}/vdir

%files -n coreutils-gnu
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/gnu_*
%dir %{_libdir}/coreutils-gnu
%dir %{_libdir}/coreutils-gnu/bin
%{_libdir}/coreutils-gnu/bin/*
