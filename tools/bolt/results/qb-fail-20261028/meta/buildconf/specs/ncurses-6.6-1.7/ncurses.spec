#
# spec file for package ncurses
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

#

Name:           ncurses
VCS:            platform/upstream/ncurses#d630312a2456592fa1c41ff03d06ddf8748c1ccc
#!BuildIgnore: terminfo
BuildRequires:  gcc-c++
BuildRequires:  pkg-config
BuildRequires:  gnutar

%define terminfo() %{_datadir}/%{0}/%{1}
%define tabset()   %{_datadir}/%{0}/%{1}
Version:        6.6
Release:        1.7
Summary:        Terminal control library
License:        MIT
Group:          System/Base
Url:            http://invisible-island.net/ncurses/ncurses.html
Source0:        ncurses-%{version}.tar.gz
Source2:        handle.linux
Source4:        ncurses-rpmlintrc
Source6:        edit.sed
Source7:        baselibs.conf
Source8:        terminfo_mini.src
Source1001: 	ncurses.manifest
%global         _sysconfdir /etc
%global         _miscdir    %{_datadir}/misc
%global         _incdir     %{_includedir}
%global         root        %{_tmppath}/%{name}-%{version}-store

%description
As soon as a text application needs to directly control its output to
the screen (if it wants to place the cursor at location (x,y) then
write text), ncurses is used. The panel and the forms libraries are
included in this package. The ncurses libraries support color, special
characters, forms, and panels.



%package -n ncurses-utils
Summary:        Tools using the new curses libraries
License:        MIT
Group:          System/Base
Provides:       ncurses:%{_bindir}/tput

%description -n ncurses-utils
The ncurses based utilities are as follows:

clear -- emits clear-screen for current terminal

tabs -- set tabs on a terminal

toe   -- table of entries utility

tput  -- shell-script access to terminal capabilities.

tset  -- terminal-initialization utility

reset -- terminal initialization utility

%package -n terminfo-base-full
Summary:        A terminal descriptions database
License:        MIT
Group:          Base/Utilities
Provides:       ncurses:%{_datadir}/tabset
Provides:		terminfo-base
Requires:       coreutils

%description -n terminfo-base-full
This is the terminfo basic database, maintained in the ncurses package.
This database is the official successor to the 4.4BSD termcap file and
contains information about any known terminal. The ncurses library
makes use of this database to use terminals correctly.

%package -n terminfo-base-mini
Summary:        A terminal descriptions database
License:        MIT
Group:          Base/Utilities
Provides:       ncurses:%{_datadir}/tabset
Provides:		terminfo-base
Requires:       coreutils

%description -n terminfo-base-mini
This is the terminfo basic database, maintained in the ncurses package.
This database is the official successor to the 4.4BSD termcap file and
contains information about any known terminal. The ncurses library
makes use of this database to use terminals correctly.

%package -n libncurses
Summary:        Terminal control library
License:        MIT
Group:          System/Libraries
Requires:       libncurses6

%description -n libncurses
The ncurses library is used by many terminal applications for
controlling output to the screen and input from the user.
This package contains the library built with the version 6 ABI.

%package -n libncurses5
Summary:        Terminal control library
License:        MIT
Group:          System/Libraries
Requires:       terminfo-base
Recommends:		terminfo-base-full
Provides:       ncurses = 5.9
Obsoletes:      ncurses < 5.9

%description -n libncurses5
The ncurses library is used by many terminal applications for
controlling output to the screen and input from the user.

This package contains the library built with the version 5 ABI.


%package -n libncurses6
Summary:        Terminal control library
License:        MIT
Group:          System/Libraries
Requires:       terminfo-base
Recommends:		terminfo-base-full
Provides:       ncurses = %{version}
provides:       libncurses = %{version}

%description -n libncurses6
The ncurses library is used by many terminal applications for
controlling output to the screen and input from the user.

This package contains the library built with the version 6 ABI.



%package -n terminfo
Summary:        A terminal descriptions database
License:        Public-Domain
Group:          System/Base
Requires:       terminfo-base = %{version}
Recommends:	terminfo-base-full

