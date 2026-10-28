%global tarversion 3510000

Name:           sqlite
VCS:            platform/upstream/sqlite#4e62b2b6835a78ac20621b089e9bcf353266031e
Version:        3.51.0
Release:        1.14
License:        Public-Domain
Summary:        Embeddable SQL Database Engine
URL:            http://www.sqlite.org/
Group:          System/Database
Source0:        sqlite-autoconf-%{tarversion}.tar.gz
Source1:        baselibs.conf
Source2:        sqlite_journal_mode_persist.patch
Source3:        Add-pie-compile-option.patch
Source4:        sqlite-harden-shell-cli.patch
Source5:        sqlite-safe-mode-default.patch
Source1001: 	sqlite.manifest

BuildRequires:  pkgconfig(pkg-config)

Requires:       libsqlite = %{version}
Provides:       sqlite3

%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server. SQLite is a server and the SQLite library reads and writes
directly to and from the database files on disk.

SQLite can be used via the sqlite command line tool or via any
application that supports the Qt database plug-ins.

%package -n libsqlite
Summary:        Shared libraries for the Embeddable SQL Database Engine
Group:          System/Database
Provides:       libsqlite3

%description -n libsqlite
This package contains the shared libraries for the Embeddable SQL
Database Engine.

SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server. SQLite is a server and the SQLite library reads and writes
directly to and from the database files on disk.

SQLite can be used via the sqlite command line tool or via any
application that supports the Qt database plug-ins.

%package devel
Summary:        Embeddable SQL Database Engine
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       libsqlite = %{version}
Requires:       sqlite
Provides:       sqlite3-devel = %{version}
Obsoletes:      sqlite3-devel < %{version}
Conflicts:      sqlcipher-devel

%description devel
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server; SQLite is the server. The SQLite library reads and writes
directly to and from the database files on disk.

SQLite can be used via the sqlite command-line tool or via any
application which supports the Qt database plug-ins.

%prep
%setup -q -n sqlite-autoconf-%tarversion
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE2}
%{__patch} -p1 < %{SOURCE3}
%{__patch} -p1 < %{SOURCE4}
%{__patch} -p1 < %{SOURCE5}

%build
export CFLAGS=`echo %{optflags} |sed -e 's/-ffast-math//g'`
export CFLAGS="$CFLAGS -fPIC"
%{?asan:CFLAGS="$CFLAGS -lpthread -ldl "}

export CFLAGS="$CFLAGS -DSQLITE_ENABLE_COLUMN_METADATA \
                -DSQLITE_ENABLE_MEMORY_MANAGEMENT \
                -DSQLITE_DEFAULT_AUTOVACUUM=1 \
                -DSQLITE_DEFAULT_PAGE_SIZE=4096 \
                -Dfdatasync=fdatasync \
                -DSQLITE_TIZEN_FEATURE \
                -DSQLITE_TEMP_STORE=2 \
                -DHAVE_USLEEP=1 \
                -DSQLITE_DEFAULT_JOURNAL_SIZE_LIMIT=4194304 \
                -DSQLITE_DEFAULT_FILE_FORMAT=4 \
                -DSQLITE_POWERSAFE_OVERWRITE=1 \
                -DSQLITE_ENABLE_ATOMIC_WRITE"

%configure  --disable-static \
            --soname=legacy \
            --disable-readline \
            --fts3 \
            --all
%{make_build}

%install
%{make_install}
%{remove_docs}

%post -n libsqlite -p /sbin/ldconfig

%postun -n libsqlite -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_bindir}/sqlite3

%files -n libsqlite
%manifest %{name}.manifest
%{_libdir}/libsqlite*.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/*.h
%{_libdir}/libsqlite*.so
%{_libdir}/pkgconfig/sqlite3.pc
%changelog
* Thu Apr 11 2013 Anas Nashif <anas.nashif@intel.com> submit/trunk/20130319.034032@4baf1c1
- enable thread safe option
* Sun Mar 17 2013 Anas Nashif <anas.nashif@intel.com> submit/trunk/20130104.051124@7fc6e9d
- Update package groups
* Thu Jan  3 2013 Anas Nashif <anas.nashif@intel.com> upstream/3.7.14@aad28b0
- devel package requires exec
