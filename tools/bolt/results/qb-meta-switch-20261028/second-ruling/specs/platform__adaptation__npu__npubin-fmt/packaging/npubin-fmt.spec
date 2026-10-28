Name:		npubin-fmt
Summary:	SR NPU binary metadata format
Version:	3.0.2
Release:	0
Group:		System Environment/Daemons
Packager:	MyungJoo Ham <myungjoo.ham@samsung.com>
License:	Apache-2.0
Source0:	npubin-fmt-%{version}.tar.gz
Source1001:	npubin-fmt.manifest

BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	pkg-config

%prep
%setup -q
cp %{SOURCE1001} .

%build
meson setup --buildtype=plain --prefix=%{_prefix} \
      --libdir=%{_libdir} --includedir=%{_includedir} \
      --datadir=%{_datadir} --sysconfdir=%{_sysconfdir} \
      build
ninja -C build %{?_smp_mflags}

%install
DESTDIR=%{buildroot} ninja install -C build %{?_smp_mflags}

%description
This provides npu metadata information for NPU.

%files
%manifest npubin-fmt.manifest
%defattr(-,root,root,-)
%{_includedir}/npubin-fmt/npubinfmt.h
%{_includedir}/npubin-fmt/typedef.h
%{_libdir}/pkgconfig/npubin-fmt.pc

%changelog
* Wed Sep 10 2025 Wook Song <wook16.song@samsung.com>
- Release of 3.0.2

* Mon Jun 17 2024 Jiho Chu <jiho.chu@samsung.com>
- Release of 3.0.1

* Fri Jul 14 2023 Yelin Jeong <yelini.jeong@samsung.com>
- Release of 3.0.0

* Sat Jun 17 2023 Jiho Chu <jiho.chu@samsung.com>
- Release of 1.0.0

* Tue Jun 13 2023 MyungJoo Ham <myungjoo.ham@samsung.com>
- Release of 0.0.1
