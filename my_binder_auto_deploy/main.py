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
# =========================================== Available Categories =====================================================
# ======================================================================================================================
branch_prefix = "myBinder/"
nb_categories = ["Test7"]

# ======================================================================================================================
# ====================================== Creating a Branch per Category ================================================
# ======================================================================================================================
# >>> Identification of the path for the local version of the repository
#     (in the parent directory of the current project).
curr_dir = os.path.dirname(os.path.realpath(""))
repo = git.Repo(curr_dir)

# >>> Push pending changes into master branch.
if repo.index.diff(None) or repo.untracked_files:
    repo.git.add(A=True)
    repo.git.commit(m='Preparation for myBinder release')
    repo.git.push()
else:
    print('no changes')

# >>> Creating/Checkout the new branch reference.
for category in nb_categories:
    branch_name = branch_prefix + category.lower()
    if branch_name in repo.references:
        # Checkout to an existing branch.
        current = repo.git.checkout(branch_name)
    else:
        try:
            # Create an orphan branch.
            current = repo.git.checkout('--orphan', branch_name)
            repo.git.reset("--hard")

            # Migration of .gitignore file
            repo.git.checkout("master", ".gitignore")
        except git.exc.GitCommandError:
            print("Local branch already exists...")

    # creating file
    dtime = strftime('%d-%m-%Y %H:%M:%S', localtime())
    with open(curr_dir + os.sep + 'lastCommit' + '.txt', 'w') as f:
        f.write(str(dtime))
    print('file created---------------------')

    # >>> Push data to the remote version of the repository.
    if repo.index.diff(None) or repo.untracked_files:
        repo.git.add(A=True)
        repo.git.commit(m='msg')
        repo.git.push("--set-upstream", "origin", branch_name)
    else:
        print('no changes')

# Return to master branch.
current = repo.git.checkout("master")