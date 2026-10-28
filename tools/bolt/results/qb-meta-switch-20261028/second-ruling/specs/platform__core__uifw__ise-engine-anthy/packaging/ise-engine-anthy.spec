Name:       ise-engine-anthy
Summary:    Anthy (Japanese) Input Method Engine for ISF
Version:    1.0.13
Release:    1
Group:      Graphics & UI Framework/Input
License:    GPL-2.0+
URL:        http://sourceforge.jp/projects/scim-imengine/
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(isf)
BuildRequires:  pkgconfig(anthy)
BuildRequires:  pkgconfig(tizen-core-imf)

%description
ISF is an input service framework for TIZEN.
ise-engine-anthy is ISF IMEngine module for Japanese input method base.It converts Hiragana text to Kana Kanji mixed text.


%prep
%setup -q

%build
export CFLAGS="$CFLAGS -fvisibility=hidden -fPIC"
export CXXFLAGS="$CXXFLAGS -fvisibility=hidden -fPIC"
export CPPFLAGS="$CPPFLAGS -DEXPORTED=__attribute__\(\(visibility\(\\\"default\\\"\)\)\)"

./bootstrap
%configure --prefix=%{_prefix} --disable-static

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post

%postun

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_datadir}/scim/icons/*
%{_datadir}/locale/*
%{_datadir}/packages/*
%{_datadir}/scim/Anthy/*
%{_libdir}/scim-1.0/1.4.0/IMEngine/*
