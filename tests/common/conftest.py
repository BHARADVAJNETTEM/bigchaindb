import pytest


USER_PRIVATE_KEY = '8eJ8q9ZQpReWyQT5aFCiwtZ5wDZC4eDnCen88p3tQ6ie'
USER_PUBLIC_KEY = 'JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE'

USER2_PRIVATE_KEY = 'F86PQPiqMTwM2Qi2Sda3U4Vdh3AgadMdX3KNVsu5wNJr'
USER2_PUBLIC_KEY = 'GDxwMFbwdATkQELZbMfW8bd9hbNYMZLyVXA3nur2aNbE'

USER3_PRIVATE_KEY = '4rNQFzWQbVwuTiDVxwuFMvLG5zd8AhrQKCtVovBvcYsB'
USER3_PUBLIC_KEY = 'Gbrg7JtxdjedQRmr81ZZbh1BozS7fBW88ZyxNDy7WLNC'


CC_FULFILLMENT_URI = 'cf:0:'
CC_CONDITION_URI = 'cc:0:3:47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU:0'

ASSET_DEFINITION = {
    'data': {
        'definition': 'Asset definition'
    }
}

ASSET_LINK = {
    'id': 'a' * 64
}

DATA = {
    'msg': 'Hello BigchainDB!'
}


@pytest.fixture
def user_priv():
    return USER_PRIVATE_KEY


@pytest.fixture
def user_pub():
    return USER_PUBLIC_KEY


@pytest.fixture
def user2_priv():
    return USER2_PRIVATE_KEY


@pytest.fixture
def user2_pub():
    return USER2_PUBLIC_KEY


@pytest.fixture
def user3_priv():
    return USER3_PRIVATE_KEY


@pytest.fixture
def user3_pub():
    return USER3_PUBLIC_KEY


@pytest.fixture
def ffill_uri():
    return CC_FULFILLMENT_URI


@pytest.fixture
def cond_uri():
    return CC_CONDITION_URI


@pytest.fixture
def user_Ed25519(user_pub):
    from cryptoconditions import Ed25519Fulfillment
    return Ed25519Fulfillment(public_key=user_pub)


@pytest.fixture
def user_user2_threshold(user_pub, user2_pub):
    from cryptoconditions import (ThresholdSha256Fulfillment,
                                  Ed25519Fulfillment)
    user_pub_keys = [user_pub, user2_pub]
    threshold = ThresholdSha256Fulfillment(threshold=len(user_pub_keys))
    for user_pub in user_pub_keys:
        threshold.add_subfulfillment(Ed25519Fulfillment(public_key=user_pub))
    return threshold


@pytest.fixture
def user2_Ed25519(user2_pub):
    from cryptoconditions import Ed25519Fulfillment
    return Ed25519Fulfillment(public_key=user2_pub)


@pytest.fixture
def user_input(user_Ed25519, user_pub):
    from bigchaindb.common.transaction import Input
    return Input(user_Ed25519, [user_pub])


@pytest.fixture
def user2_input(user2_Ed25519, user2_pub):
    from bigchaindb.common.transaction import Input
    return Input(user2_Ed25519, [user2_pub])


@pytest.fixture
def user_user2_threshold_output(user_user2_threshold, user_pub, user2_pub):
    from bigchaindb.common.transaction import Output
    return Output(user_user2_threshold, [user_pub, user2_pub])


@pytest.fixture
def user_user2_threshold_input(user_user2_threshold, user_pub, user2_pub):
    from bigchaindb.common.transaction import Input
    return Input(user_user2_threshold, [user_pub, user2_pub])


@pytest.fixture
def user_output(user_Ed25519, user_pub):
    from bigchaindb.common.transaction import Output
    return Output(user_Ed25519, [user_pub])


@pytest.fixture
def user2_output(user2_Ed25519, user2_pub):
    from bigchaindb.common.transaction import Output
    return Output(user2_Ed25519, [user2_pub])


@pytest.fixture
def asset_definition():
    return ASSET_DEFINITION


@pytest.fixture
def asset_link():
    return ASSET_LINK


@pytest.fixture
def data():
    return DATA


@pytest.fixture
def utx(user_input, user_output):
    from bigchaindb.common.transaction import Transaction
    return Transaction(Transaction.CREATE, {'data': None}, [user_input],
                       [user_output])


@pytest.fixture
def tx(utx, user_priv):
    return utx.sign([user_priv])


@pytest.fixture
def transfer_utx(user_output, user2_output, utx):
    from bigchaindb.common.transaction import (Input, TransactionLink,
                                               Transaction)
    user_output = user_output.to_dict()
    input = Input(utx.outputs[0].fulfillment,
                  user_output['public_keys'],
                  TransactionLink(utx.id, 0))
    return Transaction('TRANSFER', {'id': utx.id}, [input], [user2_output])


@pytest.fixture
def transfer_tx(transfer_utx, user_priv):
    return transfer_utx.sign([user_priv])
