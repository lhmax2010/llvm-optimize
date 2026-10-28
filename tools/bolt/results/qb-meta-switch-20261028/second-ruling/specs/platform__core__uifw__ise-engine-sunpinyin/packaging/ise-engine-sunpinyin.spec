Name:       ise-engine-sunpinyin
Summary:    Chinese Pinyin ISE
Version:    1.0.13
Release:    1
Group:      Graphics & UI Framework/Input
License:    LGPL-2.1+ and CDDL-1.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(isf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(sqlite3)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
Chinese Pinyin Engine ISE and it has been supported by Input Service Framework(ISF).

%package devel
Summary:    Chinese Pinyin ISE header files
Group:      Development/Libraries

%description devel
This package contains Chinese Pinyin engine ISE header files and static libraries for Soft ISE development.

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -fvisibility=hidden -fPIC "
export CXXFLAGS="$CXXFLAGS -fvisibility=hidden -fvisibility-inlines-hidden -fPIC "
export CPPFLAGS="$CPPFLAGS -DEXPORTED=__attribute__\(\(visibility\(\\\"default\\\"\)\)\)"

./bootstrap
%configure  --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%{nil}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/scim/icons/sunpinyin_logo.png
%{_datadir}/scim/ise-engine-sunpinyin/*
%{_datadir}/packages/*
%{_libdir}/scim-1.0/1.4.0/IMEngine/ise-engine-sunpinyin.so
%{_libdir}/libsunpinyin*.so
%license LGPL.LICENSE
%license OPENSOLARIS.LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/sunpinyin-2.0.pc
%license LGPL.LICENSE
%license OPENSOLARIS.LICENSE
