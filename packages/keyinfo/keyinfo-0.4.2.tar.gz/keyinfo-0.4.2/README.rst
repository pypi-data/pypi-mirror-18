=======
keyinfo
=======

Python library to convert X.509 certificates to and from W3C XML Signature KeyInfo structures


Description
===========

This library provides functionlity to convert X.509 certificates to and from W3C XML Signature 
KeyInfo structures.  

For X.509, the module is based on the python "cryptography" module (which in turn is based on OpenSSL).  
The keyinfo library converts to and from *cryptography.x509.certificate* objects. For XML, the module 
is based on the *lxml* library.  (Future versions may also use the simpler 
ElementTree library).

If you want to generate KeyInfo structures, your code needs to use existing functionality in that library 
to create certificates, or to load certificates in common file formats like PEM. The keyinfo module then
allows you to convert these certificate objects to KeyInfo XML trees.  Then, using the lxml library, you 
can save those trees to file or otherwise process them. There first two export functions are the 
following:

- to_keyinfo_sig1 export to XML Signature version 1.0.  In this case the issuer and serial number are provided.
- to_keyinfo_sig11 exports to XML Signature version 1.1. In this case SHA256 and SHA512 X509 digests are provided. 

These functions take either a certificate or a list of certificate objects representing a certificate chain as
parameters.

From version 0.4, ff the SHA3 library is availble, additionally SHA3-256 and SHA3-515 digests are provided.

The following code show how to load a certificate from a PEM format and save it as a KeyInfo XML file.

.. code-block:: python

    from keyinfo import keyinfo
    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.hazmat.backends import default_backend
    from lxml import etree

    # set infile, outfile
    with open(infile, 'r') as f:
        data = f.read()
        cert = load_pem_x509_certificate(data, default_backend())
        cert_xml = keyinfo.to_keyinfo_sig1(cert)
        fd = open(outfile,'w')
        fd.write(etree.tostring(cert_xml, pretty_print=True))
        fd.close()

It turns out the *load_pem_x509_certificate* actually only loads the first certificate.  To load a chain
from a PEM file, you can use *load_pem_x509_certificate_chain* from *keyinfo*.

.. code-block:: python

    from keyinfo import keyinfo
    from lxml import etree

    # set infile, outfile
    with open(infile, 'r') as f:
        data = f.read()
        cert_list = keyinfo.load_pem_x509_certificate_chain(data)
        cert_xml = keyinfo.to_keyinfo_sig1(cert_list)
        fd = open(outfile,'w')
        fd.write(etree.tostring(cert_xml, pretty_print=True))
        fd.close()


If you want to parse KeyInfo structures, your code needs to parse the XML data using lxml. You can
then use the *from_keyinfo(keyinfo)* function to create a *cryptography.x509.certificate* object.
For backwards compatibility reasons, these functions return the first certificate only.

To load the full chain, you can an optional *chain* parameter, i.e. *from_keyinfo(keyinfo, chain=True)*.
The result then is a list of certificate objects.


  


Validation
==========

When loading certificates from KeyInfo, some consistency checks are done between the X509Digest and 
X509Issuerserial element and the X509Certificate objects.  If you want additional certificate validation,
including path validation, you can use pyopenssl or wait for a future release of cryptography that will
provide this functionality.

Tests and Examples
==================

The *tests* subdirectory has a complete test suite and *tests/data* has sample KeyInfo and PEM files 
used by the tests.



Version History
===============

0.4, 2016.12.07   SHA3 feature added

0.3.*, 2016.10.09  Fixed README 

0.3, 2016.10.08.  Support for certificate chains added.

0.2, 2016.04.01.  Provided readme, tests, examples, validation.

0.1.3, 2016.03.27. First public Release.

