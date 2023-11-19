from modelos.modelos import db, Role, TechnicalSkills, SoftSkills

def upsert_role(name):
    role = Role.query.filter_by(name=name).first()
    if not role:
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()

def upsert_technical_skill(name):
    technical_skill = TechnicalSkills.query.filter_by(name=name).first()
    if not technical_skill:
        technical_skill = TechnicalSkills(name=name)
        db.session.add(technical_skill)
        db.session.commit()

def upsert_soft_skill(name):
    soft_skill = SoftSkills.query.filter_by(name=name).first()
    if not soft_skill:
        soft_skill = SoftSkills(name=name)
        db.session.add(soft_skill)
        db.session.commit()

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

    technical_skills_data = [
        {"name": "Java"},
        {"name": "Python"},
        {"name": "C#"},
        {"name": "C++"},
        {"name": "JavaScript"},
        {"name": "PHP"},
        {"name": "Ruby"},
        {"name": "Swift"},
        {"name": "Kotlin"},
        {"name": "Go"},
        {"name": "Scala"},
        {"name": "Rust"},
        {"name": "TypeScript"},
        {"name": "SQL"},
        {"name": "NoSQL"},
    ]
    for technical_skill in technical_skills_data:
        upsert_technical_skill(technical_skill["name"])

    soft_skills_data = [
        {"name": "Escuchar"},
        {"name": "Comunicación"},
        {"name": "Trabajo en equipo"},
        {"name": "Pensamiento crítico"},
        {"name": "Resolución de problemas"},
        {"name": "Flexibilidad"},
        {"name": "Creatividad"},
        {"name": "Empatía"},
        {"name": "Liderazgo"},
        {"name": "Gestión del tiempo"},
    ]
    for soft_skill in soft_skills_data:
        upsert_soft_skill(soft_skill["name"])
