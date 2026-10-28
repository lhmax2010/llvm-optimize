Name:		lzma-sdk
Url:		https://www.7-zip.org/sdk.html
Summary:	The SDK for LZMA Compression
Version:	9.20
Release:	1
Group:		System
License:	PD
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	cmake

%define keepstatic 1

%description
LZMA SDK provides the documentation, samples, header files, libraries,
and tools you need to develop applications that use LZMA compression

%package -n liblzma-tool
Summary:	LZMA tool library package

%description -n liblzma-tool
LZMA tool shared library

%package -n liblzma-tool-devel
Summary:	LZMA tool library for (devel)

%description -n liblzma-tool-devel
LZMA tool library package for (devel)

%prep
%setup -q

%build
%cmake . \
	-DCMAKE_INSTALL_PREFIX=%{_prefix}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%files -n liblzma-tool
%defattr(-,root,root,-)
%{_libdir}/liblzma-tool.so.*

%files -n liblzma-tool-devel
%defattr(-,root,root,-)
%{_includedir}/lzma-tool/*.h
%{_libdir}/liblzma-tool.so
%{_libdir}/liblzma-tool-static.a
%{_libdir}/pkgconfig/liblzma-tool.pc