%description -n terminfo
This is the terminfo reference database, maintained in the ncurses
package. This database is the official successor to the 4.4BSD termcap
file and contains information about any known terminal. The ncurses
library makes use of this database to use terminals correctly. If you
just use the Linux console, xterm, and VT100, you probably will not
need this database -- a minimal /usr/share/terminfo tree for these
terminals is already included in the terminfo-base package.

%package -n ncurses-devel
Summary:        Development files for the ncurses5 terminal control library
License:        MIT
Group:          Development/Libraries/C and C++
Provides:       ncurses6-devel
Provides:       ncurses:%{_incdir}/ncurses.h
Requires:       ncurses = %{version}-%{release}
Requires:       libncurses6 = %{version}-%{release}
Requires:       ncurses = %{version}-%{release}

%description -n ncurses-devel
This package contains the headers needed to build against
the ncurses library in its ABI version 6 form.

%package -n ncurses5-devel
Summary:        Development files for the ncurses5 terminal control library
License:        MIT
Group:          Development/Libraries/C and C++
Provides:       ncurses:%{_incdir}/ncurses5/ncurses.h
Requires:       libncurses5 = %{version}-%{release}
Requires:       ncurses = %{version}-%{release}
Requires:       ncurses-devel = %{version}-%{release}

%description -n ncurses5-devel
This package contains the headers needed to build against
the ncurses library in its ABI version 5 form.

%prep
%setup -q -n ncurses-%{version}
cp %{SOURCE1001} .
cp %{SOURCE8} ./misc/
rm -vf include/ncurses_dll.h
rm -vf mkdirs.sh
rm -vf tar-copy.sh
rm -vf mk-dlls.sh

