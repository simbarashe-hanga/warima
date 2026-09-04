from typing import Dict, Any

from app.services.identity.session_manager import SessionManager
from app.services.stokvel.stokvel_service import StokvelService
from app.models.enums import MembershipRole


class StokvelEngine:
    """
    Handles stokvel-related conversational flows.

    Supported flows:

    stokvel.create
        Start creating a stokvel and collect its name.

    stokvel.join
        Join an existing stokvel using its join code.

    stokvel.view
        Display the member's active stokvels.

    Transaction ownership remains with the worker.
    """

    async def handle(
        self,
        message: str,
        intent: Dict[str, Any],
        session,
        member_context: Dict[str, Any],
        db=None,
    ) -> Dict[str, Any]:

        if db is None:
            return {
                "message": "I’m unable to access your stokvel account right now.",
                "type": "text",
                "context_update": {},
            }

        member_account = member_context.get("member_account")

        if member_account is None:
            return {
                "message": "Your member account could not be found.",
                "type": "text",
                "context_update": {},
            }

        service = StokvelService(db)

        step = SessionManager.stokvel_step(session)
        intent_name = intent.get("intent")

        # -------------------------------------------------------------
        # Continue an active stokvel flow
        # -------------------------------------------------------------

        if SessionManager.stokvel_active(session):

            if step == "awaiting_name":
                return self._handle_create_name(
                    message=message,
                    session=session,
                    member_account=member_account,
                    service=service,
                )

            if step == "awaiting_join_code":
                return self._handle_join_code(
                    message=message,
                    session=session,
                    member_account=member_account,
                    service=service,
                )

            if step == "awaiting_selection":
                return self._handle_selection(
                    message=message,
                    session=session,
                    member_account=member_account,
                    service=service,
                )

            if step == "menu":
                return self._handle_menu(
                    message=message,
                    session=session,
                    member_account=member_account,
                    service=service,
                )


        #-------------------------------------------------------------
        # Create
        #-------------------------------------------------------------

        if intent_name == "stokvel.create":

            SessionManager.start_stokvel(
                session,
                step="awaiting_name",
            )

            return {
                "message": (
                    "Sure. What would you like to name "
                    "your stokvel?"
                ),
                "type": "text",
                "context_update": {},
            }

        #-------------------------------------------------------------
        # Join
        #-------------------------------------------------------------

        if intent_name == "stokvel.join":

            SessionManager.start_stokvel(
                sesson,
                step="awaiting_join_code",
            )

            return {
                "message": (
                    "Sure. Please enter the stokvel "
                    "join code."
                ),
                "type": "text",
                "context_update": {},
            }

        #--------------------------------------------------------------
        # View / list
        #--------------------------------------------------------------

        if intent_name == "stokvel.view":

            return self._list_stokvels(
                session=session,
                member_account=member_account,
                service=service,
            )

        return {
            "message": (
                "I can help you create a stokvel. "
                "join a stokvel, or view your stokvel."
            ),
            "type": "text",
            "context_update": {},
        }

    # -----------------------------------------------------------------
    # Create
    # -----------------------------------------------------------------

    def _handle_create_name(
        self,
        message,
        session,
        member_account,
        service,
    ):

        name = message.strip()

        if not name:
            return {
                "message": "Please enter a name for your stokvel.",
                "context_update": {},
            }

        if len(name) < 2:
            return {
                "message": (
                    "Please enter a stokvel name "
                    "with at least 2 characters."
                ),
                "type": "text",
                "context_update": {},
            }

        if len(name) > 120:
            return {
                "message": "That name is too long. Please keep it under 120 characters.",
                "type": "text",
                "context_update": {},
            }

        stokvel = service.create_stokvel(name)

        membership = service.add_member(
            member_account_id=member_account.id,
            stokvel_id=stokvel.id,
            role=MembershipRole.OWNER,
        )

        service.active_stokvel(stokvel_id)

        SessionManager.finish_stokvel(session)

        return {
            "message": (
                f"Your stokvel '{stokvel.name}' has been created successfully.\n\n"
                f"Join code: {stokvel.join_code}\n\n"
                "Share this code with the people you want to invite."
            ),
            "type": "text",
            "context_update": {
                "stokvel": {
                    "selected_stokvel_id": str(stokvel.id),
                },
            },
        }

    # -----------------------------------------------------------------
    # Join
    # -----------------------------------------------------------------

    def _handle_join_code(
        self,
        message,
        session,
        member_account,
        service,
    ):

        code = message.strip().upper()

        stokvel = service.get_stokvel_by_join_code(code)

        if stokvel is None:
            return {
                "message": (
                    "I couldn't find a stokvel with that "
                    "join code. Please check the code and try again."
                ),
                "type": "text",
                "context_update": {},
            }

        if stokvel.status.value != "ACTIVE":
            return {
                "message": (
                    "That stokvel is not currently active."
                ),
                "type": "text",
                "context_update": {},
            }

        existing = service.get_membership(
            member_account.id,
            stokvel.id,
        )

        if existing:
            SessionManager.set_selected_stokvel(
                session,
                stokvel.id,
            )
            SessionManager.finish_stokvel(session)

            return {
                "message": (
                    f"You're already a member of '{stokvel.name}'."
                ),
                "type": "text",
                "context_update": {},
            }

        membership = service.add_member(
            member_account_id=member_account.id,
            stokvel_id=stokvel.id,
            role=MembershipRole.MEMBER,
        )

        SessionManager.set_selected_stokvel(
            session,
            stokvel.id,
        )

        SessionManager.finish_stokvel(session)

        return {
            "message": (
                f"You've successfully joined '{stokvel.name}'."
                f"Join code: *{stokvel.join_code}*"
            ),
            "type": "text",
            "context_update": {},
        }

    # -----------------------------------------------------------------
    # View / list
    # -----------------------------------------------------------------

    def _list_stokvels(
        self,
        session,
        member_account,
        service,
    ):

        stokvels = service.get_member_stokvels(
            member_account.id
        )

        if not stokvels:

            SessionManager.finish_stokvel(session)

            return {
                "message": (
                    "You aren't a member of any stokvels yet.\n\n"
                    "You can *create* a stokvel or *join* one using a join code."
                ),
                "type": "text",
                "context_update": {},
            }

        options = []

        lines = ["*Your stokvels:*"]

        for index, stokvel in enumerate(stokvels, start=1):

            options.append(
                {
                    "index": index,
                    "stokvel_id": str(stokvel.id),
                }
            )

            lines.append(
                f"{index}. *{stokvel.name}*)"
            )

        lines.extend(
            [
                "",
                "Reply with the number of the stokvel "
                "you'd like to manage.",
            ]
        )

        SessionManager.start_stokvel(
            session,
            step="awaiting_selection",
            options=options,
        )

        return {
            "message": "\n".join(lines),
            "type": "text",
            "context_update": {},
        }

    #=========================================================================
    # Selection
    #=========================================================================

    def _handle_selection(
        self,
        message,
        session,
        member_account,
        service,
    ):
        text = message.strip()

        if not text.isdigit():
            return {
                "message": (
                    "Please reply with the number of "
                    "the stokvel you'd like to manage."
                ),
                "type": "text",
                "context_update": {},
            }

        index = int(text)

        options = SessionManager.stokvel_options(session)

        selected = next(
            (
                option
                for option in options
                if option.get("index") == index
            ),
            None,
        )

        if selected is None:
            return {
                "message": (
                    "That isn't a valid selection. "
                    "Please choose one of the numbers listed."
                ),
                "type": "text",
                "context_update": {},
            }

        stokvel_id = selected["stokvel_id"]

        stokvel = service.get_stokvel(stokvel_id)

        if stokvel is None:
            SessionManager.finish_stokvel(session)

            return {
                "message": (
                    "I couldn't find that stokvel. "
                    "Please try again."
                ),
                "type": "text",
                "context_update": {},
            }

        membership = service.get_membership(
            member_account.id,
            stokvel.id,
        )

        if membership is None:
            SessionManager.finish_stokvel(session)

            return {
                "message": (
                    "You are no longer an active member "
                    "of that stokvel."
                ),
                "type": "text",
                "context_update": {},
            }

        SessionManager.set_selected_stokvel(
            session,
            stokvel.id,
        )

        SessionManager.set_stokvel_step(
            session,
            "menu",
        )

        return self._stokvel_menu(stokvel)

    #========================================================================
    # Menu
    #========================================================================

    def _stokvel_menu(self, stokvel):

        return {
            "message": (
                f"*{stokvel.name}*\n\n"
                "What would you like to do?\n\n"
                "1. View details\n"
                "2. Contribute\n"
                "3. Members\n"
                "4. Back"
            ),
            "type": "text",
            "context_update": {},
        }

    def _handle_menu(
        self,
        message,
        session,
        member_account,
        service,
    ):
        selected_id = SessionManager.selected_stokvel_id(
            session
        )

        if not selected_id:
            SessionManager.finish_stokvel(session)

            return {
                "message": (
                    "No stokvel is currently selected. "
                    "Please type *Stokvels* to choose one."
                ),
                "type": "text",
                "context_update": {},
            }

        stokvel = service.get_stokvel(selected_id)

        if stokvel is None:
            SessionManager.finish_stokvel(session)

            return {
                "message": (
                    "That stokvel could not be found."
                ),
                "type": "text",
                "context_update": {},
            }

        choice = message.strip()

        if choice == "1":
            return self._view_details(
                session=session,
                stokvel=stokvel,
            )

        if choice == "2":
            return self._start_contribution(
                session=session,
                stokvel=stokvel,
            )

        if choice == "3":
            return self._view_members(
                stokvel=stokvel,
                service=service,
            )

        if choice == "4":
            SessionManager.finish_stokvel(session)

            return {
                "message": (
                    "Okay. You're back at your stokvel list."
                ),
                "type": "text",
                "context_update": {},
            }

        return {
            "message": (
                "Please choose:\n\n"
                "1. View details\n"
                "2. Contribution\n"
                "3. Members\n"
                "4. Back"
            ),
            "type": "text",
        }

    #=============================================================================
    # Details
    #=============================================================================

    def _view_details(
        self,
        stokvel,
        member_account,
        service,
    ):

        membership = service.get_membership(
            member_account.id,
            stokvel.id,
        )

        role = (
            membership.role.value
            if membership
            else "MEMBER"
        )

        description = (
            stokvel.description
            or "No description provided."
        )

        return {
            "message": (
                f"*{stokvel.name}*\n\n"
                f"Status: {stokvel.status.value}\n"
                f"Join code: *{stokvel.join_code}*\n"
                f"Your role: {role}\n\n"
                f"{description}\n\n"
                "Reply *2* to contribute, "
                "*3* to view members, or "
                "*4* to go back."
            ),
            "type": "text",
            "context_update": {},
        }

    #=============================================================================
    # Members
    #=============================================================================

    def _view_members(
        self,
        stokvel,
        service,
    ):

        memberships = service.get_stokvel_members(
            stokvel.id
        )

        if not memberships:
            return {
                "message": (
                    f"*{stokvel.name}* currently has "
                    "no active members."
                ),
                "type": "text",
                "context_update": {},
            }

        lines = [
            f"*{stokvel.name} members:*",
            "",
        ]

        for index, membership in enumerate(
            memberships,
            start=1,
        ):

            user = membership.member_account.user

            name = (
                user.display_name
                or " ".join(
                    value
                    for value in [
                        user.first_name,
                        user.last_name,
                    ]
                    if value
                )
                or "Member"
            )

            role = membership.role.value

            lines.append(
                f"{index}. {name} - {role}"
            )

        lines.extend(
            [
                "",
                "Reply *4* to go back.",
            ]
        )

        return {
            "message": "\n".join(lines),
            "type": "text",
            "context_update": {},
        }

    #=============================================================================
    # Contribution Handoff
    #=============================================================================

    def _start_contribution(
        self,
        session,
        stokvel,
    ):

        # The selected stokvel remains stored in session
        # WalletEngine will consume selected_stokvel_id.
        SessionManager.clear_other_flows(
            session,
            active_flow="wallet",
        )

        SessionManager.start_wallet(
            session,
            step="awaiting_amount",
        )

        return {
            "message": (
                f"How much would you like to contribute "
                f"to *{stokvel.name}*?"
            ),
            "type": "text",
            "context_update": {},
        }
