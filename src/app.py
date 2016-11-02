from docxtpl import DocxTemplate
import json
import datetime
import os


def load_users():
    users_path = "USERS.json"
    with open(users_path, "r") as JSON:
        return json.load(JSON)


def verify(user):
    return user


def make_claimant_dir(full_name, disaster):
    try_path = os.path.abspath(".") + "/outputs/" + disaster + "/" + full_name
    if not os.path.exists(try_path):
        os.makedirs(try_path)
    return try_path


def fill_template(doctype, user):
    doc_metadata = {
        "decision": {
            "template_path": "templates/TemplateDecisionNotice.docx",
            "template_path_nopay": "templates/TemplateDecisionNoticeNoPay.docx",
            "output_path": "{0}/DecisionNotice_Final({1}).docx"
        },
        "recommendation": {
            "template_path": "templates/TemplatePayRecVer.docx",
            "output_path": "{0}/PayRecVer({1}).docx"
        },
    }

    # when CL recommends no payment
    if doctype == "decision" and user["pay_amount"] == "0":
        doc = DocxTemplate(doc_metadata[doctype]["template_path_nopay"])
    else:
        doc = DocxTemplate(doc_metadata[doctype]["template_path"])
    doc.render(user)
    full_claim_name = user["claim_number"] + "-" + user["claim_name"]
    path_to_claimant = make_claimant_dir(full_claim_name, user["disasterId"])
    output_path_string = doc_metadata[doctype]["output_path"]
    output_path = output_path_string.format(
        path_to_claimant, full_claim_name)
    doc.save(output_path)


def main():
    users = load_users()
    total_users = len(users)
    processed_users = 0
    print("")
    print("================")
    print("Beginning claim processing...")
    print("================")
    for user in users:
        if not verify(user):
            raise NotImplementedError(
                "User {0} is messed up!".format(user["claim_number"]))
        user["date"] = datetime.date.today().strftime("%B %-d, %Y")
        fill_template("decision", user)
        fill_template("recommendation", user)
        print(
            "Processed claim {0}-{1}".format(user["claim_number"], user["claim_name"]))
        processed_users += 1
    print("================")
    print("Done processing.")
    print("Processed {0} claims out of {1} read from JSON.".format(
        processed_users, total_users))
    print("================")
    print("")

if __name__ == '__main__':
    main()
