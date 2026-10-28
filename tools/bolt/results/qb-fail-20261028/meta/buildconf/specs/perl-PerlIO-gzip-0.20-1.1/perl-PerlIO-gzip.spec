Name: perl-PerlIO-gzip
VCS:  platform/upstream/perl-PerlIO-gzip#652e7280534529bfa110be55117f12d332165977
Version: 0.20
Release: 1.1
Summary: Perl extension to provide a PerlIO layer to gzip/gunzip
License: perl_5
Group: Development/Tools
URL: http://ltp.sourceforge.net/coverage/lcov.php
Source0: http://downloads.sourceforge.net/ltp/lcov-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-root
Requires: perl >= 5.8.8
BuildRequires: pkgconfig(zlib)

%description
PerlIO::gzip provides a PerlIO layer that manipulates files in the format
used by the 'gzip' program. Compression and Decompression are implemented,
but not together. If you attempt to open a file for reading and writing the
open will fail.

%prep
%setup -q -n %{name}-%{version}

%build
perl Makefile.PL
make

%install
rm -rf $RPM_BUILD_ROOT
%perl_make_install
%remove_docs
%perl_process_packlist
%perl_gen_filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.files
%defattr(-,root,root)
