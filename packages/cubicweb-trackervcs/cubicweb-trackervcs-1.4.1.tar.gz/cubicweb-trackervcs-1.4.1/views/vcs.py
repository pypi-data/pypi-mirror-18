# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""cubicweb-trackervcs views"""

from cubicweb import _
from cubicweb.view import EntityView
from cubicweb.predicates import is_instance, score_entity
from cubicweb.web.views import ibreadcrumbs, uicfg

from cubes.tracker.views import project

_pvs = uicfg.primaryview_section
_pvdc = uicfg.primaryview_display_ctrl

_pvs.tag_subject_of(('Project', 'source_repository', '*'), 'attributes')
_pvs.tag_subject_of(('Ticket', 'closed_by', '*'), 'attributes')


class SourceRepositoryIBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = is_instance('Repository') & score_entity(lambda x: x.reverse_source_repository)

    def parent_entity(self):
        return self.entity.reverse_source_repository[0]


class ProjectRepoTab(EntityView):
    __regid__ = _('vcreview.project.vcsrepo_tab')
    __select__ = is_instance('Project') & score_entity(
        lambda x: x.source_repository and x.source_repository[0].source_url)

    def entity_call(self, entity):
        entity.source_repository[0].view(
            'vcsfile.repository.checkout', w=self.w)


project.ProjectPrimaryView.tabs.append(ProjectRepoTab.__regid__)
