# -*- coding: utf-8 -*-

import os
import mistune
from mako.lookup import TemplateLookup
import json
import shutil

class apihero:
    config_path = None
    template_path = None
    docs_path = None
    build_path = None
    config = None
    docs_list = {}
    docs_list_detail = {}
    doc_response_reserved = {
        '_res_ok.json': 'res_ok',
        '_res_fail.json': 'res_fail',
        '_res_sample.json': 'res_sample',
        '_res_ok.xml': 'res_sample',
        '_res_fail.xml': 'res_sample',
        '_res_sample.xml': 'res_sample'}

    def __init__(self):
        self.template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'bootstrap-material')
        if os.path.isdir(self.template_path):
            self.template_lookup = TemplateLookup(directories=[self.template_path],
                                                  input_encoding='utf-8',
                                                  output_encoding='utf-8',
                                                  encoding_errors='replace')
        self.markdown = mistune.Markdown()



    def set_template_path(self, path):
        if self.config is not None:
            if "template" in self.config:
                tmp_path = os.path.join(path, self.config['template'])
                if os.path.isdir(tmp_path):
                    self.template_path = tmp_path
                    self.template_lookup = TemplateLookup(directories=[self.template_path])

    def set_config_path(self, path):
        self.config_path = path
        self._read_config()

    def _read_config(self):
        import json
        config_path = os.path.join(self.config_path, 'config.json')
        self.config = json.loads(self.get_file_content(config_path))

    def set_docs_path(self, path):
        self.docs_path = path
        self._read_docs_list()
        self._read_docs_list_detail()

    def _read_docs_list(self):
        reserved_ends = ['.md']
        for reserved, restype in self.doc_response_reserved.items():
            reserved_ends.append(reserved)

        self.versions = os.listdir(self.docs_path)
        temp_docs = {}
        for version in self.versions:
            version_path = os.path.join(self.docs_path, version)
            temp_docs[version]= os.listdir(version_path)
            # find and remove reserved substring's
            for doc in list(temp_docs[version]):
                for findfor in reserved_ends:
                    if doc[-len(findfor):] == findfor:
                        temp_docs[version].remove(doc)

        self.docs_list = temp_docs


    def _read_docs_list_detail(self):
        self.docs_list_detail = {}
        for version, docs in self.docs_list.items():
            self.docs_list_detail[version]=[]
            for doc in docs:
                filename, file_extension = os.path.splitext(doc)
                doc_path = os.path.join(self.docs_path, version, doc)
                doc_content = self.get_file_content(doc_path)
                if doc_content.strip() != "":
                    doc_content = json.loads(doc_content)
                    self.docs_list_detail[version].append({
                        "name": filename,
                        "title": doc_content["title"],
                        "resource": doc_content["resource"],
                        "method": doc_content["method"]
                    })



    def set_build_path(self, path):
        self.build_path = path



    def build_index(self):
        index_description_path = os.path.join(self.config_path, "description.md")
        build_index_path = os.path.join(self.build_path, "index.html")

        # load description
        description = ""
        if os.path.exists(index_description_path):
            description = self.get_file_content(index_description_path)
            if description.strip() != "":
                description = self.markdown(description)
        if description == "":
            if "description" in self.config:
                description = self.config['description']

        template = self.template_lookup.get_template("index.html")
        template_output = template.render(config=self.config, versions=self.versions, description= description)
        self.put_file_content(build_index_path, template_output)


    def get_file_content(self, path):
        res = ""
        with open(path) as data_file:
            res = data_file.read()
        return res

    def put_file_content(self, path, content, writemode="w+"):
        with open(path, writemode) as data_file:
            data_file.write(content.decode("utf-8") )

    def build_versions_index(self):
        template = self.template_lookup.get_template("docs_list.html")
        for version, docs in self.docs_list.items():
            build_version_index_path = os.path.join(self.build_path, version, "index.html")
            version_index_description_path = os.path.join(self.docs_path, version, "_description.md")
            # load description
            description = ""
            if os.path.exists(version_index_description_path):
                description = self.get_file_content(version_index_description_path)
                if description.strip() != "":
                    description = self.markdown(description)
            template_output = template.render(config=self.config,
                                              version=version,
                                              docs= self.docs_list_detail[version],
                                              description=description)
            self.put_file_content(build_version_index_path, template_output)


    def get_doc_all_res(self, version, doc_name):
        filename, file_extension = os.path.splitext(doc_name)
        out = {}
        for reserved, restype in self.doc_response_reserved.items():
            path = os.path.join(self.docs_path, version, filename + reserved)
            out[restype] = ""
            if os.path.exists(path):
                out[restype] = self.get_file_content(path)
        return out

    def get_doc_description(self, version, doc_name):
        filename, file_extension = os.path.splitext(doc_name)
        doc_description_path = os.path.join(self.docs_path, version, filename + ".md")
        out = ""
        if os.path.exists(doc_description_path):
            out = self.markdown(self.get_file_content(doc_description_path))
        return out


    def build_docs(self):
        # template_docs_single_path = os.path.join(self.template_path, "docs_single.html")
        template = self.template_lookup.get_template("docs_single.html")
        for version, docs in self.docs_list.items():
            for doc_name in docs:
                filename, file_extension = os.path.splitext(doc_name)
                build_docs_single_path = os.path.join(self.build_path, version, filename+".html")
                doc_path = os.path.join(self.docs_path, version, doc_name)
                doc_content_raw = self.get_file_content(doc_path)
                doc_content = None
                try:
                    doc_content = json.loads(doc_content_raw)
                except:
                    doc_content = None

                if doc_content is not None:
                    # include external description file
                    if "description" in doc_content:
                        doc_content['description'] = self.markdown(doc_content["description"])
                    else:
                        doc_content['description'] = self.get_doc_description(version, doc_name)

                    # prepare contents for template
                    doc_content['name']= filename
                    doc_content.update(self.get_doc_all_res(version, doc_name))

                    template_output = template.render(config=self.config,
                                                      version=version,
                                                      doc=doc_content,
                                                      docs=self.docs_list_detail)
                    self.put_file_content(build_docs_single_path, template_output)

    def build_assets(self):
        template_assets_path = os.path.join(self.template_path, "assets")
        if os.path.isdir(template_assets_path):
            build_assets_path = os.path.join(self.build_path, "assets")
            shutil.copytree(template_assets_path, build_assets_path)

    def build_prepare(self):
        if(os.path.isdir(self.build_path)):
            shutil.rmtree(self.build_path)

        os.makedirs(self.build_path, exist_ok=True)
        for version, docs in self.docs_list.items():
            version_path = os.path.join(self.build_path, version)
            os.makedirs(version_path, exist_ok=True)


def run():
    CWD_PATH = os.getcwd()
    app = apihero()
    app.set_config_path(CWD_PATH)
    app.set_docs_path(os.path.join(CWD_PATH, 'doc'))
    app.set_build_path(os.path.join(CWD_PATH, 'build'))
    app.set_template_path(os.path.join(CWD_PATH, 'template'))

    app.build_prepare()
    print("Build index...")
    app.build_index()
    print("Build version index...")
    app.build_versions_index()
    print("Build documents...")
    app.build_docs()
    print("Copy template assets...")
    app.build_assets()
    print("Done")


if __name__ == "__main__":
    try:
        run()

    except KeyboardInterrupt:
        print("Force exit, Keyboard Interrupt")