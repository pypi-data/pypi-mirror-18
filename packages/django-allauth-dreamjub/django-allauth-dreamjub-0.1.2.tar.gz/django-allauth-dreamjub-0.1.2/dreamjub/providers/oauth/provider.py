from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class Scope(object):
    PROFILE = 'profile'
    COURSES = 'courses'
    EDIT = 'edit'


class DreamjubAccount(ProviderAccount):

    def get_avatar_url(self):
        return None

    def to_str(self):
        dflt = super(DreamjubAccount, self).to_str()
        return self.account.extra_data.get('username', dflt)


class DreamjubProvider(OAuth2Provider):
    id = 'dreamjub'
    name = 'Dreamjub'
    package = 'dreamjub.providers.oauth'
    account_class = DreamjubAccount

    def get_default_scope(self):
        scope = [Scope.PROFILE]
        return scope

    def extract_uid(self, data):
        return str(data['eid'])

    def extract_common_fields(self, data):
        return dict(
            email=data.get('email'),
            username=data.get('username'),
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            name="%s %s" % (data.get('firstName'), data.get('lastName')),
        )

    def extract_extra_data(self, data):
        return data


providers.registry.register(DreamjubProvider)
