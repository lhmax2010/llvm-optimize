Name:       ise-engine-glm
Summary:    Global Language Model ISE
Version:    1.0.18
Release:    1
Group:      Graphics & UI Framework/Input
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake

%description
ise-engine-glm is an GLM (Global Language Model) based input method
engine. it supports Pinyin and Stroke input mode for Chinese language,
and provides some usefull user interfaces using ISF.

%prep
%setup -q -n %{name}-%{version}

%build
%if 0%{?tizen_build_binary_release_type_eng}
export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"
%endif
CFLAGS="$CFLAGS -fvisibility=hidden "; export CFLAGS
CXXFLAGS="$CXXFLAGS -fvisibility=hidden -fvisibility-inlines-hidden ";export CXXFLAGS

rm -rf CMakeFiles
rm -rf CMakeCache.txt

%cmake .

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/usr/share/scim/glm
%make_install

%post


%postun


%files
%manifest %{name}.manifest
%defattr(-,root,root)
/usr/share/packages/%{name}.xml
/usr/share/scim/ise-engine-glm/*
%{_libdir}/scim-1.0/1.4.0/IMEngine/*.so
%license LICENSE
