%global project jitsi
%global project_version 5142

Name:       jitsi-meet
Version:    2.0.%{project_version}
Release:    0.10%{?dist}
Summary:    Jitsi Videoconferencing Web App
Url:        https://jitsi.org
License:    ASL 2.0
Source0:    https://github.com/%{project}/%{name}/archive/stable/%{project}-meet_%{project_version}.tar.gz
Source1:    README.fedora
Source2:    README.meta
Source3:    jitsi-meet.prosody
Source4:    jitsi-meet.nginx
Source5:    jitsi-meet.apache
Source6:    jitsi-meet.tmpfiles

# config.js for now, but in future generate other config via patch as well
# this makes it easier to pick up changes upstream
Patch0:     0001-harmonize-placeholders.patch
Patch1:     0002-disable-thirdparty.patch
#Patch2:     0003-use-system-ssl-conf.patch

BuildArch:      noarch
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  git
BuildRequires:  systemd-rpm-macros
Requires:       jre-headless

%description
blablablabla

See /usr/share/doc/jitsi-meet/README.fedora for details.


%package -n %{project}
Summary:        Jitsi Videoconferencing Server (meta package)
Version:        %{project_version}
BuildArch:      noarch
Requires:       %{name} = 2.0.%{project_version}
Requires:       jitsi-videobridge = 2.0.%{project_version}
Requires:       jicofo = 2.0.%{project_version}
Requires:       %{name}-prosody = 2.0.%{project_version}
Requires:       %{name}-webconfig = 2.0.%{project_version}
Suggests:       coturn
Suggests:       jibri = 8.0
Suggests:       jigasi = 1.1

%description -n %{project}
blablablablaba

This is a meta package that pulls in all components needed to
set up a single-machine Jitsi Videoconferencing Server

See /usr/share/doc/jitsi/README.fedora for details.


%package prosody
Summary:        Jitsi Videoconferencing Server (prosody config)
Version:        2.0.%{project_version}
BuildArch:      noarch
Requires:       prosody

%description prosody
Prosody configuration files for the Jitsi Videoconferencing Server


%package nginx
Summary:        Jitsi Videoconferencing Server (nginx config)
Version:        2.0.%{project_version}
BuildArch:      noarch
Requires:       nginx
Requires:       %{name} = 2.0.%{project_version}
Provides:       %{name}-webconfig = 2.0.%{project_version}

%description nginx
Nginx configuration files for the Jitsi Videoconferencing Server


%package apache
Summary:        Jitsi Videoconferencing Server (apache config)
Version:        2.0.%{project_version}
BuildArch:      noarch
Requires:       httpd
Requires:       %{name} = 2.0.%{project_version}
Provides:       %{name}-webconfig = 2.0.%{project_version}

%description apache
Apache configuration files for the Jitsi Videoconferencing Server


#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%prep
%autosetup -p1 -n %{name}-stable-%{project}-meet_%{project_version}

%build
# build & pack compiled output into archive
npm install
make
make source-package
cp %{SOURCE2} .

%install
# site
install -m 0755 -p -d %{buildroot}%{_datadir}/%{name}
tar xjvf jitsi-meet.tar.bz2 -C %{buildroot}%{_datadir}/%{name} --strip 1

for country in $(ls "node_modules/i18n-iso-countries/langs"); do
    install -m644 "node_modules/i18n-iso-countries/langs/${country}" %{buildroot}%{_datadir}/%{name}/lang/countries-${country}
done

# prosody plugins
install -d -m 0755 %{buildroot}%{_datadir}/%{name}-prosody/
cp -rp resources/prosody-plugins %{buildroot}%{_datadir}/%{name}-prosody/plugins

# config
install -m 0755 -p -d %{buildroot}%{_sysconfdir}/%{name}
for conffile in interface_config.js logging_config.js config.js; do
    install -D -m 0644 %{buildroot}%{_datadir}/%{name}/${conffile} %{buildroot}%{_sysconfdir}/%{name}/${conffile}
    ln -sf %{_sysconfdir}/%{name}/${conffile} %{buildroot}%{_datadir}/%{name}/${conffile}
done
install -D -m 0640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prosody/conf.d/jitsi-meet.cfg.lua
install -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/nginx/conf.d/jitsi-meet.conf
install -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/httpd/conf.d/jitsi-meet.conf
install -D -m 0644 %{SOURCE6} %{buildroot}%{_tmpfilesdir}/%{name}-prosody.conf

# documentation
install -D -m 0644 -t %{buildroot}%{_pkgdocdir}/ *.md
install -D -m 0644 -t %{buildroot}%{_pkgdocdir}/ doc/*.md
install -D -m 0644 %{SOURCE1} %{buildroot}%{_pkgdocdir}/README.fedora
install -D -m 0644 -t %{buildroot}%{_pkgdocdir}/config/ \
    doc/debian/jitsi-meet/jitsi-meet.example \
    doc/debian/jitsi-meet/jitsi-meet.example-apache \
    doc/debian/jitsi-meet-prosody/prosody.cfg.lua-jvb.example \
    doc/debian/jitsi-meet-turn/turnserver.conf
install -m 0644 %{SOURCE2} ./README.fedora

#-- FILES ---------------------------------------------------------------------#
%files
%doc %{_pkgdocdir}/
%license LICENSE
%{_datadir}/%{name}/
%dir %attr(0755,root,root) %{_sysconfdir}/%{name}/
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/%{name}/*

%files -n %{project}
%doc README.fedora
%license LICENSE

%files prosody
%license LICENSE
%{_datadir}/%{name}-prosody/
%{_tmpfilesdir}/%{name}-prosody.conf
%config(noreplace) %attr(0640,root,prosody) %{_sysconfdir}/prosody/conf.d/jitsi-meet.cfg.lua

%files nginx
%license LICENSE
%config(noreplace) %{_sysconfdir}/nginx/conf.d/jitsi-meet.conf

%files apache
%license LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/jitsi-meet.conf

#-- CHANGELOG -----------------------------------------------------------------#
%changelog
* Sat Nov 28 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-0.10
- include tmpfile to set prosody conf permissions

* Fri Nov 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-0.9
- various corrections to config files
- create config.js from upstream via patches

* Fri Nov 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5142-0.8
- Update to 2.0.5142
- fix permissions for prosody config

* Wed Oct 07 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.7
- add plugins to prosody subpackage, use __jitsiFQDN__ in config files

* Wed Oct 07 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.6
- switch to virtual provides for web config subpackages
- fix wrong focus user

* Mon Sep 28 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.5
- correct boolean deps
- fix webserver conf conditional

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.4
- rich dependencies second try

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.3
- fix rich dependencies

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.2
- fix errors in jitsi-meet.spec

* Sun Sep 27 2020 Christopher Engelhard <ce@lcts.de> 2.0.5076-0.1
- new package built with tito


