%global ns_dir /opt/cpanel

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

%global with_systemd 1

Name:    ea-valkey72
Vendor:  cPanel, Inc.
Summary: Valkey
Version: 7.2.5
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 2
Release: %{release_prefix}%{?dist}.cpanel
License: BSD-3-Clause
Group:   System Environment/Daemons
URL: https://github.com/valkey-io/valkey

Source0: https://github.com/valkey-io/valkey/archive/refs/tags/%{version}.tar.gz
Source1: pkg.prerm
Source2: valkey.conf
Source3: podman_entrypoint.sh
Source4: ea-podman-local-dir-setup
Source5: README.md
Source6: pkg.postinst

# if I do not have autoreq=0, rpm build will recognize that the ea_
# scripts need perl and some Cpanel pm's to be on the disk.
# unfortunately they cannot be satisfied via the requires: tags.
Autoreq: 0

Requires: ea-podman

%description
Valkey is an open source key-value store that functions as a data structure server.

%prep

# nothing to do here

%build
# empty build section

%install

mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-valkey72
echo -n "%{version}-%{release_prefix}" > $RPM_BUILD_ROOT/opt/cpanel/ea-valkey72/pkg-version
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-valkey72/
cp %{SOURCE3} $RPM_BUILD_ROOT/opt/cpanel/ea-valkey72/
cp %{SOURCE4} $RPM_BUILD_ROOT/opt/cpanel/ea-valkey72/
cp %{SOURCE5} $RPM_BUILD_ROOT/opt/cpanel/ea-valkey72/README.md

cat << EOF > $RPM_BUILD_ROOT/opt/cpanel/ea-valkey72/ea-podman.json
{
    "ports" : [],
    "image" : "docker.io/valkey/valkey:%{version}",
    "startup" : {
        "-v"     : [
            ":/socket_dir",
            "valkey.conf:/usr/local/etc/valkey/valkey.conf",
            "podman_entrypoint.sh:/usr/local/bin/docker-entrypoint.sh"
       ]
    }
}
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%preun

%include %{SOURCE1}

%files
%defattr(0644,root,root,-)
/opt/cpanel/ea-valkey72
%attr(0755,root,root) /opt/cpanel/ea-valkey72/ea-podman-local-dir-setup
%attr(0755,root,root) /opt/cpanel/ea-valkey72/podman_entrypoint.sh

%changelog
* Tue May 14 2024 Brian Mendoza <brian.mendoza@cpanel.net> - 7.2.5-2
- ZC-11805 - Initial build

* Fri Apr 12 2024 Julian Brown <julian.brown@cpanel.net> - 7.2.5-1
- ZC-11761 - Evaluate Valkey