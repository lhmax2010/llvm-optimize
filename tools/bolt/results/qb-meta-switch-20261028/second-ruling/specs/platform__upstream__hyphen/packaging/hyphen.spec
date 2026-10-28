Name:           hyphen
Summary:        Hyphenation library to use converted TeX hyphenation patterns
Version:        2.8.8
Release:        1
Group:          Graphics & UI Framework/Utilities
License:        LGPL-2.1+
Url:            http://hunspell.sourceforge.net
Source0:        http://sourceforge.net/projects/hunspell/files/Hyphen/2.8/hyphen-%{version}.tar.gz
Source1001:     packaging/hyphen.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Hyphenation library to use converted TeX hyphenation patterns.

%package -n libhyphen
Summary:        Hyphenation Library
Group:          Development/Libraries

%description -n libhyphen
Hyphenation Library.

%package tools
Summary:        Hyphenatione development tools
Group:          Development/Libraries
Requires:       libhyphen = %{version}
Requires:       pkgconfig

%description tools
Hyphenatione development tools.

%package devel
Summary:        Hyphenatione development libraries and header files
Group:          Development/Libraries
Requires:       libhyphen = %{version}
Requires:       zlib-devel
Requires:       pkgconfig

%description devel
Hyphenatione development libraries and header file.

%prep
%setup -q 

%build
cp %{SOURCE1001} .

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%makeinstall gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

# Don't package static a or .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a $RPM_BUILD_ROOT%{_libdir}/*.la

%post -n libhyphen -p /sbin/ldconfig

%postun -n libhyphen -p /sbin/ldconfig

%files -n libhyphen
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libhyphen.so.*
%{_datadir}/hyphen/hyph_en_US.dic
%license COPYING COPYING.LGPL

%files tools
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/substrings.pl

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libhyphen.so
%{_includedir}/*.h
