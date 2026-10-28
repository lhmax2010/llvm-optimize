Name:           perl
VCS:            platform/upstream/perl#f75e09484fdb3978a627c923d752ad442351610b
Summary:        The Perl interpreter
License:        Artistic-1.0 or GPL-2.0-or-later
Group:          Platform Development/Perl
Version:        5.42.0
Release:        1.12
Url:            http://www.perl.org/

Source0:        perl-%{version}.tar.bz2
Source1:        %name-rpmlintrc
Source2:        macros.perl
Source3:        README.macros
Source4:        baselibs.conf
Source10:       add_pie_compile_option.patch
Source1001:     perl.manifest

BuildRequires:  gdbm-devel
BuildRequires:  bzip2-devel
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel

%define debug_package %{nil}
%define __debug_package %{nil}
%define __debug_install_post %{nil}

Provides:       /bin/perl
Provides:       perl-500
Provides:       perl-macros
Provides:       perl(:MODULE_COMPAT_%{version})
Obsoletes:      perl-macros
Provides:       perl-base
Obsoletes:      perl-base
Provides:       perl-Filter-Simple
Provides:       perl-I18N-LangTags
Provides:       perl-MIME-Base64
Provides:       perl-Storable
Provides:       perl-Test-Simple = 0.98-%{release}
Obsoletes:      perl-Filter-Simple
Obsoletes:      perl-I18N-LangTags
Obsoletes:      perl-MIME-Base64
Obsoletes:      perl-Storable
Obsoletes:      perl-Test-Simple < 0.98
Provides:       perl-Text-Balanced
Provides:       perl-Time-HiRes
Provides:       perl-libnet
Obsoletes:      perl-Text-Balanced
Obsoletes:      perl-Time-HiRes
Obsoletes:      perl-libnet
Provides:       perl-Compress-Raw-Zlib
Provides:       perl-Compress-Zlib
Obsoletes:      perl-Compress-Raw-Zlib
Obsoletes:      perl-Compress-Zlib
Provides:       perl-IO-Compress-Base
Provides:       perl-IO-Compress-Zlib
Provides:       perl-IO-Zlib
Obsoletes:      perl-IO-Compress-Base
Obsoletes:      perl-IO-Compress-Zlib
Obsoletes:      perl-IO-Zlib
Provides:       perl-Archive-Tar
Provides:       perl-Module-Build
Obsoletes:      perl-Archive-Tar
Provides:       perl-Locale-Maketext-Simple
Provides:       perl-Module-Pluggable
Obsoletes:      perl-Locale-Maketext-Simple
Obsoletes:      perl-Module-Pluggable
Provides:       perl-Pod-Escapes
Provides:       perl-Pod-Simple
Obsoletes:      perl-Pod-Escapes
Obsoletes:      perl-Pod-Simple
Provides:       perl-ExtUtils-ParseXS
Provides:       perl-version
Obsoletes:      perl-ExtUtils-ParseXS
Obsoletes:      perl-version

%description
perl - Practical Extraction and Report Language
Perl is optimized for scanning arbitrary text files, extracting
information from those text files, and printing reports based on that
information.  It is also good for many system management tasks. Perl is
intended to be practical (easy to use, efficient, and complete) rather
than beautiful (tiny, elegant, and minimal).
Some of the modules available on CPAN can be found in the "perl"
series.

%package doc
Summary:        Perl Documentation
Requires:       perl = %{version}
Provides:       perl:%{_mandir}/man3/CORE.3pm.gz

%description doc
Perl man pages and pod files.

%prep
%setup -q -n perl-%{version}
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE10}
cp -p %{S:3} .

%build
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -e "s/--param=ssp-buffer-size=4//g" )

%if "%{asan}" == "1"
export LD_PRELOAD="$LD_PRELOAD libasan.so"
%endif

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wall -pipe"

cp -a lib savelib
export LD_AS_NEEDED=0
export BZIP2_LIB=%{_libdir}
export BZIP2_INCLUDE=%{_includedir}
export BUILD_BZIP2=0
export ldflags="$ldflags -lpthread"

