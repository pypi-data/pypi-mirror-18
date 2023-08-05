import pymongo

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.resources.schema import Thing
from ereuse_devicehub.validation.validation import ALLOWED_WRITE_ROLES


class Account(Thing):
    """
    An account represents a physical person or an organization.
    """
    email = {
        'type': 'email',
        'required': True,
        'unique': True,
        'sink': 5
    }
    password = {
        'type': 'string',
        # 'required': True, todo active OR password required
        'minlength': 4,
        'sink': 4,
        'doc': 'Users can only see their own passwords.'
    }
    role = {
        'type': 'string',
        'allowed': set(Role.ROLES),
        'default': Role.BASIC,
        'doc': 'See the Roles section to get more info.',
        ALLOWED_WRITE_ROLES: Role.MANAGERS
    }
    token = {
        'type': 'string',
        'readonly': True,
    }
    name = {
        'type': 'string',
        'sink': 3,
        'description': 'The name of an account, if it is a person or an organization.'
    }
    organization = {
        'type': 'string',
        'sink': 1,
        'description': 'The name of the organization the account is in. Organizations can be inside other organizations.'
    }
    active = {
        'type': 'boolean',
        'default': True,
        'sink': -1,
        'description': 'Activate the account so you can start using it.',
        'doc': 'Inactive accounts cannot login, and they are created through regular events. `Employee` or below cannot see this parameter.'
    }
    blocked = {
        'type': 'boolean',
        'default': True,
        'sink': -2,
        'description': 'As a manager, you need to specifically accept the user by unblocking it\'s account.',
        ALLOWED_WRITE_ROLES: Role.MANAGERS
    }
    isOrganization = {
        'type': 'boolean',
        'sink': 2
    }
    databases = {  # todo set allowed for the active databases
        'type': 'databases',
        'required': True,
        ALLOWED_WRITE_ROLES: Role.MANAGERS,
        'teaser': False,
        'sink': -4,
    }
    defaultDatabase = {
        'type': 'string',  # todo If this is not set, the first databased in 'databases' it should be used
        ALLOWED_WRITE_ROLES: Role.MANAGERS,
        'teaser': False,
        'sink': -5
    }
    fingerprints = {
        'type': 'list',
        'readonly': True,
    }
    publicKey = {
        'type': 'string',
        'writeonly': True
    }


class AccountSettings(ResourceSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['PATCH', 'DELETE', 'GET']
    # the standard account entry point is defined as
    # '/accounts/<ObjectId>'. We define  an additional read-only entry
    # point accessible at '/accounts/<username>'.
    # Note that this regex is weak; it will accept more string that are not emails, which is fine; it is fast.
    additional_lookup = {
        'url': 'regex("[^@]+@[^@]+\.[^@]+")',
        'field': 'email',
    }
    # 'public_methods': ['POST'],  # Everyone can create an account, which will be blocked (not active)

    datasource = {
        'projection': {'token': 0},  # We exclude from showing tokens to everyone
        'source': 'accounts'
    }

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    cache_control = ''
    cache_expires = 0

    # Allow 'token' to be returned with POST responses
    extra_response_fields = ResourceSettings.extra_response_fields + ['token', 'email', 'role', 'active', 'name',
                                                                      'databases', 'defaultDatabase', 'organization',
                                                                      'isOrganization']

    # Finally, let's add the schema definition for this endpoint.
    _schema = Account

    mongo_indexes = {
        'email': [('email', pymongo.DESCENDING)],
        'name': [('name', pymongo.DESCENDING)],
        'email and name': [('email', pymongo.DESCENDING), ('name', pymongo.DESCENDING)]
    }

    get_projection_blacklist = {  # whitelist has more preference than blacklist
        '*': ('password',),  # No one can see password
        Role.EMPLOYEE: ('active',)  # Regular users cannot see if someone is active or not
    }
    get_projection_whitelist = {
        'author': ('password', 'active')  # Except the own author
    }
    allowed_item_write_roles = {Role.AMATEUR}  # Amateur can write it's account
    use_default_database = True  # We have a common shared database with accounts


unregistered_user = {
    'email': Account.email,
    'name': Account.name,
    'organization': Account.organization,
    'isOrganization': Account.isOrganization
}
