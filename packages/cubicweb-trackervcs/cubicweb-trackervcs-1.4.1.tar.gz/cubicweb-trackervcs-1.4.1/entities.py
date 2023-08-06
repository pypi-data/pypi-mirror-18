# copyright 2011-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

from logilab.common.decorators import monkeypatch
from cubes.vcsfile import entities as vcsfile
from cubes.vcreview import entities as vcsreview
from cubes.tracker.entities import project as tracker


@monkeypatch(vcsfile.Repository, 'project')
@property
def project(self):
    if self.reverse_source_repository:
        return self.reverse_source_repository[0]
    return None


@monkeypatch(tracker.Project, 'repository')
@property
def repository(self):
    if self.source_repository:
        return self.source_repository[0]


class PatchReviewBehaviour(vcsreview.PatchReviewBehaviour):
    """Select a reviewer for a patch.
    Try first to filter cwusers to ones that are already reviewers of
    a patch related to the same ticket. If the filter returns an empty
    set we fallback to the previous pre-selection.
    """
    def reviewers_rset(self):
        rset = self._cw.execute(
            'DISTINCT Any U, NULL '
            'WHERE P eid %(p)s,'
            '      P patch_ticket T,'
            '      PS patch_ticket T,'
            '      PS patch_reviewer U,'
            '      P patch_revision RE,'
            '      RE from_repository R,'
            '      EXISTS(R use_global_groups TRUE, U in_group G, G name "reviewers")'
            '      OR EXISTS(R repository_reviewer U)',
            {'p': self.entity.eid})
        if not rset:
            rset = super(PatchReviewBehaviour, self).reviewers_rset()
        return rset


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, butclasses=(PatchReviewBehaviour,))
    vreg.register_and_replace(PatchReviewBehaviour, vcsreview.PatchReviewBehaviour)

    # Skip `patch_ticket` and `closed_by` relations from Ticket copy.
    # This must be done here because cubicweb-forge overloads Ticket's entity
    # class from cubicweb-tracker and forge does not depend on
    # cubicweb-trackervcs.
    ticketcls = vreg['etypes'].etype_class('Ticket')
    ticketcls.cw_skip_copy_for.extend([('closed_by', 'subject'),
                                       ('patch_ticket', 'object')])
