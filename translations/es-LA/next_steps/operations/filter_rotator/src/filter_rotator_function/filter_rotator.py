# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
import json
import time
import boto3
from aws_lambda_powertools import Logger
from template_evaluation import eval_expression, eval_template

logger = Logger()
personalize = boto3.client('personalize')
event_bridge = boto3.client('events')

publish_filter_events = os.environ.get('PUBLISH_FILTER_EVENTS', 'yes').lower() == 'yes'

def put_event(detail_type: str, detail: str, resources = []):
    """
    Called to publish an event to the default EventBridge event bus when a filter
    is created or deleted. Allows applications to synchronize their configuration
    such as switching from an old filter to a newly created filter.
    """
    logger.info({
        'detail_type': detail_type,
        'detail': detail,
        'resources': resources
    })

    event_bridge.put_events(
        Entries=[
            {
                'Source': 'personalize.filter.rotator',
                'Resources': resources,
                'DetailType': detail_type,
                'Detail': detail
            }
        ]
    )

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, _):
    dataset_group_arn = event["datasetGroupArn"]
    current_filter_name_template = event["currentFilterNameTemplate"]
    current_filter_expression_template = event["currentFilterExpressionTemplate"]
    delete_filter_match_template = event["deleteFilterMatchTemplate"]

    current_filter_name = eval_template(current_filter_name_template)
    logger.info('Current filter resolved name: %s', current_filter_name)

    current_filter_exists = False
    filters_to_delete = []

    # Step 1: Iterate over existing filters for the dataset group to determine if a new filter
    # needs to be created and to collect filters that should be deleted.
    paginator = personalize.get_paginator('list_filters')
    for paginate_result in paginator.paginate(datasetGroupArn = dataset_group_arn):
        for filter in paginate_result['Filters']:
            if filter['name'] == current_filter_name:
                logger.info('Current filter %s already exists; skipping creation', current_filter_name)
                current_filter_exists = True
            elif delete_filter_match_template:
                delete_match = eval_expression(delete_filter_match_template, {'filter': filter})

                if delete_match:
                    logger.info('Filter %s matched the delete filter template; queueing for deletion', filter['filterArn'])
                    filters_to_delete.append(filter)

    # Step 2: If the current filter does not exist, create it and send an event when it's active (if configured to do so).
    if not current_filter_exists:
        logger.info('Current filter %s does not exist; creating', current_filter_name)

        expression = eval_template(current_filter_expression_template)

        response = personalize.create_filter(
            datasetGroupArn = dataset_group_arn,
            filterExpression = expression,
            name = current_filter_name
        )

        filter_arn = response['filterArn']
        logger.info('Filter %s created', filter_arn)

        if publish_filter_events:
            # FUTURE: move this logic into Step Functions for efficiency and robustness.
            logger.info('Waiting for new filter to become active so we can publish filter created event')

            status = None
            start_time = time.time()
            max_time = start_time + 60*12 # 12 minutes
            while time.time() < max_time:
                describe_filter_response = personalize.describe_filter(filterArn = filter_arn)
                status = describe_filter_response["filter"]["status"]

                if status == "ACTIVE" or status == "CREATE FAILED":
                    break

                time.sleep(10)
                logger.info('Waiting for new filter to become active; status is %s; %d seconds elapsed', status, int(time.time() - start_time))

            elapsed_time = time.time() - start_time

            if status == "CREATE FAILED":
                logger.error('Filter %s status is %s', filter_arn, status)

                put_event(
                    detail_type='PersonalizeFilterCreateFailed',
                    detail = json.dumps({
                                'datasetGroupArn': dataset_group_arn,
                                'filterName': current_filter_name,
                                'filterExpression': expression,
                                'filterStatus': status,
                                'failureReason': describe_filter_response['filter'].get('failureReason'),
                                'waitTimeSeconds': int(elapsed_time)
                    }),
                    resources = [ filter_arn ]
                )
            else:
                # Filter status may be ACTIVE or still PENDING/IN PROGRESS (if we timed out).
                logger.info('Filter %s status is %s', filter_arn, status)

                put_event(
                    detail_type='PersonalizeFilterCreated',
                    detail = json.dumps({
                                'datasetGroupArn': dataset_group_arn,
                                'filterName': current_filter_name,
                                'filterExpression': expression,
                                'filterStatus': status,
                                'waitTimeSeconds': int(elapsed_time)
                    }),
                    resources = [ filter_arn ]
                )

    # Step 3: Delete any filters eligible for delection according to the match template and send events (if configured).
    if len(filters_to_delete) > 0:
        logger.info('%s filters marked for deletion', len(filters_to_delete))

        for filter in filters_to_delete:
            logger.info('Deleting filter %s', filter['filterArn'])
            personalize.delete_filter(filterArn = filter['filterArn'])

            if publish_filter_events:
                put_event(
                    detail_type='PersonalizeFilterDeleted',
                    detail = json.dumps({
                        'datasetGroupArn': dataset_group_arn,
                        'filterName': filter['name'],
                        'filterArn': filter['filterArn']
                    }),
                    resources = [ filter['filterArn'] ]
                )
