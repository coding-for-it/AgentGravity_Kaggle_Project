from services.antigravity_service import AntigravityService

service = AntigravityService()

print(
    service.generate_investigation_plan(
        "Revenue Drop"
    )
)

print(
    service.generate_recovery_plan(
        "Inventory Shortage"
    )
)

print(
    service.generate_executive_summary(
        "Revenue Drop",
        "Inventory Shortage",
        12000
    )
)