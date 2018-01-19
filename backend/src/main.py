# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Server main."""

# -------------------------------------------------------------------------

import json
import traceback
from pprint import pprint

import argparse
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_mongoengine import MongoEngine

import tasks
import tasks_wrapper
from log import log
from utils import to_str, path_to_dirs
from models import Sample, RefFile, RefGroup, RefDir, RefFileBelongTo, SampleBelongTo
from models import recur_del_ref_dir, clear_documents
from models_pe import clear_pe_documents, get_pe_value_list, pe_value_list_to_dict
from models_log import LogLine

# -------------------------------------------------------------------------

app = Flask(__name__)

# 跨站
CORS(app, supports_credentials=True)

# MongoDB 数据库
app.config["MONGODB_SETTINGS"] = {
    "host": "127.0.0.1",
    "port": 27019,
    "username": "lyclovechl",
    "password": "yGeIgWof97zXrzayOwcIhIaF5EqcUR",
    "authentication_source": "admin",
    "db": "malwrdb"
}
db = MongoEngine(app)


# -------------------------------------------------------------------------


def warn(info):
    """Warn."""
    log(__file__, info, "warn")


def error(info):
    """Error."""
    log(__file__, info, "error")


def debug(info):
    """Debug."""
    log(__file__, info, "debug")


# -------------------------------------------------------------------------

# Restful
api = Api(app)

# -------------------------------------------------------------------------


class TestAction(Resource):
    """Test stuff."""

    def get(self):
        """Wrapper for self._get()."""
        print("-" * 30 + "Test Action Get Start" + "-" * 30)
        ret = self._get()
        pprint(ret)
        print("+" * 30 + "Test Action Get End" + "+" * 30)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                raise Exception("no action provided!")

            print("action: " + action)

            if action == "test":
                return self.test_get()

            else:
                raise Exception("invalid action: %s" % action)

        except:
            error(traceback.format_exc())
            return "exception!"

    def post(self):
        """Wrapper of self._post()."""
        print("-" * 30 + "Test Action Set Start" + "-" * 30)
        ret = self._post()
        pprint(ret)
        print("+" * 30 + "Test Action Set End" + "+" * 30)
        return ret

    def _post(self):
        try:
            args = json.loads(to_str(request.data))
            if "action" not in args:
                raise Exception("no action!")

            action = args["action"]
            if action == "test":
                return self.test_set(args)

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception:\n" + str(e)

    def test_get(self):
        """Test get."""
        # import time
        # for x in range(10):
        #     yield x
        #     time.sleep(1)
        # yield "finish"
        return "test get finish"

    def test_set(self, args):
        """Test post."""
        pass


class LogLineAction(Resource):
    """LogLine manipulation."""

    def get(self):
        """Wrapper for self._get()."""
        print("-" * 30 + "LogLine Action Start" + "-" * 30)
        ret = self._get()
        pprint(ret)
        print("+" * 30 + "LogLine Action End" + "+" * 30)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                raise Exception("no action provided!")

            print("action: " + action)

            if action == "get_logLines":
                return self.get_log_lines()

            elif action == "clearLogLines":
                return self.clear_log_lines()

            else:
                raise Exception("invalid action: %s" % action)

        except:
            error(traceback.format_exc())
            return "exception!"

    def get_log_lines(self):
        """Return all logs from mongodb."""
        ret = []
        for log_ in LogLine.objects.order_by("-add_time"):
            ret.append(log_.json_ui())
        return ret

    def clear_log_lines(self):
        """Clear all logs in mongodb."""
        LogLine.drop_collection()
        return "success"


# -------------------------------------------------------------------------


class Action(Resource):
    """Default get handler.

    Will be refeactored in the future.
    """

    def get(self):
        """Wrapper for self._get()."""
        print("-" * 30 + "Action Start" + "-" * 30)
        ret = self._get()
        pprint(ret)
        print("+" * 30 + "Action End" + "+" * 30)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                raise Exception("no action provided!")

            if action == "":
                pass

            else:
                raise Exception("invalid action: %s" % action)

        except:
            error(traceback.format_exc())
            return "exception!"


class SetAction(Resource):
    """Default post handler."""

    def post(self):
        """Wrapper of self._post()."""
        print("-" * 30 + "Set Action Start" + "-" * 30)
        ret = self._post()
        pprint(ret)
        print("+" * 30 + "Set Action End" + "+" * 30)
        return ret

    def _post(self):
        try:
            args = json.loads(to_str(request.data))
            if "action" not in args:
                raise Exception("no action!")

            action = args["action"]
            if action == "":
                pass

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception:\n" + str(e)


class TreeAction(Resource):
    """Get or Set THE tree."""

    # -------------------------------------------------------------------------
    # Get

    def get(self):
        """Wrapper for self._get()."""
        print("-" * 30 + "Tree Action Get Start" + "-" * 30)
        ret = self._get()
        pprint(ret)
        print("+" * 30 + "Tree Action Get End" + "+" * 30)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                raise Exception("no action provided!")

            if action == "get_refGroupList":
                return self.get_ref_group_list()

            elif action == "get_topRefDirs":
                return self.get_top_ref_dir_list()

            elif action == "get_subRefDirs":
                return self.get_sub_ref_dir_list()

            elif action == "get_subSamples":
                return self.get_sub_sample_list()

            elif action == "get_subRefFiles":
                return self.get_sub_ref_file_list()

            else:
                raise Exception("invalid action: %s" % action)

        except:
            error(traceback.format_exc())
            return "exception!"

    def get_ref_group_list(self):
        """Retrieve all RefGroup from mongodb."""
        page_size = request.args.get("pageSize", None)
        page_index = request.args.get("pageIndex", None)
        if not page_size or not page_index:
            raise Exception("no pageSize or pageIndex provided!")
        page_size = int(page_size)
        page_index = int(page_index)

        ret = {"group_length": RefGroup.objects.count()}

        group_list = []
        for group in RefGroup.objects.order_by("-update_time").skip(page_index * page_size).limit(page_size):
            group_list.append(group.json_ui())
        # ret["group_list"] = group_list
        # todo: test....
        ret["group_list"] = group_list[:2]

        return ret

    def get_top_ref_dir_list(self):
        """Retrieve top RefDir by group_id from mongodb."""
        group_id = request.args.get("group_id", None)
        if not group_id:
            raise Exception("no group_id provided!")

        q_group = RefGroup.objects(group_id=group_id)
        if q_group.count() != 1:
            raise Exception("%d refGroup found by group_id %s" % (q_group.count(), group_id))
        group = q_group[0]

        q_dir = RefDir.objects(refGroup=group, parnetRefDir=None)
        if q_dir.count() != 1:
            raise Exception("no or too many top RefDir in group_id")

        # return a list, instead of standalone obj, to make it easier for frontend
        return [q_dir[0].json_ui()]

    def get_sub_ref_dir_list(self):
        """Retrieve sub RefDir list by parent ref_idr_id from mongodb."""
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            raise Exception("no refDir id provided!")

        q_ref_dir = RefDir.objects(pk=ref_dir_id)
        if q_ref_dir.count() != 1:
            raise Exception("no or too many refDir by ref_dir_id")
        ref_dir_cur = q_ref_dir[0]

        ret = []
        for ref_dir in RefDir.objects(parnetRefDir=ref_dir_cur):
            ret.append(ref_dir.json_ui())
        return ret

    def get_sub_sample_list(self):
        """Retrieve sub Sample by parent ref_dir_id from mongodb."""
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            raise Exception("no refDir id provided!")

        q_ref_dir = RefDir.objects(pk=ref_dir_id)
        if q_ref_dir.count() != 1:
            raise Exception("no or too many refDir by ref_dir_id")
        ref_dir_cur = q_ref_dir[0]

        ret = []
        for sample_belongto in SampleBelongTo.objects(refDir=ref_dir_cur):
            q_sample = Sample.objects(pk=sample_belongto.sample_id)
            if q_sample.count() != 1:
                raise Exception("no or too many sample by sample_id")
            sample = q_sample[0].json_ui()
            sample["sample_name"] = sample_belongto.sample_name
            ret.append(sample)
        return ret

    def get_sub_ref_file_list(self):
        """Retrieve sub RefFile list by parent ref_dir_id from mongodb."""
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            raise Exception("no refDir id provided!")

        q_ref_dir = RefDir.objects(pk=ref_dir_id)
        if q_ref_dir.count() != 1:
            raise Exception("no or too many refDir by ref_dir_id")
        ref_dir_cur = q_ref_dir[0]

        ret = []
        for file_belongto in RefFileBelongTo.objects(refDir=ref_dir_cur):
            q_ref_file = RefFile.objects(pk=file_belongto.ref_file_id)
            if q_ref_file.count() != 1:
                raise Exception("%d refFile by ref_file_id: %s" % (q_ref_file.count(), file_belongto.ref_file_id))
            ref_file = q_ref_file[0].json_ui()
            ref_file["file_name"] = file_belongto.file_name
            ret.append(ref_file)
        return ret

    # -------------------------------------------------------------------------
    # Post

    def post(self):
        """Wrapper for self._post()."""
        print("-" * 30 + "Tree Action Set Start" + "-" * 30)
        ret = self._post()
        pprint(ret)
        print("+" * 30 + "Tree Action Set End" + "+" * 30)
        return ret

    def _post(self):
        try:
            args = json.loads(to_str(request.data))
            if "action" not in args:
                raise Exception("no action!")

            action = args["action"]
            if action == "deleteRefDir":
                return self.del_ref_dir(args)

            elif action == "clearTree":
                return self.clear_tree(args)

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception:\n" + str(e)

    def del_ref_dir(self, args):
        """Delete RefDir and it's sub contents."""
        if "refDirId" not in args:
            raise Exception("no ref dir id provided!")
        ref_dir_id = args["refDirId"]

        q_ref_dir = RefDir.objects(pk=ref_dir_id)
        if q_ref_dir.count() != 1:
            raise Exception("0 or more than 1 ref dir by ref_dir_id")
        ref_dir = q_ref_dir[0]

        recur_del_ref_dir(ref_dir)

        return "delete ref dir success"

    def clear_tree(self, args):
        """Clear this tree."""
        clear_documents()
        clear_pe_documents()

        return "success"


class PeAction(Resource):
    """Get or Set Pe info."""

    # -------------------------------------------------------------------------
    # Get

    def get(self):
        """Wrapper for self._get()."""
        print("-" * 30 + "PE Action Get Start" + "-" * 30)
        ret = self._get()
        pprint(ret)
        print("+" * 30 + "PE Action Get End" + "+" * 30)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                raise Exception("no action provided!")

            if action == "get_HeaderInfo":
                return self.get_header_info()

            if action == "get_SectionInfo":
                return self.get_section_info()

            if action == "get_ImportInfo":
                return self.get_import_info()

            if action == "get_ExportInfo":
                return self.get_export_info()

            if action == "get_BehvFileInfo":
                return self.get_behv_file_info()

            else:
                raise Exception("invalid action: %s" % action)

        except:
            error(traceback.format_exc())
            return "exception!"

    def get_header_info(self):
        """Get pe header info."""
        sample_id = request.args.get("sample_id", None)
        if not sample_id:
            raise Exception("no sample id provided!")

        from models_pe import PeDosHeader, PeFileHeader, PeNtHeader

        # dos header

        q_dos_header = PeDosHeader.objects(sample_id=sample_id)
        if q_dos_header.count() != 1:
            raise Exception("%d dos header found for sample_id %s" % (q_dos_header.count(), sample_id))

        dos_header = []
        for value_structure in get_pe_value_list(q_dos_header[0]):
            dos_header.append(value_structure.json_ui())

        # file header

        q_file_header = PeFileHeader.objects(sample_id=sample_id)
        if q_file_header.count() != 1:
            raise Exception("%d file header found for sample_id %s" % (q_file_header.count(), sample_id))

        file_header = []
        for value_structure in get_pe_value_list(q_file_header[0]):
            file_header.append(value_structure.json_ui())

        # nt header

        q_nt_header = PeNtHeader.objects(sample_id=sample_id)
        if q_nt_header.count() != 1:
            raise Exception("%d nt header found for sample_id %s" % (q_nt_header.count(), sample_id))

        nt_header = []
        for value_structure in get_pe_value_list(q_nt_header[0]):
            nt_header.append(value_structure.json_ui())

        # combine

        ret = {}
        ret["dos_header"] = dos_header
        ret["file_header"] = file_header
        ret["nt_header"] = nt_header
        return ret

    def get_section_info(self):
        """Get pe section info."""
        sample_id = request.args.get("sample_id", None)
        if not sample_id:
            raise Exception("no sample id provided!")

        from models_pe import PeSection

        q_section = PeSection.objects(sample_id=sample_id)
        if q_section.count() == 0:
            raise Exception("0 section found for sample_id %s" % sample_id)

        ret = []
        for section in q_section:
            ret.append(pe_value_list_to_dict(section))

        return ret

    def get_import_info(self):
        """Get pe import info."""
        sample_id = request.args.get("sample_id", None)
        if not sample_id:
            raise Exception("no sample id provided!")

        from models_pe import PeImportDllTable

        q_import_dll = PeImportDllTable.objects(sample_id=sample_id)
        if q_import_dll.count() == 0:
            raise Exception("0 import dll table found for sample_id %s" % sample_id)

        ret = []
        for import_dll in q_import_dll:

            import_dll_ui = {"dll_name": import_dll.dll_name}
            import_dll_ui["value_dict"] = pe_value_list_to_dict(import_dll)
            import_dll_ui["item_list"] = []
            for item in import_dll.import_item_list:
                import_dll_ui["item_list"].append(item.json_ui())

            ret.append(import_dll_ui)

        return ret

    def get_export_info(self):
        """Get pe export info."""
        return "success"

    def get_behv_file_info(self):
        """Get pe behv file info."""
        return "success"

    # -------------------------------------------------------------------------
    # Post

    def post(self):
        """Wrapper for self._post()."""
        print("-" * 30 + "PE Action Set Start" + "-" * 30)
        ret = self._post()
        pprint(ret)
        print("+" * 30 + "PE Action Set End" + "+" * 30)
        return ret

    def _post(self):
        try:
            args = json.loads(to_str(request.data))
            if "action" not in args:
                raise Exception("no action!")

            action = args["action"]
            if action == "":
                pass

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception:\n" + str(e)


class SampleSimpleAction(Resource):
    """Some get handler for Sample."""

    def get(self):
        """Wrapper of self._get()."""
        try:
            return self._get()
        except Exception as e:
            print("异常: SampleSimpleAction: %s" % e)

    def _get(self):
        action = request.args.get("action", None)
        if not action:
            return "无效的行为类型"

        if action == "count":
            return self._count()

        elif action == "check_exists":
            return self._check_exists()

        elif action == "list":
            return self._list()

        else:
            return "不支持的操作类型"

    def _count(self):
        """Get count of all Samples."""
        type_ = request.args.get("type", "all")
        author = request.args.get("author", "all")

        print("get sample count: type: %s, author: %s" % (type_, author))

        return Sample.objects.count()

    def _list(self):
        """Get list of refGroup, sorted by update_time."""
        # type_ = request.args.get("type", "all")
        # author = request.args.get("author", "all")

        ret = []
        for group in RefGroup.objects():
            ret.append(group.json_ui())
        return ret

    def _check_exists(self):
        # 检查是否存在
        sha256 = request.args.get("sha256", None)
        if not sha256:
            return "Invalid SHA256"

        return Sample.objects(sha256=sha256).count() != 0


class SampleUpload(Resource):
    """Post handler for Sample Upload."""

    def post(self):
        """Wrapper for self._post()."""
        print("-" * 30 + "Sample Upload Start" + "-" * 30)
        ret = self._post()
        pprint(ret)
        print("+" * 30 + "Sample Upload End" + "+" * 30)
        return ret

    def _post(self):
        try:
            file = request.files['file']
            if not file:
                raise Exception("no file uploaded!")

            type_ = request.args.get("type", None)
            if not type_:
                raise Exception("no upload type provided!")

            if type_ == "sample_group":
                return self.upload_by_group(file)

            elif type_ == "sample_standalone":
                return self.upload_standalone_sample(file)

            elif type_ == "sample_parent":
                return self.upload_by_parent(file)

            else:
                raise Exception("invalid upload type: %s" % type_)
            """
            import pprint
            # pprint.pprint(dir(request))
            # print(request.headers)
            print(request.files)
            print(request.form)
            print(request.args)
            file = request.files['file']
            if file:
                # pprint.pprint(dir(file))
                # print(type(file))         -> werkzeug.datastructures.FileStorage
                # print(file.name)          # -> 'file'
                # print(file.filename)      # -> '生成器.exe'
                # print(type(file.stream))  -> `tempfile.SpooledTemporaryFile`
                # print(file.stream.read()) -> 实际的数据
                # file.save('f.tmp')        -> 保存到本地磁盘
                # binary = file.stream.read()
                # sample = sample_check_exist_or_insert(binary)
                return "save success"
            else:
                return "invalid file"
            """
        except:
            error(traceback.format_exc())
            return "exception!"

    def upload_by_group(self, file_):
        """Upload a group of files."""
        group_id = request.args.get("group_id", None)
        relative_path = request.args.get("relative_path", None)
        if not group_id or not relative_path:
            raise Exception("invalid args!")

        # check if group_id already exists
        q_ref_group = RefGroup.objects(group_id=group_id)
        if q_ref_group.count() > 1:
            raise Exception("group with same group_id more than 1, error!")

        # get refGroup and refDir
        if q_ref_group.count() == 0:
            # no group, create one group and relative dir
            tar_ref_group = RefGroup()
            tar_ref_group.group_id = group_id
            tar_ref_group.save()
            debug("create tar_ref_group with group_id: %s" % group_id)
            dir_str_list = path_to_dirs(relative_path)
            tar_ref_dir = None
            for index, dir_str in enumerate(dir_str_list):
                dir_tmp = RefDir()
                dir_tmp.dir_name = dir_str
                dir_tmp.refGroup = tar_ref_group
                if index != 0:
                    assert tar_ref_dir
                    dir_tmp.parnetRefDir = tar_ref_dir
                dir_tmp.save()
                tar_ref_dir = dir_tmp
                debug("(1st)create dir with name: %s" % dir_str)
        else:
            # already has group, get target dir
            tar_ref_group = q_ref_group[0]
            dir_tmp = None
            dir_str_list = path_to_dirs(relative_path)
            tar_ref_dir = None
            for index, dir_str in enumerate(dir_str_list):
                if index == 0:
                    q = RefDir.objects(refGroup=tar_ref_group, parnetRefDir=None)
                    if q.count() != 1:
                        raise Exception("get top dir of file fail!")
                    dir_tmp = q[0]
                    tar_ref_dir = dir_tmp
                else:
                    q = RefDir.objects(refGroup=tar_ref_group, parnetRefDir=dir_tmp, dir_name=dir_str)
                    if q.count() > 1:
                        raise Exception("get dir of file fail!")
                    if q.count() == 1:
                        dir_tmp = q[0]
                        tar_ref_dir = dir_tmp
                        continue
                    else:
                        # now we need to create dir
                        dir_tmp = RefDir()
                        dir_tmp.dir_name = dir_str
                        dir_tmp.refGroup = tar_ref_group
                        dir_tmp.parnetRefDir = tar_ref_dir
                        dir_tmp.save()
                        tar_ref_dir = dir_tmp
                        debug("create dir with name: %s" % dir_str)

        assert tar_ref_group and tar_ref_dir

        # check if file with same sha256 exists

        _binary = file_.stream.read()

        if len(_binary) == 0:
            # empty file
            # may store as EMPTY ref file if not already exists
            q_ref_file = RefFile.objects(file_size=0)
            if q_ref_file.count() > 1:
                raise Exception("ref file with 0 size exists more than 1, error!: %s" % (relative_path))
            if q_ref_file.count() == 1:
                ref_file = q_ref_file[0]
            else:
                ref_file = RefFile()
                ref_file.save()
            # add link
            link = RefFileBelongTo()
            link.refGroup = tar_ref_group
            link.refDir = tar_ref_dir
            link.ref_file_id = str(ref_file.pk)
            link.file_name = file_.filename
            link.file_relative_path = relative_path
            link.save()
            debug("save empty file as refFile")
            return "upload success"

        import hashlib
        sha256 = hashlib.sha256(_binary).hexdigest()
        q_sample = Sample.objects(sha256=sha256)
        if q_sample.count() > 1:
            raise Exception("sample with same sha256 exists and more than 1: %s - %d" % (sha256, q.count()))

        if q_sample.count() == 1:
            if RefFile.objects(sha256=sha256).count() != 0:
                raise Exception("file exists both as sample and ref file. error!: %s" % sha256)

            # file only exists as sample -> update database
            sample = q_sample[0]
            sample_belongto = SampleBelongTo()
            sample_belongto.refGroup = tar_ref_group
            sample_belongto.refDir = tar_ref_dir
            sample_belongto.sample_id = str(sample.pk)
            sample_belongto.sample_name = file_.filename
            sample_belongto.sample_relative_path = relative_path
            sample_belongto.save()
            print("sample already exists, save sample_belongto")
            return "upload success"

        else:
            q_ref_file = RefFile.objects(sha256=sha256)
            if q_ref_file.count() > 1:
                raise Exception("ref file with same sha256 exists and more than 1: %s - %d" % (sha256, q.count()))

            if q_ref_file.count() == 1:

                # file exists as ref file -> update database
                ref_file = q_ref_file[0]
                debug("refFile already exists")

            else:
                # file not exists in database -> store in database (as ref file) and update something
                ref_file = RefFile()
                ref_file._binary = _binary
                ref_file.save()
                debug("save file as ref file")

            ref_file_belongto = RefFileBelongTo()
            ref_file_belongto.refGroup = tar_ref_group
            ref_file_belongto.refDir = tar_ref_dir
            ref_file_belongto.ref_file_id = str(ref_file.pk)
            ref_file_belongto.file_name = file_.filename
            ref_file_belongto.file_relative_path = relative_path
            ref_file_belongto.save()
            debug("save ref_file_belongto")

            return "upload success"

    def upload_standalone_sample(self, file):
        """Upload standalone sample as one group."""
        pass

    def upload_by_parent(self, file):
        """Upload some files as child of some Stuff."""
        pass


