Using Git on my iPad
====================

By Matthias Mittelstein
Hauptstraße 23
23816 Neversdorf
Germany
Matthias@Mittelstein.name 

Written May 2024.

My Environment
==============

I am using Pythonista on iPad since some years to have a programming playground when sitting on a sofa.
And I have an iPhone. I don't use that for development but only to execute Python programs.

I am switching between two homes. At one place I have an 10 year old Mac, on the other place I have an old PC with Windows-10 (and Linux). I have a portable hard disk which I use as main storage at both computers.

Python sources I moved one by one with copy&paste | mail | copy&paste.

Choosing Tool
=============

I was building a tool to save my growing number of Python programs. The idea was someting like tar|mail.
Then I learnt about Git and GitHub and follwed the idea to use a common tool instead of building my own.

Searching the Internet I read that it is simple to get Git and GitHub on Linux and even on Windows-10.
I had to learn that GitHub cannot understand that a direcory can be connected to two computers. So I have now two directory tree on my portable disk: python_on_macos and python_on_win10.

But it is not that simple on iPadOS. There seem to be several approaches. I decided to go with 'git' on 'StaSh'.

I already has StaSh installed on my iPad some years ago but used only one as an installation tool.

StaSh
=====

With the current versions of iPadOS and Pythonista StaSh was not working any longer.
In internet I read that others had those problems too and offered some suggestions.

Issuse #491, #484, ...

With two or three corrections StaSh came alive and was able to execute
'autoupdate'.
During some short tests I recognized, that 'printhex' was working only after
'autoupdate dev'.
I decided to go on with the 'dev'-branch.

It is hard to use StaSh because some kind of autocorrection is very often modifying my commands while I am typing. I thing is has been reported as #506, #497 already.

A couple of commands seem to work properly, but 'git' did not. 'git' loaded and installed some additional software but after it still did not work.

For 'git' on 'StaSh' I did not find a solution in internet, so I started debugging. Somehow I could not draw help from issues #397 nor #357.

StaSh and git clone (unfinished)
================================

I copied two small projects to desk computers and used Git and GitHub there to create repositories there.
Then I tried to 'git clone' that onto my iPad.
After some corrections done I stopped that approach. I had the feeling that it is two complicate to debug the HTTP procedures for remote access and the local problems to handle Git at the same time.

StaSh and some local git Commands (ongoing)
===========================================

I created an empty directory and started to debug some less complicated commands:
* git init
* git add
* git commit
* git status
* git diff

After several program modifications four commands seem to work reasonably with a small example.
'git diff' gives me some head aches still.

Problems I saw
--------------
I think that the python sources I am working on are still asking for Python 2 partly. I am not sure whether Python 2 is still working on my iPad, but I decided, that I will not try that.

With my own programs I had no serious problems to switch from Python 2 to Python 3. So I did not learn anything about the problems you have to handle. As I don't have that knowledge I will not try to make the software compatible for both language releases. Programs I modify will be designed and tested for Python 3.10 only.

### Modifcations on some details ###

In some cases the language had small incompatible changes, which need software modification.

### Renamed Packages ###

In some cases packages had been renamed and I had to adjust import statements.

### Separation of Bytes Sequences and Text Strings ###

I looks to me that in Python 2 byte sequences and character sequences had been quite compatible. But in Python 3 they are different things.

I know about the difference because I was working as a C-programmer on that specific subject od some decades in my former live.

But here I had to recognize
* that the software I am looking at is often assuming that bytes and strings are compatible
* and I often cannot find a concept or design specification which explains whether a package wants (or should) work on bytes or on strings.

I am looking at sources and at test data and see bytes in some cases and strings in other cases. Because of that I am inserting a lot of calls to encode() and decode() without knowing whether a propper solution should go the other way round.

Modifcations to stash/bin
=========================

stash/bin/git
-------------

Near line 190 in find_repo() :

        # MatthiasMitt versuche...
        #old: subdirs = os.walk(path).next()[1]
        unused_dirpath, subdirs ,unused_filenames = next(os.walk(path))
        #print('deb:','path:',path)
        #print('deb:','os.walk(path)',os.walk(path))
        #ddd = os.walk(path)
        #for xxx in ddd:
        #    print('each:',xxx)
        #i = 5/0
        #unused_dirpath, subdirs ,unused_filenames = os.walk(path)

