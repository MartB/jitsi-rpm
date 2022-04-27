%global project jitsi
%global project_version 7210
%global user %{name}

Name:       jicofo
Version:    2.0.%{project_version}
Release:    0.3%{?dist}
Summary:    Jitsi Conference Focus
Url:        https://jitsi.org
License:    ASL 2.0
Source0:    https://github.com/%{project}/%{name}/archive/stable/%{project}-meet_%{project_version}.tar.gz
Source1:    config
Source2:    sip-communicator.properties
Source3:    %{name}.service
Source4:    %{name}.sysusers
Source5:    %{name}.tmpfiles
Source6:    README.fedora
Source7:    jicofo.sh
Patch1:     0001-log-to-syslog.patch

BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  maven-local
BuildRequires:  java-latest-openjdk-devel
BuildRequires:  systemd-rpm-macros

Requires:       jre-headless
Requires:       systemd
%{?sysusers_requires_compat}

%description
Jitsi Conference Focus is a server side focus component used in
Jitsi conferences.

Conference focus is a mandatory component of the Jitsi conferencing
system next to the videobridge. It is responsible for managing media
sessions between each of the participants and the videobridge.
Whenever new conference is about to start an IQ is sent to the component
to allocate new a focus instance. After that a special focus participant
joins the Multi User Chat room and creates sessions between Jitsi
videobridge and the participants.

Jitsi is a set of open-source projects that allows you to easily
build and deploy secure video conferencing solutions. At the heart
of Jitsi are Jitsi Videobridge and Jitsi Meet, which let you have
conferences on the internet, while other projects in the community
enable other features such as audio, dial-in, recording, and
simulcasting.

See /usr/share/doc/jicofo/README-fedora.md for setup
instructions.


#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%prep
%autosetup -p1 -n %{name}-stable-%{project}-meet_%{project_version}
%pom_xpath_inject //pom:manifest \
    '<addClasspath>true</addClasspath><useUniqueVersions>false</useUniqueVersions><classpathPrefix>lib</classpathPrefix><mainClass>org.jitsi.jicofo.Main</mainClass>'

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
# install -m 755 resources/%{name}.sh %{buildroot}%{_datadir}/%{name}/%{name}.sh
install -D -m 755 %{SOURCE7} %{buildroot}%{_libexecdir}/%{name}

# config
install -D -m 640 -t %{buildroot}%{_sysconfdir}/%{name}/ lib/logging.properties
install -D -m 640 -t %{buildroot}%{_sysconfdir}/%{name}/ %{SOURCE1} %{SOURCE2}

# rundir
install -d -m 0755 %{buildroot}%{_rundir}/%{name}/

# system config
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# documentation
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ *.md
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ doc/*.md
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
%{_libexecdir}/%{name}
%dir %attr(0750,root,%{user}) %{_sysconfdir}/%{name}/
%config(noreplace) %attr(0649,root,%{user}) %{_sysconfdir}/%{name}/*
%dir %attr(0700,%{user},%{user}) %{_rundir}/%{name}/

# system config
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf

#-- CHANGELOG -----------------------------------------------------------------#
%changelog
* Sun Dec 19 2021 Christopher Engelhard <ce@lcts.de> 2.0.6726-0.3
- rename dep java-latest-openjdk-devel

* Sun Dec 19 2021 Christopher Engelhard <ce@lcts.de> 2.0.6726-0.2
- update to 2.0.6726
- Misc. fixes for jicofo
- fix leftover macros in tmpfiles

* Mon Feb 08 2021 Christopher Engelhard <ce@lcts.de> 2.0.5390-3
- rebuild for git repo move

* Wed Feb 03 2021 Christopher Engelhard <ce@lcts.de> 2.0.5390-2
- Permit service to write to its rundir and config dir (Issue #4)

* Wed Jan 27 2021 Christopher Engelhard <ce@lcts.de> 2.0.5390-1
- Update to 5390

* Fri Dec 04 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-2
- Update README

* Sun Nov 29 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-1
- add proper documentation

* Fri Nov 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-0.5
- update and unify service files

* Fri Nov 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-0.4
- Update to 2.0.5142

* Wed Oct 07 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.3
- add plugins to prosody subpackage, use __jitsiFQDN__ in config files

* Mon Sep 28 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.2
- fix service files

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.1
- new package built with tito


