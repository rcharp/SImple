import stripe

stripe_keys = {
    'secret_key': 'sk_test_aPce5SASjjzwyGWHlokJUOqt',
    'publishable_key': 'pk_test_NSVlCKiuhd89Nft1EmZDivY9'
}

stripe.api_key = stripe_keys['secret_key']