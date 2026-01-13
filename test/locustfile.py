from locust import HttpUser, task, between

class WagtailUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def view_homepage(self):
        # Replace with your actual Wagtail page URL
        self.client.get("/")
