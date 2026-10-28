Name:           perl-Module-Build
VCS:            platform/upstream/perl-Module-Build#904a0c94fb80bc593e606e8f2c79193dad26fd53
Version:        0.4234
Release:        1.1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Module::Build - Build and install Perl modules
Url:            https://metacpan.org/pod/Module::Build
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Module-Build.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl-inc-latest
BuildRequires:  perl-Software-License

%description
Module::Build is a system for building, testing, and installing Perl modules. 
It is meant to be an alternative to ExtUtils::MakeMaker. Developers may alter 
the behavior of the module through subclassing. It also does not require 
a make on your system - most of the Module::Build code is pure-perl 
and written in a very cross-platform way.

See "COMPARISON" for more comparisons between Module::Build and other installer tools.

To install Module::Build, and any other module that uses Module::Build 
for its installation process, do the following:

perl Build.PL       # 'Build.PL' script creates the 'Build' script
./Build             # Need ./ to ensure we're using this "Build" script
./Build test        # and not another one that happens to be in the PATH
./Build install

This illustrates initial configuration and the running of three 'actions'. 
In this case the actions run are 'build' (the default action), 'test', 
and 'install'. Other actions defined so far include:

build                          manifest
clean                          manifest_skip
code                           manpages
config_data                    pardist
diff                           ppd
dist                           ppmdist
distcheck                      prereq_data
distclean                      prereq_report
distdir                        pure_install
distinstall                    realclean
distmeta                       retest
distsign                       skipcheck
disttest                       test
docs                           testall
fakeinstall                    testcover
help                           testdb
html                           testpod
install                        testpodcoverage
installdeps                    versioninstall

You can run the 'help' action for a complete list of actions.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%license LICENSE