%build
    test ! -f /.buildenv || . /.buildenv
    OPATH=$PATH
    FALLBK="xterm,linux,vt100,vt102"
    CFLAGS="$CFLAGS -pipe -D_REENTRANT -fPIC"
    case "$BUILD_BASENAME" in
        debug-*)
            CFLAGS="$CFLAGS -g -DTRACE"
            ;;
    esac
    LDFLAGS="$LDFLAGS -Wl,-O2,-Bsymbolic-functions,--hash-size=8599,--as-needed"
    CXXFLAGS=$CFLAGS
    test -n "$TERM" || export TERM=linux
    export GZIP="-9"
    #
    # Detect 64bit architecures and be sure that we use an
    # unsigned long for chtype to be backward compatible with
    # already existing ncurses applications.  Otherwise we
    # might break existing applications on any update!
    #
    if test $(getconf LONG_BIT) -gt 32 ; then
	WITHCHTYPE="--with-chtype=long"
    else
	WITHCHTYPE=""
	CFLAGS="$CFLAGS $(getconf LFS_CFLAGS)"
    fi
    #
    # Let's care about people which build ncurses on their own
    # system. That is take care that some configure tests might
    # be exploitable below /tmp ... compare with aclocal.m4
    #
    TMPDIR=$(mktemp -d /tmp/ncurses.XXXXXXXX) || exit 1
    trap 'rm -rf ${TMPDIR}' EXIT
    export TMPDIR
    #
    # No --enable-term-driver as this had crashed last time
    # in ncurses/tinfo/lib_setup.c due to the fact that
    # _nc_globals.term_driver was a NULL function pointer as
    # this is for the MinGW port!
    #
    # No --enable-tcap-names because we may have to recompile
    # programs or foreign programs won't work
    #
    # No --enable-safe-sprintf because this seems to
    # crash on some architectures
    #
    # No --enable-xmc-glitch because this seems to break yast2
    # on console/konsole (no magic cookie support on those?)
    #
    # No --enable-hard-tabs for users which have disabled
    # the use of tabs
    #
    touch --reference=README config.sub config.guess
    %configure \
	--without-ada		\
	--without-debug		\
	--without-profile	\
	--without-manpage-tbl	\
	--with-shared		\
	--with-normal		\
	--with-manpage-format=gzip \
	--with-manpage-renames=${PWD}/man/man_db.renames \
	--with-manpage-aliases	\
	--with-ospeed=short	\
	--with-gpm		\
	--with-dlsym		\
	--with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo \
	--with-termlib		\
	--with-ticlib		\
	--with-xterm-kbs=del	\
	--disable-root-environ	\
	--disable-termcap	\
	--disable-overwrite	\
	--disable-rpath		\
	--disable-rpath-hack	\
	--disable-leaks		\
	--disable-xmc-glitch	\
	--enable-symlinks	\
	--enable-big-core	\
	--enable-const		\
	--enable-hashmap	\
	--enable-no-padding	\
	--enable-symlinks	\
	--enable-sigwinch	\
	--enable-colorfgbg	\
	--enable-sp-funcs	\
	--enable-interop	\
	--with-pthread		\
	--enable-reentrant	\
	--enable-ext-mouse	\
	--disable-widec		\
	--enable-ext-colors	\
	--enable-weak-symbols	\
	--enable-wgetch-events	\
	--enable-pthreads-eintr	\
	--enable-string-hacks	\
	--prefix=%{_prefix}	\
	--exec-prefix=%{_prefix}\
	--libdir=%{_libdir}	\
	--datadir=%{_datadir}	\
	--mandir=%{_mandir}	\
	--includedir=%{_incdir}	\
	"${WITHCHTYPE}" 	\
	--disable-tic-depends	\
	--with-cxx-shared	\
	--with-pc-suffix	\
	--enable-pc-files	\
	--without-manpage-renames \
	--with-fallbacks=""	\
	--with-pkg-config-libdir=%{_libdir}/pkgconfig
    sleep 1

    #
    #  The configure line used above.  Note that we override
    #  several options later with other configurations.
    #  It has been verified several times that this works.
    #
    c=$(grep '^ *$ *\./configure' config.log)
    make -C c++ etip.h
    make %{?_smp_mflags}
    #
    # Refresh second install path
    #
    rm -rf %{root}
    mkdir  %{root}

    #
    # This is a hack to be able to boot strap libncurses with
    # our preferred fallback.c.  For this we need the appropiate
    # tools list infocmp(1) and tic(1).  The first step was with
    # an empty fallback.c, now we include the latest terminfo
    # of our preferred fallback terminfo list into the final
    # fallback.c.
    #
    cp -p progs/tic progs/tic.build
    cp -p progs/infocmp progs/infocmp.build
    PATH=$PWD/progs:$OPATH
    LD_LIBRARY_PATH=$PWD/lib
    export LD_LIBRARY_PATH PATH
    _ncurses_saved_pwd=$(pwd)
    cd ncurses/
	TERMINFO=$PWD/tmp
	export TERMINFO
	mkdir -p $TERMINFO
	(cat > ${PWD}/.build_tic)<<-EOF
		export BUILD_TIC=$PWD/../progs/tic.build
		export BUILD_INFOCMP=$PWD/../progs/infocmp.build
	EOF
	. ${PWD}/.build_tic
	$BUILD_TIC -I -r -e $FALLBK ../misc/terminfo.src > terminfo.src
	$BUILD_TIC -o $TERMINFO -s terminfo.src
	sh -e ./tinfo/MKfallback.sh $TERMINFO ../misc/terminfo.src $BUILD_TIC $BUILD_INFOCMP $(echo "$FALLBK" | tr ',' ' ') > fallback.c
	rm -rf $TERMINFO
	unset  TERMINFO
	cp -p fallback.c ../fallback.c.build
    cd "$_ncurses_saved_pwd"
    PATH=$OPATH
    unset LD_LIBRARY_PATH
    #
    # Now rebuild libncurses and do the rest of this job
    #
    find -name fallback.o -print -delete
    cp fallback.c.build ncurses/fallback.c
    make -C c++ etip.h
    make %{?_smp_mflags}
    # must not use %jobs here (would lead to: ln: ncurses.h already exists)
    find man/ -name '*.[1-8]x.*' -print -delete
    make install DESTDIR=%{root} includedir=%{_incdir} includesubdir=/ncurses libdir=%{_libdir}
    ln -sf %{_incdir}/ncurses/curses.h %{root}%{_incdir}
    ln -sf %{_incdir}/ncurses/ncurses.h %{root}%{_incdir}
    ln -sf %{_incdir}/ncurses/term.h %{root}%{_incdir}
    ln -sf %{_incdir}/ncurses/termcap.h %{root}%{_incdir}
    sh %{S:6} --cflags "-D_GNU_SOURCE -I%{_incdir}/ncurses" --libs "-lncurses" --libs "-ltinfo" %{root}%{_bindir}/ncurses6-config
    mkdir pc
    mv -f %{root}%{_libdir}/pkgconfig/*.pc pc/

    make clean
    #
    # Now use --without-pthread to disable pthread support (abi == 5).
    #
        eval ./${c#*./} --with-abi-version=5		\
				    --without-pthread		\
				    --disable-reentrant		\
				    --disable-ext-mouse		\
				    --disable-widec		\
				    --disable-ext-colors	\
				    --disable-overwrite		\
				    --without-progs
    sleep 1
    find -name fallback.o -print -delete
    cp fallback.c.build ncurses/fallback.c

	make -C c++ etip.h
    make %{?_smp_mflags}
    # must not use %jobs here (would lead to: ln: ncurses.h already exists)
    make install.libs install.includes DESTDIR=%{root} includedir=%{_incdir}/ncurses5 includesubdir=/ncurses libdir=%{_libdir}/ncurses5
    ln -sf %{_incdir}/ncurses5/ncurses/curses.h %{root}%{_incdir}/ncurses5/
    ln -sf %{_incdir}/ncurses5/ncurses/ncurses.h %{root}%{_incdir}/ncurses5/
    ln -sf %{_incdir}/ncurses5/ncurses/term.h %{root}%{_incdir}/ncurses5/
    sh %{S:6} --cflags "-D_GNU_SOURCE -I%{_incdir}/ncurses5/ncurses -I%{_incdir}/ncurses5" --libs "-L%{_libdir}/ncurses5 -lncurses" --libs "-ltinfo" %{root}%{_bindir}/ncurses5-config
    _ncurses_saved_pwd=$(pwd)
    cd man
	sh ../edit_man.sh normal installing %{root}%{_mandir} . ncurses5-config.1
    cd "$_ncurses_saved_pwd"
    for pc in %{root}%{_libdir}/pkgconfig/*.pc
    do
	test -e "$pc" || break
	base=${pc%%.pc}
	base=${base##*/}
	case "$base" in
	ncurses) sed -ri 's@^(Requires.private: ).*@\1@' "$pc" ;;
	tic) sed -ri 's@^(Requires.private: ).*@\1tinfo5@'   "$pc" ;;
	*)   sed -ri 's@^(Requires.private: ).*@\1ncurses5@' "$pc"
	esac
	sed -ri 's@^(libdir=).*@\1%{_libdir}/ncurses5@
		s@^(includedir=).*@\1%{_incdir}/ncurses5@' "$pc"
	mv -f $pc pc/${base}5.pc
    done

    #
    # Now use --enable-widec for UTF8/wide character support.
    # The libs with 16 bit wide characters are binary incompatible
    # to the normal 8bit wide character libs.
    #
    make clean

    eval ./${c#*./} --with-pthread			\
				    --enable-reentrant		\
				    --enable-ext-mouse		\
				    --enable-widec		\
				    --enable-ext-colors		\
				    --disable-overwrite		\
				    --without-progs
    sleep 1

	find -name fallback.o -print -delete
    cp fallback.c.build ncurses/fallback.c
    make -C c++ etip.h
    make %{?_smp_mflags}
    # must not use %jobs here (would lead to: ln: ncurses.h already exists)
    make install.libs install.includes DESTDIR=%{root} includedir=%{_incdir} includesubdir=/ncursesw libdir=%{_libdir}
    sh %{S:6} --cflags "-D_GNU_SOURCE -I%{_incdir}/ncursesw" --libs "-lncursesw" --libs "-ltinfow" %{root}%{_bindir}/ncursesw6-config
    _ncurses_saved_pwd=$(pwd)
    cd man
	sh ../edit_man.sh normal installing %{root}%{_mandir} . ncursesw6-config.1
    cd "$_ncurses_saved_pwd"
    mv -f %{root}%{_libdir}/pkgconfig/*.pc pc/
    make clean
    #
    # ABI == 5
    #

    #
    # Now use --without-pthread to disable pthread support (abi == 5).
    #
    eval ./${c#*./} --with-abi-version=5		\
				    --without-pthread		\
				    --disable-reentrant		\
				    --disable-ext-mouse		\
				    --enable-widec		\
				    --disable-ext-colors	\
				    --disable-overwrite		\
				    --without-progs
    sleep 1


    find -name fallback.o -print -delete
    cp fallback.c.build ncurses/fallback.c

    make -C c++ etip.h
    make %{?_smp_mflags}
    # must not use %jobs here (would lead to: ln: ncurses.h already exists)
    make install.libs install.includes DESTDIR=%{root} includedir=%{_incdir}/ncurses5 includesubdir=/ncursesw libdir=%{_libdir}/ncurses5
    sh %{S:6} --cflags "-D_GNU_SOURCE -I%{_incdir}/ncurses5/ncursesw -I%{_incdir}/ncurses5" --libs "-L%{_libdir}/ncurses5 -lncursesw" --libs "-ltinfow" %{root}%{_bindir}/ncursesw5-config
    _ncurses_saved_pwd=$(pwd)
    cd man
	sh ../edit_man.sh normal installing %{root}%{_mandir} . ncursesw5-config.1
    cd "$_ncurses_saved_pwd"
    for pc in %{root}%{_libdir}/pkgconfig/*.pc
    do
	test -e "$pc" || break
	base=${pc%%.pc}
	base=${base##*/}
	case "$base" in
	ncursesw) sed -ri 's@^(Requires.private: ).*@\1@' "$pc" ;;
	ticw)     sed -ri 's@^(Requires.private: ).*@\1tinfow5@'   "$pc" ;;
	*)        sed -ri 's@^(Requires.private: ).*@\1ncursesw5@' "$pc"
	esac
	sed -ri 's@^(libdir=).*@\1%{_libdir}/ncurses5@
		s@^(includedir=).*@\1%{_incdir}/ncurses5@' "$pc"
	mv -f $pc pc/${base}5.pc
    done

