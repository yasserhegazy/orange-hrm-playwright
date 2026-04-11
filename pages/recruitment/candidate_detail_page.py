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
    def shortlist(self) -> CandidateDetailPage:
        expect(self.shortlist_button).to_be_visible()
        self.shortlist_button.click()

        # Navigates to a separate action page — wait for it, then save
        action_heading = self.page.get_by_role("heading", name="Shortlist Candidate")
        expect(action_heading).to_be_visible(timeout=10000)

        save_button = self.page.get_by_role("button", name="Save")
        save_button.click()

        # After save, redirects back to candidate detail page
        expect(self.page).to_have_url(re.compile(r".*/addCandidate/\d+$"), timeout=10000)
        expect(self.heading).to_be_visible(timeout=10000)
        return self

    @pw_trace("Reject Candidate")
    def reject(self) -> CandidateDetailPage:
        expect(self.reject_button).to_be_visible()
        self.reject_button.click()

        # Navigates to a separate action page — wait for it, then save
        action_heading = self.page.get_by_role("heading", name="Reject Candidate")
        expect(action_heading).to_be_visible(timeout=10000)

        save_button = self.page.get_by_role("button", name="Save")
        save_button.click()

        # After save, redirects back to candidate detail page
        expect(self.page).to_have_url(re.compile(r".*/addCandidate/\d+$"), timeout=10000)
        expect(self.heading).to_be_visible(timeout=10000)
        return self
