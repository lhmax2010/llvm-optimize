Name:           dash
VCS:            platform/upstream/dash#c783b9d85841476c488023f7caf6c909fcad4eec
Version:        0.5.13.4
Release:        1.1
Summary:        Small and fast POSIX-compliant shell
Group:          Base/Utilities
License:        BSD-3-Clause AND GPL-2.0-or-later
URL:            http://gondor.apana.org.au/~herbert/dash/
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest

%description
DASH is a POSIX-compliant implementation of /bin/sh that aims to be as small as
possible. It does this without sacrificing speed where possible. In fact, it is
significantly faster than bash (the GNU Bourne-Again SHell) for most tasks.

%prep
%setup -q
cp %{SOURCE1} .

%build
export CFLAGS+=" -fPIC"
export LDFLAGS+=" -pie"
autoreconf -fiv
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/bin
mv %{buildroot}%{_bindir}/dash %{buildroot}/bin/
rm -rf %{buildroot}%{_bindir}/

%post
grep -q '^/bin/dash$' /etc/shells || echo '/bin/dash' >> /etc/shells

%postun
if [ $1 -eq 0 ]; then
    sed -i '/^\/bin\/dash$/d' /etc/shells
fi

%docs_package

%files
%manifest %{name}.manifest
%license COPYING
/bin/dash

