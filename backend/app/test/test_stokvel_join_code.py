import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.engine.stokvel_engine import StokvelEngine
from app.models.enums import (
    MembershipRole,
    MembershipStatus,
    StokvelStatus,
)


class StokvelJoinCodeTests(unittest.TestCase):

    def setUp(self):
        self.engine = StokvelEngine()
        self.session = {}
        self.db = Mock()
        self.member_account = SimpleNamespace(id="member-123")

        self.stokvel = SimpleNamespace(
            id="stokvel-456",
            name="Community Wealth",
            join_code="JOIN123",
            status=StokvelStatus.ACTIVE,
        )

        self.service = Mock()
        self.service.get_stokvel_by_join_code.return_value = (
            self.stokvel
        )
        self.service.get_membership_record.return_value = None

        self.finish_stokvel_patcher = patch(
            "app.engine.stokvel_engine.SessionManager.finish_stokvel"
        )
        self.finish_stokvel = self.finish_stokvel_patcher.start()
        self.addCleanup(self.finish_stokvel_patcher.stop)

        self.blockchain_patcher = patch.object(
            self.engine,
            "_ensure_blockchain_account",
        )
        self.ensure_blockchain_account = self.blockchain_patcher.start()
        self.addCleanup(self.blockchain_patcher.stop)

    def call_handler(self, code="JOIN123"):
        return self.engine._handle_join_code(
            message=code,
            session=self.session,
            member_account=self.member_account,
            service=self.service,
            db=self.db,
        )

    def test_invalid_code_returns_safe_message(self):
        self.service.get_stokvel_by_join_code.return_value = None

        result = self.call_handler(" invalid ")

        self.assertIn("couldn't find a stokvel", result["message"])
        self.assertEqual(result["context_update"], {})
        self.service.get_stokvel_by_join_code.assert_called_once_with(
            "INVALID"
        )
        self.service.get_membership_record.assert_not_called()
        self.service.add_member.assert_not_called()
        self.ensure_blockchain_account.assert_not_called()

    def test_inactive_stokvel_is_rejected(self):
        self.stokvel.status = StokvelStatus.SUSPENDED

        result = self.call_handler()

        self.assertIn("not currently active", result["message"])
        self.service.get_membership_record.assert_not_called()
        self.service.add_member.assert_not_called()
        self.ensure_blockchain_account.assert_not_called()

    def test_existing_active_membership_selects_stokvel(self):
        self.service.get_membership_record.return_value = (
            SimpleNamespace(status=MembershipStatus.ACTIVE)
        )

        result = self.call_handler()

        self.assertIn("already a member", result["message"])
        self.assertEqual(
            result["context_update"]["stokvel"]["selected_stokvel_id"],
            str(self.stokvel.id),
        )
        self.finish_stokvel.assert_called_once_with(self.session)
        self.service.add_member.assert_not_called()
        self.ensure_blockchain_account.assert_not_called()

    def test_pending_membership_is_not_recreated(self):
        self.assert_existing_status_blocked(
            MembershipStatus.PENDING,
            "pending",
            "approve",
        )

    def test_suspended_membership_is_not_recreated(self):
        self.assert_existing_status_blocked(
            MembershipStatus.SUSPENDED,
            "suspended",
            "contact",
        )

    def test_left_membership_requires_restoration(self):
        self.assert_existing_status_blocked(
            MembershipStatus.LEFT,
            "previously left",
            "restore",
        )

    def assert_existing_status_blocked(
        self,
        status,
        expected_message,
        expected_guidance,
    ):
        self.service.get_membership_record.return_value = (
            SimpleNamespace(status=status)
        )

        result = self.call_handler()

        self.assertIn(expected_message, result["message"])
        self.assertIn(expected_guidance, result["message"])
        self.assertEqual(result["context_update"], {})
        self.finish_stokvel.assert_called_once_with(self.session)
        self.service.add_member.assert_not_called()
        self.ensure_blockchain_account.assert_not_called()

    def test_new_member_is_added_and_blockchain_setup_requested(self):
        result = self.call_handler()

        self.assertIn("successfully joined", result["message"])
        self.service.get_stokvel_by_join_code.assert_called_once_with(
            "JOIN123"
        )
        self.service.get_membership_record.assert_called_once_with(
            self.member_account.id,
            self.stokvel.id,
        )
        self.service.add_member.assert_called_once_with(
            member_account_id=self.member_account.id,
            stokvel_id=self.stokvel.id,
            role=MembershipRole.MEMBER,
        )
        self.ensure_blockchain_account.assert_called_once_with(
            stokvel=self.stokvel,
            member_account_id=self.member_account.id,
            db=self.db,
        )
        self.finish_stokvel.assert_called_once_with(self.session)
        self.assertEqual(
            result["context_update"]["stokvel"]["selected_stokvel_id"],
            str(self.stokvel.id),
        )


if __name__ == "__main__":
    unittest.main()
