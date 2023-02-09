# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019-2023, Vathos GmbH
#
# All rights reserved.
#
################################################################################
"""Authentication with the cloud REST API."""

import requests


def get_service_account_token(client_id, client_secret):
  """Impersonates a client by the help of a service account token."""
  token_response = requests.post(
      'https://auth.gke.vathos.net/auth/realms/picking/protocol/openid-connect/token',
      headers={'content-type': 'application/x-www-form-urlencoded'},
      data={
          'client_id': client_id,
          'client_secret': client_secret,
          'grant_type': 'client_credentials',
      },
      timeout=5)
  return token_response.json()['access_token']
