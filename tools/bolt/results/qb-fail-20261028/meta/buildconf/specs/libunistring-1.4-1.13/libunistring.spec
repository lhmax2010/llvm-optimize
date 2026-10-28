%define keepstatic 1
%if "%{run_tests}" == "1"
    %define __spec_check_pre %___build_pre
    %define check %%check
%endif

Name:           libunistring
VCS:            platform/upstream/libunistring#4f1bcdb124f4d091ef364156d563b7e2ccae1893
Version:        1.4
Release:        1.13
License:        LGPL-3.0-or-later
Summary:        GNU Unicode string library
Url:            http://www.gnu.org/software/libunistring/
Group:          Development/Libraries/C and C++
Source:         %{name}-%{version}.tar.bz2
Source1001:     libunistring.manifest

%description
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%package devel
Summary:        GNU Unicode string library - development files
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description devel
Development files for programs using libunistring and documentation
for UniString library.

%package devel-static
Summary:        GNU Unicode string library - static libraries
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel = %{version}

%description devel-static
Static libraries of UniString library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --enable-static --enable-shared --disable-rpath --docdir=%{_docdir}/%{name}
%make_build

# %check
# %make_build check %{?_smp_mflags} || exit 0

%install
%make_install DESTDIR=%{buildroot}

# Remove documentation and manual pages as per Tizen policy
%remove_docs

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license COPYING.LIB
%defattr(-,root,root)
%{_libdir}/libunistring.so.*

%files devel
%manifest %{name}.manifest
%license COPYING.LIB
%defattr(-,root,root)
%{_libdir}/libunistring.so
%{_includedir}/unistring
%{_includedir}/*.h

%files devel-static
%license COPYING
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libunistring.a
