###############################################################################
# if you build icu date files,
# please remove file source/data/in/icudt60l.dat file
###############################################################################

%define tzdata_version 2025b

Name:      icu
VCS:       platform/upstream/icu#e4a4d7411b0f288581cf020a176b5dddbb504ae7
Version:   78.1
Release:   1.4
Summary:   International Components for Unicode
Group:     System/Libraries
License:   ICU and Unicode-TOU and BSD-2.0
URL:       http://www.icu-project.org/
Source0:   %{name}-%{version}.tar.gz
Source1:   tzdata%{tzdata_version}.tar.gz
Source2:   set_disable_renameing.patch
Source3:   Disable-the-default-LDFLAGSICUDT.patch
Source4:   Add_PIE_option_for_tzcode.patch
Source5:   Set_define_false_and_true.patch
Source6:   Change_localtime_path.patch
Source7:   Set_icu_timezone_files_dir.patch
Source1001: icu.manifest

BuildRequires: autoconf
BuildRequires: pkgconfig(python3)

%description
Tools and utilities for developing with icu.

%package -n libicu
Summary: International Components for Unicode - libraries

%description -n libicu
The International Components for Unicode (ICU) libraries provide
robust and full-featured Unicode services on a wide variety of
platforms. ICU supports the most current version of the Unicode
standard, and they provide support for supplementary Unicode
characters (needed for GB 18030 repertoire support).
As computing environments become more heterogeneous, software
portability becomes more important. ICU lets you produce the same
results across all the various platforms you support, without
sacrificing performance. It offers great flexibility to extend and
customize the supplied services.

%package  -n libicu-devel
Summary:  Development files for International Components for Unicode
Requires: libicu = %{version}-%{release}
Requires: pkgconfig

%description -n libicu-devel
Includes and definitions for developing with icu.

%package  -n libicu-tzdata
Summary:  package for ICU TimeZone Updating
Requires: libicu = %{version}-%{release}
Requires: pkgconfig

%description -n libicu-tzdata
Initial setup for ICU timezone .res file

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE2}
%{__patch} -p1 < %{SOURCE3}
%{__patch} -p1 < %{SOURCE4}
%{__patch} -p1 < %{SOURCE5}
%{__patch} -p1 < %{SOURCE6}
%{__patch} -p1 < %{SOURCE7}

cp %{SOURCE1} ./source/tools/tzcode

%build
export CFLAGS="$CFLAGS -D_TIZEN_FEATURE_ -fPIC"
export CXXFLAGS="$CXXFLAGS -D_TIZEN_FEATURE_ -fPIC"
export LINKFLAGS=" -pie"
export LANG=C.UTF-8

cd source
%{configure} --enable-static=no \
            --enable-renaming=no \
            --enable-shared \
            --enable-plugins=yes \
            --enable-samples=no \
%ifarch armv7hl
            --with-data-packaging=archive
%else
            --with-data-packaging=library
%endif
%{__make} %{?_smp_mflags}

%check
#    pushd source
#    %__make check || exit 0
#    popd

%install
cd source
%make_install

# bugs of rpmdeps
chmod +x %{buildroot}/%{_libdir}/lib*.so.*
mkdir -p %{buildroot}/opt/share/icu_tzdata/
mkdir -p %{buildroot}/usr/share/icu_zoneinfo/
export ICUDATA_NAME=`cat ./data/makedata.mak  | grep "^U_ICUDATA_NAME=" | head -n 1 | sed -e 's/^.*=//g' | sed -e 's/\r$//g'`
export ICUDATA_ENDIAN_SUFFIX=`cat ./data/makedata.mak  | grep "^U_ICUDATA_ENDIAN_SUFFIX=" | head -n 1 | sed -e 's/^.*=//g' | sed -e 's/\r$//g'`
echo "============================================="
echo "ICUDATA_NAME [$ICUDATA_NAME]"
echo "ICUDATA_ENDIAN_SUFFIX [$ICUDATA_ENDIAN_SUFFIX]"
echo "============================================="
cp -af ./data/out/build/"$ICUDATA_NAME$ICUDATA_ENDIAN_SUFFIX"/zoneinfo64.res %{buildroot}/usr/share/icu_zoneinfo/
cp -af ./data/out/build/"$ICUDATA_NAME$ICUDATA_ENDIAN_SUFFIX"/metaZones.res %{buildroot}/usr/share/icu_zoneinfo/
cp -af ./data/out/build/"$ICUDATA_NAME$ICUDATA_ENDIAN_SUFFIX"/timezoneTypes.res %{buildroot}/usr/share/icu_zoneinfo/
ln -sf /usr/share/icu_zoneinfo/zoneinfo64.res %{buildroot}/opt/share/icu_tzdata/zoneinfo64.res
ln -sf /usr/share/icu_zoneinfo/metaZones.res %{buildroot}/opt/share/icu_tzdata/metaZones.res
ln -sf /usr/share/icu_zoneinfo/timezoneTypes.res %{buildroot}/opt/share/icu_tzdata/timezoneTypes.res
cp -af ./data/misc/timezoneTypes.txt %{buildroot}/opt/share/icu_tzdata/
cp -af ./data/misc/metaZones.txt %{buildroot}/opt/share/icu_tzdata/
cp -af ./tools/tzcode/zoneinfo %{buildroot}/usr/share/icu_zoneinfo/
cp -af ./tools/tzcode/zone.tab %{buildroot}/usr/share/icu_zoneinfo/
cp -af ./tools/tzcode/icu_zone.txt %{buildroot}/usr/share/icu_zoneinfo/
cp -af ./tools/tzcode/zoneinfo64.txt %{buildroot}/usr/share/icu_zoneinfo/
cp -af ./tools/tzcode/icuregions %{buildroot}/usr/share/icu_zoneinfo/

mkdir -p %{buildroot}/usr/sbin/icu_bin/
cp ./bin/zic %{buildroot}/usr/sbin/icu_bin/
cp ./bin/tz2icu %{buildroot}/usr/sbin/icu_bin/

%remove_docs


%post -n libicu -p /sbin/ldconfig

%postun -n libicu -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE

%files -n libicu
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/*.so*
%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencfu
%{_bindir}/gencnval
%{_bindir}/gendict
%{_bindir}/genrb
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%{_bindir}/icuinfo
%{_bindir}/icu-config
%{_bindir}/icuexportdata
%{_sbindir}/*
%dir %{_datadir}/icu/%{version}
%{_datadir}/icu/%{version}/config/mh-linux
%{_datadir}/icu/%{version}/install-sh
%{_datadir}/icu/%{version}/LICENSE
%{_datadir}/icu/%{version}/mkinstalldirs
%ifarch armv7hl
%{_datadir}/icu/%{version}/*.dat
%endif

%files -n libicu-devel
%manifest %{name}.manifest
%license LICENSE
%{_includedir}/unicode
%{_libdir}/*.so
%{_libdir}/pkgconfig/icu-*.pc
%{_libdir}/%{name}

%files -n libicu-tzdata
%{_sbindir}/icu_bin/*
/opt/share/icu_tzdata/*
%{_datadir}/icu_zoneinfo/*
