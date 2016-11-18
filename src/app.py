import json
import logging_utils
from write_templates import write_templates_for_user


def load_users():
    users_path = "USERS.json"
    with open(users_path, "r") as JSON:
        return json.load(JSON)


def main():
    log = logging_utils.get_logger()
    logging_utils.write_preprocess_log(log)

    users = load_users()
    total_users = len(users)
    processed_users = 0

    for user in users:
        write_templates_for_user(user)
        log.info(
            "Processed claim {0}-{1}".format(user["claim_number"], user["claim_name"]))
        processed_users += 1

    logging_utils.write_postprocess_log(log, processed_users, total_users)


if __name__ == '__main__':
    main()
