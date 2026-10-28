Name:       behaviortree_cpp_v3
Summary:    behaviortree_cpp_v3
Version:    3.6.1
Release:    0
License:    MIT and Apache-2.0
Group:      Development/Tools
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires: cmake
BuildRequires: tinyxml2-devel

%description
This C++ library provides a framework to create BehaviorTrees. It was designed to be flexible, easy to use, reactive and fast.

%package devel
Summary:  %{name}-devel
Requires: %{name} = %{version}-%{release}
%description devel
%{name}-devel version %{version}

%prep
%setup -q

%build
cp %{SOURCE1001} .
mkdir build
cd build
%{cmake} -DBUILD_UNIT_TESTS=OFF ..
%{make_build}
cd -

%install
cd build
%{make_install}
cd -

%clean

######## ROS2 Files List #######
%files
%license LICENSE
%manifest %{name}.manifest
%{_prefix}/bin/*
%{_prefix}/lib/libbehaviortree_cpp_v3.so

%files devel
%license LICENSE
%manifest %{name}.manifest
%{_prefix}/lib/*/cmake
%{_prefix}/include/*

