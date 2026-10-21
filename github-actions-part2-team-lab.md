# Part 2: Team Collaboration Lab

In Part 1 you protected `main` on your own. In real projects, several developers change the same code at the same time. In this hands-on lab, your team of three will add new features to the same repository, each on your own branch, and merge them into `main` one at a time.

By the end you will have practised:

- Working on a feature branch while teammates work on theirs
- Opening and reviewing Pull Requests
- Updating your branch with your teammates' latest work
- Resolving a **merge conflict**
- Getting your changes through CI and branch protection into `main`

**Estimated time:** 60–75 minutes

---

## Words you'll see

| Term | Meaning |
| --- | --- |
| **Collaborator** | A person who has been given permission to push branches to a GitHub repository. |
| **Code review** | A teammate reads your Pull Request and comments on it or approves it before it is merged. |
| **Out of date** | Your branch is missing commits that were added to `main` after you created the branch. |
| **Merge conflict** | Two branches changed the same lines of a file, and Git needs a person to decide what the final version should be. |
| **Conflict markers** | The `<<<<<<<`, `=======`, and `>>>>>>>` lines Git adds to a file to show both versions of a conflict. |

Part 1 terms (CI, workflow, status check, Pull Request, LF/CRLF) are in the **Words you'll see** table in Part 1.

---

## Before You Start

### What you need

- Part 1 completed (you will reuse its VS Code settings and pre-push hook)
- An invitation email from GitHub to your team's repository (your instructor sends this)
- The same terminal you used in Part 1 (Git Bash *or* WSL)

### Choose your roles

Decide as a team who is Student 1, Student 2, and Student 3. Each role adds one function and its tests.

| Role | Branch | You add | Merge order |
| --- | --- | --- | --- |
| **Student 1** | `feature/subtract` | `subtract_numbers` | 1st |
| **Student 2** | `feature/multiply` | `multiply_numbers` | 2nd |
| **Student 3** | `feature/divide` | `divide_numbers` | 3rd |

### How this lab works

The lab has two phases:

1. **Phase 1, Build (Steps 1–7):** everyone works **at the same time** on their own branch and opens a Pull Request. Nobody merges yet.
2. **Phase 2, Merge (Steps 8–11):** you merge **one at a time**, in the order above. Before each merge, that student pulls in everything merged before them.

> **Heads-up: merge conflicts are part of the plan.** All three of you will add code to the same two files, in the same place. Student 2 and Student 3 **will** see a merge conflict. That is not a mistake. Resolving it is the main skill this lab teaches, and Steps 9 and 10 walk you through it.

---

# Phase 1: Build (Everyone, at the Same Time)

## Step 1: Accept the Repository Invitation

