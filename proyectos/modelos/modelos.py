from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    companyId = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(250), nullable=False)

    def __init__(self, name, companyId, details):
        self.name = name
        self.companyId = companyId
        self.details = details

class TechnicalSkills(db.Model):
    __tablename__ = 'technical_skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class SoftSkills(db.Model):
    __tablename__ = 'soft_skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class TeamProject(db.Model):
    __tablename__ = 'team_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='SET NULL'))

    def __init__(self, name, projectId):
        self.name = name
        self.projectId = projectId

class MembersTeamProject(db.Model):
    __tablename__ = 'member_team_project'
    id = db.Column(db.Integer, primary_key=True)
    teamId = db.Column(db.Integer, db.ForeignKey('team_project.id', ondelete='SET NULL'))
    userId = db.Column(db.Integer, nullable=False)
    isIntern = db.Column(db.Boolean, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='SET NULL'))

    def __init__(self, teamId, userId, isIntern, role):
        self.teamId = teamId
        self.userId = userId
        self.isIntern = isIntern
        self.role = role

vacancy_role_association = db.Table(
    'vacancy_role_id',
    db.Column('vacancy_id', db.Integer, db.ForeignKey('vacancy_project.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

vacancy_technical_skills_association = db.Table(
    'vacancy_technical_skills_id',
    db.Column('vacancy_project_id', db.Integer, db.ForeignKey('vacancy_project.id')),
    db.Column('technical_skills_id', db.Integer, db.ForeignKey('technical_skills.id'))
)

vacancy_soft_skills_association = db.Table(
    'vacancy_soft_skills_id',
    db.Column('vacancy_project_id', db.Integer, db.ForeignKey('vacancy_project.id')),
    db.Column('soft_skills_id', db.Integer, db.ForeignKey('soft_skills.id'))
)

class VacancyProject(db.Model):
    __tablename__ = 'vacancy_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='SET NULL'))
    details = db.Column(db.String(250), nullable=False)
    places = db.Column(db.Integer, nullable=False)
    roles = db.relationship('Role', secondary=vacancy_role_association,
                                     backref=db.backref('vacancy_project', lazy='dynamic'))
    technicalSkills = db.relationship('TechnicalSkills', secondary=vacancy_technical_skills_association,
                                     backref=db.backref('vacancy_project', lazy='dynamic'))
    softSkills = db.relationship('SoftSkills', secondary=vacancy_soft_skills_association,
                                     backref=db.backref('vacancy_project', lazy='dynamic'))

    def __init__(self, name, projectId, details, places, roles, technicalSkills, softSkills):
        self.name = name
        self.projectId = projectId
        self.details = details
        self.places = places
        self.roles = roles
        self.technicalSkills = technicalSkills
        self.softSkills = softSkills

class ApplicantsVacancyProject(db.Model):
    __tablename__ = 'applicants_vacancy_project'
    id = db.Column(db.Integer, primary_key=True)
    vacancyId = db.Column(db.Integer, db.ForeignKey('vacancy_project.id', ondelete='SET NULL'))
    userId = db.Column(db.Integer, nullable=False)

    def __init__(self, vacancyId, userId):
        self.vacancyId = vacancyId
        self.userId = userId

class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        load_instance = True

class TechnicalSkillsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TechnicalSkills
        include_relationships = True
        load_instance = True

class SoftSkillsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SoftSkills
        include_relationships = True
        load_instance = True

class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_relationships = True
        load_instance = True

class TeamProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TeamProject
        include_relationships = True
        load_instance = True

class MembersTeamProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MembersTeamProject
        include_relationships = True
        load_instance = True

class VacancyProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VacancyProject
        include_relationships = True
        load_instance = True

class ApplicantsVacancyProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApplicantsVacancyProject
        include_relationships = True
        load_instance = True
