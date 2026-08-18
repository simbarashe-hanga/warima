from app.db.session import SessionLocal
from app.services.identity.user_service import UserService


def main():
    db = SessionLocal()

    try:
        print("Creating UserService")
        service = UserService(db)

        print("Calling authenticate_whatsapp()")

        result = service.authenticate_whatsapp(
            "27672489700"
        )

        print("Authentication complete")
        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    main()
