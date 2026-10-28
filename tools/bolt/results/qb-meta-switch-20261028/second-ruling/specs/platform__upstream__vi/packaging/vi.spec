Name:           vi
Version:        050325
Release:        1
License:        BSD-4-Clause-UC and BSD-4-Clause-Caldera

Summary:        The Traditional Vi

Url:            http://ex-vi.sourceforge.net/
Group:          Base/Utilities
Source:         http://prdownloads.sourceforge.net/ex-vi/ex-%{version}.tar.bz2
Source1:	vi.manifest
BuildRequires:	gcc
BuildRequires:  make
BuildRequires:  glibc-devel >= 2.2.2
BuildRequires:	ncurses-devel
Conflicts:      vim-base

%description
Compared to most of its many clones, the traditional vi is a rather small
program just with its extremely powerful editing interface, but lacking fancy
features like multiple undo, multiple screens, or syntax highlighting.
This port of vi has generally preserved the original style, terminal control,
and feature set. It adds support for international character sets, including
multibyte encodings such as UTF-8, and some minor enhancements that were not
present in BSD vi 3.7, but had been included in later vi versions for System V
or in POSIX.2.

%prep
%setup -q -n ex-%{version}

cp %{SOURCE1} .

%build
export CFLAGS="%{optflags} -Wall -pipe -fno-strict-aliasing -Wno-error=implicit-function-declaration"
export CFLAGS=$(echo "$CFLAGS" | sed 's/-D_FORTIFY_SOURCE=2/-D_FORTIFY_SOURCE=1/')

make

%install
%make_install

rm -Rf %{buildroot}%{_mandir}

%files
%defattr(-,root,root,-)
%manifest vi.manifest
%{_bindir}/edit
%{_bindir}/ex
%{_bindir}/vedit
%{_bindir}/vi
%{_bindir}/view
%{_libexecdir}/expreserve
%{_libexecdir}/exrecover