%install
    PATH=$PWD/gzip:$PATH
    (cd %{root}/; /usr/bin/gnutar -cpSf - *)|/usr/bin/gnutar -xpsSf - -C %{buildroot}/
    rm -rf %{root}
#    mkdir %{buildroot}/%{_lib}
#    for model in libncurses libncursest libncursesw libncursestw libtinfo libtinfow libtic libticw
#    do
#	for lib in %{buildroot}%{_libdir}/${model}.so.* ; do
#	    test   -e "${lib}" || continue
#	    mv "${lib}" %{buildroot}/%{_lib}/ || continue
#	done
#	for lib in %{buildroot}/%{_lib}/${model}.so.6 ; do
#	    test -e "${lib}" || continue
#	    test -L "${lib}" || continue
#	    lib=${lib#%{buildroot}}
#	    lnk=%{buildroot}%{_libdir}/${model}.so
#	    case "${lib##*/}" in
#	    libncursesw*)
#		rm -f ${lnk}
#		echo '/* GNU ld script */'			>  ${lnk}
#		echo "INPUT(${lib} AS_NEEDED(-ltinfow -ldl))"	>> ${lnk}
#		;;
#	    libncurses*)
#		rm -f ${lnk}
#		echo '/* GNU ld script */'			>  ${lnk}
#		echo "INPUT(${lib} AS_NEEDED(-ltinfo -ldl))"	>> ${lnk}
#		;;
#	    *)	ln -sf ${lib} %{buildroot}%{_libdir}/${model}.so
#	    esac
#	done
#    done
#    chmod 0755 %{buildroot}/%{_lib}/lib*.so.*
    chmod 0755 %{buildroot}/%{_libdir}/lib*.so.*
    chmod a-x  %{buildroot}/%{_libdir}/lib*.a
    if test -d %{buildroot}%{_libdir}/ncurses5 ; then
	mv %{buildroot}%{_libdir}/ncurses5/*.so.5*   %{buildroot}%{_libdir}/
	for lib in %{buildroot}%{_libdir}/ncurses5/*.so
	do
	    lnk=$lib
	    lib=%{_libdir}/${lib##*/}.5
	    case "${lib##*/}" in
	    libncursesw*)
		rm -f "${lnk}"
		echo '/* GNU ld script */'		>  ${lnk}
		echo "INPUT(${lib} AS_NEEDED(-ltinfow))">> ${lnk}
		;;
	    libncurses*)
		rm -f "${lnk}"
		echo '/* GNU ld script */'		>  ${lnk}
		echo "INPUT(${lib} AS_NEEDED(-ltinfo))"	>> ${lnk}
		;;
