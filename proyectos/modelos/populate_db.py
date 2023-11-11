from modelos.modelos import db, Role

def upsert_role(name):
    role = Role.query.filter_by(name=name).first()
    if not role:
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()

    # PROJECT_MANAGER = 1
    # PRODUCT_OWNER = 2
    # SCRUM_MASTER = 3
    # DEVELOPMENT_BACK = 4
    # DEVELOPMENT_FRONT = 5
    # ARCHITECT = 6
    # UIUX_DESIGNER = 7
    # QUALITY_ASSURANCE = 8
    # BUSINESS_ANALYST = 9
    # SYSTEM_ANALYST = 10
    # DEVOPS_ENGINEER = 11
    # TECHNICAL_WRITER = 12

def populate_database():

    roles_data = [
        {"name": "Project Manager"},
        {"name": "Product Owner"},
        {"name": "Scrumb Master"},
        {"name": "Development Back"},
        {"name": "Development Front"},
        {"name": "Architect"},
        {"name": "UI/UX Designer"},
        {"name": "Quality Assurance"},
        {"name": "Business Analyst"},
        {"name": "System Analyst"},
        {"name": "DevOps Engineer"},
        {"name": "Technical Writer"}
        # Add more roles
    ]
    for role in roles_data:
        upsert_role(role["name"])
