# -*- coding: utf-8 -*-

''' Code taken from https://pagure.io/pagure/blob/master/f/pagure/lib/repo.py
    by pingou@pingoured.fr
'''


import pygit2
import sys


def get_pygit2_version():
    ''' Return pygit2 version as a tuple of integers.
    This is needed for correct version comparison.
    '''
    return tuple([int(i) for i in pygit2.__version__.split('.')])


class PagureRepo(pygit2.Repository):
    """ An utility class allowing to go around pygit2's inability to be
    stable.

    """

    @staticmethod
    def push(remote, refname):
        """ Push the given reference to the specified remote. """
        pygit2_version = get_pygit2_version()
        if pygit2_version >= (0, 22):
            remote.push([refname])
        else:
            remote.push(refname)

    def pull(self, remote_name='origin', branch='master', force=False):
        ''' pull changes for the specified remote (defaults to origin).

        Code from MichaelBoselowitz at:
        https://github.com/MichaelBoselowitz/pygit2-examples/blob/
            68e889e50a592d30ab4105a2e7b9f28fac7324c8/examples.py#L58
        licensed under the MIT license.
        '''

        for remote in self.remotes:
            if remote.name == remote_name:
                remote.fetch()
                remote_master_id = self.lookup_reference(
                    'refs/remotes/origin/%s' % branch).target

                if force:
                    repo_branch = self.lookup_reference(
                        'refs/heads/%s' % branch)
                    repo_branch.set_target(remote_master_id)

                merge_result, _ = self.merge_analysis(remote_master_id)
                # Up to date, do nothing
                if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                    return
                # We can just fastforward
                elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
                    self.checkout_tree(self.get(remote_master_id))
                    master_ref = self.lookup_reference(
                        'refs/heads/%s' % branch)
                    master_ref.set_target(remote_master_id)
                    self.head.set_target(remote_master_id)
                elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
                    sys.exit('Pulling remote changes leads to a conflict')
                else:
                    print 'Unexpected merge result: %s' % (
                            pygit2.GIT_MERGE_ANALYSIS_NORMAL)
                    raise AssertionError('Unknown merge analysis result')
