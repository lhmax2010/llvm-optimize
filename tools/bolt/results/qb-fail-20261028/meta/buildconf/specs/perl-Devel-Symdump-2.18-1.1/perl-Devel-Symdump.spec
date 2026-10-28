#
# spec file for package perl-Devel-Symdump
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%global cpan_name Devel-Symdump

Name:           perl-Devel-Symdump
VCS:            platform/upstream/perl-Devel-Symdump#31f7f4de33778139519346457071bdf5a6311d7a
Version:        2.18
Release:        1.1
License:        Artistic-1.0
Summary:        Dump symbol names or the symbol table
Url:            http://cpan.org/modules/by-module/Devel/
Group:          Development/Libraries/Perl
Source:         %{cpan_name}-%{version}.tar.gz
Source1:        Artistic.txt
Source1001: 	perl-Devel-Symdump.manifest
BuildRequires:  perl
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl-macros
Requires:       perl(Carp)

%description
%{cpan_name} module for perl
This little package serves to access the symbol table of perl.

%prep
%setup -q -n Devel-Symdump-%{version}
cp %{SOURCE1001} .
cp %{SOURCE1} .

%build
CFLAGS="%{optflags}" perl Makefile.PL
make %{?_smp_mflags}

%check
make test || exit 0

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license Artistic.txt

%changelog
