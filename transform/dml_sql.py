def insert_dtp(card):
    yield f"""
        INSERT INTO dtp (
            id, 
            registration_number, 
            date_time, 
            dtp_type, 
            district, 
            vehicle_count, 
            participant_count, 
            died, 
            injured,
            coord_l, 
            coord_w, 
            change_org_motion, 
            road, 
            road_condition,
            road_category,
            road_value,
            settlement,
            street,
            street_category,
            house,
            km_mark,
            m_mark,
            lighting_condition,
            dtp_scheme_number
        ) 
        VALUES (
            {card["KartId"]},
            '{card["emtp_number"]}',
            '14.01.2022 20:45',
            '{card["DTP_V"]}',
            '{card["District"]}',
            {card["K_TS"]},
            {card["K_UCH"]},
            {card["POG"]},
            {card["RAN"]},
            '{card["infoDtp"]["COORD_L"]}',
            '{card["infoDtp"]["COORD_W"]}',
            '{card["infoDtp"]["change_org_motion"]}',
            '{card["infoDtp"]["dor"]}',
            '{card["infoDtp"]["s_pch"]}',
            '{card["infoDtp"]["dor_k"]}',
            '{card["infoDtp"]["dor_z"]}',
            '{card["infoDtp"]["n_p"]}',
            '{card["infoDtp"]["street"]}',
            '{card["infoDtp"]["k_ul"]}',
            '{card["infoDtp"]["house"]}',
            {card["infoDtp"]["km"]},
            {card["infoDtp"]["m"]},
            '{card["infoDtp"]["osv"]}',
            {card["infoDtp"]["s_dtp"]}
        );
        """


def insert_objects(card):
    for objects in card["infoDtp"]["OBJ_DTP"]:
        yield f"""
                INSERT INTO dtp_objects (
                    card_id, 
                    object_description
                ) 
                VALUES (
                    {card["KartId"]},
                    '{objects}'
                );
                """


def insert_factors(card):
    for factor in card["infoDtp"]["factor"]:
        yield f"""
                INSERT INTO dtp_factors (
                    card_id, 
                    factor
                ) 
                VALUES (
                    {card["KartId"]},
                    '{factor.replace("'", '"')}'
                );
                """


def insert_ndu(card):
    for ndu in card["infoDtp"]["ndu"]:
        yield f"""
                INSERT INTO dtp_ndu (
                    card_id, 
                    ndu_value
                ) 
                VALUES (
                    {card["KartId"]},
                    '{ndu}'
                );
                """


def insert_weather(card):
    for weather in card["infoDtp"]["s_pog"]:
        yield f"""
                INSERT INTO dtp_weather (
                    card_id, 
                    weather_condition
                ) 
                VALUES (
                    {card["KartId"]},
                    '{weather}'
                );
                """


def insert_road_sections(card):
    for section in card["infoDtp"]["sdor"]:
        yield f"""
                INSERT INTO dtp_road_sections (
                    card_id, 
                    section_description
                ) 
                VALUES (
                    {card["KartId"]},
                    '{section}'
                );
                """


def insert_vehicles_with_participants(card):
    for ts in card["infoDtp"]["ts_info"]:
        vehicle_id = f'vehicle_{card["KartId"]}_{ts["n_ts"]}'
        yield f"""
                INSERT INTO dtp_vehicles (
                    id,
                    card_id,
                    color,
                    ownership_form,
                    manufacture_year,
                    trailer,
                    model,
                    brand,
                    owner_type,
                    drive_type,
                    technical_faults,
                    class,
                    status
                ) VALUES (
                    '{vehicle_id}',
                    {card["KartId"]},
                    '{ts["color"]}',
                    '{ts["f_sob"]}',
                    '{ts["g_v"]}',
                    '{ts["m_pov"]}',
                    '{ts["m_ts"]}',
                    '{ts["marka_ts"]}',
                    '{ts["o_pf"]}',
                    '{ts["r_rul"]}',
                    '{ts["t_n"]}',
                    '{ts["t_ts"]}',
                    '{ts["ts_s"]}'
                );
                """
        for index, participant in enumerate(ts["ts_uch"]):
            participant_id = f'participant_{participant["N_UCH"]}_{vehicle_id}_{index}'
            yield f"""
                    INSERT INTO dtp_vehicle_participants (
                        id,
                        vehicle_id,
                        role,
                        sex,
                        safety_belt,
                        fled,
                        injury_status,
                        age,
                        alco,
                        seat_group
                    ) VALUES (
                        '{participant_id}',
                        '{vehicle_id}',
                        '{participant["K_UCH"]}',
                        '{participant["POL"]}',
                        '{participant["SAFETY_BELT"]}',
                        '{participant["S_SM"]}',
                        '{participant["S_T"]}',
                        '{participant["V_ST"]}',
                        '{participant["ALCO"]}',
                        '{participant["S_SEAT_GROUP"]}'
                    );
                    """
            yield from _insert_violations(participant, participant_id)


def insert_participants(card):
    for participant in card["infoDtp"]["uchInfo"]:
        participant_id = f'participant_{card["KartId"]}_{participant["N_UCH"]}'
        yield f"""
                INSERT INTO dtp_participants (
                    id,
                    card_id,
                    role,
                    sex,
                    fled,
                    injury_status,
                    age,
                    alco
                ) VALUES (
                    '{participant_id}',
                    {card["KartId"]},
                    '{participant["K_UCH"]}',
                    '{participant["POL"]}',
                    '{participant["S_SM"]}',
                    '{participant["S_T"]}',
                    '{participant["V_ST"]}',
                    '{participant["ALCO"]}'
                );
                """
        yield from _insert_violations(participant, participant_id)


def _insert_violations(participant, participant_id):
    for violation in participant["NPDD"]:
        yield f"""
                        INSERT INTO dtp_violations (
                            participant_id,
                            violation_code
                        ) VALUES (
                            '{participant_id}',
                            '{violation}'
                        );
                        """
    for violation in participant["SOP_NPDD"]:
        yield f"""
                        INSERT INTO dtp_violations (
                            participant_id,
                            violation_code
                        ) VALUES (
                            '{participant_id}',
                            '{violation}'
                        );
                        """
