#
# spec file for package perl-FFI-CheckLib
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define cpan_name FFI-CheckLib
Name:           perl-FFI-CheckLib
Version:        0.31
Release:        0
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Check that a library is available for FFI
URL:            https://metacpan.org/release/%{cpan_name}
Source:         %{cpan_name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  perl
BuildRequires:  perl-Test2-Suite
BuildRequires:  perl-File-Which
Requires:       perl-Test2-Suite
Requires:       perl-File-Which

%description
This module checks whether a particular dynamic library is available for
FFI to use. It is modeled heavily on Devel::CheckLib, but will find dynamic
libraries even when development packages are not installed. It also
provides a find_lib function that will return the full path to the found
dynamic library, which can be feed directly into FFI::Platypus or another
FFI system.

%prep
%setup -q -n FFI-CheckLib-%{version}
cp %{SOURCE1001} .

%build
%{__perl} Makefile.PL 
%{__make} %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%check
%{__make} test

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE


