import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.modelos import db, Project, TechnicalSkills, SoftSkills, Role, TeamProject, MembersTeamProject, VacancyProject, ApplicantsVacancyProject

from application import application as app

@pytest.fixture(scope = 'module')
def new_project():
    project = Project(
        name = 'Project 1',
        companyId = 1,
        details = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    )
    return project

@pytest.fixture(scope = 'module')
def new_technical_skills():
    technical_skills = TechnicalSkills(
        name = 'Python'
    )
    return technical_skills

@pytest.fixture(scope = 'module')
def new_soft_skills():
    soft_skills = SoftSkills(
        name = 'Escuchar'
    )
    return soft_skills

@pytest.fixture(scope = 'module')
def new_role():
    role = Role(
        name = 'Project Manager'
    )
    return role

@pytest.fixture(scope = 'module')
def new_team_project():
    team_project = TeamProject(
        name = 'John Doe',
        projectId = 1
    )
    return team_project

@pytest.fixture(scope = 'module')
def new_member_team_project():
    member_team_project = MembersTeamProject(
        teamId = 1,
        userId = 1,
        isIntern = False,
        role = 1
    )
    return member_team_project

@pytest.fixture(scope = 'module')
def new_vacancy_project():
    role = Role(
        name = 'Project Manager'
    )
    technical_skills = TechnicalSkills(
        name = 'Python'
    )
    soft_skills = SoftSkills(
        name = 'Escuchar'
    )
    vacancy_project = VacancyProject(
        name = 'Project Manager',
        projectId = 1,
        details = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        places = 5,
        roles = [role],
        technicalSkills = [technical_skills],
        softSkills = [soft_skills]
    )
    return vacancy_project

@pytest.fixture(scope = 'module')
def new_applicants_vacancy_project():
    applicants_vacancy_project = ApplicantsVacancyProject(
        vacancyId = 1,
        userId = 1
    )
    return applicants_vacancy_project

def test_project_model(new_project):
    # Add the object to the database
    p = Project(new_project.name,
                new_project.companyId,
                new_project.details)

    # Check that the retrieved object matches the original object
    assert p.name == 'Project 1'
    assert p.companyId == 1
    assert p.details == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'

def test_technical_skills_model(new_technical_skills):
    # Add the object to the database
    tsp = TechnicalSkills(new_technical_skills.name)

    # Check that the retrieved object matches the original object
    assert tsp.name == 'Python'

def test_soft_skills_model(new_soft_skills):
    # Add the object to the database
    ssp = SoftSkills(new_soft_skills.name)

    # Check that the retrieved object matches the original object
    assert ssp.name == 'Escuchar'

def test_role_model(new_role):
    # Add the object to the database
    r = Role(new_role.name)

    # Check that the retrieved object matches the original object
    assert r.name == 'Project Manager'

def test_team_project_model(new_team_project):
    # Add the object to the database
    tp = TeamProject(new_team_project.name,
                     new_team_project.projectId)

    # Check that the retrieved object matches the original object
    assert tp.name == 'John Doe'
    assert tp.projectId == 1

def test_member_team_project_model(new_member_team_project):
    # Add the object to the database
    mtp = MembersTeamProject(new_member_team_project.teamId,
                             new_member_team_project.userId,
                             new_member_team_project.isIntern,
                             new_member_team_project.role)

    # Check that the retrieved object matches the original object
    assert mtp.teamId == 1
    assert mtp.userId == 1
    assert mtp.isIntern == False
    assert mtp.role == 1

def test_vacancy_project_model(new_vacancy_project):
    # Add the object to the database
    vp = VacancyProject(new_vacancy_project.name,
                        new_vacancy_project.projectId,
                        new_vacancy_project.details,
                        new_vacancy_project.places,
                        new_vacancy_project.roles,
                        new_vacancy_project.technicalSkills,
                        new_vacancy_project.softSkills)

    # Check that the retrieved object matches the original object
    assert vp.name == 'Project Manager'
    assert vp.projectId == 1
    assert vp.details == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    assert vp.places == 5

def test_applicants_vacancy_project_model(new_applicants_vacancy_project):
    # Add the object to the database
    avp = ApplicantsVacancyProject(new_applicants_vacancy_project.vacancyId,
                                   new_applicants_vacancy_project.userId)

    # Check that the retrieved object matches the original object
    assert avp.vacancyId == 1
    assert avp.userId == 1
