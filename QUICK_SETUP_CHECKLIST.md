# Quick Setup Checklist

Use this checklist to quickly set up your docs-as-code system. Check off each item as you complete it.

---

## Pre-Setup (Already Done! ✅)

- [x] MkDocs configured with Material theme
- [x] GitHub Actions workflows created
- [x] Documentation written and tested
- [x] Build passing locally (71 seconds, 1,255 pages)
- [x] All changes committed and pushed

---

## Step 1: Enable GitHub Pages (5 minutes)

**URL:** https://github.com/Chunkys0up7/docascode/settings/pages

### Actions:
- [ ] Go to repository Settings
- [ ] Click "Pages" in left sidebar
- [ ] Set Source to **"GitHub Actions"**
- [ ] (No other settings needed!)

### Then:
- [ ] Go to Settings > Actions > General
- [ ] Scroll to "Workflow permissions"
- [ ] Select **"Read and write permissions"**
- [ ] Check **"Allow GitHub Actions to create and approve pull requests"**
- [ ] Click Save

### Verify:
- [ ] Source shows "GitHub Actions"
- [ ] Permissions show "Read and write"

**📖 Detailed Guide:** See `GITHUB_PAGES_SETUP.md`

---

## Step 2: Configure Branch Protection (10 minutes)

**URL:** https://github.com/Chunkys0up7/docascode/settings/branches

### Actions:
- [ ] Go to repository Settings
- [ ] Click "Branches" in left sidebar
- [ ] Click "Add rule" button

### Settings to Configure:
- [ ] **Branch name pattern:** Type `main`
- [ ] ✅ Check "Require a pull request before merging"
  - [ ] ✅ Check "Require approvals"
  - [ ] Set number to: **1**
- [ ] ✅ Check "Require status checks to pass before merging"
  - [ ] ✅ Check "Require branches to be up to date before merging"
  - [ ] Search for and select: **build-and-test** (if available)
- [ ] ❌ Leave "Allow force pushes" UNCHECKED
- [ ] ❌ Leave "Allow deletions" UNCHECKED

### Save:
- [ ] Scroll to bottom
- [ ] Click green "Create" button
- [ ] See success message

**📖 Detailed Guide:** See `BRANCH_PROTECTION_GUIDE.md`

**⚠️ Note:** If `build-and-test` doesn't appear, that's OK! Save anyway and add it later after first workflow runs.

---

## Step 3: Deploy Documentation (15 minutes)

### Trigger First Deployment:

**Option A: Merge Current Work**
```bash
git checkout main
git pull origin main
git merge claude/docs-as-code-plan-011CV2T4yq7YmkQ3oyt25Tip
git push origin main
```

**Option B: Manual Trigger**
- [ ] Go to Actions tab on GitHub
- [ ] Click "Deploy Documentation to GitHub Pages"
- [ ] Click "Run workflow" → Select main → Run

### Monitor Deployment:
- [ ] Go to Actions tab
- [ ] Watch "Deploy Documentation to GitHub Pages" workflow
- [ ] Wait for green checkmarks (2-3 minutes)

### Verify Deployment:
- [ ] Go back to Settings > Pages
- [ ] Look for: "Your site is live at..."
- [ ] Click the URL
- [ ] **Your docs are live!** 🎉

**Expected URL:** https://chunkys0up7.github.io/docascode/

---

## Step 4: Test the System (15 minutes)

### Create a Test PR:
```bash
# Create test branch
git checkout main
git pull origin main
git checkout -b test/verify-workflow

# Make a small change
echo "\n## Test Update" >> site_docs/index.md

# Commit and push
git add site_docs/index.md
git commit -m "docs: test automated CI/CD workflow"
git push origin test/verify-workflow
```

### On GitHub:
- [ ] Create Pull Request
- [ ] Wait for checks to run
- [ ] See "build-and-test" check appear
- [ ] Wait for check to pass (green checkmark)
- [ ] Request approval from teammate (or approve yourself if allowed)
- [ ] Merge the PR
- [ ] Watch automatic deployment run
- [ ] Visit your docs URL - see the change live!

### Verify Everything Works:
- [ ] PR created successfully
- [ ] Build check ran automatically
- [ ] Build check passed
- [ ] Approval required before merge
- [ ] Deploy workflow ran after merge
- [ ] Changes appeared on live site
- [ ] All under 5 minutes from merge to live!

---

## Step 5: Go Back and Add Status Check (5 minutes)

**Only if you skipped it in Step 2:**

Now that workflows have run, the status check will be available:

- [ ] Go to Settings > Branches
- [ ] Click "Edit" on the main branch rule
- [ ] Scroll to "Require status checks to pass before merging"
- [ ] Search for: **build-and-test**
- [ ] Click it to select it
- [ ] Scroll down and click "Save changes"

---

## Final Verification Checklist

- [ ] GitHub Pages is enabled and working
- [ ] Documentation site is live at GitHub Pages URL
- [ ] Branch protection is active on main
- [ ] PRs require 1 approval
- [ ] PRs require passing build checks
- [ ] Test PR successfully completed full workflow
- [ ] Changes deploy automatically on merge
- [ ] Team can access documentation

---

## Quick Links

| Resource | Purpose |
|----------|---------|
| `GITHUB_PAGES_SETUP.md` | Detailed Pages setup |
| `BRANCH_PROTECTION_GUIDE.md` | Detailed branch protection |
| `WEEK1_PROGRESS.md` | Progress tracking |
| `site_docs/quick-start-guide.md` | Getting started guide |
| `site_docs/implementation-roadmap.md` | Full 16-week plan |

---

## Common Issues & Solutions

### "I don't see the Settings tab"
→ You need admin access. Ask the repo owner.

### "build-and-test doesn't appear"
→ Normal! Save without it, add after first workflow runs.

### "GitHub Pages shows 404"
→ Wait 5-10 minutes after first deployment.

### "Workflow permissions error"
→ Enable "Read and write permissions" in Settings > Actions > General

### "Can't merge PR even with approval"
→ Build must pass first. Check Actions tab for errors.

---

## Time Estimate

| Step | Time | Can Skip? |
|------|------|-----------|
| Enable GitHub Pages | 5 min | No |
| Branch Protection | 10 min | Optional* |
| First Deployment | 15 min | No |
| Test PR | 15 min | Optional** |
| Add Status Check | 5 min | Yes |
| **Total** | **30-50 min** | |

\* Branch protection is highly recommended but can be added later
\** Testing is recommended to verify everything works

---

## Success Criteria

You're done when:

✅ Your documentation is live at: https://chunkys0up7.github.io/docascode/
✅ You can create PRs and they build automatically
✅ Changes deploy automatically when you merge to main
✅ Build failures prevent merging (protecting quality)

---

## What You've Accomplished

After completing this checklist:

- 🚀 **Automated CI/CD** - Builds and deploys automatically
- 🛡️ **Quality Gates** - Bad docs can't be merged
- 📚 **Live Documentation** - Always up-to-date, always online
- 👥 **Team Collaboration** - PR reviews built into workflow
- ⚡ **Fast Deployment** - Changes live in 2-3 minutes

**You now have a production-grade docs-as-code system!**

---

## Next: Week 2

After completing setup, move to Week 2 tasks:

- Create documentation templates
- Define naming conventions
- Set up issue templates
- Train team members

See `site_docs/implementation-checklist.md` for Week 2 details.

---

## Need Help?

1. Check the detailed guides listed above
2. Look at workflow logs in Actions tab
3. Review troubleshooting sections
4. Create an issue with screenshots
5. Ask in team chat

**You've got this! 🎉**
