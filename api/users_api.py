from api.base_api import BaseAPI


class UsersAPI(BaseAPI):

    def __init__(self, api_context):
        super().__init__(api_context)

    def create_user(self, payload):
        return self.post(endpoint="users", data=payload)

    def get_all_users(self):
        """Fetches the list of all users."""
        return self.get(endpoint="users")

    def get_user(self, user_id):
        """Fetches a single user by their ID."""
        return self.get(endpoint=f"users/{user_id}")

    def update_user_partial(self, user_id, payload):
        """Use PATCH when you only want to update specific fields (e.g., just the name)."""
        return self.patch(endpoint=f"users/{user_id}", data=payload)

    def update_user_full(self, user_id, payload):
        """Use PUT when you want to completely replace the user's entire record."""
        return self.put(endpoint=f"users/{user_id}", data=payload)

    def delete_user(self, user_id):
        return self.delete(endpoint=f"users/{user_id}")