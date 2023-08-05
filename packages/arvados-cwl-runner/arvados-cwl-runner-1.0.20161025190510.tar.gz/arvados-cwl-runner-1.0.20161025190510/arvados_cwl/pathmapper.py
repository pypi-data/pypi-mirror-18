import re
import logging
import uuid
import os

import arvados.commands.run
import arvados.collection

from cwltool.pathmapper import PathMapper, MapperEnt, abspath, adjustFileObjs, adjustDirObjs
from cwltool.workflow import WorkflowException

logger = logging.getLogger('arvados.cwl-runner')

class ArvPathMapper(PathMapper):
    """Convert container-local paths to and from Keep collection ids."""

    pdh_path = re.compile(r'^keep:[0-9a-f]{32}\+\d+/.+$')
    pdh_dirpath = re.compile(r'^keep:[0-9a-f]{32}\+\d+(/.+)?$')

    def __init__(self, arvrunner, referenced_files, input_basedir,
                 collection_pattern, file_pattern, name=None, **kwargs):
        self.arvrunner = arvrunner
        self.input_basedir = input_basedir
        self.collection_pattern = collection_pattern
        self.file_pattern = file_pattern
        self.name = name
        super(ArvPathMapper, self).__init__(referenced_files, input_basedir, None)

    def visit(self, srcobj, uploadfiles):
        src = srcobj["location"]
        if srcobj["class"] == "File":
            if "#" in src:
                src = src[:src.index("#")]
            if isinstance(src, basestring) and ArvPathMapper.pdh_path.match(src):
                self._pathmap[src] = MapperEnt(src, self.collection_pattern % src[5:], "File")
            if src not in self._pathmap:
                # Local FS ref, may need to be uploaded or may be on keep
                # mount.
                ab = abspath(src, self.input_basedir)
                st = arvados.commands.run.statfile("", ab, fnPattern="keep:%s/%s")
                if isinstance(st, arvados.commands.run.UploadFile):
                    uploadfiles.add((src, ab, st))
                elif isinstance(st, arvados.commands.run.ArvFile):
                    self._pathmap[src] = MapperEnt(st.fn, self.collection_pattern % st.fn[5:], "File")
                elif src.startswith("_:"):
                    if "contents" in srcobj:
                        pass
                    else:
                        raise WorkflowException("File literal '%s' is missing contents" % src)
                else:
                    raise WorkflowException("Input file path '%s' is invalid" % st)
            if "secondaryFiles" in srcobj:
                for l in srcobj["secondaryFiles"]:
                    self.visit(l, uploadfiles)
        elif srcobj["class"] == "Directory":
            if isinstance(src, basestring) and ArvPathMapper.pdh_dirpath.match(src):
                self._pathmap[src] = MapperEnt(src, self.collection_pattern % src[5:], "Directory")
            for l in srcobj.get("listing", []):
                self.visit(l, uploadfiles)

    def addentry(self, obj, c, path, subdirs):
        if obj["location"] in self._pathmap:
            src, srcpath = self.arvrunner.fs_access.get_collection(self._pathmap[obj["location"]].resolved)
            if srcpath == "":
                srcpath = "."
            c.copy(srcpath, path + "/" + obj["basename"], source_collection=src, overwrite=True)
            for l in obj.get("secondaryFiles", []):
                self.addentry(l, c, path, subdirs)
        elif obj["class"] == "Directory":
            for l in obj["listing"]:
                self.addentry(l, c, path + "/" + obj["basename"], subdirs)
            subdirs.append((obj["location"], path + "/" + obj["basename"]))
        elif obj["location"].startswith("_:") and "contents" in obj:
            with c.open(path + "/" + obj["basename"], "w") as f:
                f.write(obj["contents"].encode("utf-8"))
        else:
            raise WorkflowException("Don't know what to do with '%s'" % obj["location"])

    def setup(self, referenced_files, basedir):
        # type: (List[Any], unicode) -> None
        uploadfiles = set()

        for k,v in self.arvrunner.get_uploaded().iteritems():
            self._pathmap[k] = MapperEnt(v.resolved, self.collection_pattern % v.resolved[5:], "File")

        for srcobj in referenced_files:
            self.visit(srcobj, uploadfiles)

        if uploadfiles:
            arvados.commands.run.uploadfiles([u[2] for u in uploadfiles],
                                             self.arvrunner.api,
                                             dry_run=False,
                                             num_retries=self.arvrunner.num_retries,
                                             fnPattern="keep:%s/%s",
                                             name=self.name,
                                             project=self.arvrunner.project_uuid)

        for src, ab, st in uploadfiles:
            self._pathmap[src] = MapperEnt(st.fn, self.collection_pattern % st.fn[5:], "File")
            self.arvrunner.add_uploaded(src, self._pathmap[src])

        for srcobj in referenced_files:
            if srcobj["class"] == "Directory":
                if srcobj["location"] not in self._pathmap:
                    c = arvados.collection.Collection(api_client=self.arvrunner.api,
                                                      keep_client=self.arvrunner.keep_client,
                                                      num_retries=self.arvrunner.num_retries)
                    subdirs = []
                    for l in srcobj["listing"]:
                        self.addentry(l, c, ".", subdirs)

                    check = self.arvrunner.api.collections().list(filters=[["portable_data_hash", "=", c.portable_data_hash()]], limit=1).execute(num_retries=self.arvrunner.num_retries)
                    if not check["items"]:
                        c.save_new(owner_uuid=self.arvrunner.project_uuid)

                    ab = self.collection_pattern % c.portable_data_hash()
                    self._pathmap[srcobj["location"]] = MapperEnt(ab, ab, "Directory")
                    for loc, sub in subdirs:
                        ab = self.file_pattern % (c.portable_data_hash(), sub[2:])
                        self._pathmap[loc] = MapperEnt(ab, ab, "Directory")
            elif srcobj["class"] == "File" and (srcobj.get("secondaryFiles") or
                (srcobj["location"].startswith("_:") and "contents" in srcobj)):

                c = arvados.collection.Collection(api_client=self.arvrunner.api,
                                                  keep_client=self.arvrunner.keep_client,
                                                  num_retries=self.arvrunner.num_retries                                                  )
                subdirs = []
                self.addentry(srcobj, c, ".", subdirs)

                check = self.arvrunner.api.collections().list(filters=[["portable_data_hash", "=", c.portable_data_hash()]], limit=1).execute(num_retries=self.arvrunner.num_retries)
                if not check["items"]:
                    c.save_new(owner_uuid=self.arvrunner.project_uuid)

                ab = self.file_pattern % (c.portable_data_hash(), srcobj["basename"])
                self._pathmap[srcobj["location"]] = MapperEnt(ab, ab, "File")
                if srcobj.get("secondaryFiles"):
                    ab = self.collection_pattern % c.portable_data_hash()
                    self._pathmap["_:" + unicode(uuid.uuid4())] = MapperEnt(ab, ab, "Directory")
                for loc, sub in subdirs:
                    ab = self.file_pattern % (c.portable_data_hash(), sub[2:])
                    self._pathmap[loc] = MapperEnt(ab, ab, "Directory")

        self.keepdir = None

    def reversemap(self, target):
        if target.startswith("keep:"):
            return (target, target)
        elif self.keepdir and target.startswith(self.keepdir):
            return (target, "keep:" + target[len(self.keepdir)+1:])
        else:
            return super(ArvPathMapper, self).reversemap(target)