1. Open the email from GitHub titled something like **"invited you to collaborate"**. You can also go to [github.com/notifications](https://github.com/notifications).
2. Click **View invitation**, then **Accept invitation**.

**Checkpoint:** You can open your team's repository on GitHub, and you see the same files you had at the end of Part 1.

---

## Step 2: Clone the Team Repository

Your instructor will give you the repository URL. In your terminal, run these commands, replacing `<team-repo-url>` and `<team-repo-name>`:

```bash
cd ~
git clone <team-repo-url>
cd <team-repo-name>
code .
```

**Checkpoint:** VS Code opens and shows `app.py`, `test_app.py`, and `.github/workflows/ci.yml`. Then open the VS Code terminal (**Terminal** > **New Terminal**) and use it for the rest of the lab.

> The VS Code settings from Part 1 (showing `.git` and using `LF`) apply to every project, so you do not need to set them again.

---

## Step 3: Reinstall the Pre-Push Hook

Hooks live in the `.git` folder, and **Git never copies that folder to GitHub**. A fresh clone has no pre-push hook, so you need to add it again for this repository.

1. Repeat **Part 1, Steps 9.1–9.4** in this project: create `.git/hooks/pre-push`, paste the script, save it with **LF**, and run `chmod +x`.
2. Check the line endings:

   ```bash
   tr -cd '\r' < .git/hooks/pre-push | wc -c
   ```

**Checkpoint:** The output is `0`.

---

## Step 4: Create Your Feature Branch

Run **only the command for your role**:

**Student 1:**

```bash
git switch -c feature/subtract
```

**Student 2:**

```bash
git switch -c feature/multiply
```

**Student 3:**

```bash
git switch -c feature/divide
```

**Checkpoint:** Run `git branch`. Your branch has a `*` next to it.

---

## Step 5: Add Your Function and Tests

Every role makes the same **three changes** in the same places. Following these placement rules exactly keeps the merge conflicts in Phase 2 small and easy to read:

| Change | Where it goes |
| --- | --- |
| **A.** Your function | At the **bottom** of `app.py`, with **two blank lines** above it |
| **B.** Your import | In `test_app.py`, on a **new line directly below** `from app import add_numbers` |
| **C.** Your test(s) | At the **bottom** of `test_app.py`, with **two blank lines** above it |

Find your role below, make the changes in VS Code, and save both files.

### Student 1: Subtraction

**A.** Bottom of `app.py`:

```python
def subtract_numbers(a: int, b: int) -> int:
    return a - b
```

**B.** Below `from app import add_numbers` in `test_app.py`:

```python
from app import subtract_numbers
```

**C.** Bottom of `test_app.py`:

```python
def test_subtract_numbers():
    assert subtract_numbers(5, 3) == 2
    assert subtract_numbers(3, 5) == -2
    assert subtract_numbers(0, 0) == 0
```

### Student 2: Multiplication

**A.** Bottom of `app.py`:

```python
def multiply_numbers(a: int, b: int) -> int:
    return a * b
```

**B.** Below `from app import add_numbers` in `test_app.py`:

```python
from app import multiply_numbers
```

**C.** Bottom of `test_app.py`:

```python
def test_multiply_numbers():
    assert multiply_numbers(4, 3) == 12
    assert multiply_numbers(-2, 3) == -6
    assert multiply_numbers(5, 0) == 0
```

### Student 3: Division

Division has one extra case to handle: dividing by zero. Instead of letting Python crash with its own error, your function raises a clear `ValueError`, and a second test checks that it does.

**A.** Bottom of `app.py`:

```python
def divide_numbers(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**B.** You need **two** imports in `test_app.py`:

- At the **very top**, directly below the `# test_app.py` comment, add `import pytest` followed by **one blank line**.
- Below `from app import add_numbers`, add your function's import.

The top of your file should then look like this:

```python
# test_app.py
import pytest

from app import add_numbers
from app import divide_numbers
```

**C.** Bottom of `test_app.py`:

```python
def test_divide_numbers():
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(-9, 3) == -3
    assert divide_numbers(7, 2) == 3.5


def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError):
        divide_numbers(5, 0)
```

> `pytest.raises(ValueError)` means "this test passes only if the code inside raises a `ValueError`." This is how you test that error handling works.

### Make the tests your own (everyone)

Add **at least one more `assert`** to your test function that checks a case you think is worth testing, such as large numbers, two negatives, or (for division) a result with a long decimal. Be ready to explain your choice to your reviewer.

---

## Step 6: Run the Tests and Commit

Run the tests:

**Git Bash (Windows):**

```bash
python -m pytest
```

**WSL (Ubuntu) / Linux / macOS:**

```bash
python3 -m pytest
```

**Checkpoint:**

- **Student 1 and Student 2:** `2 passed`
- **Student 3:** `3 passed`

If a test fails, read the error, fix your code, and run the tests again before you continue.

Then commit your work, using the message for your role:

**Student 1:**

```bash
git add app.py test_app.py
git commit -m "Add subtract_numbers with tests"
```

**Student 2:**

```bash
git add app.py test_app.py
git commit -m "Add multiply_numbers with tests"
```

**Student 3:**

```bash
git add app.py test_app.py
git commit -m "Add divide_numbers with tests"
```

---

## Step 7: Push Your Branch and Open a Pull Request

### 7.1 Push your branch

```bash
git push -u origin HEAD
```

> `HEAD` means "the branch I'm on right now", so this one command works for every role. Your pre-push hook runs the tests first.

### 7.2 Open a Pull Request

1. Open your team's repository on GitHub.
2. Click **Compare & pull request** in the yellow banner. (No banner? Go to **Pull requests** > **New pull request** and choose your branch as **compare**.)
3. Set the title to your commit message, for example `Add subtract_numbers with tests`.
4. In the description, write one sentence about what you added and which extra test case you chose.
5. On the right, under **Reviewers**, select a teammate.
6. Click **Create pull request**.

**Do not merge yet.**

**Checkpoint:** Your team's **Pull requests** tab shows **three** open Pull Requests, and each one shows a green ✅ for the `test` check.

> If your instructor turned on required approvals, the **Merge** button stays disabled until a teammate approves. You'll do that in Phase 2.

---

# Phase 2: Merge (One at a Time, in Order)

From here on, take turns. When it is not your turn, help the student who is merging by reviewing their Pull Request and watching their screen or shared terminal.

## Step 8: Student 1 Merges

**Student 2 and Student 3:** review Student 1's Pull Request.

1. Open the Pull Request and click the **Files changed** tab.
2. Read the changes. Leave at least one comment (a question, a suggestion, or something done well).
3. Click **Review changes** > **Approve** > **Submit review**.

**Student 1:**

1. Confirm the `test` check is a green ✅.
2. Click **Merge pull request**, then **Confirm merge**.
3. Click **Delete branch**.
4. Tell your team: **"Merged. Student 2, you're up."**

**Student 2 and Student 3:** refresh your own Pull Requests. They now show a message like **"This branch has conflicts that must be resolved"** or **"This branch is out-of-date with the base branch."**

> **Why this happens:** `main` now has subtraction, but your branch was created before that existed. Branch protection is set to **require branches to be up to date before merging**, so GitHub will not merge your branch until it includes the latest `main`. This stops two changes that each pass their own tests from breaking each other once combined.
>
> **Do not click GitHub's "Update branch" or "Resolve conflicts" buttons.** You will update your branch on your own computer so you can run the tests before pushing.

---

## Step 9: Student 2 Updates and Merges

**Student 2** does this step. **Student 3** reviews and approves Student 2's Pull Request (as in Step 8) while Student 2 works.

### 9.1 Get the latest `main`

```bash
git switch main
git pull origin main
```

### 9.2 Merge `main` into your branch

```bash
git switch feature/multiply
git merge main --no-edit
```

> `--no-edit` tells Git to use its default merge message instead of opening a text editor.

**Expected result:** Git reports conflicts in both files. **This is expected.**

```text
Auto-merging app.py
CONFLICT (content): Merge conflict in app.py
Auto-merging test_app.py
CONFLICT (content): Merge conflict in test_app.py
Automatic merge failed; fix conflicts and then commit the result.
```

### 9.3 Read the conflict

Open `app.py` in VS Code. Git has marked the part where both branches added code:

```text
<<<<<<< HEAD
def multiply_numbers(a: int, b: int) -> int:
    return a * b
=======
def subtract_numbers(a: int, b: int) -> int:
    return a - b
>>>>>>> main
```

| Marker | Meaning |
| --- | --- |
| `<<<<<<< HEAD` | Start of **your** branch's version (VS Code calls this the **Current Change**). |
| `=======` | Divider between the two versions. |
| `>>>>>>> main` | End of the version from `main`, which is Student 1's work (the **Incoming Change**). |

Git cannot know that you want **both** functions, so it asks you. Here the answer is easy: keep both.

### 9.4 Resolve the conflicts

Do this for **every** conflict in **both** files. `app.py` has one; `test_app.py` has two (the imports and the tests).

1. Above each conflict, VS Code shows clickable options. Click **Accept Both Changes**.
2. VS Code keeps both versions but puts them directly next to each other. Between two **functions**, add **two blank lines** so the code matches the project's style. Imports stay on consecutive lines with no blank lines between them.
3. Save the file.

> **Prefer to use the keyboard, or don't see the options?** You can resolve the conflict by hand. Delete the three marker lines (`<<<<<<<`, `=======`, `>>>>>>>`), keep both blocks of code, and fix the blank lines.

When you are done, `app.py` should contain three functions with no markers:

```python
# app.py
def add_numbers(a: int, b: int) -> int:
    return a + b


def multiply_numbers(a: int, b: int) -> int:
    return a * b


def subtract_numbers(a: int, b: int) -> int:
    return a - b
```

> The order of the functions does not matter. Python finds them by name.

### 9.5 Check that no markers are left

```bash
grep -nE '^(<<<<<<<|=======|>>>>>>>)' app.py test_app.py
```

**Checkpoint:** The command prints **nothing**. If it prints any lines, those markers are still in the file. Go back to 9.4.

### 9.6 Run the tests

**Git Bash (Windows):**

```bash
python -m pytest
```

**WSL (Ubuntu) / Linux / macOS:**

```bash
python3 -m pytest
```

**Checkpoint:** `3 passed` (add, subtract, and multiply). Your code and Student 1's code now work together.

### 9.7 Finish the merge and push

```bash
git add app.py test_app.py
git commit --no-edit
git push
```

### 9.8 Merge your Pull Request

1. On GitHub, refresh your Pull Request. The conflict message is gone, and CI runs again on the combined code.
2. Wait for the `test` check to turn into a green ✅, and for Student 3's approval if your team requires it.
3. Click **Merge pull request** > **Confirm merge** > **Delete branch**.
4. Tell your team: **"Merged. Student 3, you're up."**

---

## Step 10: Student 3 Updates and Merges

**Student 3** does this step. **Student 1** reviews and approves Student 3's Pull Request while Student 3 works.

Wait until Student 2 says they have merged. If you update your branch before then, you will have to do it twice.

### 10.1 Get the latest `main` and merge it into your branch

```bash
git switch main
git pull origin main
git switch feature/divide
git merge main --no-edit
```

**Expected result:** Conflicts in `app.py` and `test_app.py`, just like Student 2 saw. This time the `main` side of each conflict contains **both** of your teammates' work.

`app.py` will look like this:

```text
<<<<<<< HEAD
def divide_numbers(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
=======
def multiply_numbers(a: int, b: int) -> int:
    return a * b


def subtract_numbers(a: int, b: int) -> int:
    return a - b
>>>>>>> main
```

> Your `import pytest` line at the top of `test_app.py` does **not** conflict, because nobody else changed that line. Git merged it automatically.

### 10.2 Resolve, check, and test

Follow **Steps 9.4–9.6** in your files. Use **Accept Both Changes**, fix the blank lines between functions, save, and check that no markers are left.

**Checkpoint:** The tests report `5 passed`: add, subtract, multiply, divide, and divide-by-zero. (Extra `assert` lines go inside existing tests, so they don't change this count.)

### 10.3 Finish the merge, push, and merge your Pull Request

```bash
git add app.py test_app.py
git commit --no-edit
git push
```

Then follow **Step 9.8**: wait for the green ✅ (and approval), then click **Merge pull request** > **Confirm merge** > **Delete branch**.

Tell your team: **"Merged. Everyone, sync up!"**

---

## Step 11: Everyone Syncs and Verifies

**All three students** run this on their own computer to get the final version of `main` and delete their finished branch. Run **only the `git branch -d` line for your role**:

```bash
git switch main
git pull origin main
```

**Student 1:**

```bash
git branch -d feature/subtract
```

**Student 2:**

```bash
git branch -d feature/multiply
```

**Student 3:**

```bash
git branch -d feature/divide
```

Then run the tests one last time:

**Git Bash (Windows):**

```bash
python -m pytest
```

**WSL (Ubuntu) / Linux / macOS:**

```bash
python3 -m pytest
```

**Checkpoint (everyone):**

- [ ] `app.py` contains `add_numbers`, `subtract_numbers`, `multiply_numbers`, and `divide_numbers`.
- [ ] The tests report `5 passed`.
- [ ] The **Actions** tab on GitHub shows a green ✅ for the latest run on `main`.
- [ ] The **Pull requests** tab shows **3 Closed** (merged) Pull Requests.

To see the whole team's history as a diagram, run:

```bash
git log --oneline --graph -15
```

🎉 **Your team is done!** You took three changes made at the same time, combined them safely, and every step was checked by CI before it reached `main`.

---

## Reflect as a Team

Spend five minutes discussing these questions:

1. Student 3 had to combine more code than Student 2. What would happen with 10 developers merging in the same order? How could a team reduce that?
2. Why did we run the tests **after** resolving the conflict, even though every branch had already passed CI on its own?
3. What would have been different if all three of you had put your functions in **separate files**?

---

## Troubleshooting

### A text editor opened in the terminal after `git merge` or `git commit`

You probably left off `--no-edit`, so Git opened a text editor (often **Vim**) for the merge message. To accept the default message and continue:

- **Vim** (the screen shows `~` down the left side): press **Esc**, type `:wq`, and press **Enter**.
- **Nano** (the bottom of the screen shows `^X Exit`): press **Ctrl+X**.

### CI fails with `SyntaxError` after resolving a conflict

A conflict marker was probably left in a file. Run the marker check from Step 9.5, remove anything it finds, run the tests, then commit and push again.

### `git push` is rejected with `non-fast-forward` or `fetch first`

Your branch on GitHub has commits that your computer does not have. This usually happens if someone clicked **Update branch** on GitHub. Run `git pull`, then push again.

### My push went through without the tests running

The pre-push hook is missing in this clone, or it isn't executable. Redo Step 3.

### The **Merge pull request** button is disabled

Check the message at the bottom of the Pull Request:

| Message | What to do |
| --- | --- |
| Conflicts must be resolved / branch is out of date | It's your turn to update. Follow Step 9 (or Step 10). |
| Required statuses must pass | Wait for CI. If it's red ❌, click **Details** to read the error. |
| Review required | Ask a teammate to approve the Pull Request. |

### I committed on `main` by mistake

If you haven't pushed yet, move the commit onto a new branch and reset `main`:

```bash
git switch -c feature/rescue
git switch main
git reset --hard origin/main
```

Your work is now on `feature/rescue`. Ask your instructor if you're unsure which branch name to use.

### Anything from Part 1

Line-ending errors, `python: command not found`, and password or token problems are covered in **Part 1, Troubleshooting**.
