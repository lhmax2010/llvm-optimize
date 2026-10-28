Name:           python-pycrypto
Version:        2.6.1
Release:        0
Url:            http://www.pycrypto.org/
Summary:        Cryptographic modules for Python
License:        Public Domain
Group:          Development/Languages/Python
Source:         https://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz
Source1001:     python-pycrypto.manifest

BuildRequires:  pkgconfig(python)
BuildRequires:  gmp-devel

%description
The package contains:

  * Hash functions: MD2, MD4, RIPEMD, SHA256.
  * Block encryption algorithms: AES, ARC2, Blowfish, CAST, DES,
    Triple-DES, IDEA, RC5.
  * Stream encryption algorithms: ARC4, simple XOR.
  * Public-key algorithms: RSA, DSA, ElGamal, qNEW.
  * Protocols: All-or-nothing transforms, chaffing/winnowing.
  * Miscellaneous: RFC1751 module for converting 128-key keys into a
    set of English words, primality testing.
  * Some demo programs (currently all quite old and outdated).

%prep
%setup -q -n pycrypto-%{version}
cp %{SOURCE1001} .

%build
%{__python} setup.py build

# %check
# %{__python} setup.py test

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}


%files
%manifest %{name}.manifest
%license COPYRIGHT
%{python_sitearch}/Crypto/
%{python_sitearch}/pycrypto-%{version}-py*.egg-info
