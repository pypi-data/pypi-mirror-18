"""forge test application"""

from cubicweb.devtools.testlib import AutomaticWebTest


class AutomaticWebTest(AutomaticWebTest):
    no_auto_populate = ('TestInstance', 'Email', 'EmailPart', 'EmailThread', 'Comment')
    ignored_relations = set(('nosy_list', 'comments'))

    def post_populate(self, cnx):
        cnx.commit()
        for version in cnx.execute('Version X').entities():
            version.cw_adapt_to('IWorkflowable').change_state('published')


if __name__ == '__main__':
    import unittest
    unittest.main()
