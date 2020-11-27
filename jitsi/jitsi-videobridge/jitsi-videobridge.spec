%global project jitsi
%global project_version 5142
%global user jvb

Name:       jitsi-videobridge
Version:    2.0.%{project_version}
Release:    0.5%{?dist}
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
Source7:    README.fedora
Patch1:     0001-log-to-syslog.patch

BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  java-openjdk-devel
BuildRequires:  systemd-rpm-macros

Requires:       jre-headless
Requires:       systemd
%{?sysusers_requires_compat}

%description
blablablablabla

See /usr/share/doc/jitsi-videobridge/README.fedora for details.


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
# Create and empty key file and pid file to be marked as a ghost file below.
# i.e it is not actually included in the rpm, only the record of it is.
#touch %{buildroot}%{_rundir}/%{name}/%{name}.pid

# system config
install -D -m 644 config/20-jvb-udp-buffers.conf %{buildroot}%{_sysconfdir}/sysctl.d/%{name}.conf
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# documentation
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ *.md
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ doc/*.md
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ jvb/target/classes/reference.conf
install -D -m 644 %{SOURCE7} %{buildroot}/%{_pkgdocdir}/README.fedora

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
%dir %attr(0700,%{user},root) %{_sysconfdir}/%{name}/
%config(noreplace) %attr(0644,%{user},root) %{_sysconfdir}/%{name}/*
%dir %attr(0755,%{user},%{user}) %{_rundir}/%{name}/

# system config
%config(noreplace) %{_sysconfdir}/sysctl.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf

#-- CHANGELOG -----------------------------------------------------------------#
%changelog
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