class RefFileAction(Resource):
    """RefFile post handler."""

    def post(self):
        """Wrapper of self._post()."""
        print("-" * 30 + "RefFile Action Start" + "-" * 30)
        ret = self._post()
        pprint(ret)
        print("+" * 30 + "RefFile Action End" + "+" * 30)
        return ret

    def _post(self):
        try:
            args = json.loads(to_str(request.data))
            if "action" not in args:
                raise Exception("no action!")

            action = args["action"]
            if action == "analyzeAsSample":
                return self.analyze_as_sample(args)

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception:\n" + str(e)

    def analyze_as_sample(self, args):
        """Analyze refFile as Sample."""
        if "refFileId" not in args:
            raise Exception("no ref file id provided!")

        return tasks_wrapper.analyze_ref_file_as_sample(args["refFileId"])


# -------------------------------------------------------------------------


class TaskAction(Resource):
    """Some actions for group/sample/file."""

    def get(self):
        """Wrapper for self._get()."""
        print("-" * 30 + "Task Action Get Start" + "-" * 30)
        ret = self._get()
        pprint(ret)
        print("+" * 30 + "Task Action Get End" + "+" * 30)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                raise Exception("no action provided!")

            if action == "get_TaskList":
                return self.get_task_list()

            else:
                raise Exception("invalid action: %s" % action)

        except:
            error(traceback.format_exc())
            return "exception!"

    def get_task_list(self):
        """Get all tasks."""
        ret = {}

        ret["active"] = tasks.get_active_task_list()
        ret["history"] = tasks_wrapper.get_task_history()
        ret["reversed"] = tasks.get_reserved_task_list()
        ret["scheduled"] = tasks.get_scheduled_task_list()

        return ret

    def post(self):
        """Wrapper of self._post()."""
        print("-" * 30 + "Task Action Set Start" + "-" * 30)
        ret = self._post()
        pprint(ret)
        print("+" * 30 + "Task Action Set End" + "+" * 30)
        return ret

    def _post(self):
        try:
            args = json.loads(to_str(request.data))
            if "action" not in args:
                raise Exception("no action!")

            action = args["action"]
            if action == "cancelTask":
                return self.cancel_task(args)

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception:\n" + str(e)

    def cancel_task(self, args):
        """Cancel task."""
        if "taskId" not in args:
            raise Exception("no task id provided!")

        return tasks_wrapper.cancel_celery_task(args["taskId"])


# -------------------------------------------------------------------------

api.add_resource(TestAction, '/test/')

api.add_resource(LogLineAction, '/logline/')

api.add_resource(Action, '/action/')
api.add_resource(SetAction, '/')

api.add_resource(TreeAction, '/tree/')

api.add_resource(RefFileAction, '/reffile/')
api.add_resource(PeAction, '/pe/')

api.add_resource(SampleSimpleAction, '/sample/action/')
api.add_resource(SampleUpload, '/sample/upload/')

api.add_resource(TaskAction, '/task/')

# -------------------------------------------------------------------------

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='start server config')

    parser.add_argument('--notask', dest="is_no_task", action="store_true", help="is start server without any task stuff")

    args = parser.parse_args()

    if not args.is_no_task:

        tasks_wrapper.retrieve_tasks_from_celery()

        import threading
        t = threading.Thread(target=tasks_wrapper.check_close_task_history)
        t.start()

    app.run(debug=True)

    if not args.is_no_task:
        t.join()

# -------------------------------------------------------------------------
