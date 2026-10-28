%define run_tests 0
%if %{run_tests}
    # check is defined off at .rpmmacros file.
    %undefine check
%endif

Name:           tar
Version:        1.17
Release:        0
Summary:        GNU implementation of tar ((t)ape (ar)chiver)
License:        GPL-2.0-or-later
Group:          System/Utilities
Url:            http://www.gnu.org/software/tar/
Source0:        %{name}-%{version}.tar.gz
Source1001: 	tar.manifest
BuildRequires:  help2man
BuildRequires:  libacl-devel
Provides:       gnutar = %{version}-%{release}

%description
This package normally also includes the program "rmt", which provides
remote tape drive control. Since there are compatible versions of 'rmt'
in either the 'star' package or the 'dump' package, we didn't put 'rmt'
into this package. If you are planning to use the remote tape features
provided by tar you have to also install the 'dump' or the 'star'
package.

%prep
%setup -q
cp %{SOURCE1001} .

%build
#%define my_cflags -W -Wall -Wpointer-arith -Wstrict-prototypes -Wformat-security -Wno-unused-parameter
#export CFLAGS="%{optflags} %my_cflags"
#export RSH="/usr/bin/rsh"
#export DEFAULT_ARCHIVE_FORMAT="POSIX"
#%configure \
#	gl_cv_func_linkat_follow="yes" \
#	--disable-silent-rules \
#	--disable-nls

export CFLAGS="$CFLAGS -Wno-error=implicit-function-declaration -Wno-error=int-conversion"
export CFLAGS="$CFLAGS -fPIE"
export LDFLAGS="$LDFLAGS -pie"

%configure --disable-static \
           --disable-nls
make %{?_smp_mflags}

%check
%if %{run_tests}
    %__make check || exit 0
%endif

%install
%{?make_install} %{!?make_install:make install DESTDIR=%{buildroot}}
mv %{buildroot}%{_bindir}/tar %{buildroot}%{_bindir}/gnutar
install -d -m 755 %{buildroot}/%{_mandir}/man1
help2man ./src/tar --name "The GNU version of the tar archiving utility" -p gnutar \
        | gzip -c > %{buildroot}/%{_mandir}/man1/gnutar.1.gz
rm -rf %{buildroot}%{_libexecdir}/rmt
rm -f %{buildroot}%{_infodir}/dir


%remove_docs

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%{_bindir}/gnutar
%license COPYING
