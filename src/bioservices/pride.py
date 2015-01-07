# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      https://github.com/cokelaer/bioservices
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  source: http://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################

"""Interface to PRIDE web service

.. topic:: What is PRIDE ?

    :URL: http://www.ebi.ac.uk/pride/ws/
    :URL: http://www.ebi.ac.uk/pride/ws/

    .. highlights::

        TODO

        -- From PRIDE web site, Jan 2015


"""
#from decorator import decorator
import wrapt

from bioservices.services import REST

__all__ = ["PRIDE"]


@wrapt.decorator
def params_to_update(wrapped, instance, args, kwargs):
    vars(wrapped)['actual_kwargs'] = kwargs
    return wrapped(*args, **kwargs)



class PRIDE(REST):
    """Interface to the `PRIDE <http://rest.ensembl.org>`_ service

    For the BioServices documentation see the documentation of
    each method for the list of parameters. The API was copied
    from the Ensemble API (http://rest.ensembl.org)

    All methods have been tests using this BioServices
    `notebook <http://nbviewer.ipython.org/github/bioservices/notebooks/blob/master/ensembl/Ensembl.ipynb>`_


    .. todo:: There are 3 methods out of 50 that are not implemented so far.
    .. todo:: some methods have a parameter called *feature*. The official
       Ensembl API allows one to provide several features at the same time.
       This is not yet implemented. Only one at a time is accepted.
    """
    _url = "http://www.ebi.ac.uk/pride/ws/archive"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(PRIDE, self).__init__(name="PRIDE", url=PRIDE._url,
                verbose=verbose, cache=cache)

    def get_project_accession(self, identifier):
        """Retrieve project information by accession

        :param str identifier: a valid PRIDE identifier e.g., PRD000001
        :return: a dictionary with the project details

        .. doctest::


            >>> from bioservices import PRIDE
            >>> p = PRIDE()
            >>> res = p.get_project_accession("PRD000001")
            >>> res['numPeptides']
            6758

        """
        res = self.http_get('project/%s' % identifier)
        return res

    @params_to_update
    def get_project_list(self, query="", show=10, page=0, sort=None, order='desc',
                         speciesFilter=None, ptmsFilter=None, tissueFilter=None, diseaseFilter=None,
                         titleFilter=None, instrumentFilter=None, experimentTypeFilter=None,
                         quantificationfilter=None, projectTagFilter=None):
        """list projects or given criteria

        TODO: parameters documentation from http://www.ebi.ac.uk/pride/ws/archive/
        ::

            >>> p = PRIDE()
            >>> projects = p.get_project_list(show=100)

        """
        params = self.get_project_list.actual_kwargs

        res = self.http_get('project/list', params=params)
        try:
            res = res['list']
        except:
            pass
        return res

    @params_to_update
    def get_project_count(self,
        query="", show=10, page=0, sort=None, order='desc',
                         speciesFilter=None, ptmsFilter=None, tissueFilter=None, diseaseFilter=None,
                         titleFilter=None, instrumentFilter=None, experimentTypeFilter=None,
                         quantificationfilter=None, projectTagFilter=None):

        """Count  projects for given criteria
        
        .. todo:: show and sort and others probably not required.
        """
        params = self.get_project_count.actual_kwargs
        res = self.http_get('project/count', params=params)

        return res

