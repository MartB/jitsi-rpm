%global meet_version 4966

Name:       jicofo
Version:    1.0_626
Release:    0%{?dist}
Summary:    Jitsi conference focus
Url:        https://jitsi.org
License:    ASL 2.0
Source0:    https://github.com/jitsi/%{name}/archive/stable/jitsi-meet_%{meet_version}.tar.gz
Source1:    config
Source2:    sip-communicator.properties
Source3:    jicofo.service
Source4:    sysusers.conf
Source5:    tmpfiles.conf
Source6:    README.fedora

BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  java-openjdk-devel
BuildRequires:  systemd-rpm-macros
Requires:       systemd
Requires:       jre-headless

%description
blablablabla

#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%prep
%autosetup -p1 -n %{name}-stable-jitsi-meet_%{meet_version}


%build
# build & pack compiled output into archive
mvn clean
mvn versions:set -DnewVersion="%{version}"
mvn package -DskipTests -Dassembly.skipAssembly=true
mvn dependency:copy-dependencies -DincludeScope=runtime

%install
# jicofo directories
install -p -d %{buildroot}%{_datadir}/%{name}/
install -p -d %{buildroot}%{_sysconfdir}/%{name}/
install -p -d %{buildroot}%{_localstatedir}/%{name}/

# jicofo files
install -D -m 644 -t %{buildroot}%{_datadir}/%{name}/lib/ target/dependency/*
install -D -m 644 target/jicofo*.jar %{buildroot}%{_datadir}/%{name}/%{name}.jar
install -D -m 755 resources/jicofo.sh %{buildroot}%{_datadir}/%{name}/%{name}.sh

install -D -m 640 lib/logging.properties %{buildroot}%{_sysconfdir}/%{name}/logging.properties
install -D -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/config
install -D -m 640 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/sip-communicator.properties

# systemd files & directories
install -p -d %{buildroot}%{_unitdir}/
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -p -d %{buildroot}%{_tmpfilesdir}/
install -D -m 644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -d %{buildroot}%{_sysuserdir}/
install -D -m 644 %{SOURCE5} %{buildroot}%{_sysusersdir}/%{name}.conf

# documentation
install -p -d %{buildroot}%{_pkgdocdir}
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ *.md
install -D -m 644 -t %{buildroot}/%{_pkgdocdir}/ doc/*.md
install -D -m 644 %{SOURCE6} %{buildroot}/%{_pkgdocdir}/README.fedora

#-- SCRIPTLETS -----------------------------------------------------------------#
%post
%systemd_post jicofo.service

%preun
%systemd_preun jicofo.service

%postun
%systemd_postun_with_restart jicofo.service

#-- FILES ---------------------------------------------------------------------#
%files
%doc %{_pkgdocdir}
%license LICENSE
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%dir %{_localstatedir}/%{name}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf

#-- CHANGELOG -----------------------------------------------------------------#
%changelog

