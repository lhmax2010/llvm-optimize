Name:           freetype2
Summary:        A free and portable font rendering engine
Version:        2.13.2
Release:        1
Group:          Graphics/Font Management
License:        FTL
Url:            http://www.freetype.org
Source0:        http://download.savannah.gnu.org/releases-noredirect/freetype/freetype-%{version}.tar.gz
Source1001:     packaging/freetype2.manifest
BuildRequires:  pkgconfig(libpng)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:       %{name}-bytecode

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.

%package -n libfreetype
Summary:        A TrueType Font Library
Group:          Graphics/Font Management

%description -n libfreetype
This library features TrueType fonts for open source projects. This
version also contains an autohinter for producing improved output.

%package devel
Summary:        FreeType development libraries and header files
Group:          Development/Libraries
Requires:       libfreetype = %{version}
Requires:       zlib-devel
Requires:       pkgconfig
Provides:       freetype-devel

%description devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-devel if you want to develop programs which will use
FreeType.



%prep
%setup -q -n freetype-%{version}

%build
cp %{SOURCE1001} .
export CFLAGS="$CFLAGS -fstack-protector-strong -D_FORTIFY_SOURCE=2"
export LDFLAGS="$LDFLAGS -Wl,--as-needed -Wl,-z,relro"

%configure --disable-static --enable-freetype-config
# libtool moves -Wl,--as-needed from LDFLAGS after dependency libraries.
# Keep it before $deplibs so unused DT_NEEDED entries can be pruned.
sed -i 's|\\$libobjs \\$deplibs \\$compiler_flags|\\$libobjs -Wl,--as-needed \\$deplibs \\$compiler_flags|g' builds/unix/libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%makeinstall gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

# fix multilib issues
%ifarch x86_64 s390x ia64 ppc64 alpha sparc64 aarch64 riscv64
%define wordsize 64
%else
%define wordsize 32
%endif

mv $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h \
$RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig-%{wordsize}.h
cat >$RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h <<EOF
#ifndef __FTCONFIG_H__MULTILIB
#define __FTCONFIG_H__MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "ftconfig-32.h"
#elif __WORDSIZE == 64
# include "ftconfig-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

# Don't package static a or .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a $RPM_BUILD_ROOT%{_libdir}/*.la


%post -n libfreetype -p /sbin/ldconfig

%postun -n libfreetype -p /sbin/ldconfig

%files -n libfreetype
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libfreetype.so.*
%license docs/FTL.TXT

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%dir %{_includedir}/freetype2
%{_datadir}/aclocal/freetype2.m4
%{_includedir}/freetype2/*
%{_libdir}/libfreetype.so
%{_bindir}/freetype-config
%{_libdir}/pkgconfig/*.pc
%{_datadir}/man/man1/*