Near line 480 a temporary modification, because I want a trace-back during debugging and not a userfriendy error message.

    if True: #debug: kein try, um Traceback zu erhalten...   try:

        author = "{0} <{1}>".format(ns.name, ns.email)

        print(
            repo.repo.do_commit(
                message=ns.message,
                author=author,
                committer=author,
                merge_heads=[merge_head] if merge_head else None
            )
        )
        if merging:
            try:
                os.remove(os.path.join(repo.repo.controldir(), 'MERGE_HEAD'))
                os.remove(os.path.join(repo.repo.controldir(), 'MERGE_MSG'))
            except OSError:
                pass  #todo, just no such file
    else: # debug   ...  except:
        print('commit Error: {0}'.format(sys.exc_info()[1]))


Modifcations to stash/lib/gittle
================================

stash/lib/gittle/gittle.py
--------------------------

Near line 80:

    MODE_DIRECTORY = 0o040000  # Used to tell if a tree entry is a directory
    # MatthiasMitt:  0o  Prefix is requested now.

Near line 110 in __init__() :

        #MatthiasMitt: old: elif isinstance(repo_or_path, basestring):
        elif isinstance(repo_or_path, str):
            path = os.path.abspath(repo_or_path)
            self.repo = DulwichRepo(path)

Near line 360 in fetch_remote() :

        #MatthasMitt
        print('debug:','client._fetch_capabilities',':',client._fetch_capabilities)
        #alt: client._fetch_capabilities.remove('thin-pack')
        client._fetch_capabilities.remove(b'thin-pack')
        #.

Near line 760 in _to_commit() :

        #MatthiasMitt    basestring is gone.
        # I don't know the specifications.
        # But I switched to  str  in  __init__  too.
        #
        #old: if isinstance(commit_obj, basestring):
        #old:     return self.repo[commit_obj]
        if isinstance(commit_obj, str):
            return self.repo[commit_obj]
        return commit_obj

Near line 780 in _commit_sha() :

        #MatthiasMitt    basestring is gone.
        # I don't know the specifications.
        # But I switched to  str  in  __init__  too.
        #
        #old: elif isinstance(commit_obj, basestring):
        elif isinstance(commit_obj, str):
            # Can't use self[commit_obj] to avoid infinite recursion
            #MatthiasMitt  but dulwich  is working with bytes.
            #old: commit_obj = self.repo[commit_obj]
            commit_obj_name = commit_obj.encode('utf-8')
            commit_obj = self.repo[commit_obj_name]
            #.
        return commit_obj.id

Near line 830 in _parse_reference() :

        #MatthiasMitt
        print('debug(.../gittle/_parse_reference)','ref_string:',ref_string)
        print('debug(.../gittle/_parse_reference)','type(..)  :',type(ref_string))
        # if  ref_string  is  bytes , then convert
        #
        #old: if '~' in ref_string:
        #old:     ref, count = ref_string.split('~')
        #old:     count = int(count)
        #old:     commit_sha = self._commit_sha(ref)
        #old:     return self.get_previous_commit(commit_sha, count)
        #old: return self._commit_sha(ref_string)
        if type(ref_string) == bytes:
            ref_string_s = ref_string.decode('ascii')
        else:
            ref_string_s = ref_string
        if '~' in ref_string_s:
            ref, count = ref_string_s.split('~')
            count = int(count)
            commit_sha = self._commit_sha(ref)
            return self.get_previous_commit(commit_sha, count)
        return self._commit_sha(ref_string_s)



Modifcations to stash/lib/gittle/utils
======================================

stash/lib/gittle/utils/git.py
-----------------------------

Near line 3:

     # MatthiasMitt nach fremden Vorschlägen:
     try:
         from StringIO import StringIO ## for Python 2
     except ImportError:
         from io import StringIO ## for Python 3

Near line 210 in is_sha() :

     MatthiasMitt   basestring   is gone.
     # I did not find a good definion about sha1-hashes used by git.
     # I think it is either 20 arbitray bytes or a bytes-object with
     #         40 hexadecimal digits.
     # Do I have to expect string-objects with hexadecimal digits here?
     #
     #old: return isinstance(sha, basestring) and len(sha) == 40
     if isinstance(sha, bytes) and len(sha) == 40:
        return True
     elif isinstance(sha, str) and len(sha) == 40:
        print('debug(gittle/utils/git/is_sha)','I allowed type str!?')
        return True
     else:
        return False


