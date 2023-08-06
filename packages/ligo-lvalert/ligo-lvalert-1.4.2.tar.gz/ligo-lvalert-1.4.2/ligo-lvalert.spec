%define name              ligo-lvalert
%define version           1.4.2
%define unmangled_version 1.4.2
%define release           1

Summary:   LVAlert Client Tools
Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Source0:   %{name}-%{unmangled_version}.tar.gz
License:   GPL
Group:     Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:    %{_prefix}
BuildArch: noarch
Vendor:    Tanner Prestegard <tanner.prestegard@ligo.org>, Alexander Pace <alexander.pace@ligo.org>
Requires:  python ligo-common pyxmpp
BuildRequires: python-setuptools
Url:       https://wiki.ligo.org/DASWG/LVAlert

%description
LVAlert is an XMPP-based alert system. This package provides client
tools for interacting with the LVAlert jabber server.

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%exclude %{python_sitelib}/ligo/lvalert/*pyo
