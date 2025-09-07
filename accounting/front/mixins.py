import requests
from django.contrib import messages

from django.conf import settings


class ApiRequestMixin:

    def _process_response(self, response):
        if response.status_code not in [200, 201, 204]:
            messages.error(self.request, "Something went wrong")
            try:
                print(f"Api call error: {response.json()}")
            except Exception:
                print(f"Api call error: {response.text}")
            return super().render_to_response(self.get_context_data())

        if response.status_code == 204 or not response.content.strip():
            return None

        return response.json()

    def api_post(self, url, data):
        response = requests.post(settings.API_BASE_URL + url, json=data)
        return self._process_response(response)

    def api_put(self, url, data):
        response = requests.put(settings.API_BASE_URL + url, json=data)
        return self._process_response(response)

    def api_patch(self, url, data):
        """Partial update (only update the provided fields)."""
        response = requests.patch(settings.API_BASE_URL + url, json=data)
        return self._process_response(response)

    def api_get(self, url, params=None):
        response = requests.get(settings.API_BASE_URL + url, params=params)
        return self._process_response(response)

    def api_delete(self, url):
        response = requests.delete(settings.API_BASE_URL + url)
        return self._process_response(response)


class FormInvalidMessageMixin:

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, error)  # non-field errors
                else:
                    messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def formset_invalid(self, formset):
        print(formset)
        for form in formset.forms:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "__all__":
                        messages.error(self.request, error)  # non-field errors
                    else:
                        messages.error(self.request, f"{field.capitalize()}: {error}")
        return self.render_to_response(
            self.get_context_data(form=self.get_form(), formset=formset)
        )
