import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.modelos import db, Project, TechnicalSkillsProject, SoftSkillsProject, Role, TeamProject, VacancyProject, ApplicantsVacancyProject
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
def new_technical_skills_project():
    technical_skills_project = TechnicalSkillsProject(
        name = 'Python',
        projectId = 1
    )
    return technical_skills_project

@pytest.fixture(scope = 'module')
def new_soft_skills_project():
    soft_skills_project = SoftSkillsProject(
        name = 'Escuchar',
        projectId = 1
    )
    return soft_skills_project

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
        projectId = 1,
        userId = 1,
        isIntern = False,
        role = 1
    )
    return team_project

@pytest.fixture(scope = 'module')
def new_vacancy_project():
    vacancy_project = VacancyProject(
        name = 'Project Manager',
        details = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        places = 5,
        roles = [1, 2, 3],
        technicalSkills = [1, 2, 3],
        softSkills = [1, 2, 3]
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

def test_technical_skills_project_model(new_technical_skills_project):
    # Add the object to the database
    tsp = TechnicalSkillsProject(new_technical_skills_project.name,
                                new_technical_skills_project.projectId)

    # Check that the retrieved object matches the original object
    assert tsp.name == 'Python'
    assert tsp.projectId == 1

def test_soft_skills_project_model(new_soft_skills_project):
    # Add the object to the database
    ssp = SoftSkillsProject(new_soft_skills_project.name,
                            new_soft_skills_project.projectId)

    # Check that the retrieved object matches the original object
    assert ssp.name == 'Escuchar'
    assert ssp.projectId == 1

def test_role_model(new_role):
    # Add the object to the database
    r = Role(new_role.name)

    # Check that the retrieved object matches the original object
    assert r.name == 'Project Manager'

def test_team_project_model(new_team_project):
    # Add the object to the database
    tp = TeamProject(new_team_project.name,
                     new_team_project.projectId,
                     new_team_project.userId,
                     new_team_project.isIntern,
                     new_team_project.role)

    # Check that the retrieved object matches the original object
    assert tp.name == 'John Doe'
    assert tp.projectId == 1
    assert tp.userId == 1
    assert tp.isIntern == False
    assert tp.role == 1

# def test_vacancy_project_model(new_vacancy_project):
#     # Add the object to the database
#     vp = VacancyProject(new_vacancy_project.name,
#                         new_vacancy_project.details,
#                         new_vacancy_project.places,
#                         new_vacancy_project.roles,
#                         new_vacancy_project.technicalSkills,
#                         new_vacancy_project.softSkills)

#     # Check that the retrieved object matches the original object
#     assert vp.name == 'Project Manager'
#     assert vp.details == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
#     assert vp.places == 5
#     assert vp.roles == [1, 2, 3]
#     assert vp.technicalSkills == [1, 2, 3]
#     assert vp.softSkills == [1, 2, 3]

def test_applicants_vacancy_project_model(new_applicants_vacancy_project):
    # Add the object to the database
    avp = ApplicantsVacancyProject(new_applicants_vacancy_project.vacancyId,
                                   new_applicants_vacancy_project.userId)

    # Check that the retrieved object matches the original object
    assert avp.vacancyId == 1
    assert avp.userId == 1
