Name:           linux-tizen-modules-source
Version:        11.0.0
Release:        0
License:        GPL-2.0+, GPL-2.0, LGPL-2.1+
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.manifest
Summary:        Source code for Tizen-specific kernel modules
Group:          System/Kernel
%description
This package contains source code for Tizen-specific kernel modules:
- logger - provides in-kernel ring buffers for purpose of logging (via dlog)
- proc-tsm - provides system-wide process infromation for monitoring purpose (via stability monitor)

%package        -n linux-tizen-modules-headers
Summary:        Tizen-specific kernel modules headers
License:        GPL-2.0+
Group:          System/Kernel
%description    -n linux-tizen-modules-headers
This package exports userspace API headers for Tizen-specific kernel modules.

%package        -n linux-tizen-modules-tests
Summary:        Tizen-specific kernel modules tests
License:        GPL-2.0+
Group:          System/Kernel
Provides:       linux-kernel-kdbus-tests
Provides:       linux-kernel-logger-tests
BuildRequires:  pkgconfig(libcap)
%description    -n linux-tizen-modules-tests
This package contains tests for Tizen-specific kernel modules.

%prep
%setup -q
cp %{SOURCE1} .

%build
make -C tests/kdbus
make -C tests/logger
make -C tests/zlog_stdout
make -C tests/zlog_bitmap

%install
mkdir -p %{buildroot}/usr/src/%{name}/kdbus
mkdir -p %{buildroot}/usr/src/%{name}/zlogger
mkdir -p %{buildroot}/%{_includedir}/linux
mkdir -p %{buildroot}/%{_libexecdir}/%{name}/tests

cp -a include/ %{buildroot}/usr/src/%{name}
cp kernel/*.[ch] kernel/Makefile COPYING %{buildroot}/usr/src/%{name}
cp kernel/kdbus/*.[ch] kernel/kdbus/Makefile %{buildroot}/usr/src/%{name}/kdbus
cp kernel/zlogger/*.c kernel/zlogger/Makefile %{buildroot}/usr/src/%{name}/zlogger

cp include/uapi/linux/kdbus.h %{buildroot}/%{_includedir}/linux
cp include/uapi/linux/logger.h %{buildroot}/%{_includedir}/linux
cp include/uapi/linux/zlogger.h %{buildroot}/%{_includedir}/linux

cp tests/logger/logger-test %{buildroot}/%{_libexecdir}/%{name}/tests/logger-test
cp tests/kdbus/kdbus-test %{buildroot}/%{_libexecdir}/%{name}/tests/kdbus-test
cp tests/zlog_stdout/zlog_stdout %{buildroot}/%{_libexecdir}/%{name}/tests/zlog_stdout
cp tests/zlog_bitmap/zlog_bitmap %{buildroot}/%{_libexecdir}/%{name}/tests/zlog_bitmap

%files
%manifest %{name}.manifest
%license COPYING
/usr/src/%{name}/COPYING
/usr/src/%{name}/*.c
/usr/src/%{name}/*.h
/usr/src/%{name}/Makefile
/usr/src/%{name}/kdbus/*.c
/usr/src/%{name}/kdbus/*.h
/usr/src/%{name}/kdbus/Makefile
/usr/src/%{name}/include/uapi/linux/*.h

/usr/src/%{name}/zlogger/*.c
/usr/src/%{name}/zlogger/Makefile

%files -n linux-tizen-modules-headers
%manifest %{name}.manifest
%license COPYING
%{_includedir}/linux/kdbus.h
%{_includedir}/linux/logger.h
%{_includedir}/linux/zlogger.h

%files -n linux-tizen-modules-tests
%manifest %{name}.manifest
%license COPYING
%{_libexecdir}/%{name}/tests/logger-test
%{_libexecdir}/%{name}/tests/kdbus-test
%{_libexecdir}/%{name}/tests/zlog_stdout
%{_libexecdir}/%{name}/tests/zlog_bitmap
