import re

from playwright.sync_api import Locator, Page, expect

from utils.tracing import pw_trace

STATUS_PREFIX = "Status: "


class CandidateDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Application Stage")
        self.status_label = page.locator(".orangehrm-recruitment-status")
        self.shortlist_button = page.get_by_role("button", name="Shortlist")
        self.reject_button = page.get_by_role("button", name="Reject")
        self.save_button = page.get_by_role("button", name="Save")
        self.wait_until_loaded()

    def wait_until_loaded(self) -> CandidateDetailPage:
        """Wait for the candidate detail page to be fully loaded."""
        expect(self.heading).to_be_visible(timeout=10000)
        expect(self.status_label).to_be_visible(timeout=10000)
        return self

    def get_status(self) -> str:
        expect(self.status_label).to_be_visible(timeout=10000)
        text = self.status_label.inner_text().strip()
        return text.removeprefix(STATUS_PREFIX).strip()

    def has_attachment(self, filename: str) -> bool:
        """Return True if the given filename is visible in the attachments section."""
        return self.page.get_by_text(filename, exact=True).is_visible()

    @pw_trace("Shortlist Candidate")
    def shortlist(self) -> CandidateDetailPage:
        return self._perform_action(self.shortlist_button, "Shortlist Candidate")

    @pw_trace("Reject Candidate")
    def reject(self) -> CandidateDetailPage:
        return self._perform_action(self.reject_button, "Reject Candidate")

    def _perform_action(self, action_button: Locator, transition_heading: str) -> CandidateDetailPage:
        """Helper to handle the navigation flow for recruitment actions."""
        expect(action_button).to_be_visible()
        action_button.click()

        action_heading = self.page.get_by_role("heading", name=transition_heading)
        expect(action_heading).to_be_visible(timeout=10000)

        self.save_button.click()

        expect(self.page).to_have_url(re.compile(r".*/addCandidate/\d+$"), timeout=10000)
        self.wait_until_loaded()
        return self
