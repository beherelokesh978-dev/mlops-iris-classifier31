# Git Version Control Workflow

## Repository

- Project: MLOps Iris Classifier
- Repository: mlops-iris-classifier
- Platform: GitHub
- Primary Language: Python

## Branching Strategy

- `main` - stable project branch
- `develop` - development/integration branch
- `feature/*` - new features
- `conflict-demo-*` - branches used for conflict-resolution practice

## Commit Convention

Commits follow a simple convention:

- `feat:` - new feature
- `fix:` - bug fix
- `docs:` - documentation changes
- `chore:` - project maintenance
- `merge:` - merge/conflict resolution

Example:

    feat: add classification report to training script

## Standard Workflow

1. Create or switch to the required branch.
2. Make changes to the project.
3. Test the changes.
4. Check the Git status.
5. Stage the required files.
6. Commit with a meaningful message.
7. Push the branch to GitHub.
8. Create a Pull Request when required.
9. Review and merge the Pull Request.
10. Pull the latest changes locally.

## Conflict Resolution

When a merge conflict occurs:

1. Run `git status`.
2. Open the conflicted file.
3. Identify the conflict markers.
4. Decide which changes should be kept.
5. Remove the conflict markers.
6. Save the file.
7. Run `git add <file>`.
8. Commit the resolved merge.
9. Test the project.
10. Push the updated branch.

## .gitignore Policy

The `.gitignore` file prevents unnecessary or generated files from being tracked.

Ignored files include:

- Python cache files
- Virtual environments
- Generated model files
- Dataset files
- ML experiment files
- Jupyter checkpoints
- Environment files
- IDE configuration files

## Pull Request Checklist

- [ ] Code changes are complete.
- [ ] Project runs successfully.
- [ ] Tests have been performed.
- [ ] Commit messages are meaningful.
- [ ] No unnecessary generated files are committed.
- [ ] `.gitignore` is working correctly.
- [ ] Pull Request description explains the changes.

## Verification Log

The following Git operations were performed:

- Git repository initialized.
- Project structure created.
- Initial project committed.
- Repository pushed to GitHub.
- Development branch created.
- Feature branch created.
- Pull Request workflow completed.
- Merge conflict intentionally created.
- Merge conflict resolved.
- Training script tested successfully.

## Lessons Learned

This practical demonstrated:

- Git repository initialization
- Git configuration
- Branching
- Commit management
- Remote repositories
- Pull Requests
- Merge operations
- Conflict resolution
- `.gitignore`
- Git workflow documentation