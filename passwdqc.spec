Summary: A password/passphrase strength checking and policy enforcement toolset
Name: passwdqc
Version: 2.0.3
Release: 1
# Two manual pages (pam_passwdqc.8 and passwdqc.conf.5) are under the
# 3-clause BSD-style license as specified within the files themselves.
# The rest of the files in this package fall under the terms of
# the heavily cut-down "BSD license".
License: BSD-3-Clause
URL: https://www.openwall.com/%name/
Source0: https://www.openwall.com/%{name}/%{name}-%{version}.tar.gz
Source1: https://www.openwall.com/%{name}/%{name}-%{version}.tar.gz.sign
Requires: pam_%{name} = %{EVRD}
Requires: %{name}-utils = %{EVRD}
BuildRequires: make
BuildRequires: pkgconfig(audit)
BuildRequires: gettext
BuildRequires: pam-devel

%define libname %mklibname passwdqc
%define devname %mklibname -d passwdqc

%package -n %{libname}
Summary: Passphrase quality checker shared library

%package -n %{devname}
Summary: Development files for building %name-aware applications
Requires: %{libname} = %{EVRD}

%package -n pam_%{name}
Summary: Pluggable passphrase quality checker
Requires: %{libname} = %{EVRD}

%package utils
Summary: Password quality checker utilities
Requires: %{libname} = %{EVRD}

%description
passwdqc is a password/passphrase strength checking and policy
enforcement toolset, including a PAM module (pam_passwdqc), command-line
programs (pwqcheck, pwqfilter, and pwqgen), and a library (libpasswdqc).

pam_passwdqc is normally invoked on password changes by programs such as
passwd(1).  It is capable of checking password or passphrase strength,
enforcing a policy, and offering randomly-generated passphrases, with
all of these features being optional and easily (re-)configurable.

pwqcheck and pwqgen are standalone password/passphrase strength checking
and random passphrase generator programs, respectively, which are usable
from scripts.

The pwqfilter program searches, creates, or updates binary passphrase
filter files, which can also be used with pwqcheck and pam_passwdqc.

libpasswdqc is the underlying library, which may also be used from
third-party programs.

%description -n %{libname}
A passphrase strength checking library.

In addition to checking regular passphrases, it offers support
for passphrases and can provide randomly generated passphrases.
All features are optional and can be (re-)configured without
rebuilding.

This package contains shared %name library.

%description -n %{devname}
A passphrase strength checking library.

In addition to checking regular passphrases, it offers support
for passphrases and can provide randomly generated passphrases.
All features are optional and can be (re-)configured without
rebuilding.

This package contains development files needed for building
%name-aware applications.

%description -n pam_%{name}
pam_%{name} is a passphrase strength checking module for
PAM-aware passphrase changing programs, such as passwd(1).
In addition to checking regular passphrases, it offers support
for passphrases and can provide randomly generated passphrases.
All features are optional and can be (re-)configured without
rebuilding.

%description utils
This package contains standalone utilities which are usable from scripts:
pwqcheck (a standalone passphrase strength checking program),
pwqgen (a standalone random passphrase generator program), and
pwqfilter (a standalone program that searches, creates, or updates
binary passphrase filter files).

%prep
%autosetup -p1

%build
make %{?_smp_mflags} all locales \
	CC="%{__cc}" LD="%{__cc}" \
	CPPFLAGS="-DENABLE_NLS=1 -DHAVE_LIBAUDIT=1 -DLINUX_PAM=1" \
	CFLAGS_lib="$RPM_OPT_FLAGS -W -DLINUX_PAM -fPIC" \
	CFLAGS_bin="$RPM_OPT_FLAGS -W"

%install
make install install_locales \
	CC=false LD=false \
	INSTALL='install -p' \
	DESTDIR="$RPM_BUILD_ROOT" \
	MANDIR=%{_mandir} \
	SHARED_LIBDIR=%{_libdir} \
	DEVEL_LIBDIR=%{_libdir} \
	SECUREDIR=%{_libdir}/security

%find_lang passwdqc

%files

%files -n %{libname} -f passwdqc.lang
%config(noreplace) %{_sysconfdir}/passwdqc.conf
%{_libdir}/lib*.so*
%{_mandir}/man5/*.5*
%doc LICENSE README *.php

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/pkgconfig/passwdqc.pc
%{_libdir}/lib*.so
%{_mandir}/man3/*.3*

%files -n pam_%{name}
%{_libdir}/security/*
%{_mandir}/man8/*.8*

%files utils
%{_bindir}/*
%{_mandir}/man1/*.1*
