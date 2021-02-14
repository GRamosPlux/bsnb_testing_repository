# ======================================================================================================================
# ============================================== Import Packages =======================================================
# ======================================================================================================================
import os
import git
from time import *

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< REQUIREMENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ---> Git should be installed and configured in the computer where the script will be executed.

# ======================================================================================================================
# ============================================= Repository Info ========================================================
# ======================================================================================================================
root_path = ".." + os.sep

# ======================================================================================================================
# ====================================== Creating a Branch per Category ================================================
# ======================================================================================================================
# >>> Identification of the path for the local version of the repository
#     (in the parent directory of the current project).
curr_dir = os.path.dirname(os.path.realpath(""))
repo = git.Repo(curr_dir)

# >>> Creating/Checkout the new branch reference.
new_branch = 'test_branch'
current = repo.git.checkout(new_branch)

#creating file
dtime = strftime('%d-%m-%Y %H:%M:%S', localtime())
with open(curr_dir + os.sep + 'lastCommit' + '.txt', 'w') as f:
    f.write(str(dtime))
print('file created---------------------')

# >>> Push data to the remote version of the repository.
if repo.index.diff(None) or repo.untracked_files:
    repo.git.add(A=True)
    repo.git.commit(m='msg')
    repo.git.push('--set-upstream', 'origin', current)
    print('git push')
else:
    print('no changes')