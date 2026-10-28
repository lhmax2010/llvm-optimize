Name: GraphicsMagick
Summary: An ImageMagick fork, offering faster image generation and better quality
Version: 1.3.45
Release: 2
Group: Multimedia/Libraries
Url: http://www.graphicsmagick.org/
License: MIT
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires: bzip2-devel
BuildRequires: freetype-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: libxml2-devel
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libwebpdemux)
BuildRequires: pkgconfig(libwebpmux)
BuildRequires: xz-devel
BuildRequires: zlib-devel

# upgrade path for introduction of -doc subpkg in 1.3.19-4
Obsoletes: GraphicsMagick < 1.3.19-4

%description
GraphicsMagick is a comprehensive image processing package which is initially
based on ImageMagick 5.5.2, but which has undergone significant re-work by
the GraphicsMagick Group to significantly improve the quality and performance
of the software.

%package devel
Summary: Libraries and header files for GraphicsMagick app development
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
GraphicsMagick-devel contains the Libraries and header files you'll
need to develop GraphicsMagick applications. GraphicsMagick is an image
manipulation program.

If you want to create applications that will use GraphicsMagick code or
APIs, you need to install GraphicsMagick-devel as well as GraphicsMagick.
You do not need to install it if you just want to use GraphicsMagick,
however.

%package doc
Summary: GraphicsMagick documentation
Group: Documentation
# upgrade path for introduction of -doc subpkg in 1.3.19-4
Obsoletes: GraphicsMagick < 1.3.19-4
%{!?el5:BuildArch: noarch}

%description doc
Documentation for GraphicsMagick.

%package tool
Summary: GraphicsMagick tools
Group: Development/Tools
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tool
GraphicsMagick tools.

Install GraphicsMagick-perl if you want to use any perl scripts that use
GraphicsMagick.

%prep
%setup -q
cp %{SOURCE1001} .

%if ! 0%{?__isa_bits:1}
%ifarch x86_64
%global __isa_bits 64
%else
%global __isa_bits 32
%endif
%endif

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

%global __provides_exclude_from ^%{_libdir}/GraphicsMagick-%{version}/.*\\.(la|so)$


for f in ChangeLog.2006 ChangeLog.2008 ChangeLog.2009 ChangeLog.2012 NEWS.txt ; do
    iconv -f iso-8859-2 -t utf8 < $f > $f.utf8
    touch -r $f $f.utf8 ; mv -f $f.utf8 $f
done

# Avoid lib64 rpaths (FIXME: recheck this on newer releases)
%if "%{_libdir}" != "/usr/lib"
sed -i.rpath -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build
%configure --enable-shared --disable-static \
           --disable-broken-coders \
           --enable-openmp \
           --docdir=%{_datadir}/%{name} \
           %{?_with_quantum_depth} \
           %{?_enable_quantum_library_names} \
           --with-modules \
           --with-threads \
           --without-magick-plus-plus \
           --without-perl \
           --without-bzlib \
           --without-dps \
           --without-fpx \
           --without-gslib \
           --without-jbig \
           --without-jp2 \
           --with-lcms2 \
           --without-lzma \
           --without-tiff \
           --without-trio \
           --without-ttf \
           --with-webp \
           --without-wmf \
           --without-x \
           --without-xml \
           --with-zlib \

make %{?_smp_mflags}

%install
#rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

find %{buildroot} -name "*.bs" |xargs rm -fv
find %{buildroot} -name ".packlist" |xargs rm -fv
find %{buildroot} -name "perllocal.pod" |xargs rm -fv

rm -rf %{buildroot}%{_datadir}/%{name}
# Keep config
rm -rf %{buildroot}%{_datadir}/%{name}-%{version}/[a-b,d-z,A-Z]*
rm -vf  %{buildroot}%{_libdir}/lib*.la

# fix multilib issues
%ifarch %ix86 x86_64
cp %{buildroot}%{_includedir}/%{name}/magick/magick_types.h \
   %{buildroot}%{_includedir}/%{name}/magick/magick_types-%{__isa_bits}.h
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license Copyright.txt
%{_libdir}/libGraphicsMagick.so.*
%{_libdir}/libGraphicsMagickWand.so.*
%{_libdir}/%{name}-%{version}/config/*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/bmp.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/gif.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/jpeg.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/meta.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/png.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/pnm.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/rgb.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/wbmp.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/webp.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/yuv.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/uyvy.*
%{_libdir}/%{name}-%{version}/modules-Q8/filters/*

%files devel
%{_bindir}/GraphicsMagick-config
%{_bindir}/GraphicsMagickWand-config
%{_libdir}/libGraphicsMagick.so
%{_libdir}/libGraphicsMagickWand.so
%{_libdir}/%{name}-%{version}/config/*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/bmp.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/gif.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/jpeg.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/meta.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/png.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/pnm.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/rgb.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/wbmp.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/webp.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/yuv.*
%{_libdir}/%{name}-%{version}/modules-Q8/coders/uyvy.*
%{_libdir}/%{name}-%{version}/modules-Q8/filters/*
%{_libdir}/pkgconfig/GraphicsMagick.pc
%{_libdir}/pkgconfig/GraphicsMagickWand.pc
%dir %{_includedir}/GraphicsMagick/
%{_includedir}/GraphicsMagick/magick/
%{_includedir}/GraphicsMagick/wand/
%{_mandir}/man1/GraphicsMagick-config.*
%{_mandir}/man1/GraphicsMagickWand-config.*
%{_libdir}/%{name}-%{version}/
%{_datadir}/%{name}-%{version}/

%files doc
%{_mandir}/man[145]/[a-z]*

%files tool
%{_bindir}/[a-z]*

