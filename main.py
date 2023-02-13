#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020, Vathos GmbH
#
# All rights reserved.
#
################################################################################

import os
import logging
from time import sleep
from datetime import datetime

import requests
import numpy as np

from lib.authentication import get_service_account_token
from lib.files import upload_data

if __name__ == '__main__':

  # get a service account token
  token = get_service_account_token(os.environ.get('CLIENT_ID'),
                                    os.environ.get('CLIENT_SECRET'))

  # generate a random session id
  session = 'handeye_' + datetime.now().isoformat()
  logging.info('Storing data under session id %s', session)

  # upload images and poses under that session id
  upload_data('./resources/poses.csv', token, session)

  # fill in task parameters
  data = {
      'service': '2d.handeye.calibration.vathos.net',
      'parameters': {
          'eye_in_hand':
              True,
          'session':
              session,
          'pattern_size': [10, 7],
          'pattern_side_length':
              0.025,
          'intrinsics': [
              1759.1642, 0.0, 0.0, 0.0, 1764.0677, 0.0, 962.8343, 595.8946, 1.0
          ]
      }
  }

  task_request = requests.post('https://staging.api.gke.vathos.net/v1/tasks',
                               headers={'Authorization': f'Bearer {token}'},
                               json=data,
                               timeout=5)

  task_data = task_request.json()
  logging.info('Started task %s', task_data)

  while True:

    logging.debug('Waiting for task to finish...')
    # poll the task status
    sleep(5.0)
    task_status_request = requests.get(
        f'https://staging.api.gke.vathos.net/v1/tasks/{task_data["_id"]}',
        headers={'Authorization': f'Bearer {token}'},
        timeout=5)
    task_data = task_status_request.json()

    # break out of the loop as soon as the task is completed
    if task_data['status'] == 1:
      result = np.reshape(np.array(task_data['result']['transform'], dtype='f'),
                          (4, 4), 'F')
      logging.info('Calibration result: %s', result)
      break
    elif task_data['status'] == -1:
      logging.error('Task failed')
      break
