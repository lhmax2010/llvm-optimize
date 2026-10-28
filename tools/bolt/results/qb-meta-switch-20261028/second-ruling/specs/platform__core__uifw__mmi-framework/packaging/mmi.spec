Name:		mmi
Version:	2.2.2
Release:	0
Summary:	Multi-modal Interaction Framework
License:	Apache-2.0 and BSD-3-Clause and BSL-1.0 and MIT
URL:		http://www.tizen.org
Source:		%{name}-%{version}.tar.xz
Source1004:	%{name}.manifest

BuildRequires:	meson
BuildRequires:	tidl
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:	pkgconfig(bundle)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(rpc-port)
BuildRequires:	pkgconfig(ecore)
BuildRequires:	pkgconfig(vconf)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)

#Build dependencies for tests
BuildRequires:	pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
MMI(Multi-modal Interaction) Framework

%package plugins
Summary:	Plugins for MMI Framework
Group:		System/Libraries
%description plugins
Plugins for MMI Framework

%package cli
Summary:	CLI for MMI Framework
Group:		System/Libraries
%description cli
CLI for MMI Framework

%package devel
Summary:	Development package for MMI Framework
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig(rpc-port)
%description devel
Development package for MMI Framework

%if 0%{?gcov:1}
%package gcov
Summary:	MMI Framework (gcov)
%description gcov
MMI Framework gcov objects
%endif

%package tests
Summary:	Testcases for MMI Framework
Group:		System/Libraries
%description tests
Testcases for testing MMI Framework APIs

%prep
%setup -q
cp %{SOURCE1004} .

cat LICENSE LICENSE.BSD LICENSE.BSL LICENSE.MIT > LICENSE.merge
cp LICENSE.merge LICENSE
rm LICENSE.merge

#generate mmi-proxy using TIDL Compiler
tidlc -p -l C -i tidl/mmi.tidl -o mmi_proxy
mv mmi_proxy.* src/mmi
tidlc -s -l C -i tidl/mmi.tidl -o mmi_stub
mv mmi_stub.* src/mmi-manager

%build
%if 0%{?gcov:1}
CFLAGS+=" -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
CXXFLAGS+=" -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
LDFLAGS+=" -lgcov"
%endif
%if 0%{?debug:1}
CFLAGS=$(echo $CFLAGS | sed 's/-O[1-3]/-Og/')
CXXFLAGS=$(echo $CXXFLAGS | sed 's/-O[1-3]/-Og/')
CFLAGS=$(echo $CFLAGS | sed 's/-D_FORTIFY_SOURCE=[1-9]/-D_FORTIFY_SOURCE=0/g')
CXXFLAGS=$(echo $CXXFLAGS | sed 's/-D_FORTIFY_SOURCE=[1-9]/-D_FORTIFY_SOURCE=0/g')
%endif
%if 0%{?asan:1}
export CXXFLAGS+=" -Wno-maybe-uninitialized"
%endif

meson setup --prefix=/usr \
	--bindir %{_bindir} \
	--libdir %{_libdir} \
	--datadir %{_datadir} \
	builddir
meson configure -Dplatform_option=tizen builddir
ninja -C builddir all

%install
DESTDIR=%{buildroot} ninja -C builddir install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find ./builddir/tests/ -name '*.gcno' -exec rm {} \;
find ./builddir/plugins/ -name '*.gcno' -exec rm {} \;
find ./builddir/src/mmi-cli/ -name '*.gcno' -exec rm {} \;
find . -name '*proxy*.gcno' -exec rm {} \;
find . -name '*_stub*.gcno' -exec rm {} \;
find . -name '*tidl*.gcno' -exec rm {} \;
find . -name '*-port-instance*.gcno' -exec rm {} \;
find . -name 'mmi-data-gateway*.gcno' -exec rm {} \;
find . -name 'mmi-node-controller*.gcno' -exec rm {} \;
find . -name 'mmi-workflow-script*.gcno' -exec rm {} \;
find . -name 'mmi-plugin*.gcno' -exec rm {} \;
find . -name 'mmi-workflow-output-event*.gcno' -exec rm {} \;
find ./builddir/meson-private/ -name '*.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%check
%if "%{_mmi_test_enable}" == "true"
ninja -C builddir test
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o gcov.info
genhtml gcov.info
%endif
%endif

%post
/sbin/ldconfig
echo %{_bindir}/mmi-manager
chsmack -e "System" %{_bindir}/mmi-manager

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/*.so*
%{_bindir}/mmi-manager
%{_datadir}/packages/mmi-manager.xml

%files plugins
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_datadir}/mmi/plugins/*.so*

%files cli
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/mmi-cli
%{_bindir}/mmi-cli-node-tester
#%{TZ_SYS_RO_SHARE}/mmi/configs/mmi-config.xml

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_includedir}/mmi/mmi*.h
%{_libdir}/pkgconfig/*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files tests
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/mmi-tests
%{_bindir}/mmi-manager-tests
