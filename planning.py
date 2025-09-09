from constraint import *
problem = Problem()
slots = {
    "Sunday":    [1, 2, 3, 4, 5],
    "Monday":    [1, 2, 3, 4, 5],
    "Tuesday":   [1, 2, 3],
    "Wednesday": [1, 2, 3, 4, 5],
    "Thursday":  [1, 2, 3, 4, 5],
}
all_slots = [(day, slot) for day, slot_list in slots.items() for slot in slot_list]
variables = [
    "Securite_L", "Securite_TD",
    "MF_L", "MF_TD",
    "AN_L", "AN_TD",
    "ENT_L",
    "RO_L", "RO_TD",
    "DAIC_L", "DAIC_TD",
    "R2_L", "R2_TD", "R2_TP",
    "AI_L", "AI_TD", "AI_TP"
]

for var in variables:
    problem.addVariable(var, all_slots)
def all_different(*args):
    return len(set(args)) == len(args)
problem.addConstraint(all_different, variables)


courses = [
    ["Securite_L", "Securite_TD"],
    ["MF_L", "MF_TD"],
    ["AN_L", "AN_TD"],
    ["RO_L", "RO_TD"],
    ["DAIC_L", "DAIC_TD"],
    ["R2_L", "R2_TD", "R2_TP"],
    ["AI_L", "AI_TD", "AI_TP"],
]

for group in courses:
    problem.addConstraint(all_different, group)

def no_4_or_5_successive(*args):
    day_slots = {}
    for (day, slot) in args:
        if day not in day_slots:
            day_slots[day] = []
        day_slots[day].append(slot)
    for slot_list in day_slots.values():
        slot_list.sort()
        for i in range(len(slot_list) - 3):
            if slot_list[i+3] - slot_list[i] == 3:
                return False
        for i in range(len(slot_list) - 4):
            if slot_list[i+4] - slot_list[i] == 4:
                return False
    return True

problem.addConstraint(no_4_or_5_successive, variables)
teacher_sessions = {
    "Teacher1":  ["Securite_L", "Securite_TD"],
    "Teacher2":  ["MF_L", "MF_TD"],
    "Teacher3":  ["AN_L", "AN_TD"],
    "Teacher4":  ["ENT_L"],
    "Teacher5":  ["RO_L", "RO_TD"],
    "Teacher6":  ["DAIC_L", "DAIC_TD"],
    "Teacher7":  ["R2_L", "R2_TD"],
    "Teacher8":  ["R2_TP"],
    "Teacher9":  ["R2_TP"],
    "Teacher10": ["R2_TP"],
    "Teacher11": ["AI_L", "AI_TD"],
    "Teacher12": ["AI_TP"],
    "Teacher13": ["AI_TP"],
    "Teacher14": ["AI_TP"]
}

for teacher, sessions in teacher_sessions.items():
    if len(sessions) > 1:
        problem.addConstraint(all_different, sessions)

# Solve and display result
solution = problem.getSolution()
if solution:
    for session, slot in sorted(solution.items()):
        print(f"{session}: {slot}")
else:
    print("No solution found.")