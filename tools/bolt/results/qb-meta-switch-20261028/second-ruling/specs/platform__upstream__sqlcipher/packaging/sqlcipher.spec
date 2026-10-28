Name:           sqlcipher
Version:        4.6.1
Release:        0
Summary:        SQLCipher is an open source extension to SQLite that provides transparent 256-bit AES encryption of database files
License:        BSD-3-Clause
URL:            https://github.com/sqlcipher/sqlcipher
Group:          Security/Crypto Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001:     sqlcipher.manifest
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(tcl)
Requires:       libsqlcipher = %{version}
Provides:       sqlcipher

%description
SQLCipher is an open source library that provides transparent, secure 256-bit
AES encryption of SQLite database files. SQLCipher has been adopted as a secure
database solution by many commercial and open source products, making it one of
the most popular encrypted database platforms for Mobile, Embedded, and Desktop
applications.

%package -n libsqlcipher
Summary:        Shared libraries for SQLCipher
Group:          Security/Crypto Libraries
BuildRequires:  pkgconfig(openssl3)
Provides:       libsqlcipher

%description -n libsqlcipher
This package contains the shared libraries for SQLCipher.

%package devel
Summary:        Development files for SQLCipher
Group:          Security/Crypto Libraries
Requires:       libsqlcipher = %{version}
Provides:       sqlcipher-devel = %{version}
Conflicts:      sqlite3-devel

%description devel
The %{name}-devel package contains libraries for developing applications that
use SQLCipher.

%prep
%setup -q
cp %{SOURCE1001} .

%build
CFLAGS="%{optflags} -DSQLITE_HAS_CODEC -DSQLITE_TEMP_STORE=2 -fPIE"
LDFLAGS="%{?__global_ldflags} `pkg-config --libs libcrypto3` -Wl,--version-script=sqlcipher.ld -pie"
%configure \
    --enable-tempstore=yes \
    --enable-releasemode \
    --disable-static \
    --disable-tcl \
    --with-pic
make %{?jobs:-j%jobs}

%install
%make_install

%post -n libsqlcipher -p /sbin/ldconfig

%postun -n libsqlcipher -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%doc README.md
%license LICENSE.md
%defattr(-,root,root)
%{_bindir}/sqlcipher

%files -n libsqlcipher
%manifest %{name}.manifest
%license LICENSE.md
%defattr(-,root,root)
%{_libdir}/libsqlcipher*.so.*

%files devel
%manifest %{name}.manifest
%license LICENSE.md
%defattr(-,root,root)
%{_includedir}/sqlcipher
%{_libdir}/libsqlcipher*.so
%{_libdir}/pkgconfig/sqlcipher.pc
