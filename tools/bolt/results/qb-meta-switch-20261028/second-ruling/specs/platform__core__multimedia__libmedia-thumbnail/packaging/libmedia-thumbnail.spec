Name:       libmedia-thumbnail
Summary:    Media thumbnail service library for multimedia applications
Version:    0.4.21
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-devel.manifest

BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(mm-fileinfo)
BuildRequires: pkgconfig(mmutil-common)
BuildRequires: pkgconfig(mmutil-magick)
%if 0%{?gtests:1}
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(gmock)
%endif
BuildRequires: pkgconfig(mmutil-gif)
BuildRequires: pkgconfig(mmutil-jpeg)

%description
Description: Media thumbnail service library for multimedia applications


%package devel
Summary:        Media thumbnail service library for multimedia applications (development)
Requires:       %{name}  = %{version}-%{release}
Group:          Multimedia/Development

%description devel
Description: Media thumbnail service library for multimedia applications (development)

%prep
%setup -q
cp %{SOURCE1001} %{SOURCE1002} .


%build
%cmake . -DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
    -DWITH_DA_PROFILE=%{?_with_da_profile:1}%{!?_with_da_profile:0}
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%if 0%{?gtests:1}
%{_bindir}/gtest*
%{_bindir}/libmedia-thumbnail-unittest.jpg
%endif
#License
%license LICENSE.APLv2.0

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/media-thumbnail.pc
%{_includedir}/media-thumbnail/*.h
