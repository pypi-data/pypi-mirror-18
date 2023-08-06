from ..obisutils import *

def taxon2(id=None, **kwargs):
    '''
    Get taxon by ID

    :param id: [Fixnum] An OBIS taxon identifier

    :return: A dictionary

    Usage::

        from pyobis import taxon
        taxon.taxon(545439)
        taxon.taxon(402913)
        taxon.taxon(406296)
        taxon.taxon(415282)
    '''
    url = obis_baseurl + 'taxon/' + str(id)
    out = obis_GET(url, {}, **kwargs)
    return out
