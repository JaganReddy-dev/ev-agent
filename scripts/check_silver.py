import sys
from ev_agent.db import get_connection

CHECKS = {
    "row count unchanged by cleaning":
        "SELECT (SELECT COUNT(*) FROM ev) = (SELECT COUNT(*) FROM ev_raw)",
    "no zero electric_range":
        "SELECT COUNT(*) = 0 FROM ev WHERE electric_range = 0",
    "every raw zero/null became NULL":
        """SELECT (SELECT COUNT(*) FROM ev WHERE electric_range IS NULL)
                = (SELECT COUNT(*) FROM ev_raw WHERE electric_range = 0 OR electric_range IS NULL)""",
    "NULL range only when not researched or missing":
        """SELECT COUNT(*) <= 35 FROM ev
           WHERE electric_range IS NULL
             AND cafv_eligibility <> 'Eligibility unknown as battery range has not been researched'""",
    "dol_vehicle_id is unique":
        "SELECT COUNT(*) = COUNT(DISTINCT dol_vehicle_id) FROM ev",
}

failed = 0
with get_connection(read_only=True) as con:
    for name, sql in CHECKS.items():
        result = con.execute(sql).fetchone()
        if result is None:
            raise RuntimeError(f"check failed at: ", {name}, {sql})
        ok = result[0]
        print(f"{'✅' if ok else '❌'} {name}")
        failed += not ok

sys.exit(1 if failed else 0)