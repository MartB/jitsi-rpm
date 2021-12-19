%global project jitsi
%global project_version 6726
%global user jvb

Name:       jitsi-videobridge
Version:    2.0.%{project_version}
Release:    0.1%{?dist}
Summary:    Jitsi Videobridge
Url:        https://jitsi.org
License:    ASL 2.0
Source0:    https://github.com/%{project}/%{name}/archive/stable/%{project}-meet_%{project_version}.tar.gz
Source1:    jvb.conf
Source2:    sip-communicator.properties
Source3:    %{name}.service
Source4:    %{name}.sysusers
Source5:    %{name}.tmpfiles
Source6:    %{name}.sysconfig
Source7:    %{name}.firewalld
Source8:    README.fedora
Patch1:     0001-log-to-syslog.patch
Patch2:     0002-reduce-log-verbosity.patch

BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  java-openjdk-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  firewalld-filesystem

Requires:       jre-headless
Requires:       systemd
%{?sysusers_requires_compat}
Recommends:     (%{name}-firewalld if firewalld)

%description
Video/audio bridge for the Jitsi videoconference system.

Jitsi Videobridge is an XMPP server component that allows for
multiuser video communication. Unlike the dedicated hardware
videobridges, Jitsi Videobridge does not mix the video channels
into a composite video stream, but only relays the received video
channels to all call participants. Therefore, while it does need
to run on a server with good network bandwidth and CPU power is
not that critical for performance.

Jitsi is a set of open-source projects that allows you to easily
build and deploy secure video conferencing solutions. At the heart
of Jitsi are Jitsi Videobridge and Jitsi Meet, which let you have
conferences on the internet, while other projects in the community
enable other features such as audio, dial-in, recording, and
simulcasting.

See /usr/share/doc/jitsi-videobridge/README-fedora.md for setup
instructions.

%package firewalld
Summary: Firewalld service definition for Jitsi Videobridge
Requires: %{name} = %{version}-%{release}
Requires: firewalld-filesystem

%description firewalld
This adds a service definition file for firewalld that opens the
required ports (10000/UDP) for the Jitsi Videobridge to function.


#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%prep
%autosetup -p1 -n %{name}-stable-%{project}-meet_%{project_version}

%build
# build & copy dependencies
mvn clean
mvn versions:set -DnewVersion="%{version}"
mvn package -DskipTests -Dassembly.skipAssembly=true install
mvn dependency:copy-dependencies -DincludeScope=runtime

%install
# program
install -D -m 644 -t %{buildroot}%{_datadir}/%{name}/lib/ jvb/target/dependency/*
install -D -m 644 -t %{buildroot}%{_datadir}/%{name}/lib/ jvb/lib/videobridge.rc
install -m 644 jvb/target/%{name}-%{version}.jar %{buildroot}%{_datadir}/%{name}/%{name}.jar
install -m 755 jvb/resources/jvb.sh %{buildroot}%{_datadir}/%{name}/

# config
install -D -m 640 -t %{buildroot}%{_sysconfdir}/%{name}/ jvb/lib/logging.properties config/log4j2.xml config/callstats-java-sdk.properties
install -D -m 640 -t %{buildroot}%{_sysconfdir}/%{name}/ %{SOURCE1} %{SOURCE2}

# rundir
install -d -m 0755 %{buildroot}%{_rundir}/%{name}/

# system config
install -D -m 644 config/20-jvb-udp-buffers.conf %{buildroot}%{_sysctldir}/%{name}.conf
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -m 644 %{SOURCE7} %{buildroot}%{_prefix}/lib/firewalld/services/jitsi-videobridge.xml

# documentation
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ *.md
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ doc/*.md
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ jvb/target/classes/reference.conf
install -D -m 644 %{SOURCE8} %{buildroot}/%{_pkgdocdir}/README-fedora.md

#-- SCRIPTLETS -----------------------------------------------------------------#
%pre
%sysusers_create_compat %{SOURCE4}

%post
%systemd_post %{name}.service
%sysctl_apply %{name}.conf

%post firewalld
%firewalld_reload

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
%dir %attr(0700,%{user},root) %{_sysconfdir}/%{name}/
%config(noreplace) %attr(0644,%{user},root) %{_sysconfdir}/%{name}/*
%dir %attr(0755,%{user},%{user}) %{_rundir}/%{name}/

# system config
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_sysctldir}/%{name}.conf

%files firewalld
%{_prefix}/lib/firewalld/services/jitsi-videobridge.xml

#-- CHANGELOG -----------------------------------------------------------------#
%changelog
* Mon Feb 08 2021 Christopher Engelhard <ce@lcts.de> 2.0.5390-3
- rebuilt for git repo move
* Wed Feb 03 2021 Christopher Engelhard <ce@lcts.de> 2.0.5390-2
- Reduce log verbosity (Issue #3)

* Wed Jan 27 2021 Christopher Engelhard <ce@lcts.de> 2.0.5390-1
- Update to 5390

* Fri Dec 04 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-2
- update README
- add subpackage for firewalld service

* Sun Nov 29 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-1
- add documentation

* Sat Nov 28 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-0.7
- use _sysctldir instead of sysctl.d

* Fri Nov 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-0.6
- update and unify service files

* Fri Nov 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-0.5
- Update to 2.0.5142
- fix path to config file

* Wed Oct 07 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.4
- add plugins to prosody subpackage, use __jitsiFQDN__ in config files

* Mon Sep 28 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.3
- fix service files

* Mon Sep 28 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.2
- adapt configfile
- jvb: new style config

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.1
- new package built with tito


