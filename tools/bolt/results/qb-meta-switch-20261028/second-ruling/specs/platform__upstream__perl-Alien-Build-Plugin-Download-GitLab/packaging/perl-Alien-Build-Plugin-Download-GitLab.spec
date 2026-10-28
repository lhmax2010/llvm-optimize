#
# spec file for package perl-Alien-Build-Plugin-Download-GitLab
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


%define cpan_name Alien-Build-Plugin-Download-GitLab
Name:           perl-Alien-Build-Plugin-Download-GitLab
Version:        0.01
Release:        0
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Alien::Build plugin to download from GitLab
URL:            https://metacpan.org/release/%{cpan_name}
Source:         %{cpan_name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  perl
BuildRequires:  perl-Alien-Build
BuildRequires:  perl-Test2-Suite
BuildRequires:  perl-Path-Tiny
BuildRequires:  perl-Term-Table
BuildRequires:  perl-URI

Requires:       perl-Alien-Build
Requires:       perl-Test2-Suite
Requires:       perl-Path-Tiny
Requires:       perl-Term-Table
Requires:       perl-URI

%description
This plugin is designed for downloading assets from a GitLab instance.

%prep
%setup -q -n %{cpan_name}-%{version}
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


