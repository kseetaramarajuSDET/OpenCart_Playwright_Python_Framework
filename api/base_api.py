import json
import logging
import allure
from playwright.sync_api import APIRequestContext
from utilities.custom_logger import LogGen


class BaseAPI:
    log = LogGen.loggen()

    def __init__(self, api_context: APIRequestContext):
        self.api_context = api_context

    def _attach_to_allure(self, name: str, data: any):
        """Helper method to attach JSON data cleanly to Allure reports."""
        try:
            if data:
                allure.attach(
                    body=json.dumps(data, indent=2),
                    name=name,
                    attachment_type=allure.attachment_type.JSON
                )
        except Exception as e:
            self.log.warning(f"Could not attach data to Allure: {e}")

    def _safe_json(self, response):
        """Safely extract JSON. Prevents crashes on 204 No Content (DELETE responses)."""
        try:
            return response.json()
        except:
            return {"text_response": response.text()}

    def get(self, endpoint: str, headers: dict = None, params: dict = None):
        self.log.info(f"GET Request -> Endpoint: {endpoint}")

        response = self.api_context.get(endpoint, headers=headers, params=params)
        full_url = response.url

        self.log.info(f"Executed GET -> {full_url} | Status: {response.status}")
        # Add to Allure Report
        with allure.step(f"GET {full_url}"):
            self._attach_to_allure("Response Body", self._safe_json(response))

        return response

    def post(self, endpoint: str, data: dict, headers: dict = None):
        self.log.info(f"POST Request -> Endpoint: {endpoint} | Payload: {data}")

        response = self.api_context.post(endpoint, data=data, headers=headers)

        full_url = response.url
        self.log.info(f"Executed POST -> {full_url} | Status: {response.status}")

        # Add to Allure Report
        with allure.step(f"POST {full_url}"):
            self._attach_to_allure("Request Payload", data)
            self._attach_to_allure("Response Body", self._safe_json(response))

        return response

    def put(self, endpoint: str, data: dict, headers: dict = None):
        self.log.info(f"PUT Request -> Endpoint: {endpoint} | Payload: {data}")

        response = self.api_context.put(endpoint, data=data, headers=headers)
        full_url = response.url
        self.log.info(f"Executed PUT -> {full_url} | Status: {response.status}")
        with allure.step(f"PUT {full_url}"):
            self._attach_to_allure("Request Payload", data)
            self._attach_to_allure("Response Body", self._safe_json(response))

        return response

    def patch(self, endpoint: str, data: dict, headers: dict = None):
        self.log.info(f"PATCH Request -> Endpoint: {endpoint} | Payload: {data}")

        # Used specifically for GoRest updates
        response = self.api_context.patch(endpoint, data=data, headers=headers)
        full_url = response.url
        self.log.info(f"Executed PATCH -> {full_url} | Status: {response.status}")
        with allure.step(f"PATCH {full_url}"):
            self._attach_to_allure("Request Payload", data)
            self._attach_to_allure("Response Body", self._safe_json(response))

        return response

    def delete(self, endpoint: str, headers: dict = None):
        self.log.info(f"DELETE Request -> Endpoint: {endpoint}")

        response = self.api_context.delete(endpoint, headers=headers)
        full_url = response.url
        self.log.info(f"Executed DELETE -> {full_url} | Status: {response.status}")
        with allure.step(f"DELETE {full_url}"):
            self._attach_to_allure("Response Body", self._safe_json(response))

        return response
