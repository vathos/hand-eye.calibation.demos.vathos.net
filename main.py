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

import requests
import numpy as np

from lib.authentication import get_service_account_token

if __name__ == '__main__':

  # get a service account token
  token = get_service_account_token(os.environ.get('CLIENT_ID'),
                                    os.environ.get('CLIENT_SECRET'))

  # fill in task parameters
  data = {
      'service': '2d.handeye.calibration.vathos.net',
      'parameters': {
          'session':
              'handeye_calib_service_test',
          'pattern_size': [9, 7],
          'pattern_side_length':
              0.02,
          'intrinsics': [
              7252.223304681514, 0.0, 0.0, 0.0, 7245.700711835546, 0.0,
              1256.5517597471978, 980.6156156257105, 1.0
          ]
      }
  }

  task_request = requests.post('https://staging.api.gke.vathos.net/v1/tasks',
                               headers={'Authorization': 'Bearer ' + token},
                               json=data)

  task_data = task_request.json()
  logging.info('Started task %s', task_data)

  while True:

    logging.debug('Waiting for task to finish...')
    # poll the task status
    sleep(5.0)
    task_status_request = requests.get(
        f'https://staging.api.gke.vathos.net/v1/tasks/{task_data["_id"]}',
        headers={'Authorization': 'Bearer ' + token})
    task_data = task_status_request.json()

    # break out of the loop as soon as the task is completed
    if task_data['status'] == 1:
      eye2hand = np.reshape(
          np.array(task_data['result']['eye2hand'], dtype='f'), (4, 4), 'F')
      logging.info('Calibration result: %s', eye2hand)
      break
    elif task_data['status'] == -1:
      logging.error('Task failed')
      break
