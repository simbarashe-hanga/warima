from sqlalchemy import inspect

from app.db.session import engine

inspector = inspect(engine)

print("=" * 80)
print("TABLES")
print("=" * 80)

for table in inspector.get_table_names():

    print(f"\n{table}")

    print("-" * 80)

    for column in inspector.get_columns(table):

        print(
            f"{column['name']:<25}"
            f"{str(column['type']):<25}"
            f"nullable={column['nullable']}"
        )

    fks = inspector.get_foreign_keys(table)

    if fks:
        print("\nForeign Keys")

        for fk in fks:
            print(
                f"  {fk['constrained_columns']} "
                f"-> "
                f"{fk['referred_table']}."
                f"{fk['referred_columns']}"
            )
