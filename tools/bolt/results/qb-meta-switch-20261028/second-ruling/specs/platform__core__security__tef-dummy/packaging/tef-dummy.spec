Name:       tef-dummy
Summary:    Dummy plugin for libteec.
Version:    0.0.1
Release:    0
Group:      Security/Testing
License:    Apache License, Version 2.0
URL:        N/A
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires: cmake
Provides: libteec

%define _unpackaged_files_terminate_build 0

%description
Plug for apps using libteec instead of it.

%prep
%setup -q

%build
cmake .

%install
%make_install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
cp $RPM_BUILD_ROOT/libtef_dummy.so $RPM_BUILD_ROOT/%{_libdir}/libtef_dummy.so

%files
%manifest packaging/%{name}.manifest
%defattr(-, root, root, -)
%{_libdir}/libtef_dummy.so


%changelog

%pre
if [ -f %{_libdir}/libteec.so ]
then
	cp -a $(readlink -f %{_libdir}/libteec.so) %{_libdir}/teec_optee_lib.so-orig
fi

%post
ln -sf %{_libdir}/libtef_dummy.so %{_libdir}/libteec.so.1.0
ln -sf %{_libdir}/libteec.so.1.0 %{_libdir}/libteec.so.1
ln -sf %{_libdir}/libteec.so.1 %{_libdir}/libteec.so

/sbin/ldconfig

%postun
if [ -f %{_libdir}/teec_optee_lib.so-orig ]
then
	CURR="%{_libdir}/libteec.so"
	NEXT=$CURR

	while [ -L $NEXT ]
	do
		CURR=$NEXT
		NEXT=$(readlink $CURR)
	done

	rm -f $CURR
	cp -a %{_libdir}/teec_optee_lib.so-orig $CURR
	rm -f %{_libdir}/teec_optee_lib.so-orig
fi

/sbin/ldconfig
