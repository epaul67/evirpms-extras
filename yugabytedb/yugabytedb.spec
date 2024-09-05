# Use md5 file digest method. 
# The first macro is the one used in RPM v4.9.1.1
%define _binary_filedigest_algorithm 1
# This is the macro I find on OSX when Homebrew provides rpmbuild (rpm v5.4.14)
%define _build_binary_file_digest_algo 1
%define debug_package %{nil}

# Use gzip payload compression
%define _binary_payload w9.gzdio 
%define _build_id_links none
%define appdir /opt/yugabytedb

%global debug_package %{nil}
%global __strip /bin/true
%global __jar_repack /bin/true

Name: yugabytedb
Version: 2.20.6.0
%define subversion b66
Release: 1%{?dist}
Source0: https://downloads.yugabyte.com/releases/%{version}/yugabyte-%{version}-%{subversion}-linux-x86_64.tar.gz
Source1: yugabyted.service
Source2: yugabytedb.conf
Source3: yugabyte-client-post_install.sh
Summary: YugabyteDB is a free and open-source, distributed, relational, NewSQL database management system
Group: default
License: Apache 2.0
URL: https://www.yugabyte.com/
BuildRoot: %{_tmppath}/%{name}-root
AutoReqProv: no

%description
YugabyteDB is a free and open-source, distributed, relational, NewSQL database management system designed to handle large amounts of data spanning across multiple availability zones and geographic regions while providing single-digit latency, high availability, and no single point of failure.

%package server
Summary: YugabyteDB is a free and open-source, distributed, relational, NewSQL database management system
Requires: python python-libs python-devel python3-pip
Requires: procps-ng
%if 0%{?rhel} < 8
BuildRequires: systemd
%else
BuildRequires: systemd-rpm-macros
%{?systemd_requires}
%endif
AutoReqProv: no

%description server
YugabyteDB is a free and open-source, distributed, relational, NewSQL database management system designed to handle large amounts of data spanning across multiple availability zones and geographic regions while providing single-digit latency, high availability, and no single point of failure.

%package client
Summary: YugabyteDB is a free and open-source, distributed, relational, NewSQL database client tools
AutoReqProv: no

%description client
YugabyteDB is a free and open-source, distributed, relational, NewSQL database management system designed to handle large amounts of data spanning across multiple availability zones and geographic regions while providing single-digit latency, high availability, and no single point of failure.

%prep
%setup -q -n yugabyte-%{version}

%build
# noop

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}
mkdir -p %{buildroot}/etc/yugabytedb
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}%{appdir}
mkdir -p %{buildroot}%{appdir}/bin
mkdir -p %{buildroot}%{appdir}/tools


%{__install} -m 644 %{SOURCE1} %{buildroot}/lib/systemd/system/yugabyted.service
%{__install} -d -m 640 %{buildroot}/var/log/yugabytedb
%{__install} -d -m 640 %{buildroot}/var/lib/yugabytedb
ls -l %{buildroot} %{buildroot}/etc %{buildroot}/etc/yugabytedb
%{__install} -m 640 %{SOURCE2} %{buildroot}/etc/yugabytedb/yugabytedb.conf
ln -s "%{appdir}/bin/yugabyted" "%{buildroot}/usr/bin/yugabyted"
ln -s "%{appdir}/bin/cqlsh" "%{buildroot}/usr/bin/cqlsh"
ln -s "%{appdir}/bin/ysqlsh" "%{buildroot}/usr/bin/ysqlsh"
ln -s "%{appdir}/bin/ycqlsh" "%{buildroot}/usr/bin/ycqlsh"

mv -f * %{buildroot}%{appdir}/
ls -al %{buildroot}/opt/yugabytedb
sed -i 's/.*#!.*python.*/\#!\/usr\/bin\/env\ python3/' %{buildroot}/opt/yugabytedb/bin/yugabyted
sed -i 's/.*#!.*python.*/\#!\/usr\/bin\/env\ python3/' %{buildroot}/opt/yugabytedb/bin/yb-ctl
sed -i 's/.*#!.*python.*/\#!\/usr\/bin\/env\ python3/' %{buildroot}/opt/yugabytedb/tools/yb-prof.py
sed -i 's/.*#!.*python.*/\#!\/usr\/bin\/env\ python3/' %{buildroot}/opt/yugabytedb/tools/k8s_preflight.py
sed -i 's/.*#!.*python.*/\#!\/usr\/bin\/env\ python3/' %{buildroot}/opt/yugabytedb/tools/k8s_parent.py
sed -i 's/.*#!.*python.*/\#!\/usr\/bin\/env\ python3/' %{buildroot}/opt/yugabytedb/tools/k8s_ybc_parent.py

