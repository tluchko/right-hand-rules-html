import magneticrhr

for charge_type in ['current']:  # , 'particle']
    rhr = magneticrhr.MagneticRHR(charge_type=charge_type)
    directions = list(rhr.directions.keys())
    directions.remove((0, 0, 0))
    for choice in ['magnetic force', 'magnetic field', 'particle']:
        for direction1 in directions:
            for direction2 in directions:
                for charge in [-1, 1]:
                    rhr.display_problem(
                        charge=charge, unknown_choice=choice, known1Vec=direction1, known2Vec=direction2)
