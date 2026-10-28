Name:           rsync
Version:        3.4.1
Release:        1
License:        GPL-3.0-or-later
Summary:        A program for synchronizing files over a network
URL:            http://rsync.samba.org/
#X-Vcs-Url:     git://git.samba.org/rsync
Group:          Base/Utilities
Source0:        http://rsync.samba.org/ftp/rsync/src/rsync-%{version}.tar.gz
Source10:       Chnage_nanosleep_to_gettimeofday.patch
Source1001:     rsync.manifest

BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  libzstd-devel

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE10}

%build
export CFLAGS="$CFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"

%configure --disable-xxhash --disable-lz4
make reconfigure
%make_build

%install
%make_install
%{remove_docs}

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/rsync
%{_bindir}/rsync-ssl