Modifcations to stash/lib/dulwich
=================================

stash/lib/dulwich/config.py
---------------------------

Near line 30:

    #MatthiasMitt
    #old
    #from collections import (
    #    OrderedDict,
    #    MutableMapping,
    #    )
    from collections     import OrderedDict
    from collections.abc import MutableMapping

Near line 350 in write_to_file() :

            #MatthiasMitt
            print('debug(config:360)','section,values',section,values)
            print('debug(config)    ','type(...)     ',type(section),type(values))
            try:
                section_name, subsection_name = section
            except ValueError:
                (section_name, ) = section
                subsection_name = None
            print('debug(config)    ','type(section_name)/(subsection_name)',type(section_name),type(subsection_name))
            #MatthiasMitt
            #old: if subsection_name is None:
            #old:     f.write(b"[" + section_name + b"]\n")
            #old: else:
            #old:     f.write(b"[" + section_name + b" \"" + subsection_name + b"\"]\n")
            if subsection_name is None:
                if type(section_name) == str:
                    section_name_b = section_name.encode('utf-8')      #  'ascii'? Handle or disallow?
                else:
                    section_name_b = section_name
                f.write(b"[" + section_name_b + b"]\n")
            else:
                if type(section_name) == str:
                    section_name_b = section_name.encode('utf-8')      #  'ascii'? Handle or disallow?
                else:
                    section_name_b = section_name
                if type(subsection_name) == str:
                    subsection_name_b = subsection_name.encode('utf-8')      #  'ascii'? Handle or disallow?
                else:
                    subsection_name_b = subsection_name
                f.write(b"[" + section_name_b + b" \"" + subsection_name_b + b"\"]\n")
            for key, value in values.items():
                if value is True:
                    value = b"true"
                elif value is False:
                    value = b"false"
                else:
                    value = _escape_value(value)
                if type(key) == str:
                    key_b = key.encode('utf-8')      #  'ascii'? Handle or disallow?
                else:
                    key_b = key
                f.write(b"\t" + key_b + b" = " + value + b"\n")


stash/lib/dulwich/hooks.py
--------------------------

iPadOS does not allow subprocess. But that is no real problem as long as there are no hooks requested. If was only a poor idea to use a side-effect of 'subprocess.call(...)' to test, whether a hook is requested.

Near line 80 in execute():

    def execute(self, *args):
        """Execute the hook with given args"""
        
        print('debug(dulwich.hooks.execute)','args', args)

        if len(args) != self.numparam:
            raise HookError("Hook %s executed with wrong number of args. \
                            Expected %d. Saw %d. args: %s"
                            % (self.name, self.numparam, len(args), args))

        if (self.pre_exec_callback is not None):
            print('debug(dulwich.hooks.execute)','pre_exec_callback', self.pre_exec_callback)
            args = self.pre_exec_callback(*args)

        #old: try:
        
        #MatthiasMitt
        print('debug(dulwich.hooks.execute)','call(', [self.filepath] + list(args) ,')')
        if os.path.isfile(self.filepath):
            
            try:
            
                ret = subprocess.call([self.filepath] + list(args))
                if ret != 0:
                    if (self.post_exec_callback is not None):
                        self.post_exec_callback(0, *args)
                    raise HookError("Hook %s exited with non-zero status"
                                    % (self.name))
                if (self.post_exec_callback is not None):
                    return self.post_exec_callback(1, *args)
            except OSError:  # no file. silent failure.
                if (self.post_exec_callback is not None):
                    self.post_exec_callback(0, *args)
        #MatthiasMitt
        else:  # no file. silent failure.
            print('debug(dulwich.hooks.execute)','not isfile():', self.filepath )
            if (self.post_exec_callback is not None):
                self.post_exec_callback(0, *args)




stash/lib/dulwich/objects.py
----------------------------

Near line 190:

def git_line(*items):
     """Formats items into a space sepreated line."""
     #MatthiasMitt
     #old: return b' '.join(items) + b'\n'
     #
     items_b = []
     bad_ix  = -1
     ix      = 0
     for item in items:
        if type(item) == str:
            item_b = item.encode('utf-8')      #  'ascii'? Handle or disallow?
            print('debug(dulwich.objects.git_line)','has type str:',item)
            bad_ix = ix
        else:
            item_b = item
        items_b.append(item_b)
        ix += 1
     if bad_ix >= 0:
        print('debug(dulwich.objects.git_line)','bad index:',bad_ix)
        print('debug(dulwich.objects.git_line)',items)
     return b' '.join(items_b) + b'\n'
     #.

Near line 260 in as_legacy_object_chunks():

        for chunk in self.as_raw_chunks():
            #MatthiasMatt
            #old: yield compobj.compress(chunk)
            if type(chunk) == str:
                chunk_b = chunk.encode('utf-8')      #  'ascii'? Handle or disallow?
                print('debug(dulwich.objects.as_legacy_object_chunks)','type(',chunk,') is chr')
                print('debug','self.as_raw_chunks():',self.as_raw_chunks())
            else:
                chunk_b = chunk
            yield compobj.compress(chunk_b)
            #.
        yield compobj.flush()

Near 290 in sha():

            for chunk in self.as_raw_chunks():
                #MatthiasMatt
                #old: new_sha.update(chunk)
                if type(chunk) == str:
                    chunk_b = chunk.encode('utf-8')      #  'ascii'? Handle or disallow?
                    print('debug(dulwich.objects.sha)','type(',chunk,') is chr')
                    print('debug','self.as_raw_chunks():',self.as_raw_chunks())
                else:
                    chunk_b = chunk
                new_sha.update(chunk_b)
                #.
            self._sha = new_sha
        return self._sha
       

Near line 925 in _init_maybe_bare() :

    def _init_maybe_bare(cls, path, bare):
        for d in BASE_DIRECTORIES:
            #MatthiasMitt
            #old: os.mkdir(os.path.join(path, *d))
            dirname = os.path.join(path, *d)
            try:
                st = os.stat(dirname)
                print('Cannot make directory',dirname)
                print('       Already exists with st_type {0:X)'.format(st.st_type))
                pass
            except FileNotFoundError:
                os.mkdir(dirname)
            #.
        DiskObjectStore.init(os.path.join(path, OBJECTDIR))

Near line 950 in init() :

        if mkdir:
            os.mkdir(path)
        controldir = os.path.join(path, CONTROLDIR)
        #MatthiasMitt
        #old: os.mkdir(controldir)
        try:
            st = os.stat(controldir)
            print('Cannot make directory',controldir)
            print('       Already exists with st_type {0:X)'.format(st.st_type))
            pass
        except FileNotFoundError:
            os.mkdir(controldir)
        #.
        cls._init_maybe_bare(controldir, False)
        return cls(path)