class InitialWorkDirPathMapper(PathMapper):

    def visit(self, obj, stagedir, basedir, copy=False):
        # type: (Dict[unicode, Any], unicode, unicode, bool) -> None
        loc = obj["location"]
        if obj["class"] == "Directory":
            self._pathmap[loc] = MapperEnt(obj["location"], stagedir, "Directory")
            self.visitlisting(obj.get("listing", []), stagedir, basedir)
        elif obj["class"] == "File":
            if loc in self._pathmap:
                return
            tgt = os.path.join(stagedir, obj["basename"])
            if "contents" in obj and obj["location"].startswith("_:"):
                self._pathmap[loc] = MapperEnt(obj["contents"], tgt, "CreateFile")
            else:
                if copy:
                    self._pathmap[loc] = MapperEnt(obj["path"], tgt, "WritableFile")
                else:
                    self._pathmap[loc] = MapperEnt(obj["path"], tgt, "File")
                self.visitlisting(obj.get("secondaryFiles", []), stagedir, basedir)

    def setup(self, referenced_files, basedir):
        # type: (List[Any], unicode) -> None

        # Go through each file and set the target to its own directory along
        # with any secondary files.
        self.visitlisting(referenced_files, self.stagedir, basedir)

        for path, (ab, tgt, type) in self._pathmap.items():
            if type in ("File", "Directory") and ab.startswith("keep:"):
                self._pathmap[path] = MapperEnt("$(task.keep)/%s" % ab[5:], tgt, type)


class FinalOutputPathMapper(PathMapper):
    def visit(self, obj, stagedir, basedir, copy=False):
        # type: (Dict[unicode, Any], unicode, unicode, bool) -> None
        loc = obj["location"]
        if obj["class"] == "Directory":
            self._pathmap[loc] = MapperEnt(loc, stagedir, "Directory")
        elif obj["class"] == "File":
            if loc in self._pathmap:
                return
            tgt = os.path.join(stagedir, obj["basename"])
            self._pathmap[loc] = MapperEnt(loc, tgt, "File")
            self.visitlisting(obj.get("secondaryFiles", []), stagedir, basedir)

    def setup(self, referenced_files, basedir):
        # type: (List[Any], unicode) -> None
        self.visitlisting(referenced_files, self.stagedir, basedir)
