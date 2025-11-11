# Branch Protection Setup - Step-by-Step Guide

Follow these exact steps to configure branch protection for your main branch.

---

## Step-by-Step Instructions

### Step 1: Navigate to Branch Settings

1. **Open your repository** on GitHub:
   - Go to: https://github.com/Chunkys0up7/docascode

2. **Click the "Settings" tab**
   - Located at the top of the page, to the right of "Insights"
   - If you don't see Settings, you may need admin access

3. **In the left sidebar**, scroll down and click **"Branches"**
   - It's under the "Code and automation" section
   - Icon looks like a branch symbol

### Step 2: Add Branch Protection Rule

1. **Look for the "Branch protection rules" section**
   - You'll see a heading "Branch protection rules"
   - Below it, there may be a message "You don't have any protected branches"

2. **Click the green "Add rule" button** (or "Add branch protection rule")
   - It's on the right side of the Branch protection rules section

### Step 3: Configure the Rule

**You'll now see a form with many options. Follow these settings:**

#### A. Branch Name Pattern

At the top of the page:

```
Branch name pattern: main
```

- **Type exactly:** `main`
- This tells GitHub to protect the main branch

#### B. Protect Matching Branches

Scroll down and check these boxes:

**1. Require a pull request before merging**
- ✅ **CHECK THIS BOX**
- After checking it, you'll see sub-options appear

**Sub-options that appear:**
- ✅ **Require approvals**
  - A number field appears next to it
  - **Enter:** `1`
  - This means 1 person must approve before merging

- ✅ **Dismiss stale pull request approvals when new commits are pushed** (optional but recommended)

**2. Require status checks to pass before merging**
- ✅ **CHECK THIS BOX**
- After checking it, you'll see sub-options appear

**Sub-options that appear:**
- ✅ **Require branches to be up to date before merging**
  - Check this box

- **Search box: "Search for status checks in the last week for this repository"**
  - Type: `build-and-test`
  - If it appears in the list, click it to select it
  - **Note:** If `build-and-test` doesn't appear yet, that's OK! It will appear after your first workflow runs. You can come back and add it later.

**3. Other settings (leave unchecked for now)**
- ❌ Require conversation resolution before merging (optional)
- ❌ Require signed commits (not needed)
- ❌ Require linear history (not needed)
- ❌ Require deployments to succeed before merging (not needed)

**4. At the bottom of the form:**
- ❌ **Do not** check "Allow force pushes"
- ❌ **Do not** check "Allow deletions"

### Step 4: Save the Rule

1. **Scroll to the very bottom** of the page

2. **Click the green "Create" button** (or "Save changes" if editing)

3. **You'll see a success message**
   - The rule is now active!

---

## Visual Checklist

Here's what your settings should look like:

```
✅ Branch name pattern: main
✅ Require a pull request before merging
  ✅ Require approvals: 1
  ✅ Dismiss stale pull request approvals when new commits are pushed
✅ Require status checks to pass before merging
  ✅ Require branches to be up to date before merging
  ✅ Status checks: build-and-test (if available)
❌ Allow force pushes: UNCHECKED
❌ Allow deletions: UNCHECKED
```

---

## If You Don't See "build-and-test" Status Check

**This is normal if you haven't run any workflows yet!**

**Option 1: Come Back Later (Recommended)**
1. Save the rule without selecting a status check
2. After you enable GitHub Pages and run a workflow
3. Come back to Settings > Branches
4. Click "Edit" on the main branch rule
5. The `build-and-test` check will now appear in the search
6. Select it and save

**Option 2: Run a Workflow First**
1. First enable GitHub Pages (see GITHUB_PAGES_SETUP.md)
2. Push a small change to trigger the workflow
3. Wait for it to complete
4. Then come back and set up branch protection

---

## What This Does

Once configured, the main branch is protected:

- ❌ **Cannot push directly to main**
  - Must create a pull request

- ❌ **Cannot merge without approval**
  - At least 1 person must approve

- ❌ **Cannot merge with failing tests**
  - Build must pass (green checkmark)

- ❌ **Cannot merge outdated branches**
  - Branch must be up-to-date with main

---

## Testing the Protection

After setting up, test that it works:

1. **Try to push directly to main** (this should fail):
   ```bash
   git checkout main
   echo "test" >> README.md
   git commit -am "test: direct push"
   git push origin main
   ```
   **Expected:** GitHub rejects the push

2. **Create a PR instead** (this should work):
   ```bash
   git checkout -b test/branch-protection
   git push origin test/branch-protection
   # Then create PR on GitHub
   ```
   **Expected:** PR is created, but you can't merge without approval

---

## Troubleshooting

### "I don't see the Settings tab"

**Reason:** You need admin access to the repository

**Solution:**
- Ask the repository owner to give you admin access
- Or ask them to set up branch protection using this guide

### "The Create button is grayed out"

**Reason:** The branch name pattern is required

**Solution:**
- Make sure you entered `main` in the "Branch name pattern" field at the top

### "I can't find the Branches section"

**Steps to find it:**
1. Go to repository main page
2. Click "Settings" (top right)
3. Look at left sidebar
4. Scroll down to find "Branches" (under "Code and automation")

### "build-and-test doesn't appear in status checks"

**This is normal!**

**Reason:** No workflows have run yet

**Solution:**
- Save the rule without selecting it
- Enable GitHub Pages first
- Run your first workflow
- Come back and add the status check later

---

## Quick Reference

**GitHub Path:**
```
Repository → Settings → Branches → Add rule
```

**Required Fields:**
```
Branch name pattern: main
✅ Require a pull request before merging
   - Require approvals: 1
✅ Require status checks to pass before merging
   - Require branches to be up to date before merging
```

**Save:**
```
Click "Create" at bottom of page
```

---

## Next Steps

After branch protection is set up:

1. ✅ Verify the rule appears in the list
2. ✅ Test with a practice PR
3. ✅ Move on to enabling GitHub Pages
4. ✅ Run your first automated deployment

See `GITHUB_PAGES_SETUP.md` for the next step!

---

## Need Help?

If you get stuck:

1. **Take a screenshot** of what you see
2. **Check you have admin access** to the repository
3. **Try refreshing** the GitHub page
4. **Ask in team chat** or create an issue

The most important settings are:
- ✅ Require pull request
- ✅ Require 1 approval
- Everything else can be added later!