Near line 520 in do_commit() no correction, only tracing:

        import time
        print('debug(repo.do_commit:547)')
        c = Commit()
        if tree is None:
            index = self.open_index()
            c.tree = index.commit(self.object_store)
        else:
            if len(tree) != 40:
                raise ValueError("tree must be a 40-byte hex sha string")
            c.tree = tree

        print('debug(repo.do_commit:556)')
        
        try:
            self.hooks['pre-commit'].execute()
        except HookError as e:
            raise CommitError(e)
        except KeyError:  # no hook defined, silent fallthrough
            pass

        if merge_heads is None:
            # FIXME: Read merge heads from .git/MERGE_HEADS
            merge_heads = []
        print('debug(repo.do_commit:567)')
        if committer is None:
            # FIXME: Support GIT_COMMITTER_NAME/GIT_COMMITTER_EMAIL environment
            # variables
            committer = self._get_user_identity()
        c.committer = committer
        if commit_timestamp is None:
            # FIXME: Support GIT_COMMITTER_DATE environment variable
            commit_timestamp = time.time()
        c.commit_time = int(commit_timestamp)
        if commit_timezone is None:
            # FIXME: Use current user timezone rather than UTC
            commit_timezone = 0
        c.commit_timezone = commit_timezone
        if author is None:
            # FIXME: Support GIT_AUTHOR_NAME/GIT_AUTHOR_EMAIL environment
            # variables
            author = committer
        c.author = author
        if author_timestamp is None:
            # FIXME: Support GIT_AUTHOR_DATE environment variable
            author_timestamp = commit_timestamp
        c.author_time = int(author_timestamp)
        if author_timezone is None:
            author_timezone = commit_timezone
        c.author_timezone = author_timezone
        if encoding is not None:
            c.encoding = encoding
        if message is None:
            # FIXME: Try to read commit message from .git/MERGE_MSG
            raise ValueError("No commit message specified")
        print('debug(repo.do_commit:597)')
        try:
            h = self.hooks['commit-msg']
            print('debug(repo.do_commit:598)','hook',h)
        except KeyError:  # no hook defined
            print('debug(repo.do_commit:598)',"kein  self.hooks['commit-msg']")

        try:
            print('debug(repo.do_commit:600)','  message',  message)
            print('debug(repo.do_commit:600)','type(message)',type(message))
            c.message = self.hooks['commit-msg'].execute(message)
            print('debug(repo.do_commit:601)','c.message',c.message)
            if c.message is None:
                c.message = message
        except HookError as e:
            raise CommitError(e)
        except KeyError:  # no hook defined, message not modified
            c.message = message

        print('debug(repo.do_commit:608)')
        if ref is None:
            # Create a dangling commit
            c.parents = merge_heads
            self.object_store.add_object(c)
        else:
            try:
                old_head = self.refs[ref]
                c.parents = [old_head] + merge_heads
                self.object_store.add_object(c)
                ok = self.refs.set_if_equals(ref, old_head, c.id)
            except KeyError:
                c.parents = merge_heads
                self.object_store.add_object(c)
                ok = self.refs.add_if_new(ref, c.id)
            if not ok:
                # Fail if the atomic compare-and-swap failed, leaving the commit and
                # all its objects as garbage.
                raise CommitError("%s changed during commit" % (ref,))

        print('debug(repo.do_commit:628)')
        try:
            self.hooks['post-commit'].execute()
        except HookError as e:  # silent failure
            warnings.warn("post-commit hook failed: %s" % e, UserWarning)
        except KeyError:  # no hook defined, silent fallthrough
            pass

        print('debug(repo.do_commit:634)','<--',c.id)
        return c.id


stash/lib/dulwich/refs.py
-------------------------

In refs.py currently tracing only.

Near line 200 in _follow() :

The method returns empty contents quite often aand that makes its callers fail.
But in the mean time I think, that is quite normal behavior.

        depth = 0
        print('debug(refs._follows())','type(self):',type(self))
        while contents.startswith(SYMREF):
            #MatthiasMitt
            print('debug(refs._follows())','    contents:',contents)
            refname = contents[len(SYMREF):]
            print('debug(refs._follows())','     refname:',refname)
            contents = self.read_ref(refname)
            print('debug(refs._follows())','new contents:',contents)
            if not contents:
                break
            depth += 1
            if depth > 5:
                raise KeyError(name)
        print('debug(refs._follows())','<-- (',refname,',',contents,')')
        return refname, contents

Near line 300 in __init__() :

        #MatthiasMitt
        print('debug(refs.DictRefsContainer','refs:',refs)

Near line 390 in __init__() :

        #MatthiasMitt
        print('debug(refs.DiskRefsContainer','path:',path)

Near line 510 in read_loose_ref() :

            #MatthiasMitt
            print('debug(refs.DiskRefsContainer.read_loose_ref','filename:',filename)
            with GitFile(filename, 'rb') as f:
                header = f.read(len(SYMREF))
                if header == SYMREF:
                    # Read only the first line
                    #MatthiasMitt
                    #old: return header + next(iter(f)).rstrip(b'\r\n')
                    res = header + next(iter(f)).rstrip(b'\r\n')
                    print('debug(refs.DiskRefsContainer.read_loose_ref','<--',res)
                    return res
                else:
                    # Read only the first 40 bytes
                    #MatthiasMitt
                    #old: return header + f.read(40 - len(SYMREF))
                    res = header + f.read(40 - len(SYMREF))
                    print('debug(refs.DiskRefsContainer.read_loose_ref','<--',res)
                    return res

stash/lib/dulwich/repo.py
-------------------------

Near line 447 in __getitem__:

        #MatthiasMitt   accept a  str  also
        if type(name) == str:
            name = name.encode('utf-8')
        if not isinstance(name, bytes):