#	    libtinfo*)
#		test -L "${lnk}" || continue
#		ln -sf ${lib} ${lnk}
#		;;
	    *)
		test -L "${lnk}" || continue
		ln -sf ../${lib##*/} ${lnk}
	    esac
	done
#	for model in libncurses libncursest libncursesw libncursestw libtinfo libtinfow libtic libticw
#	do
#	    for lib in %{buildroot}%{_libdir}/${model}.so.* ; do
#		test   -e "${lib}" || continue
#		mv "${lib}" %{buildroot}/%{_lib}/ || continue
#	    done
#	    for lib in %{buildroot}/%{_lib}/${model}.so.5 ; do
#		test -e "${lib}" || continue
#		test -L "${lib}" || continue
#		lib=${lib#%{buildroot}}
#		lnk=%{buildroot}%{_libdir}/ncurses5/${model}.so
#		case "${lib##*/}" in
#		libncursesw*)
#		    rm -f ${lnk}
#		    echo '/* GNU ld script */'		    >  ${lnk}
#		    echo 'SEARCH_DIR(%{_libdir}/ncurses5)'  >> ${lnk}
#		    echo "INPUT(${lib} AS_NEEDED(-ltinfow))">> ${lnk}
#		    ;;
#		libncurses*)
#		    rm -f ${lnk}
#		    echo '/* GNU ld script */'		    >  ${lnk}
#		    echo 'SEARCH_DIR(%{_libdir}/ncurses5)'  >> ${lnk}
#		    echo "INPUT(${lib} AS_NEEDED(-ltinfo))" >> ${lnk}
#		    ;;
#		*)  ln -sf ${lib} %{buildroot}%{_libdir}/ncurses5/${model}.so
#	    esac
#	    done
#	done
#	chmod 0755 %{buildroot}/%{_lib}/lib*.so.5*
	chmod 0755 %{buildroot}/%{_libdir}/lib*.so.5*
	chmod 0755 %{buildroot}/%{_libdir}/ncurses5/lib*.so*
	chmod a-x  %{buildroot}/%{_libdir}/ncurses5/lib*.a
    fi
    test -n "%{buildroot}" || ldconfig -N
    mkdir -p %{buildroot}%{_defaultdocdir}/ncurses
    bzip2 -c misc/terminfo.src > misc/terminfo.src.bz2
    install -m 644 misc/terminfo.src.bz2	%{buildroot}%{_defaultdocdir}/ncurses/
    install -m 644 doc/html/*.html		%{buildroot}%{_defaultdocdir}/ncurses/
    bzip2 doc/ncurses-intro.doc -c > doc/ncurses-intro.txt.bz2
    install -m 644 doc/ncurses-intro.txt.bz2	%{buildroot}%{_defaultdocdir}/ncurses/
    bzip2 doc/hackguide.doc -c > doc/hackguide.txt.bz2
    install -m 644 doc/hackguide.txt.bz2	%{buildroot}%{_defaultdocdir}/ncurses/
    install -m 644 README			%{buildroot}%{_defaultdocdir}/ncurses/
    install -m 644 NEWS				%{buildroot}%{_defaultdocdir}/ncurses/
    mkdir -p %{buildroot}%{_sysconfdir}/terminfo
    mkdir -p %{buildroot}%{_miscdir}
    LD_LIBRARY_PATH=%{buildroot}%{_libdir}
    export LD_LIBRARY_PATH
    _ncurses_saved_pwd=$(pwd)
    cd ncurses/
	. ${PWD}/.build_tic

	# termcap.mini
	$BUILD_TIC -C -r ../misc/terminfo_mini.src | grep -E -v '^#' | tee termcap
	# Gererate new termcap entries for various linux consoles
	TERMCAP=termcap \
	TERMINFO=%{buildroot}%{_datadir}/terminfo \
	    bash %{SOURCE2}
	install -m 0644 termcap.new %{buildroot}%{_miscdir}/termcap.mini

	# termcap.full
	$BUILD_TIC -C -r ../misc/terminfo.src | grep -E -v '^#' | tee termcap
	# Gererate new termcap entries for various linux consoles
	TERMCAP=termcap \
	TERMINFO=%{buildroot}%{_datadir}/terminfo \
	    bash %{SOURCE2}
	sed '/^$/d' -i termcap.new
	install -m 0644 termcap.new %{buildroot}%{_miscdir}/termcap.full

    cd "$_ncurses_saved_pwd"
    unset LD_LIBRARY_PATH
    if test `%{_bindir}/id -u` = '0' ; then
	chown root:root %{buildroot}%{_miscdir}/termcap.full
	chmod 0644      %{buildroot}%{_miscdir}/termcap.full

	chown root:root %{buildroot}%{_miscdir}/termcap.mini
	chmod 0644      %{buildroot}%{_miscdir}/termcap.mini
    fi

    ln -sf %{_miscdir}/termcap %{buildroot}%{_sysconfdir}/termcap

    (cat > default_mini.list) <<-EOF
	%{tabset std}
	%{tabset stdcrt}
	%{tabset vt100}
	%{tabset vt300}
	%{terminfo d/dumb}
	%{terminfo l/linux}
	%{terminfo v/vt100}
	%{terminfo v/vt102}
	%{terminfo x/xterm}
	EOF
	find %{buildroot}%{tabset ""} %{buildroot}%{terminfo ""} \
	\( -type f -or -type l \) | \
	sed "s@^%{buildroot}@@g" | \
	grep -v -F -x -f default_mini.list \
	> extension_mini.list

    (cat > default.list) <<-EOF
	%{tabset std}
	%{tabset stdcrt}
	%{tabset vt100}
	%{tabset vt300}
	%{terminfo a/ansi}
	%{terminfo d/dumb}
	%{terminfo g/gnome}
	%{terminfo g/gnome-rh72}
	%{terminfo g/gnome-rh80}
	%{terminfo g/gnome-rh90}
	%{terminfo g/gnome-fc5}
	%{terminfo i/ibm327x}
	%{terminfo k/klone+color}
	%{terminfo k/konsole}
	%{terminfo k/konsole-256color}
	%{terminfo k/kvt}
	%{terminfo l/linux}
	%{terminfo l/linux-m}
	%{terminfo l/linux-nic}
	%{terminfo m/mlterm}
	%{terminfo n/nxterm}
	%{terminfo r/rxvt}
	%{terminfo r/rxvt-basic}
	%{terminfo r/rxvt-color}
	%{terminfo r/rxvt-256color}
	%{terminfo s/screen+fkeys}
	%{terminfo s/screen}
	%{terminfo s/screen-16color}
	%{terminfo s/screen-256color}
	%{terminfo s/screen-bce}
	%{terminfo s/screen-w}
	%{terminfo s/sun}
	%{terminfo u/unknown}
	%{terminfo v/vt100}
	%{terminfo v/vt102}
	%{terminfo v/vt220}
	%{terminfo v/vt220-8}
	%{terminfo v/vt220-8bit}
	%{terminfo v/vt320}
	%{terminfo v/vt52}
	%{terminfo v/vte}
	%{terminfo x/xterm}
	%{terminfo x/xterm-color}
	%{terminfo x/xterm-256color}
	%{terminfo x/xterm-basic}
	%{terminfo x/xterm-nic}
	%{terminfo x/xterm-r6}
	EOF
    find %{buildroot}%{tabset ""} %{buildroot}%{terminfo ""} \
	\( -type f -or -type l \) | \
	sed "s@^%{buildroot}@@g" | \
	grep -v -F -x -f default.list \
	> extension.list
    rm -f %{buildroot}%{_prefix}/lib/terminfo
    mv pc/*.pc %{buildroot}%{_libdir}/pkgconfig/
%remove_docs

%post   -n libncurses5 -p /sbin/ldconfig

%postun -n libncurses5 -p /sbin/ldconfig

%post   -n libncurses6 -p /sbin/ldconfig

%postun -n libncurses6 -p /sbin/ldconfig

%post   -n terminfo-base-mini
ln -sf %{_miscdir}/termcap.mini %{_miscdir}/termcap

%post   -n terminfo-base-full
ln -sf %{_miscdir}/termcap.full %{_miscdir}/termcap

%files -n terminfo-base-mini -f default_mini.list
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright
%{_sysconfdir}/termcap
%config %{_miscdir}/termcap.mini
%dir %{_datadir}/tabset/
/usr/share/terminfo/d/dumb
/usr/share/terminfo/l/linux
/usr/share/terminfo/v/vt100
/usr/share/terminfo/v/vt102
/usr/share/terminfo/x/xterm

%files -n terminfo-base-full -f default.list
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright
%{_sysconfdir}/termcap
%config %{_miscdir}/termcap.full
%dir %{_datadir}/tabset/
%dir %{_datadir}/terminfo/
%dir %{_datadir}/terminfo/*/

%files -n ncurses-utils
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright
%{_bindir}/clear
%{_bindir}/reset
%{_bindir}/tabs
%{_bindir}/toe
%{_bindir}/tput
%{_bindir}/tset

%files -n libncurses
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright

%files -n libncurses5
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright
%{_libdir}/lib*.so.5*

%files -n libncurses6
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright
%{_libdir}/lib*.so.6*

%files -n ncurses-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright
## ncurses 5
%{_bindir}/ncurses*5-config
%dir %{_incdir}/ncurses5/ncurses/
%dir %{_incdir}/ncurses5/ncursesw/
%{_incdir}/ncurses5/*.h
%{_incdir}/ncurses5/ncurses/*.h
%{_incdir}/ncurses5/ncursesw/*.h
%dir %{_libdir}/ncurses5/
%{_libdir}/ncurses5/lib*.a
%{_libdir}/ncurses5/lib*.so
%{_libdir}/pkgconfig/*5.pc

## ncurses 6
%{_bindir}/ncurses*6-config
%{_bindir}/captoinfo
%{_bindir}/infotocap
%{_bindir}/infocmp
%{_bindir}/tic
%dir %{_incdir}/ncurses/
%dir %{_incdir}/ncursesw/
%{_incdir}/*.h
%{_incdir}/ncurses/*.h
%{_incdir}/ncursesw/*.h
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*[clmosuw\+].pc

%files -n ncurses5-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright
%{_bindir}/ncurses*5-config
%dir %{_incdir}/ncurses5/
%dir %{_incdir}/ncurses5/ncurses/
%dir %{_incdir}/ncurses5/ncursesw/
%{_incdir}/ncurses5/*.h
%{_incdir}/ncurses5/ncurses/*.h
%{_incdir}/ncurses5/ncursesw/*.h
%dir %{_libdir}/ncurses5/
%{_libdir}/ncurses5/lib*.a
%{_libdir}/ncurses5/lib*.so
%{_libdir}/pkgconfig/*5.pc


%files -f extension.list -n terminfo
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING package/debian/copyright
%changelog
* Tue Feb 11 2014 Patrick McCarty <patrick.mccarty@linux.intel.com> 86dca7a
- Fix ncurses build with tar 1.27: the -s option (equivalent to --same-order)
  can no longer be used with the -c option.
* Mon Sep 16 2013 Anas Nashif <anas.nashif@intel.com> accepted/tizen/20130912.195247@fc238d7
- remove remaining undefined macro for abi
* Tue Sep 10 2013 Jacek Bukarewicz <j.bukarewicz@samsung.com> submit/tizen/20130719.024302@c4b2a54
- Moved documentation to a separate package
* Fri Jun 14 2013 Anas Nashif <anas.nashif@intel.com> submit/tizen/20130509.182512@cb86ca0
- Install pc files and move everything to /usr/lib
* Fri Mar 22 2013 Anas Nashif <anas.nashif@intel.com> submit/trunk/20130207.035821@9e28094
- Fixed package groups
* Fri Feb 22 2013 Patrick McCarty <patrick.mccarty@linux.intel.com> aaeb115
- Fix package name in baselibs.conf
* Wed Feb  6 2013 Anas Nashif <anas.nashif@intel.com> upstream/5.9@ba2924c
- Update patches and package from git
