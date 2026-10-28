Name:           perl-gettext
VCS:            platform/upstream/perl-gettext#197036a30a2da560adfbca1eaf9e68aa65a73ebd
Version:        1.07
Release:        1.13
License:        GPL-1.0 or Artistic-1.0
Summary:        Message handling functions
Group:          Development/Libraries/Perl
Url:            http://search.cpan.org/dist/gettext/
Source:         %{name}-%{version}.tar.gz
Source1001: 	perl-gettext.manifest
Source1002: 	LICENSE

BuildRequires:  perl

%description
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.

gettext(), dgettext(), and dcgettext() attempt to retrieve a string
matching their 'msgid' parameter within the context of the current locale.
dcgettext() takes the message's category and the text domain as parameters
while dcgettext() defaults to the LC_MESSAGES category and gettext()
defaults to LC_MESSAGES and uses the current text domain. If the string is
not found in the database, then 'msgid' is returned.

textdomain() sets the current text domain and returns the previously active
domain.

_bindtextdomain(domain, dirname)_ instructs the retrieval functions to look
for the databases belonging to domain 'domain' in the directory 'dirname'

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%check
make test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE

%changelog
