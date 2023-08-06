# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers for interacting with ``git``."""

import os

from ci_diff_helper import _utils


def git_root():
    """Return the root directory of the current ``git`` checkout.

    Returns:
        str: Filesystem path to ``git`` checkout root.
    """
    return _utils.check_output('git', 'rev-parse', '--show-toplevel')


def get_checked_in_files():
    """Gets a list of files in the current ``git`` repository.

    Effectively runs:

    .. code-block:: bash

      $ git ls-files ${GIT_ROOT}

    and then finds the absolute path for each file returned.

    Returns:
        list: List of all filenames checked into.
    """
    root_dir = git_root()
    cmd_output = _utils.check_output('git', 'ls-files', root_dir)

    result = []
    for filename in cmd_output.split('\n'):
        result.append(os.path.abspath(filename))

    return result


def merge_commit(revision='HEAD'):
    """Checks if a ``git`` revision is a merge commit.

    Args:
        revision (Optional[str]):  A ``git`` revision, any of a branch
            name, tag, a commit SHA or a special reference.

    Returns:
        bool: Flag indicating if the given revision.

    Raises:
        NotImplementedError: if the number of parents is not 1 or 2.
    """
    parents = _utils.check_output(
        'git', 'log', '--pretty=%P', '-1', revision)
    num_parents = len(parents.split())
    if num_parents == 1:
        return False
    elif num_parents == 2:
        return True
    else:
        raise NotImplementedError(
            'Unexpected number of parent commits', parents)


def commit_subject(revision='HEAD'):
    """Gets the subject of a ``git`` commit.

    Args:
        revision (Optional[str]): A ``git`` revision, any of a branch
            name, tag, a commit SHA or a special reference.

    Returns:
        str: The commit subject.
    """
    return _utils.check_output(
        'git', 'log', '--pretty=%s', '-1', revision)
