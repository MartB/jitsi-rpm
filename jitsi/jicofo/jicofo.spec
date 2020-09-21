%global meet_version 4966

Name:       jicofo
Version:    1.0_626
Release:    0%{?dist}
Summary:    Jitsi conference focus
Url:        https://jitsi.org
License:    ASL 2.0
Source0:    https://github.com/jitsi/%{name}/archive/stable/jitsi-meet_%{meet_version}.tar.gz
Source1:    jicofo.service
#Source2:    README.jitsi-meet

BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  maven-local
Requires:       systemd
Requires:       jre-headless

%description
blablablabla

#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%prep
%autosetup -p1 -n %{name}-stable-jitsi-meet_%{meet_version}


%build
# build & pack compiled output into archive
#mvn dependency:resolve
#mvn versions:set -DnewVersion="%{version}"

#xmvn dependency:resolve-plugins
#%mvn_build
mvn verify package

%install
#%mvn_install

#-- SCRIPTLETS -----------------------------------------------------------------#
%post
%systemd_post jicofo.service

%preun
%systemd_preun jicofo.service

%postun
%systemd_postun_with_restart jicofo.service

#-- FILES ---------------------------------------------------------------------#
%files

#-- CHANGELOG -----------------------------------------------------------------#
%changelog

