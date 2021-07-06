%global srcname pynetbox

Name:           python-%{srcname}
Version:        3.3.1
Release:        0%{?dist}
Summary:        Python API client library for Netbox

License:        ASL 2.0
URL:            https://github.com/digitalocean/pynetbox
Source:         https://github.com/netbox-community/pynetbox/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

%global _description \
%{summary}.

%description %{_description}

%package     -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-requests
BuildRequires:  python-six
Requires:       python-requests
Requires:       python-six
Requires:       python-netaddr
%description -n python2-%{srcname} %{_description}

Python 2 version.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build

%install
%py2_install

%check

%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{srcname}-*.egg-info/

%changelog
* Sat Jun 26 2021 Antonio Huete <ahuete@evicertia.com> - 3.3.1-0
- Initial package for evirpms
