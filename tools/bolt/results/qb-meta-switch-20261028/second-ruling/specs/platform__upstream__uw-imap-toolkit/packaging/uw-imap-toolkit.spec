#sbs-git:slp/pkgs/u/uw-imap-toolkit uw-imap-toolkit 0.1.1 a675e5c581b6726dcb93c63d826d6827bf29d671
%define _optdir	/opt
%define _appdir	%{_optdir}/apps


Name:       uw-imap-toolkit
Summary:    IMAP-2007e developed by University of Washington
Version:    0.1.37
Release:    0
Group:      Messaging/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:	libuw-imap-toolkit.manifest
Source1002:	libuw-imap-toolkit-devel.manifest

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: libgcrypt-devel
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(dlog)

%description
IMAP-2007e run-time library for E-mail Framework


%package -n libuw-imap-toolkit
Summary:    IMAP-2007e developed by University of Washington
Group:      Messaging/Libraries

%description -n libuw-imap-toolkit
IMAP-2007e run-time library for E-mail Framework


%package -n libuw-imap-toolkit-devel
Summary:    IMAP-2007e developed by University of Washington
Group:      Messaging/Development
Requires:   libuw-imap-toolkit = %{version}-%{release}

%description -n libuw-imap-toolkit-devel
IMAP-2007e development library for E-mail Framework

%prep
%setup -q
cp %{SOURCE1001} %{SOURCE1002} .

%build
# for ignoring warning messages(It is opensource)
export CFLAGS="$CFLAGS -Wno-unused-result -Wno-pointer-sign -Wno-unused-function -Wno-parentheses -Wmisleading-indentation -Wno-unused-variable -Wno-unused-variable -Wno-unused-value -Wno-cpp -Wno-incompatible-pointer-types -Wno-implicit-function-declaration -Wno-implicit-int"
./autogen.sh
%configure --disable-static


make %{?jobs:-j%jobs}
find -name '*.pc' -exec sed -i -e 's/\$version/%{version}/g' {} \;


%install
rm -rf %{buildroot}
%make_install

%post -n libuw-imap-toolkit -p /sbin/ldconfig


%postun -n libuw-imap-toolkit -p /sbin/ldconfig


%files -n libuw-imap-toolkit
%manifest libuw-imap-toolkit.manifest
%defattr(-,root,root,-)
%{_libdir}/libuw-imap-toolkit.so.*
%license LICENSE

%files -n libuw-imap-toolkit-devel
%manifest libuw-imap-toolkit-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/libuw-imap-toolkit.so
%{_libdir}/pkgconfig/uw-imap-toolkit.pc
%{_includedir}/uw-imap-toolkit/*
