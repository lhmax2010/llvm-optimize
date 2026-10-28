Name:       opencore-amr
Summary:    Opencore AMR package
Version:    0.1.3
Release:    2
Group:      Multimedia/Framework
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	opencore-amr.manifest


%description
opencore AMRNB and AMRWB package


%package devel
Summary:    Opencore AMR package (Development)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
opencore AMRNB and AMRWB development package

%prep
%setup -q
cp %{SOURCE1001} .

%build
./autogen.sh
%configure
make %{?jobs:-j%jobs}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libopencore-amrnb.so.*
%{_libdir}/libopencore-amrwb.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/opencore-amrnb/*.h
%{_includedir}/opencore-amrwb/*.h
%{_libdir}/libopencore-amrnb.so
%{_libdir}/libopencore-amrwb.so
%{_libdir}/pkgconfig/opencore-amrnb.pc
%{_libdir}/pkgconfig/opencore-amrwb.pc
