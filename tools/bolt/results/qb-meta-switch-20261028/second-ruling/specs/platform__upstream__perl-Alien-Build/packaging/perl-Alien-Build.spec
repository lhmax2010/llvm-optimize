#
# spec file for package perl-Alien-Build
#
# Copyright (c) 2023 Andreas Vögele <andreas@andreasvoegele.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please send bugfixes or comments to the author.
#

Name:           perl-Alien-Build
Version:        2.84
Release:        0
Summary:        Build external dependencies for use in CPAN
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Alien-Build
Source:         Alien-Build-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  perl
BuildRequires:  perl-File-Which
BuildRequires:  perl-Test2-Suite
BuildRequires:  perl-File-chdir
BuildRequires:  perl-Capture-Tiny
BuildRequires:  perl-Path-Tiny
BuildRequires:  perl-FFI-CheckLib

Requires:       perl-File-Which
Requires:       perl-Test2-Suite
Requires:       perl-File-chdir
Requires:       perl-Capture-Tiny
Requires:       perl-Path-Tiny
Requires:       perl-FFI-CheckLib

%description
This Perl module provides tools for building external dependencies, such as C
libraries, for CPAN.

%prep
%setup -q -n Alien-Build-%{version}
cp %{SOURCE1001} .

%build
%{__perl} Makefile.PL 
%{__make} %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%check
#%%{__make} test

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE


