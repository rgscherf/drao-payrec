from docxtpl import DocxTemplate
import os
import shutil

doc_metadata = {
    "decision": {
        "template_path": "templates/TemplateDecisionNotice.docx",
        "template_path_nopay": "templates/TemplateDecisionNoticeNoPay.docx",
        "output_path": "{0}/DecisionNotice_Final({1}).docx"
    },
    "verification": {
        "template_path": "templates/TemplatePayRecVer.docx",
        "output_path": "{0}/PayRecVer({1}).docx"
    },
    "payrec_from_cl": {
        "output_path": "{0}/PayRec({1}).docx"
    },
    "adjexp": {
        "output_path": "{0}/AdjExp({1}).docx"
    },
}


def make_claimant_dir(full_name, disaster):
    try_path = os.path.abspath(".") + "/outputs/" + disaster + "/" + full_name
    if not os.path.exists(try_path):
        os.makedirs(try_path)
    return try_path


def make_filepath(doctype, user):
    full_claim_name = user["claim_number"] + "-" + user["claim_name"]
    path_to_claimant = make_claimant_dir(full_claim_name, user["disasterId"])
    output_path_string = doc_metadata[doctype]["output_path"]
    output_path = output_path_string.format(
        path_to_claimant, full_claim_name)
    return output_path


def fill_template(doctype, user):
    if doctype == "decision":
        if user["pay_amount"] != 0:
            template_document = DocxTemplate(
                doc_metadata[doctype]["template_path_nopay"])
        else:
            template_document = DocxTemplate(
                doc_metadata[doctype]["template_path"])
        template_document.render(user)
        new_path = make_filepath(doctype, user)
        template_document.save(new_path)
    elif doctype == "verification":
        template_document = DocxTemplate(
            doc_metadata[doctype]["template_path"])
        template_document.render(user)
        new_path = make_filepath(doctype, user)
        template_document.save(new_path)
    elif doctype == "payrec_from_cl":
        old_path_local = "./payrecs/{}rec.DOC".format(user["claim_number"])
        old_path_abs = os.path.abspath(old_path_local)
        new_path = make_filepath(doctype, user)
        shutil.copy(old_path_abs, new_path)
    elif doctype == "adjexp":
        if user["adj_exp_included"]:
            old_path_local = "./payrecs/{}adj.DOC".format(user["claim_number"])
            old_path_abs = os.path.abspath(old_path_local)
            new_path = make_filepath(doctype, user)
            shutil.copy(old_path_abs, new_path)


def verify(user):
    return user


def write_templates_for_user(user):
    """ root for this module 
    called once for every user in pay rec list. """

    if not verify(user):
        raise NotImplementedError(
            "User {0} is messed up!".format(user["claim_number"]))

    fill_template("decision", user)
    fill_template("verification", user)
    fill_template("payrec_from_cl", user)
    fill_template("adjexp", user)
