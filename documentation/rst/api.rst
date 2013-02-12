API
=============================================

.. http:get:: /api/v1/search

   Search for multiple document types across multiple indexes. By default we search in all indexes for all available document types.

   Hits are sorted by relevance based on their similarity to the query (see query parameter ``q``).

   The query parameters ``brin``, ``board_id``, ``branch_id``, ``zip_code`` and ``city`` each act as a filter on the result set. When more than one filter is specified, an ``AND`` condition is formed between the filters.

   **Example: find all school branches in Amsterdam Zuidoost**

   .. parsed-literal::

      $ curl -i "http://<api_domain>/api/v1/search?city=AMSTERDAM%20ZUIDOOST&doctypes=vo_branch"

   Example response (only one hit with some of it's fields are shown here):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Length: 173883
      Date: Tue, 12 Feb 2013 12:19:49 GMT   
      Content-Type: application/json

      {
        "total": 22,
        "took": 14,
        "hits": [
          {
            "_index": "duo",
            "_type": "vo_branch",
            "_id": "2011-03AQ-0",
            "_score": 1
            "_source": {
              "name": "Open Sgm Bylmer Vath Havo Mavo Lhno Lto Leao",
              "address": {
                "city": "AMSTERDAM ZUIDOOST",
                "street": "Gulden Kruis 5",
                "zip_code": "1103BE"
              }
            }
          }
        ]
      }

   **Example: find all Lyceum's in the :ref:`schoolvodata` and :ref:`owinspdata` indexes**

   .. parsed-literal::

      $ curl -i "http://<api_domain>/api/v1/search?q=Lyceum&indexes=schoolvo,onderwijsinspectie"

   Example response (only one hit with some of it's fields are shown here):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Length: 67846
      Date: Tue, 12 Feb 2013 13:09:58 GMT
      Content-Type: text/javascript

      {
        "total": 22,
        "took": 14,
        "hits": [
          {
            "_index": "onderwijsinspectie",
            "_type": "vo_school",
            "_id": "01KL-0",
            "_score": 2.4677997,
            "_source": {
              "name": "Lorentz Lyceum",
              "address": {
                "city": "Arnhem",
                "street": "Groningensingel 1235",
                "zip_code": "6835 HZ"
              }
            }
          } 
        ]
      }

   :query q: a term based query that searchers the ``name``, ``address`` (``street``, ``city``, ``zip_code``) and ``website`` fields. When the query consists of multiple terms, an ``OR`` query is constructed between the terms. *Optional*.
   :query brin: filter results on ``brin``. *Optional*.
   :query board_id: filter results on ``board_id``. *Optional*.
   :query branch_id: filter results on ``branch_id``. *Optional*.
   :query zip_code: filter results on ``address.zip_code``. *Optional*.
   :query city: filter results on ``address.city``. *Optional*.
   :query indexes: comma separated list of index names that should be searched. *Optional*, *default*: search all available indexes.
   :query doctypes: comma separated list of document types that should be included in the search. *Optinal*, *default*: search all available doctypes.
   :query size: the number of documents to return. *Optional*, *default*: 10, *min*: 1, *max*: 50.
   :query from: the offset from the first result in the result set. For example, when ``size=10`` and the total number of hits is 20, ``from=10`` will return result 10 to 20. *Optional*, *default*: 0.
   :statuscode 200: OK, no error
   :statuscode 400: Bad Request. An accompanying error message will explain why the request was invalid.

.. http:get:: /get_docment/(str:index)/(str:doctype)/(str:doc_id)
   
   :statuscode 200: no error
   :statuscode 404: document, collection or document type does not exist