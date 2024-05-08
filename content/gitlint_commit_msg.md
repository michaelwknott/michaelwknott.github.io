Title: TIL: Editing Git Commit Messages after Gitlint commit-msg Hook Failure
Date: 2024-05-08 11:00
Category: Python
Tags: TIL, Python, gitlint
Authors: Michael Knott
Summary: A shortcut to save time when editing Git commit messages after a Gitlint commit-msg hook failure
Status: Published

## Editing Git Commit Messages after Gitlint commit-msg Hook Failure

In the course of working on a project that utilizes [Gitlint](https://jorisroovers.com/gitlint/latest/) with [pre-commit](https://pre-commit.com/), I encountered a situation where the Gitlint commit-msg hook would fail due to a commit message not meeting the required format. Initially, it seemed as though I had lost my previous commit message, which meant I had to waste time retyping the message.

However, I discovered a handy command that solves the issue thanks to this [issue thread](https://github.com/jorisroovers/gitlint/issues/90#issuecomment-511425183) in the Gitlint GitHub repository.

```bash
git commit --edit --file .git/COMMIT_EDITMSG
```

This command opens up the text editor with the previous commit message already populated, allowing for easy editing and saving a lot of time. 
