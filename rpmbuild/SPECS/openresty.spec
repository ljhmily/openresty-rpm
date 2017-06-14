Name:           openresty
Version:        1.11.2.3
Release:        15%{?dist}.l
Summary:        OpenResty, scalable web platform by extending NGINX with Lua

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            https://openresty.org/

Source0:        https://openresty.org/download/openresty-%{version}.tar.gz
Source1:        openresty.init
Source2:        openresty.log
Source3:        openresty.nginx
Source4:        openresty.nginx.service
Source5:        openresty.conf

#Patch0:         openresty-%{version}.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  gcc, make, perl, systemtap-sdt-devel
BuildRequires:  openresty-zlib-devel >= 1.2.11-1
BuildRequires:  openresty-openssl-devel >= 1.0.2k-1
BuildRequires:  openresty-pcre-devel >= 8.40-1
Requires:       openresty-zlib >= 1.2.11-1
Requires:       openresty-openssl >= 1.0.2k-1
Requires:       openresty-pcre >= 8.40-1
Requires:       gd-devel >= 2.0.35-26

# for /sbin/service
Requires(post):  chkconfig
Requires(preun): chkconfig, initscripts

AutoReqProv:        no

# spec文档中常用的几个宏(变量)
# /usr/lib/rpm/macros
# 1. RPM_BUILD_DIR:    /usr/src/redhat/BUILD
# 2. RPM_BUILD_ROOT:   /usr/src/redhat/BUILDROOT
# 3. %{_sysconfdir}:   /etc
# 4. %{_sbindir}：     /usr/sbin
# 5. %{_bindir}:       /usr/bin
# 6. %{_datadir}:      /usr/share
# 7. %{_mandir}:       /usr/share/man
# 8. %{_libdir}:       /usr/lib64
# 9. %{_prefix}:       /usr
# 10. %{_localstatedir}:   /usr/var
%define base_prefix         %{_usr}/local/%{name}
%define zlib_prefix         %{base_prefix}/zlib
%define pcre_prefix         %{base_prefix}/pcre
%define openssl_prefix      %{base_prefix}/openssl
%define ngx_conf            %{_sysconfdir}/nginx
%define ngx_sbin            %{_sbindir}
%define ngx_log             /var/log/nginx
%define ngx_pid             /var/run
%define ngx_lock            /var/lock/subsys


%description
This package contains the core server for OpenResty. Built for production
uses.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

By taking advantage of various well-designed Nginx modules (most of which
are developed by the OpenResty team themselves), OpenResty effectively
turns the nginx server into a powerful web app server, in which the web
developers can use the Lua programming language to script various existing
nginx C modules and Lua modules and construct extremely high-performance
web applications that are capable to handle 10K ~ 1000K+ connections in
a single box.


%package resty

Summary:        OpenResty command-line utility, resty
Group:          Development/Tools
Requires:       perl, openresty >= %{version}-%{release}
Requires:       perl(File::Spec), perl(FindBin), perl(List::Util), perl(Getopt::Long), perl(File::Temp), perl(POSIX), perl(Time::HiRes)

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description resty
This package contains the "resty" command-line utility for OpenResty, which
runs OpenResty Lua scripts on the terminal using a headless NGINX behind the
scene.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.


%package doc

Summary:        OpenResty documentation tool, restydoc
Group:          Development/Tools
Requires:       perl, perl(Getopt::Std), perl(File::Spec), perl(FindBin), perl(Cwd), perl(File::Temp), perl(Pod::Man), perl(Pod::Text)

%if (!0%{?rhel} || 0%{?rhel} < 7) && !0%{?fedora}
Requires:       groff
%endif

%if (0%{?rhel} && 0%{?rhel} >= 7) || 0%{?fedora}
Requires:       groff-base
%endif

Provides:       restydoc, restydoc-index, md2pod.pl

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description doc
This package contains the official OpenResty documentation index and
the "restydoc" command-line utility for viewing it.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.


%package opm

