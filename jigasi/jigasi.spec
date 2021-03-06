%global project jitsi
%global user %{name}
%global git_hash d792d0f612c6d7928f4a63c81f1c7836ec70a9aa
Name:       jigasi
Version:    %{git_hash}
Release:    0.5%{?dist}
Summary:    Jitsi Gateway to SIP
Url:        https://jitsi.org
License:    ASL 2.0
Source0:    https://github.com/%{project}/%{name}/archive/%{git_hash}.tar.gz
Source1:    config
Source2:    sip-communicator.properties
Source3:    %{name}.service
Source4:    %{name}.sysusers
Source5:    %{name}.tmpfiles
Source6:    README.fedora
Patch1:     0001-log-to-syslog.patch

BuildRequires:  maven
BuildRequires:  java-openjdk-devel
BuildRequires:  systemd-rpm-macros

Requires:       jre-headless
Requires:	systemd
%{?sysusers_requires_compat}

%description
SIP Gateway for the Jitsi videoconferencing system.

Jitsi is a set of open-source projects that allows you to easily
build and deploy secure video conferencing solutions. At the heart
of Jitsi are Jitsi Videobridge and Jitsi Meet, which let you have
conferences on the internet, while other projects in the community
enable other features such as audio, dial-in, recording, and
simulcasting.

See /usr/share/doc/jigasi/README-fedora.md for setup
instructions.


#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%global debug_package %{nil}
%prep
%autosetup -p1

%build
# build & copy dependencies
mvn clean
mvn versions:set -DnewVersion="%{version}"
mvn package -DskipTests -Dassembly.skipAssembly=true
mvn dependency:copy-dependencies -DincludeScope=runtime

%install
# program
install -D -m 644 -t %{buildroot}%{_datadir}/%{name}/lib/ target/dependency/*
install -m 644 target/%{name}-%{version}.jar %{buildroot}%{_datadir}/%{name}/%{name}.jar
install -m 755 %{name}.sh %{buildroot}%{_datadir}/%{name}/

# config
install -D -m 640 -t %{buildroot}%{_sysconfdir}/%{name}/ lib/logging.properties %{name}-home/callstats-java-sdk.properties
install -D -m 640 -t %{buildroot}%{_sysconfdir}/%{name}/ %{SOURCE1} %{SOURCE2}

# rundir
install -d -m 0755 %{buildroot}%{_rundir}/%{name}/
# Create and empty key file and pid file to be marked as a ghost file below.
# i.e it is not actually included in the rpm, only the record of it is.
touch %{buildroot}%{_rundir}/%{name}/%{name}.pid

# system config
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# documentation
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ *.md
install -D -m 644 %{SOURCE6} %{buildroot}/%{_pkgdocdir}/README-fedora.md

#-- SCRIPTLETS -----------------------------------------------------------------#
%pre
%sysusers_create_compat %{SOURCE4}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

#-- FILES ---------------------------------------------------------------------#
%files
%doc %{_pkgdocdir}/
%license LICENSE

# package files/dirs
%{_datadir}/%{name}/
%dir %attr(0700,%{user},%{project}) %{_sysconfdir}/%{name}/
%config(noreplace) %attr(0644,%{user},%{project}) %{_sysconfdir}/%{name}/*
%dir %attr(0755,%{user},%{user}) %{_rundir}/%{name}/
%ghost %attr(0644,%{user},%{user}) %{_rundir}/%{name}/%{name}.pid

# system config
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf

#-- CHANGELOG -----------------------------------------------------------------#
%changelog
* Mon Feb 08 2021 Christopher Engelhard <ce@lcts.de> 1.1-0.5
- Rebuild for git repo move

* Sun Nov 29 2020 Christopher Engelhard <ce@lcts.de> 1.1-0.4
- add documentation
* Wed Oct 07 2020 Christopher Engelhard <ce@lcts.de> 1.1-0.3
- add plugins to prosody subpackage, use __jitsiFQDN__ in config files

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 1.1-0.2
- jigasi is not noarch

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 1.1-0.1
- new package built with tito


