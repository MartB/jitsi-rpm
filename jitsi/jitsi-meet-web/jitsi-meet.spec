%global web_version 1.0.4370

Name:       jitsi-meet
Version:    4966
Release:    1%{?dist}
Summary:    Jitsi videoconferencing server (meta package)
Url:        https://jitsi.org
License:    ASL 2.0
Source0:    https://github.com/jitsi/%{name}/archive/stable/%{name}_%{version}.tar.gz
Source1:    jitsi-meet.service
Source2:    README.jitsi-meet

BuildArch:      noarch
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  git
BuildRequires:  systemd-rpm-macros
Requires:       systemd
Requires:       jitsi-meet-web = %{web_version}
Requires:       jitsi-videobridge = 0.0
Requires:       jicofo = 0.0
Suggests:       jibri = 0.0
Suggests:       jitsi-meet-turnserver = %{web_version}

%description
blablablabla

%package web
Summary:        Jitsi videoconferencing server - webapp
Version:        %{web_version}
BuildArch:      noarch
Requires:       jre-headless
Recommends:     %{name}-web-nginx if nginx

%description web
blablablablaba

%package prosody
Summary:        Jitsi videoconferencing server - prosody config
BuildArch:      noarch
Requires:       prosody

%description prosody
blablabla

%package turnserver
Summary:        Jitsi videoconferencing server - TURN server config
Version:        %{web_version}
BuildArch:      noarch
Recommends:     coturn

%description turnserver
blablablabla

#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%prep
%autosetup -p1 -n %{name}-stable-%{name}_%{version}

%build
# build & pack compiled output into archive
npm install
make
make source-package
cp %{SOURCE2} .

%install
install -m 0755 -p -d %{buildroot}%{_datadir}/%{name}-web
install -m 0755 -p -d %{buildroot}%{_sysconfdir}/%{name}-web
install -m 0755 -p -d %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
tar xjvf jitsi-meet.tar.bz2 -C %{buildroot}%{_datadir}/%{name}-web --strip 1



for country in $(ls "node_modules/i18n-iso-countries/langs"); do
    install -m644 "node_modules/i18n-iso-countries/langs/${country}" %{buildroot}%{_datadir}/%{name}-web/lang/countries-${country}
done

#find "%{buildroot}%{_datadir}/%{name}-web" -type f -execdir sed -i "s#%{_buildirdir}##g" "{}" \;
#find "%{buildroot}%{_datadir}/%{name}-web" -type d -exec chmod 755 {} \;

for conffile in interface_config.js logging_config.js config.js; do
    install -Dm644 %{buildroot}%{_datadir}/%{name}-web/${conffile} %{buildroot}%{_sysconfdir}/%{name}-web/${conffile}
    ln -sf %{_sysconfdir}/%{name}-web/${conffile} %{buildroot}%{_datadir}/%{name}-web/${conffile}
done


#-- SCRIPTLETS -----------------------------------------------------------------#
%post
%systemd_post jitsi.service

%preun
%systemd_preun jitsi.service

%postun
%systemd_postun_with_restart jitsi.service

#-- FILES ---------------------------------------------------------------------#
%files
%license LICENSE
%doc README.jitsi-meet
%{_unitdir}/%{name}.service

%files web
%license LICENSE
%doc doc/
%dir %{_sysconfdir}/%{name}-web/
%config(noreplace) %{_sysconfdir}/%{name}-web/*
%{_datadir}/%{name}-web

#-- CHANGELOG -----------------------------------------------------------------#
%changelog

