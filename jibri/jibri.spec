%global project jitsi
%global user %{name}

Name:       jibri
Version:    8.0
Release:    0.4%{?dist}
Summary:    Jitsi Broadcasting Infrastructure
Url:        https://jitsi.org
License:    ASL 2.0
Source0:    https://github.com/%{project}/%{name}/archive/v%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}-icewm.service
Source3:    %{name}-xorg.service
Source4:    %{name}.sysusers
Source5:    %{name}.tmpfiles
Source6:    README.fedora
Source7:    jibri-modules.conf
Source8:    jibri.sh
Source9:    config.json
Source10:   finalize_recording.sh
Patch1:     0001-log-to-syslog.patch

BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  maven-local
BuildRequires:  java-openjdk-devel
BuildRequires:  systemd-rpm-macros

Requires:       ffmpeg
Requires:       alsa-utils
Requires:       icewm
Requires:       xorg-x11-drv-dummy
Requires:       curl
Requires:       jre-headless
Requires:       systemd
%{?sysusers_requires_compat}

%description
Recoding/broadcasting component for the Jitsi videoconferencing system.

Jitsi is a set of open-source projects that allows you to easily
build and deploy secure video conferencing solutions. At the heart
of Jitsi are Jitsi Videobridge and Jitsi Meet, which let you have
conferences on the internet, while other projects in the community
enable other features such as audio, dial-in, recording, and
simulcasting.

See /usr/share/doc/jibri/README-fedora.md for setup
instructions.


#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%prep
%autosetup -p1
%pom_add_dep rusv:agafua-syslog:0.4:runtime
%pom_add_plugin :maven-jar-plugin:2.3 . \
    '<configuration><archive><manifest><addClasspath>true</addClasspath><useUniqueVersions>false</useUniqueVersions><classpathPrefix>lib</classpathPrefix><mainClass>${exec.mainClass}</mainClass></manifest></archive></configuration>'

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

# config
install -D -m 640 -t %{buildroot}%{_sysconfdir}/%{name}/ lib/logging.properties resources/debian-package/etc/%{project}/%{name}/*
install -D -m 640 %{SOURCE9} %{buildroot}%{_sysconfdir}/%{name}/config.json
# helper script
install -D -m 755 -t %{buildroot}%{_sysconfdir}/%{name}/ %{SOURCE10}

# rundir
install -d -m 0755 %{buildroot}%{_rundir}/%{name}/
install -d -m 0755 %{buildroot}%{_var}/spool/%{name}/
# Create an empty key file and pid file to be marked as a ghost file below.
# i.e it is not actually included in the rpm, only the record of it is.
touch %{buildroot}%{_rundir}/%{name}/%{name}.pid
# same for .asoundrc and .icewm/settings
touch %{buildroot}%{_rundir}/%{name}/.asoundrc
install -d -m 0755 %{buildroot}%{_rundir}/%{name}/.icewm
touch %{buildroot}%{_rundir}/%{name}/.icewm/settings

# system config
install -D -m 644 -t %{buildroot}%{_unitdir}/ %{SOURCE1} %{SOURCE2} %{SOURCE3}
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -D -m 644 -t %{buildroot}%{_sysconfdir}/modules-load.d/ %{SOURCE7}
install -D -m 755 %{SOURCE8} %{buildroot}%{_libexecdir}/%{name}

# documentation
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ *.md
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ doc/*.md
install -D -m 644 %{SOURCE6} %{buildroot}/%{_pkgdocdir}/README-fedora.md

#-- SCRIPTLETS -----------------------------------------------------------------#
%pre
%sysusers_create_compat %{SOURCE4}

%post
/usr/sbin/modprobe snd_aloop
%systemd_post %{name}.service %{name}-icewm.service %{name}-xorg.service

%preun
test "$1" == "0" && rm -rf %{_rundir}/%{name}/{.cache,.config,.local} || true
%systemd_preun %{name}.service %{name}-icewm.service %{name}-xorg.service

%postun
%systemd_postun_with_restart %{name}.service %{name}-icewm.service %{name}-xorg.service

#-- FILES ---------------------------------------------------------------------#
%files
%doc %{_pkgdocdir}/
%license LICENSE

# package files/dirs
%{_datadir}/%{name}/
%dir %attr(0750,root,%{user}) %{_sysconfdir}/%{name}/
%config(noreplace) %attr(0644,root,%{user}) %{_sysconfdir}/%{name}/*.{preferences,properties,conf,json}
%config(noreplace) %attr(0644,root,%{user}) %{_sysconfdir}/%{name}/asoundrc
%config(noreplace) %attr(0755,root,%{user}) %{_sysconfdir}/%{name}/*.sh
%dir %attr(0755,%{user},%{user}) %{_rundir}/%{name}/
%dir %attr(0755,%{user},%{user}) %{_rundir}/%{name}/.icewm
%dir %attr(0755,%{user},%{user}) %{_var}/spool/%{name}/
%ghost %attr(0644,%{user},%{user}) %{_rundir}/%{name}/%{name}.pid
%ghost %attr(0644,%{user},%{user}) %{_rundir}/%{name}/.asoundrc
%ghost %attr(0644,%{user},%{user}) %{_rundir}/%{name}/.icewm/settings

# system config
%{_unitdir}/*.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_sysconfdir}/modules-load.d/%{name}-*.conf
%{_libexecdir}/%{name}

#-- CHANGELOG -----------------------------------------------------------------#
%changelog
* Mon Feb 08 2021 Christopher Engelhard <ce@lcts.de> 8.0-0.4
- rebuild for git repo move

* Sun Nov 29 2020 Christopher Engelhard <ce@lcts.de> 8.0-0.3
- add documentation

* Wed Oct 07 2020 Christopher Engelhard <ce@lcts.de> 8.0-0.2
- add plugins to prosody subpackage, use __jitsiFQDN__ in config files

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 8.0-0.1
- new package built with tito


