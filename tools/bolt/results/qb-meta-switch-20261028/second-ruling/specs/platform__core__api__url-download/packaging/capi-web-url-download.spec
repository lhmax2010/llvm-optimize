Name:	capi-web-url-download
Summary:	CAPI for content download with web url
Version:	1.2.12
Release:	0
Group:		Development/Libraries
License:	Apache-2.0
URL:		N/A
Source0:	%{name}-%{version}.tar.gz
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(download-provider-interface)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(gmock)
BuildRequires: cmake
%if 0%{?gcov:1}
BuildRequires: gtest-devel
BuildRequires: lcov
BuildRequires: tar
%endif

%description
CAPI for the content download

%package devel
Summary:	url download
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
CAPI for content downloading with web url (developement files)

%if 0%{?gcov:1}
%package gcov
Summary:  Download library(gcov)
Group:    Network/Testing
%description gcov
gcov objects for coverage test

%package unittests
Summary:    %{name} unittests binary
%description unittests
unittests binary
%endif

%package test_app
Summary:	Test application for url download
%description test_app
test_app binary

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%cmake -DBUILD_GTESTS=%{?gcov:1}%{!?gcov:0} \
	.
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    LD_LIBRARY_PATH=%{_bindir}/tizen-unittests/%{name} /usr/bin/url-download-gtest
}

teardown() {
    echo "teardown start"
}

main() {
    setup
    test_main
    teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/
cp unittest/libdp-interface-mock.so %{buildroot}%{_bindir}/tizen-unittests/%{name}/
%endif

%check
%if 0%{?gcov:1}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:unittest
unittest/url-download-gtest
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%manifest capi-web-url-download.manifest
%{_libdir}/libcapi-web-url-download.so.*
%license LICENSE.APLv2

%files devel
%defattr(-,root,root,-)
%manifest capi-web-url-download.manifest
%{_libdir}/libcapi-web-url-download.so
%{_libdir}/pkgconfig/capi-web-url-download.pc
%{_includedir}/web/download.h
%{_includedir}/web/download_product.h
%{_includedir}/web/download_private.h
%{_includedir}/web/download_extension.h
%exclude %{_includedir}/web/download_doc.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*

%files unittests
%{_bindir}/url-download-gtest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%{_bindir}/tizen-unittests/%{name}/*.so
%endif

%files test_app
%{_bindir}/url-download-test

