%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A password/passphrase strength checking and policy enforcement toolset
Name:		passwdqc
Version:	1.3.1
Release:	1
License:	BSD
Group:		System/Libraries
URL:		http://www.openwall.com/passwdqc/
Source0:	http://www.openwall.com/passwdqc/%name-%version.tar.gz
Source1:	http://www.openwall.com/passwdqc/%name-%version.tar.gz.sign
Requires:	pam_passwdqc >= %{version}-%{release}
BuildRequires:	pam-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
passwdqc is a password/passphrase strength checking and policy enforcement
toolset, including a PAM module (pam_passwdqc), command-line programs
(pwqcheck and pwqgen), and a library (libpasswdqc).

pam_passwdqc is normally invoked on password changes by programs such as
passwd(1).  It is capable of checking password or passphrase strength,
enforcing a policy, and offering randomly-generated passphrases, with
all of these features being optional and easily (re-)configurable.

pwqcheck and pwqgen are standalone password/passphrase strength checking
and random passphrase generator programs, respectively, which are usable
from scripts.

libpasswdqc is the underlying library, which may also be used from
third-party programs.

%package -n	%{libname}
Summary:        Libraries for password/passphrase strength checking and policy enforcement
Group:          System/Libraries

%description -n	%{libname}
passwdqc is a password/passphrase strength checking and policy enforcement
toolset, including a PAM module (pam_passwdqc), command-line programs
(pwqcheck and pwqgen), and a library (libpasswdqc).

libpasswdqc is the underlying library, which may also be used from
third-party programs.

%package -n	pam_passwdqc
Summary:	PAM module for passwdqc
Group:		System/Libraries

%description -n	pam_passwdqc
passwdqc is a password/passphrase strength checking and policy enforcement
toolset, including a PAM module (pam_passwdqc), command-line programs
(pwqcheck and pwqgen), and a library (libpasswdqc).

pam_passwdqc is normally invoked on password changes by programs such as
passwd(1).  It is capable of checking password or passphrase strength,
enforcing a policy, and offering randomly-generated passphrases, with
all of these features being optional and easily (re-)configurable.

%package -n	%{develname}
Summary:	Libraries and header files for building passwdqc-aware applications
Group:		Development/Other
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains development libraries and header files needed for
building passwdqc-aware applications.

%prep

%setup -q

%build
%make \
    CFLAGS_lib="%{optflags} -fPIC -DLINUX_PAM" \
    CFLAGS_bin="%{optflags} -fPIC" \
    LDFLAGS="%{ldflags}" \
    LDFLAGS_shared="%{ldflags} --shared" \
    LDFLAGS_shared_LINUX="%{ldflags} --shared"

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} \
    MANDIR=%{_mandir} SHARED_LIBDIR=/%{_lib} \
    DEVEL_LIBDIR=%{_libdir} SECUREDIR=/%{_lib}/security

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README
%config(noreplace) %{_sysconfdir}/passwdqc.conf
%{_bindir}/pwqcheck
%{_bindir}/pwqgen
%{_mandir}/man1/pwqcheck.1*
%{_mandir}/man1/pwqgen.1*
%{_mandir}/man5/passwdqc.conf.5*

%files -n pam_passwdqc
%defattr(-,root,root)
/%{_lib}/security/pam_passwdqc.so
%{_mandir}/man8/pam_passwdqc.8*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/lib*.so



%changelog
* Sat Nov 26 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-1mdv2012.0
+ Revision: 733618
- import passwdqc


* Sat Nov 26 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-1mdv2010.2
- initial Mandriva package
