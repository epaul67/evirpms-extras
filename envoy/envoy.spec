%define debug_package %{nil}
%define glibc_version 2.18
%define patchelf_version 0.14.3

Name:		envoy
Summary:	Envoy L7 Proxy
Version:	1.18.4
Release:	1%{?dist}
License:	MIT
URL:		https://www.envoyproxy.io/

Source0:	https://github.com/tetratelabs/archive-envoy/releases/download/v%{version}/envoy-v%{version}-linux-amd64.tar.xz
Source1:	https://ftp.gnu.org/gnu/glibc/glibc-%{glibc_version}.tar.xz
Source2:	https://github.com/NixOS/patchelf/releases/download/%{patchelf_version}/patchelf-%{patchelf_version}-x86_64.tar.gz
BuildRoot:     %{_tmppath}/%{name}-root


%description
Envoy is an L7 proxy and communication bus designed for large modern service oriented architectures.

%prep
tar -xvJf %{SOURCE0} 
tar -xvJf %{SOURCE1}
tar -xvzf %{SOURCE2}

%build
mkdir glibc-build
pushd glibc-build
../glibc-%{glibc_version}/configure --prefix=/opt/glibc-%{glibc_version}
make -j4
popd

./bin/patchelf --set-interpreter /opt/glibc-2.18/lib/ld-linux-x86-64.so.2 --set-rpath lib envoy-v%{version}-linux-amd64/bin/envoy

%install
rm -rf %{buildroot}

make -C glibc-build install_root=%{buildroot} install
install -p -D -m 0755 envoy-v%{version}-linux-amd64/bin/envoy %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/*
/opt/glibc-%{glibc_version}
%license LICENSE


%changelog
* Thu Jan 14 2022 Pablo Ruiz <pablo.ruiz@gmail.com> - 1.18.4
- Initial package release.

