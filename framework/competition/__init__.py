from framework.DataObjects import PkmRoster, Pkm, PkmTemplate, PkmFullTeam


def legal_move_set(pkm: Pkm, template: PkmTemplate):
    for move in pkm.moves:
        valid = False
        for roster_move in template.move_roster:
            valid = move == roster_move
            if valid:
                break
        if not valid:
            return False
    return True


def legal_team(team: PkmFullTeam, roster: PkmRoster) -> bool:
    for pkm in team.pkm_list:
        valid = False
        for template in roster:
            valid = pkm.type == template.type and pkm.max_hp == template.max_hp and legal_move_set(pkm, template)
            if valid:
                break
        if not valid:
            return False
    return True
