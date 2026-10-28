%define __libtoolize :

#
Summary: A Japanese character input system library.(with dictionary)
Name: anthy
Version: 9100h
Release: 1
URL: http://www.sourceforge.jp/projects/anthy/
Source0: %{name}-%{version}.tar.gz
Source1001: 	anthy.manifest
#
# URL: http://cannadic.oucrc.org
# Source1: cannadic-0.93.tar.gz
License: LGPL-2.1+ and GPL-2.0+
Group: Graphics & UI Framework/Input
BuildRoot: %{_tmppath}/%{name}-root

%description
A Japanese character input system library.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          System/Utilities
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q
cp %{SOURCE1001} .
#tar zxf %{_sourcedir}/cannadic-0.93.tar.gz
#ln -s ../cannadic-0.93/gcanna.t mkanthydic
#ln -s ../cannadic-0.93/gcannaf.t mkanthydic

%build
[ ! -x autogen.sh ] || { rm -f configure ; %autogen ; }
%reconfigure --disable-static --with-pic
%__make %{?_smp_mflags}

%configure --disable-zipcode

make

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall
%{__rm} -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING COPYING.alt-cannadic COPYING.anthy
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/anthy
#%{_datadir}/emacs/site-lisp/*
%{_libdir}/libanthy*.so.*
#%doc README doc

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Thu Jan  3 2002 Yusuke Tabata <yusuke@kmc.gr.jp>
- changed my mail address and URL of web page

* Thu Nov 11 2001 Takayoshi Nobuoka <taka@trans-nt.com>
- add %{_sysconfdir}/* at %files

* Wed Sep  9 2001 Takayoshi Nobuoka <taka@trans-nt.com>
- use _bindir and so on.

* Sun Aug 19 2001 Tabatee <yusuke@kmc.kyoto-u.ac.jp>
- Initial build.