Summary:        OpenResty Package Manager
Group:          Development/Tools
Requires:       perl, openresty >= %{version}-%{release}, perl(Digest::MD5)
Requires:       openresty-doc >= %{version}-%{release}, openresty-resty >= %{version}-%{release}
Requires:       curl, tar, gzip
#BuildRequires:  perl(Digest::MD5)
Requires:       perl(Encode), perl(FindBin), perl(File::Find), perl(File::Path), perl(File::Spec), perl(Cwd), perl(Digest::MD5), perl(File::Copy), perl(File::Temp), perl(Getopt::Long)

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description opm
This package provides the client side tool, opm, for OpenResty Pakcage Manager (OPM).


%prep
%setup -q -n "openresty-%{version}"

#%patch0 -p1

%define __debug_install_post   \
	%{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"\
	%{nil}

%build
./configure \
	--prefix="%{base_prefix}" \
	--sbin-path="%{ngx_sbin}/nginx" \
	--conf-path="%{ngx_conf}/nginx.conf" \
	--pid-path="%{ngx_pid}/nginx.pid" \
	--error-log-path="%{ngx_log}/error.log" \
	--lock-path="%{ngx_lock}/nginx" \
	--with-cc-opt="-I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include" \
	--with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
	--with-debug \
	--with-pcre-jit \
	--without-http_rds_json_module \
	--without-http_rds_csv_module \
	--without-lua_rds_parser \
	--with-ipv6 \
	--with-stream \
	--with-stream_ssl_module \
	--with-http_v2_module \
	--with-mail \
	--with-mail_ssl_module \
	--without-mail_pop3_module \
	--without-mail_imap_module \
	--without-mail_smtp_module \
	--with-http_stub_status_module \
	--with-http_realip_module \
	--with-http_addition_module \
	--with-http_xslt_module \
	--with-http_image_filter_module \
	--with-http_auth_request_module \
	--with-http_secure_link_module \
	--with-http_random_index_module \
	--with-http_gzip_static_module \
	--with-http_sub_module \
	--with-http_dav_module \
	--with-http_flv_module \
	--with-http_mp4_module \
	--with-http_gunzip_module \
	--with-http_gzip_static_module \
	--with-http_degradation_module \
	--with-http_slice_module \
	--with-http_stub_status_module \
	--with-select_module \
	--with-poll_module \
	--with-threads \
	--with-file-aio \
	--with-luajit \
	--with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT' \
	--with-dtrace-probes \
	%{?_smp_mflags}


make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{base_prefix}/luajit/share/man
rm -rf %{buildroot}%{base_prefix}/luajit/lib/libluajit-5.1.a

mkdir -p %{buildroot}/usr/lib/openresty/
cp -rp %{base_prefix}/* %{buildroot}/usr/lib/openresty/

mkdir -p %{buildroot}/usr/bin
ln -sf %{base_prefix}/bin/resty %{buildroot}/usr/bin/
ln -sf %{base_prefix}/bin/restydoc %{buildroot}/usr/bin/
ln -sf %{base_prefix}/bin/opm %{buildroot}/usr/bin/
ln -sf %{ngx_sbin}/nginx %{buildroot}/usr/bin/%{name}

rm -f %{buildroot}/etc/nginx/nginx.conf
mkdir -p %{buildroot}/etc/nginx/conf.d
mkdir -p %{buildroot}/etc/nginx/sites-enabled
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/etc/logrotate.d
mkdir -p %{buildroot}/etc/sysconfig
mkdir -p %{buildroot}/usr/lib/systemd/system
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/%{name}
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/nginx
%{__install} -p -m 0644 %{SOURCE2} %{buildroot}/etc/logrotate.d/nginx
%{__install} -p -m 0644 %{SOURCE3} %{buildroot}/etc/sysconfig/nginx
%{__install} -p -m 0644 %{SOURCE4} %{buildroot}/usr/lib/systemd/system/nginx.service
%{__install} -p -m 0644 %{SOURCE5} %{buildroot}/etc/nginx/nginx.conf

mkdir -p %{buildroot}/var/lib/nginx/tmp/{client_body,fastcgi,proxy,scgi,uwsgi}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%pre
%post
#/sbin/chkconfig --add %{name}
if nginx -v -t; then
	systemctl enable nginx
fi

%preun
if [ $1 = 0 ]; then
	#/sbin/service %{name} stop >/dev/null 2>&1
	#/sbin/chkconfig --del %{name}
	systemctl stop nginx.service
	systemctl disable nginx.service
	rm -f %{ngx_pid}/nginx.pid
fi

%postun
if [ $1 = 0 ]; then
	rm -fr %{base_prefix}/bin
	rm -fr %{base_prefix}/luajit
	rm -fr %{base_prefix}/lualib
	rm -fr %{base_prefix}/nginx
	rm -fr %{base_prefix}/site
	rm -fr /usr/lib/openresty/
fi


%files
%defattr(-,root,root,-)

/etc/rc.d/init.d/%{name}
/usr/bin/%{name}
%{base_prefix}/bin/openresty
%{base_prefix}/site/lualib/
%{base_prefix}/luajit/*
%{base_prefix}/lualib/*
%{base_prefix}/nginx/html/*
%{base_prefix}/nginx/logs/
%{base_prefix}/nginx/sbin/*
%{base_prefix}/nginx/tapset/*

/usr/lib/openresty/zlib
/usr/lib/openresty/pcre
/usr/lib/openresty/openssl

/etc/rc.d/init.d/nginx
/usr/sbin/nginx
/etc/logrotate.d/nginx
/etc/sysconfig/nginx
/usr/lib/systemd/system/nginx.service
/var/lib/nginx/tmp/client_body
/var/lib/nginx/tmp/fastcgi
/var/lib/nginx/tmp/proxy
/var/lib/nginx/tmp/scgi
/var/lib/nginx/tmp/uwsgi
%config(noreplace) %{ngx_conf}/*
%config(noreplace) %{ngx_log}/
%config(noreplace) %{ngx_pid}/

%files resty
%defattr(-,root,root,-)

/usr/bin/resty
%{base_prefix}/bin/resty


%files doc
%defattr(-,root,root,-)

/usr/bin/restydoc
%{base_prefix}/bin/restydoc
%{base_prefix}/bin/restydoc-index
%{base_prefix}/bin/md2pod.pl
%{base_prefix}/bin/nginx-xml2pod
%{base_prefix}/pod/*
%{base_prefix}/resty.index


%files opm
%defattr(-,root,root,-)

/usr/bin/opm
%{base_prefix}/bin/opm
%{base_prefix}/site/manifest/
%{base_prefix}/site/pod/


%changelog
* Sat May 27 2017 Yichun Zhang (agentzh) 1.11.2.3-14
- bugfix: the openresty-opm subpackage did not depend on openresty-doc and openresty-resty.
* Sat May 27 2017 Yichun Zhang (agentzh) 1.11.2.3-14
- centos 6 and opensuse do not have the groff-base package.
* Sat May 27 2017 Yichun Zhang (agentzh) 1.11.2.3-13
- openresty-doc now depends on groff-base.
* Thu May 25 2017 Yichun Zhang (agentzh) 1.11.2.3-12
- added missing groff/pod2txt/pod2man dependencies for openresty-doc.
* Thu May 25 2017 Yichun Zhang (agentzh) 1.11.2.3-11
- added missing perl dependencies for openresty-opm, openresty-resty, and openresty-doc.
* Sun May 21 2017 Yichun Zhang (agentzh) 1.11.2.3-10
- removed the geoip nginx module since GeoIP is not available everywhere.
* Fri Apr 21 2017 Yichun Zhang (agentzh)
- upgrade to the OpenResty 1.11.2.3 release: http://openresty.org/en/changelog-1011002.html
* Sat Dec 24 2016 Yichun Zhang
- init script: explicity specify the runlevels 345.
* Wed Dec 14 2016 Yichun Zhang
- opm missing runtime dependencies curl, tar, and gzip.
- enabled http_geoip_module by default.
* Fri Nov 25 2016 Yichun Zhang
- opm missing runtime dependency perl(Digest::MD5)
* Thu Nov 17 2016 Yichun Zhang
- upgraded OpenResty to 1.11.2.2.
* Fri Aug 26 2016 Yichun Zhang
- use dual number mode in our luajit builds which should usually
be faster for web application use cases.
* Wed Aug 24 2016 Yichun Zhang
- bump OpenResty version to 1.11.2.1.
* Tue Aug 23 2016 zxcvbn4038
- use external packages openresty-zlib and openresty-pcre through dynamic linking.
* Thu Jul 14 2016 Yichun Zhang
- enabled more nginx standard modules as well as threads and file aio.
* Sun Jul 10 2016 makerpm
- initial build for OpenResty 1.9.15.1.

