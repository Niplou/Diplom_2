import requests
from web_service_urls import ServiceEndpoints


class TransactionProcessing:
    @staticmethod
    def create_transaction(components, auth_token=None):
        headers = {}
        if auth_token:
            clean_token = auth_token.replace("Bearer ", "")
            headers["Authorization"] = f"Bearer {clean_token}"
        payload = {"ingredients": components}
        return requests.post(ServiceEndpoints.TRANSACTION_RECORDS, json=payload, headers=headers)