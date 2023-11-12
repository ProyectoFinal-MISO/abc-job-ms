from modelos.modelos import db, Role, TechnicalSkillsProject, SoftSkillsProject, MembersTeamProject, TeamProject

def get_roles_details(array_roles):
  roles = []
  for item in Role.query.filter(Role.id.in_(array_roles)).all():
      roles.append({
          'id': item.id,
          'name': item.name
      })
  return roles

def get_technical_skills_details(array_technical_skills):
  technical_skills = []
  for item in TechnicalSkillsProject.query.filter(TechnicalSkillsProject.id.in_(array_technical_skills)).all():
      technical_skills.append({
          'id': item.id,
          'name': item.name
      })
  return technical_skills

def get_soft_skills_details(array_soft_skills):
  soft_skills = []
  for item in SoftSkillsProject.query.filter(SoftSkillsProject.id.in_(array_soft_skills)).all():
      soft_skills.append({
          'id': item.id,
          'name': item.name
      })
  return soft_skills

def get_teams_project(project_id):
    teams = []
    for team in TeamProject.query.filter_by(projectId=project_id).all():
        teams.append({
            'id': team.id,
            'name': team.name,
            'members': get_members_team(team.id)
        })
    return teams

def get_members_team(team_id):
    members = []
    for member in MembersTeamProject.query.filter_by(teamId=team_id).all():
        # TODO: get user details by userId
        members.append({
            'id': member.id,
            'userId': member.userId,
            'isIntern': member.isIntern,
            'role': member.role
        })
    return members