Near line 550 in do_commit() lots of tracing:

        import time
        print('debug(repo.do_commit:547)')
        c = Commit()
        if tree is None:
            index = self.open_index()
            c.tree = index.commit(self.object_store)
        else:
            if len(tree) != 40:
                raise ValueError("tree must be a 40-byte hex sha string")
            c.tree = tree

        print('debug(repo.do_commit:556)')
        
        try:
            self.hooks['pre-commit'].execute()
        except HookError as e:
            raise CommitError(e)
        except KeyError:  # no hook defined, silent fallthrough
            pass

        if merge_heads is None:
            # FIXME: Read merge heads from .git/MERGE_HEADS
            merge_heads = []
        print('debug(repo.do_commit:567)')
        if committer is None:
            # FIXME: Support GIT_COMMITTER_NAME/GIT_COMMITTER_EMAIL environment
            # variables
            committer = self._get_user_identity()
        c.committer = committer
        if commit_timestamp is None:
            # FIXME: Support GIT_COMMITTER_DATE environment variable
            commit_timestamp = time.time()
        c.commit_time = int(commit_timestamp)
        if commit_timezone is None:
            # FIXME: Use current user timezone rather than UTC
            commit_timezone = 0
        c.commit_timezone = commit_timezone
        if author is None:
            # FIXME: Support GIT_AUTHOR_NAME/GIT_AUTHOR_EMAIL environment
            # variables
            author = committer
        c.author = author
        if author_timestamp is None:
            # FIXME: Support GIT_AUTHOR_DATE environment variable
            author_timestamp = commit_timestamp
        c.author_time = int(author_timestamp)
        if author_timezone is None:
            author_timezone = commit_timezone
        c.author_timezone = author_timezone
        if encoding is not None:
            c.encoding = encoding
        if message is None:
            # FIXME: Try to read commit message from .git/MERGE_MSG
            raise ValueError("No commit message specified")
        print('debug(repo.do_commit:597)')
        try:
            h = self.hooks['commit-msg']
            print('debug(repo.do_commit:598)','hook',h)
        except KeyError:  # no hook defined
            print('debug(repo.do_commit:598)',"kein  self.hooks['commit-msg']")

        try:
            print('debug(repo.do_commit:600)','  message',  message)
            print('debug(repo.do_commit:600)','type(message)',type(message))
            c.message = self.hooks['commit-msg'].execute(message)
            print('debug(repo.do_commit:601)','c.message',c.message)
            if c.message is None:
                c.message = message
        except HookError as e:
            raise CommitError(e)
        except KeyError:  # no hook defined, message not modified
            c.message = message

        print('debug(repo.do_commit:608)')
        if ref is None:
            # Create a dangling commit
            c.parents = merge_heads
            self.object_store.add_object(c)
        else:
            try:
                old_head = self.refs[ref]
                c.parents = [old_head] + merge_heads
                self.object_store.add_object(c)
                ok = self.refs.set_if_equals(ref, old_head, c.id)
            except KeyError:
                c.parents = merge_heads
                self.object_store.add_object(c)
                ok = self.refs.add_if_new(ref, c.id)
            if not ok:
                # Fail if the atomic compare-and-swap failed, leaving the commit and
                # all its objects as garbage.
                raise CommitError("%s changed during commit" % (ref,))

        print('debug(repo.do_commit:628)')
        try:
            self.hooks['post-commit'].execute()
        except HookError as e:  # silent failure
            warnings.warn("post-commit hook failed: %s" % e, UserWarning)
        except KeyError:  # no hook defined, silent fallthrough
            pass

        print('debug(repo.do_commit:634)','<--',c.id)
        return c.id


Near line 930 in _init_maybe_bare() :

            #MatthiasMitt
            #old: os.mkdir(os.path.join(path, *d))
            dirname = os.path.join(path, *d)
            try:
                st = os.stat(dirname)
                print('Cannot make directory',dirname)
                print('       Already exists with st_type {0:X)'.format(st.st_type))
                pass
            except FileNotFoundError:
                os.mkdir(dirname)
            #.

Near line 960 in init() :

        #MatthiasMitt
        #old: os.mkdir(controldir)
        try:
            st = os.stat(controldir)
            print('Cannot make directory',controldir)
            print('       Already exists with st_type {0:X)'.format(st.st_type))
            pass
        except FileNotFoundError:
            os.mkdir(controldir)
        #.



Status
======

Work is still ongoing.