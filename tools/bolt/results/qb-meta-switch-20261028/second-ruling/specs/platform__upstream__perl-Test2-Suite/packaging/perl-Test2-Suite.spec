#
# spec file for package perl-Test2-Suite
#
# Copyright (c) 2023 SUSE LLC
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

%define cpan_name Test2-Suite
Name:           perl-Test2-Suite
Version:        1.302216
Release:        0
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Distribution with a rich set of tools built upon the Test2 framework
URL:            https://metacpan.org/release/%{cpan_name}
Source0:        %{cpan_name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  perl
BuildRequires:  perl-Term-Table
Requires:       perl-Term-Table

%description
Rich set of tools, plugins, bundles, etc built upon the Test2 testing
library. If you are interested in writing tests, this is the distribution
for you.

%prep
%setup -q -n Test2-Suite-%{version}
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


