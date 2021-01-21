%define debug_package %{nil}

Name:		gdrive
Summary:	Google Drive CLI
Version:	2.1.1
Release:	1%{?dist}
License:	MIT
URL:		https://github.com/DroidFreak32/gdrive_cli

Source0:	https://github.com/DroidFreak32/gdrive_cli/releases/download/%{version}/gdrive-linux-x64
Source1:	https://raw.githubusercontent.com/DroidFreak32/gdrive_cli/development/LICENSE
BuildRoot:     %{_tmppath}/%{name}-root


%description
gdrive is a command line utility for interacting with Google Drive.


%prep

%build

%install
rm -rf %{buildroot}

# install binary
install -p -D -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}
cp %{SOURCE1} .


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/*
%license LICENSE


%changelog
* Thu Jan 21 2021 Pablo Ruiz <pablo.ruiz@gmail.com> - 2.1.1
- Initial package release.

