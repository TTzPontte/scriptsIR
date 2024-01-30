import logging
import os

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL") or logging.NOTSET

AWS_SAM_LOCAL = os.getenv("AWS_SAM_LOCAL") == "true"

API_ENDPOINT = os.getenv("API_ENDPOINT")

DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")

ENV = os.getenv("ENV") or "prod"
# todo use environment
AZT_API_TOKEN='QVotQVBJS0VZOjZCRjRDNDg5LTFCREEtNDc3QS05MTA4LTNGRUY0NUZCRTU4OQ=='
