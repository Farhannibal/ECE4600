# Git Guide
Note: In commands anything following the # character is a comment and not needed
## Basic workflow
Create a branch called myFeature off of the branch named develop:
```bash
git checkout -b myFeature develop
```

Do work here...
Stage the files for commit, this can be all changed files:
```bash
git add -A
```

or just some specific files
```bash
git add /path/from/repository/root/fileName.txt
```

When adding a specific file you must prefix it with the path from the root of the repository, as shown above.

Now you are ready to commit:
```bash
git commmit -m "Put commit message here"
```

Repeat the add and commit steps until you have completed the task of myFeature branch
Once finished with the branch, we need to merge into our other branch, in this case develop:
```bash
git checkout develop #Switch to develop branch`
git merge --no-ff myFeature -m "Put message here"
```

Your feature is now integrated into the develop branch. At this point you could push your develop changes up to your own personal GitHub if you wanted.
```bash
git push origin develop
```

If you know you are finished with the myFeature branch you should delete it too.
```bash
git branch -d myFeature
```


## Merge with upstream
Suppose you have finished working on your feature and want to put it in the main repository, i.e. upstream. To do this you must first get all changes from upstream to make sure nothing conflicts with the changes you made locally. For the following example I am assuming it is your local master branch you want to send to upstream.
```bash
git checkout master
git fetch upstream #Get the changes from upstream
git merge upstream/master #Attempt to merge upstream changes into your local master branch
```
Often this will work fine and you will be ready to do a pull request (more on that later), but sometimes your code will conflict with existing code and git will give you a message saying there are conflicts. Git will then open an editor which will show you the conflicting lines or code and let you make a decision about what to do.

Once conflicts are sorted out you are ready for a pull request. This is a GitHub feature which allows simplifies the process of merging your branch into upstream. It will be in the pull requests tab in the GitHub repository and there we can do code reviews, assign people to decide whether to accept the pull request and discuss the pull request.

## Discard unstaged changes
Sometimes you might do a lot of work and decide you want to get rid of everything you did since the last commit. Git has a convenient command for this:
```bash
git checkout -- .
```
There are many ways to jump to specific commits but for basic use, this is the one I found myself using.

## Stashing
There are times when you will be working on one branch and want to switch to another. If all your changes have been committed already then this is done by a simple `git checkout branchName`. But if you have unstaged changes, basically changes that haven't been committed you need to deal with those before switching to a branch. If the changes you made are in a rough state that you don't want to commit but you really want to switch branches and work on something else you have the option to use `git stash`.

What stashing does is it saves the state of all your differences so that you can get them again at a later time. See the example below:
```bash
#Do some work here, but don't want to commit it yet
git stash
git checkout otherBranch
# Do work in other branch and commit it
git checkout originalBranch
git stash pop
```

It is possible to have multiple states stashed, you can view them by using `git stash list`. This will display items with @{0}, @{1} where the numbers are your states. So to access a specific state you can use `git stash pop@{0}` to specifically pick the first state in your stash.

To remove a stashed state use `git stash drop` to remove the latest state or `git stash drop@{0}` to remove a specific state.
