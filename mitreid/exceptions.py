class MitreIdException(Exception):
    '''
    Base exception for this library
    '''
    @classmethod
    def _wrap_requests_response(cls, res):
        try:
            res.raise_for_status()
        except Exception, e:
            raise cls(e)
