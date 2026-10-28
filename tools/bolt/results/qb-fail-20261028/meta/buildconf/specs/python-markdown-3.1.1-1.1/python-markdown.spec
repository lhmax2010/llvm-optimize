%define srcname Markdown

Name:           python-markdown
VCS:            platform/upstream/python-markdown#4c7781a2d68d0187f782e696d9f2e393400eace1
Version:        3.1.1
Release:        1.1
Summary:        Markdown implementation in Python
Group:          Development/Languages
License:        BSD
URL:            http://www.freewisdom.org/projects/python-markdown/
Source0:        http://pypi.python.org/packages/source/M/%{srcname}/%{srcname}-%{version}.tar.gz
Source1001: python-markdown.manifest
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?rhel}
BuildRequires:  python-elementtree
Requires:       python-elementtree
%endif


%description
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.


%prep
%setup -q -n %{srcname}-%{version}

# remove shebangs
find markdown -type f -name '*.py' \
  -exec sed -i -e '/^#!/{1D}' {} \;


%build
cp %{SOURCE1001} .
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --prefix %{_prefix}


%files
%manifest %{name}.manifest
%{python_sitelib}/*
%{_bindir}/markdown_py


%changelog
* Wed Dec 23 2009 Anas Nashif <anas.nashif@intel.com> - 2.0.3
- Initial import into Moblin
* Thu Oct  8 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.
* Thu Aug 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-3
- Add requirement on python-elementtree, which was a separate package
  before Python 2.5.
- Re-add changelog entries accidentally removed earlier.
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Sat Jul 11 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-1
- Update to 2.0.1.
- Upstream stripped .py of the cmdline script.
* Sat Apr 25 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-1
- Update to 2.0.
- Adjusted source URL.
- License changed to BSD only.
- Upstream now provides a script to run markdown from the cmdline.
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.7-2
- Rebuild for Python 2.6
* Mon Aug  4 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.7-1
- New package.
