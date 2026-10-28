Name:           re2
Version:        20250812
Release:        1
License:        BSD-3-Clause
Summary:        An efficient, principled regular expression library
Url:            http://code.google.com/p/re2/
Group:          System/Libraries
Source:         re2-%{version}.tgz
Source1001:     %{name}.manifest
BuildRequires:  gcc-c++
BuildRequires:  abseil-cpp-devel

%description
RE2 is a fast, safe, thread-friendly alternative to backtracking
regular expression engines like those used in PCRE, Perl, and
Python. It is a C++ library.

%package -n libre2
License:        BSD-2.0
Summary:        An efficient, principled regular expression library
Group:          System/Libraries

%description -n libre2
RE2 is a fast, safe, thread-friendly alternative to backtracking
regular expression engines like those used in PCRE, Perl, and
Python. It is a C++ library.

%package devel
License:        BSD-2.0
Summary:        An efficient, principled regular expression library
Group:          System/Libraries
Requires:       libre2 = %{version}

%description devel
RE2 is a fast, safe, thread-friendly alternative to backtracking
regular expression engines like those used in PCRE, Perl, and
Python. It is a C++ library.

%prep
%setup -q -n re2
cp %{SOURCE1001} .

%build
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS -Wall -pthread" LDFLAGS="$LDFLAGS -Wl,--as-needed -Wl,-z,relro,-z,now" libdir=%{_libdir} prefix=%{_prefix}

%install
make DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} prefix=%{_prefix} install
rm $RPM_BUILD_ROOT%{_libdir}/libre2.a

%remove_docs

%post   -n libre2 -p /sbin/ldconfig

%postun -n libre2 -p /sbin/ldconfig

%files -n libre2
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libre2.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/re2
%{_libdir}/libre2.so
%{_libdir}/pkgconfig/re2.pc
