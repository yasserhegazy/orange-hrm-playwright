import re

from playwright.sync_api import Page, expect

from utils.tracing import pw_trace

STATUS_PREFIX = "Status: "


class CandidateDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Application Stage")
        self.status_label = page.locator(".orangehrm-recruitment-status")
        self.shortlist_button = page.get_by_role("button", name="Shortlist")
        self.reject_button = page.get_by_role("button", name="Reject")

    def wait_until_loaded(self) -> CandidateDetailPage:
        """Wait for the candidate detail page to be fully loaded."""
        expect(self.heading).to_be_visible(timeout=10000)
        expect(self.status_label).to_be_visible(timeout=10000)
        return self

    def get_status(self) -> str:
        text = self.status_label.inner_text()
        return text.removeprefix(STATUS_PREFIX)

    @pw_trace("Shortlist Candidate")
    def shortlist(self) -> "CandidateDetailPage":
        return self._perform_action("Shortlist", "Shortlist Candidate")

    @pw_trace("Reject Candidate")
    def reject(self) -> "CandidateDetailPage":
        return self._perform_action("Reject", "Reject Candidate")

    def _perform_action(self, button_name: str, transition_heading: str) -> "CandidateDetailPage":
        """Helper to handle the navigation flow for recruitment actions."""
        # Click the action button (Shortlist/Reject)
        button = self.actions_container.get_by_role("button", name=button_name)
        expect(button).to_be_visible()
        button.click()

        # Wait for the specific action page to load
        action_heading = self.page.get_by_role("heading", name=transition_heading)
        expect(action_heading).to_be_visible(timeout=10000)

        # Save the action
        save_button = self.page.get_by_role("button", name="Save")
        save_button.click()

        # Verify redirect back to detail page
        expect(self.page).to_have_url(re.compile(r".*/addCandidate/\d+$"), timeout=10000)
        expect(self.heading).to_be_visible(timeout=10000)
        return self
