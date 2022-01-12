import git


g = git.cmd.Git('.')
output = g.checkout('main')
output = g.pull('origin main')
if output != 'Already up to date.':
    print('Not up to date')
