class Provider(object):
    issuer: str

    def __init__(self, issuer: str):
        self.issuer = issuer

    def client_config(self, client_id: str):
        return {
            'issuer': self.issuer,
            'client_id': client_id,
            'behaviour': {
                'response_types': ['id_token'],
                'scope': ['openid']
            },
            'request_args': {
                'response_mode': 'form_post'
            },
            'allow': {
                'issuer_mismatch': True
            }
        }


class AzureChinaProvider(Provider):
    PROVIDER_BASE_URL = 'https://login.partner.microsoftonline.cn/'

    def __init__(self, tenant_id: str):
        super(AzureChinaProvider, self).__init__(f'{self.PROVIDER_BASE_URL}{tenant_id}/v2.0')