# chown -R 301:301 . %{buildroot}/etc/yugabytedb %{buildroot}/var/log/yugabytedb %{buildroot}/var/lib/yugabytedb

# Find dead symlinks and repoint them to right path
find "%{buildroot}%{appdir}/linuxbrew/Cellar/ncurses/6.1/share/terminfo/" -xtype l -exec rm "{}" \;

ls -al %{buildroot}/opt/yugabytedb/bin/
ls -al %{buildroot}/opt/yugabytedb/postgres/bin/
ls -al %{buildroot}/usr/bin/

%{__install} -m 755 %{SOURCE3} %{buildroot}/opt/yugabytedb/bin/post_client_install.sh

find /builddir/build/BUILDROOT/yugabytedb-2.20.6.0-1.el9.x86_64/opt/yugabytedb/bin/

%clean
# noop

%pre server
getent group yugabyte >/dev/null 2>&1 || groupadd -r -g 301 yugabyte 
getent passwd yugabyte >/dev/null || \
    useradd -M -r \
	-u 301 \
	-g yugabyte \
	-d /var/lib/yugabytedb \
	-s /sbin/nologin \
    	-c "YugaByte database" yugabyte


%pre client
getent group yugabyte >/dev/null 2>&1 || groupadd -r -g 301 yugabyte 
getent passwd yugabyte >/dev/null || \
    useradd -M -r \
	-u 301 \
	-g yugabyte \
	-d /var/lib/yugabytedb \
	-s /sbin/nologin \
    	-c "YugaByte database" yugabyte

%post server

# post_install.sh is required after upgrade of the package
if [ -f "%{appdir}/.post_install.sh.completed" ]; then
  rm "%{appdir}/.post_install.sh.completed"
fi
%{appdir}/bin/post_install.sh

%systemd_post yugabyted.service

%post client

# post_install.sh is required after upgrade of the package
if [ -f "%{appdir}/.post_client_install.sh.completed" ]; then
  rm "%{appdir}/.post_client_install.sh.completed"
fi
%{appdir}/bin/post_client_install.sh

%preun server
%systemd_preun yugabyted.service

%postun server
%systemd_postun_with_restart yugabyted.service

# post_install.sh is required after upgrade of the package
if [ -f "%{appdir}/.post_install.sh.completed" ]; then
  rm "%{appdir}/.post_install.sh.completed"
fi

%postun client
%systemd_postun_with_restart yugabyted.service

# post_install.sh is required after upgrade of the package
if [ -f "%{appdir}/.post_client_install.sh.completed" ]; then
  rm "%{appdir}/.post_client_install.sh.completed"
fi

%files server
%defattr(-,root,root,-)
%dir %attr(755,root,root) /etc/yugabytedb
%config(noreplace) %attr(640,301,301) /etc/yugabytedb/yugabytedb.conf
%dir /opt/yugabytedb
%dir %attr(750,301,301) /var/log/yugabytedb
/lib/systemd/system/yugabyted.service
/usr/bin/yugabyted
/opt/yugabytedb/*

%files client
%defattr(-,root,root,-)
%dir /opt/yugabytedb
/usr/bin/cqlsh
/usr/bin/ysqlsh
/usr/bin/ycqlsh
/opt/yugabytedb/pylib/*
/opt/yugabytedb/linuxbrew/*
/opt/yugabytedb/bin/cqlsh
/opt/yugabytedb/bin/redis-cli
/opt/yugabytedb/bin/ysqlsh
/opt/yugabytedb/bin/ycqlsh
/opt/yugabytedb/bin/ycqlsh.py*
/opt/yugabytedb/bin/patchelf
/opt/yugabytedb/bin/post_client_install.sh
/opt/yugabytedb/postgres/bin/ysqlsh
/opt/yugabytedb/postgres/bin/ysql_dump
/opt/yugabytedb/postgres/bin/ysql_dumpall
/opt/yugabytedb/postgres/bin/pg_restore
/opt/yugabytedb/postgres/bin/pg_isready
/opt/yugabytedb/postgres/bin/pg_standby
/opt/yugabytedb/lib/*.zip
/opt/yugabytedb/lib/ld.so
/opt/yugabytedb/lib/yb/*
/opt/yugabytedb/lib/yb-thirdparty/*
/opt/yugabytedb/postgres/lib/*

