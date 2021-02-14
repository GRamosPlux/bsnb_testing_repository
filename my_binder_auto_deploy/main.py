# ======================================================================================================================
# ============================================== Import Packages =======================================================
# ======================================================================================================================
import os
import git
import json
from time import *

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< REQUIREMENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ---> Git should be installed and configured in the computer where the script will be executed.

# ======================================================================================================================
# ============================================= Repository Info ========================================================
# ======================================================================================================================
root_path = ".." + os.sep
src_folder = "header_footer" + os.sep + "biosignalsnotebooks_environment" + os.sep

# ======================================================================================================================
# =========================================== Available Categories =====================================================
# ======================================================================================================================
branch_prefix = "myBinder/"
nb_categories = ["Connect", "Detect", "Evaluate", "Extract", "Install", "Load", "MainFiles", "Other", "Pre-Process",
                 "Record", "Train_And_Classify", "Understand", "Visualise"]

# ======================================================================================================================
# ====================================== Creating a Branch per Category ================================================
# ======================================================================================================================
# >>> Identification of the path for the local version of the repository
#     (in the parent directory of the current project).
curr_dir = os.path.dirname(os.path.realpath(""))
repo = git.Repo(curr_dir)

# >>> Push pending changes into master branch.
if repo.index.diff(None) or repo.untracked_files:
    print("Pushing master changes to remote repository...")
    repo.git.add(A=True)
    repo.git.commit(m='Preparation for myBinder release')
    repo.git.push()
else:
    print('No changes in this branch')

# >>> Creating/Checkout the new branch reference.
for category in nb_categories:
    # Check if the current category branch should be updated.
    # >>> Read JSON file containing the list of updated Notebooks.
    with open(src_folder + 'last_updated_nbs.json') as f:
        data = json.load(f)
    # >>> Convert JSON data into a dictionary.
    json_dict = json.loads(data)
    # >>> Store the list of updated Notebooks.
    upt_notebooks = json_dict["updated_notebooks"]

    # Get list of Notebooks in the current category folder.
    list_files = os.listdir()
    print(list_files)

    branch_name = branch_prefix + category.lower()
    if branch_name in repo.references:
        # Checkout to an existing branch.
        current = repo.git.checkout(branch_name)
        print(">>> Branch [" + branch_name + "] already exists...")
    else:
        try:
            # Create an orphan branch.
            current = repo.git.checkout('--orphan', branch_name)
            repo.git.reset("--hard")

            # Migration of .gitignore file
            repo.git.checkout("master", ".gitignore")
        except git.exc.GitCommandError:
            print("Local branch already exists...")
        print(">>> Trying to create a new branch [" + branch_name + "]...")

    # Get files from master belonging to the category under analysis.
    try:
        # Creating log file.
        dtime = strftime('%d-%m-%Y %H:%M:%S', localtime())
        with open(curr_dir + os.sep + 'log' + '.txt', 'w') as f:
            f.write(str(dtime))

        # Retrieve files from master.
        repo.git.checkout("master", src_folder + "categories" + os.sep + category)  # Notebooks belonging to this category.
        # >>> Resources folders.
        repo.git.checkout("master", src_folder + "images")  # Images.
        repo.git.checkout("master", src_folder + "signal_samples")  # Signal Samples.
        repo.git.checkout("master", src_folder + "styles")  # CSS Styles.
    except git.exc.GitCommandError:
        print("No files to be imported from master")

    # >>> Push data to the remote version of the repository.
    if repo.index.diff(None) or repo.untracked_files:
        print("Pushing [" + branch_name + "] changes to remote repository...")
        repo.git.add(A=True)
        repo.git.commit(m='msg')
        repo.git.push("--set-upstream", "origin", branch_name)
    else:
        print('No changes in this branch')

# Return to master branch.
current = repo.git.checkout("master")
