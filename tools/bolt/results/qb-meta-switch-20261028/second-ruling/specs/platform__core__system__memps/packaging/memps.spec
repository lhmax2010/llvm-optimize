Name:       memps
Summary:    Tool to summarize memory usage of processes, tmpfs and graphics memory usage
Version:    0.2.0
Release:    0
Group:      System/Utilities
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake


%description
memps displays information about current memory usage of processes (metrics like RSS, PSS, memory map of the process, clean and dirty pages), tmpfs and graphics memory usage information


%prep
%setup -q


%build
%cmake .

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install


%files
%manifest memps.manifest
%defattr(-,root,root,-)
%{_bindir}/memps
%license LICENSE
