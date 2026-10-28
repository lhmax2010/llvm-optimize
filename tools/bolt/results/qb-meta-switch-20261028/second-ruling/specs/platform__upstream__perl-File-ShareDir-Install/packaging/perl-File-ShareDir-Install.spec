Name:           perl-File-ShareDir-Install
Version:        0.14
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Install shared files
Url:            https://metacpan.org/pod/File::ShareDir::Install
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-File-ShareDir-Install.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
File::ShareDir::Install allows you to install read-only data 
files from a distribution. It is a companion module to File::ShareDir,
which allows you to locate these files after installation.

It is a port of Module::Install::Share to ExtUtils::MakeMaker
with the improvement of only installing the files you want;
.svn, .git and other source-control junk will be ignored.

Please note that this module installs read-only data files; 
empty directories will be ignored.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%license LICENSE
