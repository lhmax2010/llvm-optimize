%define         generic_name db
%define         docdir %{_defaultdocdir}/%{name}
%define         major 4
%define         minor 8

Name:           db4
Version:        4.8.30.NC
Release:        0
Summary:        Berkeley DB Database Library Version 4.8
License:        BSD-3-Clause
Group:          System/Libraries
Url:            http://www.sleepycat.com
Source:         db-%{version}.tar.gz
Source1:        %{name}.changes
Source9:        getpatches
Source1001: 	db4.manifest
BuildRequires:  autoconf
BuildRequires:  fdupes
BuildRequires:  gcc-c++
Provides:       db = %{version}

%description
The Berkeley DB Database is a programmatic toolkit that provides
database support for applications.

This package contains the necessary runtime libraries.

%package utils
Summary:        Command Line tools for Managing Berkeley DB Databases
Group:          Productivity/Databases/Tools

%description utils
The Berkeley DB Database is a programmatic toolkit that provides
database support for applications.

This package contains the command line tools for managing Berkeley DB
databases.

%package doc
Summary:        Documentation for Berkeley DB
Group:          Development/Libraries/C and C++
BuildArch:      noarch

%description doc
The Berkeley DB Database is a programmatic toolkit that provides
database support for applications.

This package contains the documentation.

%package        devel
Summary:        Development Files and Libraries for the Berkeley DB library Version 4.8
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       glibc-devel

%description    devel
The Berkeley DB Database is a programmatic toolkit that provides
database support for applications.

This package contains the header files and libraries.

%prep
%setup -q -n %{generic_name}-%{version}
cp %{SOURCE1001} .

%build
cd dist
# dist/RELEASE codes the build date into the binary.
# Use last change of changes file instead
LAST_MOD=`stat --format="%Y" %SOURCE1`
DIST_DATE=`date -d "@$LAST_MOD" '+%B %e, %Y'`
sed -i -e "s/^DB_RELEASE_DATE=.*$/DB_RELEASE_DATE=\"$DIST_DATE\"/" RELEASE
./s_config
CFLAGS="$CFLAGS -fno-strict-aliasing"

#
# Build now the NPTL version
#
mkdir ../build_nptl
cd ../build_nptl
../dist/configure --prefix=%{_prefix} \
        --libdir=%{_libdir} --enable-compat185 --disable-dump185 \
        --enable-shared --disable-static --enable-cxx \
        --with-mutex="POSIX/pthreads/library" \
	--build=%{_build} --host=%{_host}
# Make sure O_DIRECT is really disabled (build host could have old kernel)
perl -pi -e 's/#define HAVE_O_DIRECT 1/#undef HAVE_O_DIRECT/' db_config.h
# Remove libtool predep_objects and postdep_objects wonkiness
perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
perl -pi -e 's/-shared -nostdlib/-shared/' libtool

make %{?_smp_mflags} LIBSO_LIBS='$(LIBS)' LIBXSO_LIBS='$(LIBS)'" -L%{_libdir} -lstdc++"

%install
mkdir -p %{buildroot}%{_includedir}/db4
CONFIG_ARGS=$(find . -name "config.log" -exec grep "\$ \.\./dist\/configure" {} \; | sed 's/.*configure\( --.*\)/\1/g')
if [ -z "$CONFIG_ARGS" ]
then
  echo "could not find configure arguments ... exiting"
  exit 42
fi
mkdir -p %{buildroot}%{_libdir}
cd build_nptl
make prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir} strip=true install
cd ..
# make ldd happy:
chmod 755 %{buildroot}%{_libdir}/libdb*.so
# Fix header file installation
mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/db4
echo "#include <db4/db.h>" > %{buildroot}%{_includedir}/db.h
echo "#include <db4/db_185.h>" > %{buildroot}%{_includedir}/db_185.h
echo "#include <db4/db_cxx.h>" > %{buildroot}%{_includedir}/db_cxx.h
# remove dangling tags symlink from examples.
rm -f examples_cxx/tags
rm -f examples_c/tags
# Move documentation to the right directory
mkdir -p %{buildroot}%{docdir}
mv %{buildroot}%{_prefix}/docs/* %{buildroot}/%{docdir}
cp -a examples_cxx examples_c %{buildroot}/%{docdir}
cp -a LICENSE README %{buildroot}/%{docdir}
#
# Remove api documentation for C++, Java and TCL
rm -rf %{buildroot}/%{docdir}/csharp
rm -rf %{buildroot}/%{docdir}/java
rm -rf %{buildroot}/%{docdir}/api_reference/CXX
rm -rf %{buildroot}/%{docdir}/api_reference/STL
rm -rf %{buildroot}/%{docdir}/api_reference/TCL
rm -rf %{buildroot}/%{docdir}/gsg*/CXX
rm -rf %{buildroot}/%{docdir}/gsg*/JAVA
mv %{buildroot}/%{docdir}/collections/tutorial %{buildroot}/%{docdir}/
# Remove crappy *.la files
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/tls/*.la
%fdupes %{buildroot}%{_libdir}
%fdupes %{buildroot}%{docdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libdb-%{major}.%{minor}.so
%{_libdir}/libdb_cxx-%{major}.%{minor}.so

%files doc
%manifest %{name}.manifest
%defattr(-,root,root)
%license %{docdir}/LICENSE
%dir %{docdir}
%doc %{docdir}/README
%doc %{docdir}/index.html
%doc %{docdir}/license
%doc %{docdir}/articles
%doc %{docdir}/api_reference
%doc %{docdir}/examples_c
%doc %{docdir}/examples_cxx
%doc %{docdir}/gsg*
%doc %{docdir}/porting
%doc %{docdir}/programmer_reference
%doc %{docdir}/tutorial

%files utils
%manifest %{name}.manifest
%defattr(-,root,root)
%license %{docdir}/LICENSE
%{_bindir}/db_archive
%{_bindir}/db_checkpoint
%{_bindir}/db_deadlock
%{_bindir}/db_dump
%{_bindir}/db_load
%{_bindir}/db_printlog
%{_bindir}/db_recover
%{_bindir}/db_sql
%{_bindir}/db_stat
%{_bindir}/db_upgrade
%{_bindir}/db_verify
%{_bindir}/db_hotbackup

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%license %{docdir}/LICENSE
%dir %{_includedir}/db4
%{_includedir}/db.h
%{_includedir}/db_185.h
%{_includedir}/db_cxx.h
%{_includedir}/db4/db.h
%{_includedir}/db4/db_185.h
%{_includedir}/db4/db_cxx.h
%{_libdir}/libdb.so
%{_libdir}/libdb-%{major}.so
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-%{major}.so

%changelog
