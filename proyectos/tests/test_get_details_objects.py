from modelos.modelos import db, Role, TechnicalSkills, SoftSkills, MembersTeamProject, TeamProject
from utils.get_details_objects import get_role_detail, get_roles_details, get_technical_skills_details, get_soft_skills_details, get_teams_project, get_members_team
from utils.utils import generate_string_random

def test_get_roles_details():
    name = 'Project Manager' + generate_string_random(5)
    new_role = Role(
        name = name
    )
    db.session.add(new_role)
    db.session.commit()

    roles = get_roles_details([new_role.id])
    assert roles[0]['name'] == name

def test_get_technical_skills_details():
    name = 'Python' + generate_string_random(5)
    ts = TechnicalSkills(
        name = name
    )
    db.session.add(ts)
    db.session.commit()

    technical_skills = get_technical_skills_details([ts.id])
    assert technical_skills[0]['name'] == name

def test_get_soft_skills_details():
    name = 'Escuchar' + generate_string_random(5)
    ss = SoftSkills(
        name = name
    )
    db.session.add(ss)
    db.session.commit()

    soft_skills = get_soft_skills_details([ss.id])
    assert soft_skills[0]['name'] == name
