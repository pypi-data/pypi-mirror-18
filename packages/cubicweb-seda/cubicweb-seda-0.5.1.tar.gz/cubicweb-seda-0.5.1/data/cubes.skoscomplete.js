// copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
// contact http://www.logilab.fr -- mailto:contact@logilab.fr
//
// This program is free software: you can redistribute it and/or modify it under
// the terms of the GNU Lesser General Public License as published by the Free
// Software Foundation, either version 2.1 of the License, or (at your option)
// any later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
// details.
//
// You should have received a copy of the GNU Lesser General Public License along
// with this program. If not, see <http://www.gnu.org/licenses/>.

// An autocompletion widget to select a concept from a vocabulary specified by another widget
concept_autocomplete = {
    initConceptAutoCompleteWidget: function(masterSelectId, dependentSelectId, ajaxFuncName) {
        var masterSelect = cw.jqNode(masterSelectId);
        // bind vocabulary select to update concept autocompletion input on value change
        masterSelect.change(function() {
            concept_autocomplete.updateCurrentSchemeEid(this);
            concept_autocomplete.resetConceptFormField(dependentSelectId);
        });
        // initialize currentSchemeEid by looking the value of the master field
        concept_autocomplete.updateCurrentSchemeEid(masterSelect);
        // also bind the autocompletion widget
        cw.jqNode(dependentSelectId+'Label')
            .autocomplete({
                source: function(request, response) {
                    if (concept_autocomplete.currentSchemeEid) {
                        var form = ajaxFuncArgs(ajaxFuncName,
                                                {'q': request.term,
                                                 'scheme': concept_autocomplete.currentSchemeEid});
                        var d = loadRemote(AJAX_BASE_URL, form, 'POST');
                        d.addCallback(function (suggestions) { response(suggestions); });
                    }
                },
                focus: function( event, ui ) {
                    cw.jqNode(dependentSelectId+'Label').val(ui.item.label);
                    return false;
                },
                select: function(event, ui) {
                    cw.jqNode(dependentSelectId+'Label').val(ui.item.label);
                    cw.jqNode(dependentSelectId).val(ui.item.value);
                    return false;
                },
                'mustMatch': true,
                'limit': 100,
                'delay': 300})
            .tooltip({
                tooltipClass: "ui-state-highlight"
            });

        // add key press and focusout event handlers so that value which isn't matching a vocabulary
        // value will be erased
        resetIfInvalidChoice = function() {
            if (concept_autocomplete.currentSchemeEid) {
                var validChoices = $.map($('ul.ui-autocomplete li'),
                                         function(li) {return $(li).text();});
                var value = cw.jqNode(dependentSelectId + 'Label').val();
                if ($.inArray(value, validChoices) == -1) {
                    concept_autocomplete.resetConceptFormField(dependentSelectId);
                }
            }
        };
        cw.jqNode(dependentSelectId+'Label').keypress(function(evt) {
            if (evt.keyCode == $.ui.keyCode.ENTER || evt.keyCode == $.ui.keyCode.TAB) {
                resetIfInvalidChoice();
            }
        });
        cw.jqNode(dependentSelectId+'Label').focusout(function(evt) {
            resetIfInvalidChoice();
        });
    },
    updateCurrentSchemeEid: function(masterSelect) {
        concept_autocomplete.currentSchemeEid = $(masterSelect).val();
        if (concept_autocomplete.currentSchemeEid == '__cubicweb_internal_field__') {
            concept_autocomplete.currentSchemeEid = null;
        }
    },
    resetConceptFormField: function(dependentSelectId) {
        cw.jqNode(dependentSelectId+'Label').val('');
        cw.jqNode(dependentSelectId).val('');
    }
};
