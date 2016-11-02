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


def make_claimant_dir(full_name):
    try_path = os.path.abspath(".") + "/outputs/" + full_name
    if os.path.exists(try_path):
        pass
    else:
        os.mkdir(try_path)


def fill_template(doctype, user):
    doc_metadata = {
        "decision": {
            "template_path": "templates/TemplateDecisionNotice.docx",
            "output_path": "outputs/{0}/DecisionNotice_Final({1}).docx"
        },
        "recommendation": {
            "template_path": "templates/TemplatePayRecVer.docx",
            "output_path": "outputs/{0}/PayRecVer({1}).docx"
        },
    }

    doc = DocxTemplate(doc_metadata[doctype]["template_path"])
    doc.render(user)
    full_claim_name = user["claim_number"] + "-" + user["claim_name"]
    make_claimant_dir(full_claim_name)
    output_path_string = doc_metadata[doctype]["output_path"]
    output_path = output_path_string.format(
        full_claim_name, full_claim_name)
    doc.save(output_path)


def main():
    users = load_users()
    for user in users:
        if not verify(user):
            raise NotImplementedError(
                "User {0} is messed up!".format(user["claim_number"]))
        user["date"] = datetime.date.today().strftime("%B %-d, %Y")
        fill_template("decision", user)
        fill_template("recommendation", user)

if __name__ == '__main__':
    main()
