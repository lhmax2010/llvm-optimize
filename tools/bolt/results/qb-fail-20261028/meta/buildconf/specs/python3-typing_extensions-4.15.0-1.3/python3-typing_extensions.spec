Name:           python3-typing_extensions
VCS:            platform/upstream/python3-typing_extensions#a1884033297fd6822e3fbf8cb466bff2cc17402e
Version:        4.15.0
Release:        1.3
Summary:        Backported and Experimental Type Hints for Python 3.8+
License:        Python-2.0
URL:            https://github.com/python/typing_extensions
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildArch:      noarch

%description
The typing_extensions module serves two related purposes:

  * Enable use of new type system features on older Python versions.
    For example, typing.TypeGuard is new in Python 3.10, but
    typing_extensions allows users on previous Python versions to use
    it too.
  * Enable experimentation with new type system PEPs before they are
    accepted and added to the typing module.

New features may be added to typing_extensions as soon as they are
specified in a PEP that has been added to the python/peps repository.
If the PEP is accepted, the feature will then be added to typing for
the next CPython release. No typing PEP has been rejected so far, so
we haven't yet figured out how to deal with that possibility.

Starting with version 4.0.0, typing_extensions uses Semantic Versioning.
The major version is incremented for all backwards-incompatible changes.
Therefore, it's safe to depend on typing_extensions like this:
typing_extensions >=x.y, <(x+1),
where x.y is the first version that includes all features you need.

typing_extensions supports Python versions 3.7 and higher.
In the future, support for older Python versions will be dropped some time
after that version reaches end of life.

%prep
%setup -q -n typing_extensions-%{version}
cp %{SOURCE1} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/typing_extensions-%{version}-py3-*.whl

%files 
%license LICENSE
%{python3_sitelib}/*
%{python3_sitelib}/typing_extensions-%{version}.dist-info/*