# always use glibc's setenv
options="-Accflags='-DPERL_USE_SAFE_PUTENV'"
options="$options -Dotherlibdirs=%{_libdir}/perl5/site_perl"
sed -e 's|/lib/|/%{_lib}/|g' -i Configure
sed -e 's| lib/| %{_lib}/|g' -i Configure
chmod 755 ./configure.gnu

./configure.gnu -Dprefix=%{_prefix} \
                -Dvendorprefix=%{_prefix} \
                -Dman1dir=%{_mandir}/man1 \
                -Dman3dir=%{_mandir}/man3 \
                -Dinstallusrbinperl \
                -Dusethreads  \
                -Duseshrplib=\'true\' \
                -Doptimize="$RPM_OPT_FLAGS" $options

%__make %{?_smp_mflags}

cp -p libperl.so savelibperl.so
cp -p lib/Config.pm saveConfig.pm
cp -p lib/Config_heavy.pl saveConfig_heavy.pl
#%__make clean > /dev/null
%__make clobber

rm -rf lib
mv savelib lib

./configure.gnu -Dprefix=%{_prefix} \
                -Dvendorprefix=%{_prefix} \
                -Dman1dir=%{_mandir}/man1 \
                -Dman3dir=%{_mandir}/man3 \
                -Dinstallusrbinperl \
                -Dusethreads  \
                $options
%__make %{?_smp_mflags}

%install
%make_install
cp -a %{buildroot}%{_libdir}/perl5/site_perl %{buildroot}%{_libdir}/perl5/vendor_perl
cpa=`echo %{buildroot}%{_libdir}/perl5/*/*/CORE | sed -e 's@/CORE$@@'`
cp=`echo "$cpa" | sed -e 's@/[^/]*$@@'`
vpa=`echo $cpa | sed -e 's@/perl5/@/perl5/vendor_perl/@'`
vp=`echo "$vpa" | sed -e 's@/[^/]*$@@'`
install -d $vp/auto
install -d $vpa/auto
install -m 555 savelibperl.so $cpa/CORE/libperl.so
install -m 444 saveConfig.pm $cpa/Config.pm
install -m 444 saveConfig_heavy.pl $cpa/Config_heavy.pl

# install macros.perl file
install -D -m 644 %{S:2} %{buildroot}%{_sysconfdir}/rpm/macros.perl
(cd %{_includedir} &&
(rpm -ql glibc-devel | fgrep '.h'
    find %{_includedir}/asm/ -name \\*.h
    find %{_includedir}/asm-generic -name \\*.h
    find %{_includedir}/linux -name \\*.h
) | while read f; do
    %{buildroot}%{_bindir}/perl -I$cp -I$cpa %{buildroot}%{_bindir}/h2ph -d $vpa $(echo ${f} | sed 's/\/usr\/include\///g') || :
done
 )
d="`gcc -print-file-name=include`"
test -f "$d/stdarg.h" && (cd $d ; %{buildroot}%{_bindir}/perl -I$cp -I$cpa %{buildroot}%{_bindir}/h2ph -d $vpa stdarg.h stddef.h float.h)
# remove broken pm - we don't have the module
rm %{buildroot}%{_libdir}/perl5/*/Pod/Perldoc/ToTk.pm
# we don't need this in here
#rm %%{buildroot}%%{_libdir}/perl5/*/*/CORE/libperl.a
#touch %%{buildroot}%%{_mandir}/man3/perllocal.3pm
#touch $cpa/perllocal.pod
# test CVE-2007-5116
%{buildroot}%{_bindir}/perl -e '$r=chr(128)."\\x{100}";/$r/'
# test perl-regexp-refoverflow.diff
%{buildroot}%{_bindir}/perl -e '/\\6666666666/'

%{remove_docs}

%check
#rm -f /tmp/%{name}_test
#chmod +x ./run_test.sh
#sh -c "%{__make} check || exit 0"
#./run_test.sh %{name} %{version}

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license README
%dir %{_libdir}/perl5/%{version}/B
%dir %{_libdir}/perl5/%{version}/*-linux-thread-multi*/auto/POSIX
%config %{_sysconfdir}/rpm/macros.perl
%{_libdir}/perl5/*
%{_bindir}/*

