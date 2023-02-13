# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2019-2023, Vathos GmbH
#
# All rights reserved.
#
################################################################################
"""Uploads calibration images and poses to the cloud."""

import csv

import requests


def upload_data(csv_file_name, token, session):

  with open(csv_file_name, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    for i, row in enumerate(reader):

      upload_body = {}
      upload_body[f'img_{str(i).zfill(2)}'] = open(row[0], 'rb')

      upload_response = requests.post(
          'https://staging.api.gke.vathos.net/v1/blobs',
          files=upload_body,
          headers={'Authorization': f'Bearer {token}'},
          timeout=60)

      uploaded_file = upload_response.json()[0]

      post_image_response = requests.post(
          'https://staging.api.gke.vathos.net/v1/images',
          json={
              'file': uploaded_file['_id'],
              'session': session,
              'contentType': 'image/png'
          },
          headers={'Authorization': f'Bearer {token}'},
          timeout=5)
      image_id = post_image_response.json()['_id']

      requests.post('https://staging.api.gke.vathos.net/v1/detections',
                    json={
                        'image': image_id,
                        'frame': [float(r) for r in row[1:]]
                    },
                    headers={'Authorization': f'Bearer {token}'},
                    timeout=5)